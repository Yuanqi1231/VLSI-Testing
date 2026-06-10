"""Robustness / diagnosability ablations on the v2 dataset (slow; supplements
the main results -- not necessarily in the presentation deck).

    ~/miniconda3/envs/drl_hw2/bin/python ablations_v2.py --data out/wave2 --exp 6,7,8

  6. temperature holdout: entire temperature bands are held out of training
     (extrapolate to an unseen hot band / interpolate across an unseen middle
     band) instead of the random 75/25 split -> evidence the model is not just
     memorising simulation templates at the trained temperatures.
  7. telemetry sensor noise: DTS gaussian error + 1 C quantisation on temp,
     additive error + undersampling on the droop monitor (a real droop monitor
     samples the rail periodically and can miss part of the dip) -> "fusing
     telemetry lowers FA" must not depend on perfect sensor ground truth.
  8. per-class diagnosability: per-class precision/recall/F1, top confusion
     pairs, and accuracy after collapsing classes into eye-signature families
     -> which faults are truly separable and which are only confused INSIDE
     the series-resistance (attenuation) family.

Results merge into <data>/results_v2.json under keys temp_holdout /
telemetry_noise / per_class; plots under <data>/plots/.
"""
import argparse
import json
import os

import numpy as np
import torch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ml_diagnose_v2 import (load_v2, tx_reference, strat_split_by, normalize,
                            CNN1Dv2, LogisticML, fit)

torch.manual_seed(0)
np.random.seed(0)

# eye-signature families (matches the fault-modeling slides): errors inside a
# family share the same physical mechanism / eye signature
FAMILIES = {
    "healthy": "healthy",
    "resistive_open": "attenuation", "bump_void_aging": "attenuation",
    "r_drift": "attenuation", "hotspot": "attenuation",
    "supply_droop": "swing",
    "c_drift": "edge",
    "crosstalk_cap": "coupling", "bridge_short": "coupling",
    "impedance_discontinuity": "reflection",
}


def cls_metrics(p, y, h, temp, vdr):
    hmask = y == h
    stress = (temp >= 85.0) | (vdr >= 0.05)
    return {"acc": float((p == y).mean()),
            "healthy_FA": float((p[hmask] != h).mean()) if hmask.any() else None,
            "stressed_healthy_FA": float((p[hmask & stress] != h).mean())
                                   if (hmask & stress).any() else None}


def fit_10cls(rxtx, y3, classes, tr, te, epochs, tel=None):
    cw = (len(tr) / (len(classes) * np.maximum(
        np.bincount(y3[tr], minlength=len(classes)), 1))).astype(np.float32)
    lo = fit(CNN1Dv2(len(classes), in_ch=2, n_tel=0 if tel is None else tel.shape[1]),
             rxtx[tr], y3[tr], rxtx[te],
             Ttr=tel[tr] if tel is not None else None,
             Tte=tel[te] if tel is not None else None,
             task="cls", epochs=epochs, cw=cw)
    return lo.argmax(1)


# ---- 6. temperature holdout ---------------------------------------------------
def exp6(rxtx_of, X, y3, si, classes, temp, vdr, epochs):
    print("\n[6] temperature holdout (train never sees the test band):")
    h = classes.index("healthy")
    out = {}
    bands = {"extrap_hot":  ("train T<85C, test T>=85C",
                             lambda t: t >= 85.0),
             "interp_band": ("train T<60C or T>=85C, test 60<=T<85C",
                             lambda t: (t >= 60.0) & (t < 85.0))}
    for name, (desc, in_test) in bands.items():
        te = si[in_test(temp[si])]
        tr = si[~in_test(temp[si])]
        rxtx = rxtx_of(tr)                      # normalisation from train rows only
        for tag, tel in [("A_waveform_only", None),
                         ("B_plus_telemetry",
                          np.stack([temp / 100.0, vdr * 10.0], 1).astype(np.float32))]:
            p = fit_10cls(rxtx, y3, classes, tr, te, epochs, tel)
            m = cls_metrics(p, y3[te], h, temp[te], vdr[te])
            m.update(n_train=int(len(tr)), n_test=int(len(te)), split=desc)
            out[f"{name}_{tag}"] = m
            print(f"   {name:11s} {tag:18s}: acc={m['acc']:.3f}  "
                  f"healthyFA={m['healthy_FA']:.3f}  "
                  f"stressedFA={m['stressed_healthy_FA']}  "
                  f"(train {len(tr)} / test {len(te)})")
    return out


