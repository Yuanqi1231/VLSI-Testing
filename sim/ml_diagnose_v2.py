"""ML diagnosis on the v2 (sampled-operating-space) waveform dataset.

    ~/miniconda3/envs/drl_hw2/bin/python ml_diagnose_v2.py --data out/wave2

v2 dataset properties this script exploits / evaluates:
  * random PRBS per run  -> the TX bit pattern is no longer constant; seed_v is
    stored, so the model can be CONDITIONED on the known TX waveform (2-channel
    input: RX waveform + ideal TX reference). Diagnosis becomes channel
    identification rather than memorising one pattern's shape.
  * continuous T/severity for all classes -> the v1 temperature-support leak is
    gone; the telemetry ablation here is the leak-free re-run.
  * 15% of fault rows carry two concurrent faults -> MULTI-LABEL target
    (9 fault bits; healthy = all-zero).

Experiments:
  1. multi-label diagnosis: logistic vs CNN(RX) vs CNN(RX+TX) vs CNN(RX+TX)+tel
  2. pattern generalization: test on HELD-OUT PRBS seeds (vs random split)
  3. leak-free telemetry ablation: full-waveform CNN A/B + lossy scalar A/B
  4. open-set: leave-one-fault-class-out, max-softmax unknown detection
  5. severity regression on single-fault r_drift / c_drift rows

Outputs: printed summary, <data>/results_v2.json, plots under <data>/plots/.
"""
import argparse
import csv
import json
import os

import numpy as np
import torch
import torch.nn as nn

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from d2dsim.prbs import prbs_bits

torch.manual_seed(0)
np.random.seed(0)


# ---------------------------------------------------------------- data --------
def load_v2(data_dir):
    meta = json.load(open(os.path.join(data_dir, "meta.json")))
    with open(os.path.join(data_dir, "waveforms.csv")) as f:
        r = csv.reader(f)
        header = next(r)
        col = {c: i for i, c in enumerate(header)}
        s0 = col["s0"]
        has_stress = "stress_MPa" in col             # v3 mechanical telemetry
        recs, rows = [], []
        for line in r:
            if len(line) != len(header):
                continue                          # truncated mid-write line
            recs.append(dict(label=line[col["label"]], sev=float(line[col["sev"]]),
                             temp=float(line[col["temp_C"]]),
                             vdr=float(line[col["vdroop_frac"]]),
                             stress=float(line[col["stress_MPa"]]) if has_stress else 0.0,
                             seed_v=int(line[col["seed_v"]]),
                             margin=float(line[col["eye_height_V"]])))
            rows.append([float(x) for x in line[s0:]])
    X = np.asarray(rows, dtype=np.float32)
    classes = meta["classes"]                     # 10 incl healthy
    faults = [c for c in classes if c != "healthy"]
    fidx = {c: i for i, c in enumerate(faults)}
    n = len(recs)
    Y = np.zeros((n, len(faults)), dtype=np.float32)      # multi-hot fault target
    prim = np.full(n, -1, dtype=np.int64)                 # single-label (single-fault rows)
    single = np.zeros(n, dtype=bool)
    for i, rec in enumerate(recs):
        kinds = rec["label"].split("+")
        for k in kinds:
            if k != "healthy":
                Y[i, fidx[k]] = 1.0
        if len(kinds) == 1:
            single[i] = True
            prim[i] = classes.index(kinds[0])
    temp = np.asarray([r["temp"] for r in recs], np.float32)
    vdr = np.asarray([r["vdr"] for r in recs], np.float32)
    stress = (np.asarray([r["stress"] for r in recs], np.float32)
              if has_stress else None)
    tel = np.stack([temp / 100.0, vdr * 10.0]
                   + ([stress / 300.0] if has_stress else []), axis=1)
    sev = np.asarray([r["sev"] for r in recs], np.float32)
    seeds = np.asarray([r["seed_v"] for r in recs], np.int64)
    return X, Y, prim, single, classes, faults, sev, tel, temp, vdr, stress, seeds, meta