# ---- 7. telemetry sensor noise --------------------------------------------------
def exp7(rxtx, mar, X, Y, y3, si, classes, temp, vdr, tr, te, epochs):
    print("\n[7] telemetry sensor noise (does FA reduction survive imperfect sensors?):")
    h = classes.index("healthy")
    yb = (Y.sum(1) > 0).astype(np.int64)
    cwb = np.array([0.5 * len(tr) / max((yb[tr] == c).sum(), 1) for c in (0, 1)],
                   np.float32)

    def noisy_tel(s_t, s_v, under, rng):
        t = temp + rng.normal(0, s_t, temp.shape)
        if s_t > 0:
            t = np.round(t)                     # DTS reports in 1 C steps
        v = vdr * (rng.uniform(*under, vdr.shape) if under else 1.0)
        v = np.clip(v + rng.normal(0, s_v, vdr.shape), 0.0, None)
        return t.astype(np.float32), v.astype(np.float32)

    # noise levels: (label, sigma_T [C], sigma_vdr [abs frac], droop undersampling)
    levels = [("clean",          0.0, 0.0,   None),
              ("dts1C_v0.5pct",  1.0, 0.005, None),
              ("dts2C_v1pct",    2.0, 0.01,  None),
              ("dts5C_v2pct",    5.0, 0.02,  None),
              ("undersampled_droop", 2.0, 0.01, (0.6, 1.0))]
    out = {"levels": {lab: dict(sigma_T=st, sigma_vdr=sv, droop_undersampling=u)
                      for lab, st, sv, u in levels}}

    # (a) lossy scalar regime -- where telemetry was ESSENTIAL (FA 49% -> 9%)
    sweep = {}
    for lab, st, sv, under in levels:
        accs, fas, sfas, recs = [], [], [], []
        for s in range(3):                      # 3 independent sensor-noise draws
            rng = np.random.RandomState(100 + s)
            tn, vn = noisy_tel(st, sv, under, rng)
            F = np.stack([mar, tn / 100.0, vn * 10.0], 1)
            lo = fit(LogisticML(3, 2), F[tr, None, :].astype(np.float32), yb[tr],
                     F[te, None, :].astype(np.float32),
                     task="cls", epochs=200, lr=0.05, cw=cwb, seed=s)
            p = lo.argmax(1)
            hm = yb[te] == 0
            sh = hm & ((temp[te] >= 85) | (vdr[te] >= 0.05))   # stress = TRUE state
            accs.append(float((p == yb[te]).mean()))
            fas.append(float((p[hm] == 1).mean()))
            sfas.append(float((p[sh] == 1).mean()))
            recs.append(float((p[yb[te] == 1] == 1).mean()))
        sweep[lab] = {k: [float(np.mean(v)), float(np.std(v))]
                      for k, v in [("acc", accs), ("healthy_FA", fas),
                                   ("stressed_healthy_FA", sfas), ("fault_recall", recs)]}
        m = sweep[lab]
        print(f"   lossy {lab:20s}: FA={m['healthy_FA'][0]:.3f}+-{m['healthy_FA'][1]:.3f}  "
              f"stressedFA={m['stressed_healthy_FA'][0]:.3f}+-{m['stressed_healthy_FA'][1]:.3f}  "
              f"recall={m['fault_recall'][0]:.3f}")
    out["lossy_margin_tel"] = sweep

    # (b) train-clean / test-noisy mismatch (deploying as if sensors were perfect)
    rng = np.random.RandomState(200)
    tn, vn = noisy_tel(2.0, 0.01, None, rng)
    Ftr = np.stack([mar, temp / 100.0, vdr * 10.0], 1)
    Fte = np.stack([mar, tn / 100.0, vn * 10.0], 1)
    lo = fit(LogisticML(3, 2), Ftr[tr, None, :].astype(np.float32), yb[tr],
             Fte[te, None, :].astype(np.float32), task="cls", epochs=200, lr=0.05, cw=cwb)
    p = lo.argmax(1)
    hm = yb[te] == 0
    sh = hm & ((temp[te] >= 85) | (vdr[te] >= 0.05))
    out["lossy_train_clean_test_noisy"] = {
        "acc": float((p == yb[te]).mean()),
        "healthy_FA": float((p[hm] == 1).mean()),
        "stressed_healthy_FA": float((p[sh] == 1).mean()),
        "fault_recall": float((p[yb[te] == 1] == 1).mean())}
    m = out["lossy_train_clean_test_noisy"]
    print(f"   lossy train-clean/test-noisy(2C,1%): FA={m['healthy_FA']:.3f}  "
          f"stressedFA={m['stressed_healthy_FA']:.3f}  recall={m['fault_recall']:.3f}")

    # (c) full-waveform 10-class B_plus_telemetry under mid noise -- telemetry was
    # redundant there, so noise should NOT hurt (sanity that the conclusion
    # "value of telemetry is conditional on observation losslessness" stands)
    rng = np.random.RandomState(300)
    tn, vn = noisy_tel(2.0, 0.01, None, rng)
    tel_n = np.stack([tn / 100.0, vn * 10.0], 1).astype(np.float32)
    tr3, te3 = strat_split_by(y3[si], 0.25, seed=0)
    tr3, te3 = si[tr3], si[te3]
    p = fit_10cls(rxtx, y3, classes, tr3, te3, epochs, tel_n)
    out["cnn_B_noisy_tel_2C_1pct"] = cls_metrics(p, y3[te3], h, temp[te3], vdr[te3])
    m = out["cnn_B_noisy_tel_2C_1pct"]
    print(f"   CNN  B+noisy tel (2C,1%) : acc={m['acc']:.3f}  "
          f"healthyFA={m['healthy_FA']:.3f}  stressedFA={m['stressed_healthy_FA']:.3f}")
    return out