def tx_reference(seeds, meta):
    """Ideal TX waveform per row on the same resampled grid (the conditioning
    channel): the known bits upsampled to samples_per_ui, shifted by the nominal
    RX latency so TX and RX are roughly aligned. Levels +-0.5."""
    spu, nb, m = meta["samples_per_ui"], meta["n_bits"], meta["n_samples"]
    dly, order = meta["delay_samples"], meta["prbs_order"]
    cache = {}
    out = np.empty((len(seeds), m), dtype=np.float32)
    for i, s in enumerate(seeds):
        if s not in cache:
            bits = np.asarray(prbs_bits(order, nb, int(s)), np.float32)
            w = np.repeat(bits, spu)
            w = np.roll(w, dly)
            w[:dly] = w[dly]                       # pad the pre-arrival span
            cache[s] = w - 0.5
        out[i] = cache[s]
    return out


def strat_split_by(strata, frac=0.25, seed=0):
    rng = np.random.RandomState(seed)
    te = []
    for c in np.unique(strata):
        idx = np.where(strata == c)[0]
        rng.shuffle(idx)
        te.extend(idx[:max(1, int(round(len(idx) * frac)))])
    te = np.asarray(sorted(te))
    mask = np.zeros(len(strata), bool)
    mask[te] = True
    return np.where(~mask)[0], te


def seed_split(seeds, strata, frac=0.25, rng_seed=0):
    """Hold out 25% of the PRBS seed VALUES -> test patterns never seen in train."""
    rng = np.random.RandomState(rng_seed)
    uniq = np.unique(seeds)
    rng.shuffle(uniq)
    held = set(uniq[:max(1, int(round(len(uniq) * frac)))].tolist())
    te = np.where(np.isin(seeds, list(held)))[0]
    tr = np.where(~np.isin(seeds, list(held)))[0]
    return tr, te


# --------------------------------------------------------------- models -------
class CNN1Dv2(nn.Module):
    """1-D CNN; in_ch=2 adds the ideal-TX conditioning channel. Mean+max pooled."""
    def __init__(self, n_out, in_ch=1, n_tel=0):
        super().__init__()
        self.f = nn.Sequential(
            nn.Conv1d(in_ch, 16, 7, padding=3), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(16, 32, 5, padding=2), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(32, 64, 3, padding=1), nn.ReLU(),
        )
        self.head = nn.Sequential(nn.Linear(128 + n_tel, 64), nn.ReLU(),
                                  nn.Linear(64, n_out))

    def forward(self, x, tel=None):
        z = self.f(x)
        f = torch.cat([z.mean(dim=2), z.amax(dim=2)], dim=1)
        if tel is not None:
            f = torch.cat([f, tel], dim=1)
        return self.head(f)


class LogisticML(nn.Module):
    def __init__(self, n_in, n_out):
        super().__init__()
        self.lin = nn.Linear(n_in, n_out)

    def forward(self, x, tel=None):
        return self.lin(x.flatten(1))


def fit(model, Xtr, ytr, Xte, Ttr=None, Tte=None, task="ml",
        epochs=60, lr=2e-3, wd=1e-4, bs=64, pos_weight=None, cw=None, seed=0):
    """Train and return test-set raw outputs (logits / regression values)."""
    torch.manual_seed(seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)
    if task == "ml":
        lossf = nn.BCEWithLogitsLoss(
            pos_weight=torch.tensor(pos_weight) if pos_weight is not None else None)
    elif task == "cls":
        lossf = nn.CrossEntropyLoss(weight=torch.tensor(cw) if cw is not None else None)
    else:
        lossf = nn.MSELoss()
    Xt = torch.tensor(Xtr)
    yt = torch.tensor(ytr)
    Tt = torch.tensor(Ttr) if Ttr is not None else None
    n = len(Xt)
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(n)
        for i in range(0, n, bs):
            j = perm[i:i + bs]
            opt.zero_grad()
            out = model(Xt[j], Tt[j] if Tt is not None else None)
            if task == "reg":
                out = out.squeeze(-1)
            lossf(out, yt[j]).backward()
            opt.step()
    model.eval()
    with torch.no_grad():
        outs = []
        Xe = torch.tensor(Xte)
        Te = torch.tensor(Tte) if Tte is not None else None
        for i in range(0, len(Xe), 256):
            outs.append(model(Xe[i:i + 256],
                              Te[i:i + 256] if Te is not None else None))
        return torch.cat(outs).numpy()