# ---- 8. per-class diagnosability ------------------------------------------------
def exp8(rxtx, y3, si, classes, temp, vdr, epochs, plots):
    print("\n[8] per-class diagnosability (P/R/F1, confusion pairs, family collapse):")
    h = classes.index("healthy")
    tel = np.stack([temp / 100.0, vdr * 10.0], 1).astype(np.float32)
    tr3, te3 = strat_split_by(y3[si], 0.25, seed=0)
    tr3, te3 = si[tr3], si[te3]
    p = fit_10cls(rxtx, y3, classes, tr3, te3, epochs, tel)
    y = y3[te3]
    n = len(classes)
    C = np.zeros((n, n), int)
    for t, q in zip(y, p):
        C[t, q] += 1

    per = {}
    for c, name in enumerate(classes):
        tp = float(C[c, c]); fp = float(C[:, c].sum() - C[c, c])
        fn = float(C[c, :].sum() - C[c, c])
        pr = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * pr * rc / (pr + rc) if pr + rc else 0.0
        per[name] = {"precision": round(pr, 3), "recall": round(rc, 3),
                     "f1": round(f1, 3), "support": int(C[c, :].sum())}
        print(f"   {name:24s} P={pr:.3f}  R={rc:.3f}  F1={f1:.3f}  (n={per[name]['support']})")

    pairs = [(classes[i], classes[j], int(C[i, j]))
             for i in range(n) for j in range(n) if i != j and C[i, j]]
    pairs.sort(key=lambda x: -x[2])
    print("   top confusion pairs (true -> predicted):")
    for a, b, c in pairs[:8]:
        print(f"     {a:24s} -> {b:24s} {c}")

    fam_names = sorted(set(FAMILIES.values()))
    fmap = np.array([fam_names.index(FAMILIES[c]) for c in classes])
    fam_acc = float((fmap[p] == fmap[y]).mean())
    err = p != y
    in_family = float((fmap[p[err]] == fmap[y[err]]).mean()) if err.any() else 0.0
    print(f"   10-class acc={float((p == y).mean()):.3f}  ->  "
          f"{len(fam_names)}-family acc={fam_acc:.3f}  "
          f"({in_family:.0%} of errors stay inside the same eye-signature family)")

    fig, ax = plt.subplots(figsize=(9, 4))
    xs = np.arange(n)
    for off, key, col in [(-0.27, "precision", "#1f77b4"), (0.0, "recall", "#ff7f0e"),
                          (0.27, "f1", "#2ca02c")]:
        ax.bar(xs + off, [per[c][key] for c in classes], width=0.25, label=key, color=col)
    ax.set_xticks(xs); ax.set_xticklabels(classes, rotation=45, ha="right", fontsize=7)
    ax.set_ylim(0, 1.05); ax.legend(fontsize=8)
    ax.set_title("v2 per-class diagnosability (CNN + telemetry, single-fault test rows)")
    fig.tight_layout(); fig.savefig(os.path.join(plots, "per_class_v2.png"), dpi=130)
    plt.close(fig)
    return {"per_class": per,
            "top_confusions": [{"true": a, "pred": b, "n": c} for a, b, c in pairs[:10]],
            "family_names": fam_names, "family_acc": fam_acc,
            "acc": float((p == y).mean()), "in_family_error_frac": in_family}