# -------------------------------------------------------------- metrics -------
def calibrate_thresholds(lo_val, Yval):
    """Per-class logit threshold maximizing F1 on a validation split.

    With BCE pos_weight the sigmoid-0.5 operating point over-predicts positives
    (healthy-FA -> 1); the decision threshold must be calibrated, exactly like a
    production monitor's alarm threshold."""
    thr = np.zeros(Yval.shape[1], np.float32)
    for c in range(Yval.shape[1]):
        best_f1, best_t = -1.0, 0.0
        for t in np.unique(lo_val[:, c]):
            pred = lo_val[:, c] > t
            tp = float((pred & (Yval[:, c] == 1)).sum())
            fp = float((pred & (Yval[:, c] == 0)).sum())
            fn = float((~pred & (Yval[:, c] == 1)).sum())
            f1 = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 0.0
            if f1 > best_f1:
                best_f1, best_t = f1, t
        thr[c] = best_t
    return thr


def ml_metrics(logits, Ytrue, thr=None):
    """Multi-label metrics; thr = per-class logit thresholds (default 0 = sig 0.5)."""
    if thr is None:
        thr = np.zeros(Ytrue.shape[1], np.float32)
    pred = (logits > thr[None, :]).astype(np.float32)
    exact = float((pred == Ytrue).all(axis=1).mean())
    f1s = []
    for c in range(Ytrue.shape[1]):
        tp = float(((pred[:, c] == 1) & (Ytrue[:, c] == 1)).sum())
        fp = float(((pred[:, c] == 1) & (Ytrue[:, c] == 0)).sum())
        fn = float(((pred[:, c] == 0) & (Ytrue[:, c] == 1)).sum())
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * p * r / (p + r) if p + r else 0.0)
    healthy = Ytrue.sum(axis=1) == 0
    fa = float(pred[healthy].any(axis=1).mean()) if healthy.any() else float("nan")
    det = float(pred[~healthy].any(axis=1).mean()) if (~healthy).any() else float("nan")
    return {"exact_match": exact, "macro_f1": float(np.mean(f1s)),
            "healthy_FA": fa, "fault_detect_recall": det,
            "per_class_f1": [round(f, 3) for f in f1s]}


def auroc(scores_pos, scores_neg):
    """AUROC of pos>neg by rank comparison (no sklearn)."""
    s = np.concatenate([scores_pos, scores_neg])
    y = np.concatenate([np.ones(len(scores_pos)), np.zeros(len(scores_neg))])
    order = np.argsort(s)
    ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    n1, n0 = len(scores_pos), len(scores_neg)
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def normalize(X, tr):
    mu, sd = X[tr].mean(), X[tr].std() + 1e-9
    return (X - mu) / sd


# ------------------------------------------------------------- experiments ----
def run(data_dir, epochs=60, exps=("1", "2", "3", "4", "5")):
    X, Y, prim, single, classes, faults, sev, tel, temp, vdr, stress, seeds, meta = load_v2(data_dir)
    spu, settle, m = meta["samples_per_ui"], meta["settle_bits"], meta["n_samples"]
    valid = np.arange(settle * spu, m)
    h = classes.index("healthy")
    print(f"loaded {len(X)} rows  ({single.sum()} single-fault, "
          f"{(~single).sum()} concurrent)  classes={len(classes)}")
    TX = tx_reference(seeds, meta)
    plots = os.path.join(data_dir, "plots")
    os.makedirs(plots, exist_ok=True)
    res_path = os.path.join(data_dir, "results_v2.json")
    results = json.load(open(res_path)) if os.path.exists(res_path) else {}
    results.update({"n": int(len(X)), "n_concurrent": int((~single).sum()),
                    "classes": classes, "epochs": epochs})

    strata = np.array([classes[p] if p >= 0 else "mixed" for p in prim])
    tr, te = strat_split_by(strata, 0.25, seed=0)
    Xn = normalize(X, tr)
    rx = Xn[:, None, valid].astype(np.float32)
    rxtx = np.concatenate([rx, TX[:, None, valid]], axis=1).astype(np.float32)
    pw = ((len(tr) - Y[tr].sum(0)) / np.maximum(Y[tr].sum(0), 1)).astype(np.float32)
    telf = tel.astype(np.float32)

    def fit_calibrated(model, Xin, T, tr_idx, te_idx, rng_seed=0):
        """Train on 80% of tr_idx, calibrate per-class thresholds on the other
        20%, return test metrics at the calibrated operating point."""
        ftr, fval = strat_split_by(strata[tr_idx], 0.2, seed=rng_seed)
        ftr, fval = tr_idx[ftr], tr_idx[fval]
        pwc = ((len(ftr) - Y[ftr].sum(0)) / np.maximum(Y[ftr].sum(0), 1)).astype(np.float32)
        ev = np.concatenate([fval, te_idx])
        lo = fit(model, Xin[ftr], Y[ftr], Xin[ev],
                 Ttr=T[ftr] if T is not None else None,
                 Tte=T[ev] if T is not None else None,
                 task="ml", epochs=epochs, pos_weight=pwc)
        thr = calibrate_thresholds(lo[:len(fval)], Y[fval])
        return ml_metrics(lo[len(fval):], Y[te_idx], thr=thr)

    si = np.where(single)[0]
    y3 = prim

    # ---- 1. multi-label diagnosis (thresholds calibrated on validation) ----
    if "1" in exps:
        print("\n[1] multi-label diagnosis (9 fault bits, healthy = all-zero, "
              "calibrated thresholds):")
        out1 = {}
        runs = [("logistic_RX", LogisticML(len(valid), len(faults)), rx, None),
                ("cnn_RX", CNN1Dv2(len(faults), in_ch=1), rx, None),
                ("cnn_RX_TX", CNN1Dv2(len(faults), in_ch=2), rxtx, None),
                ("cnn_RX_TX_tel", CNN1Dv2(len(faults), in_ch=2, n_tel=telf.shape[1]),
                 rxtx, telf)]
        for name, model, Xin, T in runs:
            out1[name] = fit_calibrated(model, Xin, T, tr, te)
            print(f"   {name:15s}: exact={out1[name]['exact_match']:.3f}  "
                  f"macroF1={out1[name]['macro_f1']:.3f}  "
                  f"healthyFA={out1[name]['healthy_FA']:.3f}  "
                  f"detect={out1[name]['fault_detect_recall']:.3f}")
        results["multilabel"] = out1
        json.dump(results, open(res_path, "w"), indent=2)

    # ---- 2. pattern generalization: held-out PRBS seeds ----
    if "2" in exps:
        print("\n[2] pattern generalization (test = unseen TX patterns):")
        trs, tes = seed_split(seeds, strata, 0.25, rng_seed=1)
        out2 = {"n_test": int(len(tes)),
                "n_test_seeds": int(len(np.unique(seeds[tes])))}
        for name, in_ch, Xin in [("cnn_RX", 1, rx), ("cnn_RX_TX", 2, rxtx)]:
            out2[name] = fit_calibrated(CNN1Dv2(len(faults), in_ch=in_ch),
                                        Xin, None, trs, tes)
            print(f"   {name:10s}: exact={out2[name]['exact_match']:.3f}  "
                  f"macroF1={out2[name]['macro_f1']:.3f}  "
                  f"healthyFA={out2[name]['healthy_FA']:.3f}")
        results["pattern_generalization"] = out2
        json.dump(results, open(res_path, "w"), indent=2)

    # ---- 3. leak-free telemetry ablation (single-fault rows, 10-class) ----
    if "3" in exps:
        print("\n[3] telemetry ablation, leak-free dataset (single-fault, 10-class):")
        tr3, te3 = strat_split_by(prim[si], 0.25, seed=0)
        tr3, te3 = si[tr3], si[te3]
        cw = (len(tr3) / (len(classes) * np.maximum(
            np.bincount(y3[tr3], minlength=len(classes)), 1))).astype(np.float32)
        out3 = {}
        for name, ntel, T in [("A_waveform_only", 0, None),
                              ("B_plus_telemetry", telf.shape[1], telf)]:
            lo = fit(CNN1Dv2(len(classes), in_ch=2, n_tel=ntel), rxtx[tr3], y3[tr3],
                     rxtx[te3], Ttr=T[tr3] if T is not None else None,
                     Tte=T[te3] if T is not None else None,
                     task="cls", epochs=epochs, cw=cw)
            p = lo.argmax(1)
            hmask = y3[te3] == h
            stressed = (temp[te3] >= 85.0) | (vdr[te3] >= 0.05)
            out3[name] = {
                "acc": float((p == y3[te3]).mean()),
                "healthy_FA": float((p[hmask] != h).mean()) if hmask.any() else None,
                "stressed_healthy_FA": float((p[hmask & stressed] != h).mean())
                                       if (hmask & stressed).any() else None}
            if stress is not None:
                wm = hmask & ((stress[te3] - 2.486 * (temp[te3] - 27.0)) >= 150.0)
                out3[name]["warped_healthy_FA"] = (float((p[wm] != h).mean())
                                                   if wm.any() else None)
            print(f"   {name:18s}: acc={out3[name]['acc']:.3f}  "
                  f"healthyFA={out3[name]['healthy_FA']:.3f}  "
                  f"stressed-healthyFA={out3[name]['stressed_healthy_FA']:.3f}"
                  + (f"  warped-healthyFA={out3[name].get('warped_healthy_FA')}"
                     if stress is not None else ""))
            if name == "B_plus_telemetry":
                _confusion(y3[te3], p, classes,
                           os.path.join(plots, "confusion_v2.png"))
        # lossy scalar regime (margin from the stored eye height) A/B
        mar = np.asarray([np.percentile(X[i, valid], 90) - np.percentile(X[i, valid], 10)
                          for i in range(len(X))], np.float32)
        yb = (Y.sum(1) > 0).astype(np.int64)
        FA = mar[:, None]
        FB = np.stack([mar, temp / 100.0, vdr * 10.0], axis=1)
        lossy_runs = [("lossy_A_margin", FA), ("lossy_B_margin_tel", FB)]
        sigw = None
        if stress is not None:
            # warpage stress component = sensor stress minus the CTE-bridge part
            # (E/(1-nu)*dAlpha = 2.486 MPa/C); >=150 MPa ~ bow w >= 100 um
            sigw = stress - 2.486 * (temp - 27.0)
            FC = np.concatenate([FB, stress[:, None] / 300.0], axis=1)
            lossy_runs.append(("lossy_C_margin_tel_stress", FC))
        cwb = np.array([0.5 * len(tr) / max((yb[tr] == c).sum(), 1) for c in (0, 1)],
                       np.float32)
        for nm, F in lossy_runs:
            lo = fit(LogisticML(F.shape[1], 2), F[tr, None, :].astype(np.float32),
                     yb[tr], F[te, None, :].astype(np.float32),
                     task="cls", epochs=200, lr=0.05, cw=cwb)
            p = lo.argmax(1)
            hm = yb[te] == 0
            sh = hm & ((temp[te] >= 85) | (vdr[te] >= 0.05))
            out3[nm] = {"acc": float((p == yb[te]).mean()),
                        "healthy_FA": float((p[hm] == 1).mean()),
                        "stressed_healthy_FA": float((p[sh] == 1).mean()) if sh.any() else None,
                        "fault_recall": float((p[yb[te] == 1] == 1).mean())}
            if sigw is not None:
                wm = hm & (sigw[te] >= 150.0)
                out3[nm]["warped_healthy_FA"] = (float((p[wm] == 1).mean())
                                                 if wm.any() else None)
            print(f"   {nm:25s}: acc={out3[nm]['acc']:.3f}  "
                  f"healthyFA={out3[nm]['healthy_FA']:.3f}  "
                  f"stressed-healthyFA={out3[nm]['stressed_healthy_FA']}  "
                  + (f"warped-healthyFA={out3[nm].get('warped_healthy_FA')}  "
                     if sigw is not None else "")
                  + f"recall={out3[nm]['fault_recall']:.3f}")
        results["telemetry_ablation_v2"] = out3
        json.dump(results, open(res_path, "w"), indent=2)
        _lossy_plot(mar, temp, yb, os.path.join(plots, "lossy_confounder_v2.png"))

    # ---- 4. open-set: leave-one-fault-class-out ----
    out4 = {}
    if "4" in exps:
        print("\n[4] open-set unknown-fault detection (max-softmax score):")
    for held in (("bridge_short", "hotspot", "c_drift") if "4" in exps else ()):
        hi = classes.index(held)
        known = si[y3[si] != hi]
        unk = si[y3[si] == hi]
        ktr, kte = strat_split_by(y3[known], 0.25, seed=0)
        ktr, kte = known[ktr], known[kte]
        keep = sorted(set(y3[ktr]))
        remap = {c: i for i, c in enumerate(keep)}
        ytr9 = np.asarray([remap[c] for c in y3[ktr]])
        model = CNN1Dv2(len(keep), in_ch=2)
        lo_k = fit(model, rxtx[ktr], ytr9, rxtx[kte], task="cls", epochs=epochs)
        with torch.no_grad():
            lo_u = []
            Xu = torch.tensor(rxtx[unk])
            for i in range(0, len(Xu), 256):
                lo_u.append(model(Xu[i:i + 256]))
            lo_u = torch.cat(lo_u).numpy()
        sm = lambda z: np.exp(z - z.max(1, keepdims=True)) \
            / np.exp(z - z.max(1, keepdims=True)).sum(1, keepdims=True)
        s_known = sm(lo_k).max(1)
        s_unk = sm(lo_u).max(1)
        # unknown rows should score LOWER max-softmax -> rank -score
        out4[held] = {"auroc_unknown": auroc(-s_unk, -s_known),
                      "n_unknown": int(len(unk)),
                      "mean_conf_known": float(s_known.mean()),
                      "mean_conf_unknown": float(s_unk.mean())}
        print(f"   held-out {held:14s}: AUROC={out4[held]['auroc_unknown']:.3f}  "
              f"conf known={out4[held]['mean_conf_known']:.2f} "
              f"unknown={out4[held]['mean_conf_unknown']:.2f}")
    if "4" in exps:
        results["open_set"] = out4

    # ---- 5. severity regression (single-fault drift rows) ----
    if "5" in exps:
        print("\n[5] severity regression:")
        results["severity"] = {}
    for kind in (("r_drift", "c_drift") if "5" in exps else ()):
        ci = classes.index(kind)
        idx = si[y3[si] == ci]
        if len(idx) < 30:
            continue
        rtr, rte = strat_split_by(np.zeros(len(idx)), 0.25, seed=0)
        rtr, rte = idx[rtr], idx[rte]
        smin, smax = sev[idx].min(), sev[idx].max()
        sn = ((sev - smin) / (smax - smin + 1e-9)).astype(np.float32)
        pred = fit(CNN1Dv2(1, in_ch=2), rxtx[rtr], sn[rtr], rxtx[rte],
                   task="reg", epochs=epochs, lr=1e-3).squeeze(-1)
        true = sn[rte]
        mae = float(np.abs(pred - true).mean())
        r2 = 1 - float(((pred - true) ** 2).sum()) / \
            (float(((true - true.mean()) ** 2).sum()) + 1e-9)
        results["severity"][kind] = {"mae_norm": mae, "r2": r2, "n_test": int(len(rte))}
        print(f"   {kind}: MAE(norm)={mae:.3f}  R2={r2:.3f}  (n={len(rte)})")

    json.dump(results, open(res_path, "w"), indent=2)
    print(f"\nresults -> {os.path.join(data_dir, 'results_v2.json')}")
    return results