# ----------------------------------------------------------------------------------
def run(data_dir, epochs=60, exps=("6", "7", "8")):
    X, Y, prim, single, classes, faults, sev, tel, temp, vdr, stress, seeds, meta = load_v2(data_dir)
    spu, settle, m = meta["samples_per_ui"], meta["settle_bits"], meta["n_samples"]
    valid = np.arange(settle * spu, m)
    TX = tx_reference(seeds, meta)
    si = np.where(single)[0]
    y3 = prim
    plots = os.path.join(data_dir, "plots")
    os.makedirs(plots, exist_ok=True)
    res_path = os.path.join(data_dir, "results_v2.json")
    results = json.load(open(res_path)) if os.path.exists(res_path) else {}

    def rxtx_of(tr_idx):
        Xn = normalize(X, tr_idx)
        rx = Xn[:, None, valid].astype(np.float32)
        return np.concatenate([rx, TX[:, None, valid]], 1).astype(np.float32)

    # default random-split inputs (exp 7/8 reuse the exp-1/3 split conventions)
    strata = np.array([classes[p] if p >= 0 else "mixed" for p in prim])
    tr, te = strat_split_by(strata, 0.25, seed=0)
    rxtx = rxtx_of(tr)
    mar = np.asarray([np.percentile(X[i, valid], 90) - np.percentile(X[i, valid], 10)
                      for i in range(len(X))], np.float32)

    if "6" in exps:
        results["temp_holdout"] = exp6(rxtx_of, X, y3, si, classes, temp, vdr, epochs)
        json.dump(results, open(res_path, "w"), indent=2)
    if "7" in exps:
        results["telemetry_noise"] = exp7(rxtx, mar, X, Y, y3, si, classes,
                                          temp, vdr, tr, te, epochs)
        json.dump(results, open(res_path, "w"), indent=2)
    if "8" in exps:
        results["per_class"] = exp8(rxtx, y3, si, classes, temp, vdr, epochs, plots)
        json.dump(results, open(res_path, "w"), indent=2)
    print(f"\nresults -> {res_path}")
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/wave2")
    ap.add_argument("--epochs", type=int, default=60)
    ap.add_argument("--exp", default="6,7,8",
                    help="comma list of ablations to run (results are merged)")
    a = ap.parse_args()
    run(a.data, epochs=a.epochs, exps=tuple(a.exp.split(",")))