# ------------------------------------------------------------- plotting -------
def _confusion(true, pred, classes, path):
    n = len(classes)
    C = np.zeros((n, n), int)
    for t, p in zip(true, pred):
        C[t, p] += 1
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(C, cmap="Blues")
    ax.set_xticks(range(n)); ax.set_xticklabels(classes, rotation=60, ha="right", fontsize=7)
    ax.set_yticks(range(n)); ax.set_yticklabels(classes, fontsize=7)
    ax.set_xlabel("predicted"); ax.set_ylabel("true")
    ax.set_title("v2 CNN confusion (single-fault rows, leak-free dataset)")
    for i in range(n):
        for j in range(n):
            if C[i, j]:
                ax.text(j, i, C[i, j], ha="center", va="center", fontsize=7,
                        color="white" if C[i, j] > C.max() / 2 else "black")
    fig.colorbar(im); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _lossy_plot(mar, temp, yb, path):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    # draw faulty FIRST so the (fewer) healthy dots stay visible on top
    for lab, c, name, z in [(1, "#d62728", "faulty", 2), (0, "#2ca02c", "healthy", 3)]:
        m = yb == lab
        ax.scatter(mar[m] * 1e3, temp[m], c=c, alpha=0.45, s=14, label=name,
                   zorder=z, edgecolors="white", linewidths=0.25)
    ax.set_xlabel("eye margin [mV] (the only runtime scalar)")
    ax.set_ylabel("temperature [C] (telemetry)")
    ax.set_title("v2 (leak-free): margin vs temperature, healthy/faulty overlap")
    ax.legend(); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/wave2")
    ap.add_argument("--epochs", type=int, default=60)
    ap.add_argument("--exp", default="1,2,3,4,5",
                    help="comma list of experiments to run (results are merged)")
    a = ap.parse_args()
    run(a.data, epochs=a.epochs, exps=tuple(a.exp.split(",")))
