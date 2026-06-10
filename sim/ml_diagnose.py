"""ML fault diagnosis from RAW D2D RX waveforms (run with the numpy/torch env).

    ~/miniconda3/envs/drl_hw2/bin/python ml_diagnose.py --data out/wave

Experiments:
  1. baseline (multinomial logistic) vs 1-D CNN on the raw waveform.
  2. TELEMETRY ablation (the confounder story): CNN-A (waveform only) vs CNN-B
     (waveform + observable [temp, droop] telemetry). A hot/drooped-but-healthy
     link closes its eye like a fault; telemetry lets B reject those false alarms.
     Reported: overall acc, acc on the high-stress subset, healthy false-alarm rate.
  3. REGION ablation: CNN on full vs signal/edge-only vs held-only samples ->
     where does each fault's signature live?
  4. severity regression on the continuous r_drift / c_drift faults.
Outputs: printed summary, out/wave/results.json, plots under out/wave/plots/.
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

DEV = "cpu"
torch.manual_seed(0)
np.random.seed(0)


# ---------------------------------------------------------------- data --------
def load_data(data_dir):
    meta = json.load(open(os.path.join(data_dir, "meta.json")))
    with open(os.path.join(data_dir, "waveforms.csv")) as f:
        r = csv.reader(f)
        header = next(r)
        col = {c: i for i, c in enumerate(header)}
        s0 = col["s0"]
        labels, sev, temp, vdr, rows = [], [], [], [], []
        for line in r:
            labels.append(line[col["label"]])
            sev.append(float(line[col["sev"]]))
            temp.append(float(line[col["temp_C"]]))
            vdr.append(float(line[col["vdroop_frac"]]))
            rows.append([float(x) for x in line[s0:]])
    X = np.asarray(rows, dtype=np.float32)
    labels = np.asarray(labels)
    classes = sorted(set(labels.tolist()))
    cidx = {c: i for i, c in enumerate(classes)}
    y = np.asarray([cidx[c] for c in labels], dtype=np.int64)
    # observable telemetry, scaled to ~O(1): temp/100C, droop*10
    tel = np.stack([np.asarray(temp, np.float32) / 100.0,
                    np.asarray(vdr, np.float32) * 10.0], axis=1)
    return X, y, classes, np.asarray(sev, np.float32), tel, np.asarray(temp, np.float32), meta


def region_masks(meta):
    """Indices of (valid, signal/edge, non-signal/held) samples from the fixed bits."""
    bits, spu, m = meta["bits"], meta["samples_per_ui"], meta["n_samples"]
    dly, settle = meta["delay_samples"], meta["settle_bits"]
    w = spu // 2                                   # +-0.5 UI window around a transition
    is_sig = np.zeros(m, dtype=bool)
    for b in range(1, len(bits)):
        if bits[b] != bits[b - 1]:
            c = b * spu + dly
            is_sig[max(0, c - w):min(m, c + w + 1)] = True
    valid = np.arange(settle * spu, m)             # drop the leading channel-fill bits
    return valid, valid[is_sig[valid]], valid[~is_sig[valid]]


def strat_split(y, frac=0.25, seed=0):
    rng = np.random.RandomState(seed)
    te = []
    for c in np.unique(y):
        idx = np.where(y == c)[0]
        rng.shuffle(idx)
        te.extend(idx[:max(1, int(round(len(idx) * frac)))])
    te = np.asarray(sorted(te))
    tr = np.asarray([i for i in range(len(y)) if i not in set(te.tolist())])
    return tr, te


# --------------------------------------------------------------- models -------
class CNN1D(nn.Module):
    """1-D CNN over the waveform; optionally fuses n_tel scalar telemetry inputs.

    Pools the final feature maps by BOTH average and max over time (concatenated):
    average keeps the settled-level/amplitude signature, max keeps peaks/edges --
    a plain global-average-pool alone collapses the waveform to a mean and loses
    the amplitude-vs-extreme distinction the fault classes need."""
    def __init__(self, n_out, n_tel=0):
        super().__init__()
        self.f = nn.Sequential(
            nn.Conv1d(1, 16, 7, padding=3), nn.ReLU(), nn.MaxPool1d(2),
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


class Logistic(nn.Module):
    def __init__(self, n_in, n_cls):
        super().__init__()
        self.lin = nn.Linear(n_in, n_cls)

    def forward(self, x, tel=None):
        return self.lin(x.squeeze(1))


def _fit(model, Xtr, ytr, Xte, yte, Ttr=None, Tte=None,
         epochs=120, lr=2e-3, wd=1e-4, task="cls", cw=None):
    model = model.to(DEV)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)
    if task == "cls":
        wt = torch.tensor(cw) if cw is not None else None
        lossf = nn.CrossEntropyLoss(weight=wt)
    else:
        lossf = nn.MSELoss()
    Xtr_t, Xte_t = torch.tensor(Xtr), torch.tensor(Xte)
    ytr_t = torch.tensor(ytr)
    Ttr_t = torch.tensor(Ttr) if Ttr is not None else None
    Tte_t = torch.tensor(Tte) if Tte is not None else None
    n, bs = len(Xtr), 32
    for ep in range(epochs):
        model.train()
        perm = torch.randperm(n)
        for i in range(0, n, bs):
            j = perm[i:i + bs]
            opt.zero_grad()
            tel = Ttr_t[j] if Ttr_t is not None else None
            out = model(Xtr_t[j], tel)
            if task == "reg":
                out = out.squeeze(-1)
            loss = lossf(out, ytr_t[j])
            loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        out = model(Xte_t, Tte_t)
        return (out.argmax(1).numpy() if task == "cls" else out.squeeze(-1).numpy()), yte


def _logreg(Xtr, ytr, Xte, n_cls=2, epochs=400, lr=0.1, wd=1e-3, cw=None):
    """Logistic regression on tabular features (standardized). Returns test preds."""
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    m = nn.Linear(Xtr.shape[1], n_cls)
    opt = torch.optim.Adam(m.parameters(), lr=lr, weight_decay=wd)
    wt = torch.tensor(cw) if cw is not None else None
    lf = nn.CrossEntropyLoss(weight=wt)
    Xt, yt = torch.tensor(Xtr, dtype=torch.float32), torch.tensor(ytr)
    for _ in range(epochs):
        opt.zero_grad(); lf(m(Xt), yt).backward(); opt.step()
    with torch.no_grad():
        return m(torch.tensor(Xte, dtype=torch.float32)).argmax(1).numpy()


def lossy_ablation(X, valid, y, classes, temp, vdr, tr, te, h, data_dir):
    """Confounder rejection in the REALISTIC lossy regime: reduce the waveform to a
    single runtime-observable scalar (eye margin) and detect healthy-vs-faulty with
    margin-only (A) vs margin+telemetry (B). Benign hot/drooped links have low margin
    (look faulty); telemetry rejects those false alarms."""
    mar = (np.percentile(X[:, valid], 90, axis=1)
           - np.percentile(X[:, valid], 10, axis=1)).astype(np.float32)  # eye margin [V]
    yb = (y != h).astype(np.int64)                                       # 1 = faulty
    cw = np.array([0.5 * len(yb[tr]) / max((yb[tr] == c).sum(), 1) for c in (0, 1)], np.float32)
    FA = np.column_stack([mar]).astype(np.float32)
    FB = np.column_stack([mar, temp / 100.0, vdr * 10.0]).astype(np.float32)

    def metrics(pred):
        yt = yb[te]
        acc = float((pred == yt).mean())
        hmask = yt == 0
        fa = float((pred[hmask] == 1).mean()) if hmask.any() else float("nan")
        sh = hmask & ((temp[te] >= 85) | (vdr[te] >= 0.05))
        fa_sh = float((pred[sh] == 1).mean()) if sh.any() else float("nan")
        rec = float((pred[yt == 1] == 1).mean())
        return {"acc": acc, "healthy_FA": fa, "stressed_healthy_FA": fa_sh, "fault_recall": rec}

    pA = _logreg(FA[tr], yb[tr], FA[te], cw=cw)
    pB = _logreg(FB[tr], yb[tr], FB[te], cw=cw)
    out = {"A_margin_only": metrics(pA), "B_margin_plus_telemetry": metrics(pB)}
    print("\n[lossy ablation]  scalar eye-margin detection (healthy vs faulty):")
    print(f"   A margin-only        : acc={out['A_margin_only']['acc']:.3f} "
          f"healthy-FA={out['A_margin_only']['healthy_FA']:.3f} "
          f"stressed-healthy-FA={out['A_margin_only']['stressed_healthy_FA']:.3f}")
    print(f"   B margin+telemetry   : acc={out['B_margin_plus_telemetry']['acc']:.3f} "
          f"healthy-FA={out['B_margin_plus_telemetry']['healthy_FA']:.3f} "
          f"stressed-healthy-FA={out['B_margin_plus_telemetry']['stressed_healthy_FA']:.3f}")
    _lossy_plot(mar, temp, yb, h, os.path.join(data_dir, "plots", "lossy_confounder.png"))
    return out


def _lossy_plot(mar, temp, yb, h, path):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for lab, c, name in [(0, "#2ca02c", "healthy"), (1, "#d62728", "faulty")]:
        m = yb == lab
        ax.scatter(mar[m] * 1e3, temp[m], c=c, alpha=0.5, s=22, label=name)
    ax.axvspan(390, 470, color="grey", alpha=0.12)
    ax.set_xlabel("eye margin [mV]  (the only runtime scalar)")
    ax.set_ylabel("temperature [C]  (telemetry)")
    ax.set_title("Why telemetry helps under lossy observation:\n"
                 "healthy & faulty OVERLAP in margin (grey), separable by adding temperature")
    ax.legend(); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def normalize(X, tr):
    mu, sd = X[tr].mean(), X[tr].std() + 1e-9
    return (X - mu) / sd


def to_cnn(X):
    return X[:, None, :].astype(np.float32)


def acc(pred, true):
    return float((pred == true).mean())


# ------------------------------------------------------------- experiments ----
def run(data_dir):
    X, y, classes, sev, tel, temp, meta = load_data(data_dir)
    valid, sig, non = region_masks(meta)
    h = classes.index("healthy") if "healthy" in classes else -1
    print(f"loaded {len(X)} waveforms, {X.shape[1]} samples, {len(classes)} classes")
    print(f"classes: {classes}")
    print(f"region split: valid={len(valid)} signal={len(sig)} held={len(non)} samples")
    tr, te = strat_split(y, 0.25, seed=0)
    Xn = normalize(X, tr)
    Xv = to_cnn(Xn[:, valid])
    # inverse-frequency class weights (healthy etc. are under-sampled)
    counts = np.bincount(y[tr], minlength=len(classes))
    cw = (len(y[tr]) / (len(classes) * np.maximum(counts, 1))).astype(np.float32)
    os.makedirs(os.path.join(data_dir, "plots"), exist_ok=True)
    results = {"n": len(X), "classes": classes, "n_test": len(te),
               "region_samples": {"valid": len(valid), "signal": len(sig), "held": len(non)}}

    # ---- baseline (logistic) vs CNN, waveform only ----
    base = Logistic(len(valid), len(classes))
    bp, bt = _fit(base, Xv[tr], y[tr], Xv[te], y[te], epochs=120, lr=1e-2, cw=cw)
    cnn = CNN1D(len(classes))
    cp, ct = _fit(cnn, Xv[tr], y[tr], Xv[te], y[te], cw=cw)
    results["baseline_logistic_acc"] = acc(bp, bt)
    results["cnn_waveform_acc"] = acc(cp, ct)
    print(f"\n[diagnosis]  logistic baseline = {acc(bp,bt):.3f}   CNN (waveform) = {acc(cp,ct):.3f}")
    _confusion(ct, cp, classes, os.path.join(data_dir, "plots", "confusion_cnn.png"))

    # ---- TELEMETRY ablation: A (waveform) vs B (waveform + temp/droop) ----
    print("\n[telemetry ablation]  confounder rejection:")
    mA = CNN1D(len(classes), n_tel=0)
    pA, tA = _fit(mA, Xv[tr], y[tr], Xv[te], y[te], cw=cw)
    mB = CNN1D(len(classes), n_tel=tel.shape[1])
    pB, tB = _fit(mB, Xv[tr], y[tr], Xv[te], y[te],
                  Ttr=tel[tr].astype(np.float32), Tte=tel[te].astype(np.float32), cw=cw)
    # confounded subset = hot OR drooped test links (eye closed by benign stress)
    stress = (temp[te] >= 85.0) | (tel[te, 1] >= 0.5)
    tele = {"A_overall": acc(pA, tA), "B_overall": acc(pB, tB),
            "A_highstress": acc(pA[stress], tA[stress]) if stress.any() else None,
            "B_highstress": acc(pB[stress], tB[stress]) if stress.any() else None}
    if h >= 0:
        hmask = tA == h
        tele["A_healthy_false_alarm"] = float((pA[hmask] != h).mean()) if hmask.any() else None
        tele["B_healthy_false_alarm"] = float((pB[hmask] != h).mean()) if hmask.any() else None
    results["telemetry_ablation"] = tele
    print(f"   A waveform-only   : overall={tele['A_overall']:.3f}  "
          f"high-stress={tele['A_highstress']}  healthy-FA={tele.get('A_healthy_false_alarm')}")
    print(f"   B +temp/droop     : overall={tele['B_overall']:.3f}  "
          f"high-stress={tele['B_highstress']}  healthy-FA={tele.get('B_healthy_false_alarm')}")
    _telemetry_plot(tele, os.path.join(data_dir, "plots", "telemetry_ablation.png"))

    # ---- LOSSY-regime ablation: telemetry helps when observation is a scalar ----
    results["lossy_ablation"] = lossy_ablation(X, valid, y, classes, temp,
                                               tel[:, 1] / 10.0, tr, te, h, data_dir)

    # ---- REGION ablation (waveform only) ----
    print("\n[region ablation]  CNN trained on each region (mean+-std over 3 re-inits):")
    abl, abl_std, per_class = {}, {}, {}
    for name, idx in [("full", valid), ("signal", sig), ("held", non)]:
        Xr = to_cnn(Xn[:, idx])
        accs, last = [], None
        for s in range(3):
            torch.manual_seed(s)
            m = CNN1D(len(classes))
            p, t = _fit(m, Xr[tr], y[tr], Xr[te], y[te], cw=cw)
            accs.append(acc(p, t)); last = (t, p)
        abl[name] = float(np.mean(accs)); abl_std[name] = float(np.std(accs))
        per_class[name] = _per_class_acc(last[0], last[1], len(classes))
        print(f"   {name:7s} ({len(idx):4d} samp): acc = {abl[name]:.3f} +- {abl_std[name]:.3f}")
    results["region_ablation_std"] = abl_std
    results["region_ablation_acc"] = abl
    results["region_ablation_per_class"] = {k: v.tolist() for k, v in per_class.items()}
    _ablation_plot(abl, per_class, classes, os.path.join(data_dir, "plots", "region_ablation.png"))

    # ---- severity regression on continuous drifts ----
    results["severity"] = {}
    for kind in ("r_drift", "c_drift"):
        if kind not in classes:
            continue
        ci = classes.index(kind)
        m_idx = np.where(y == ci)[0]
        ytr_s = np.array([i for i in tr if y[i] == ci])
        yte_s = np.array([i for i in te if y[i] == ci])
        if len(ytr_s) < 6 or len(yte_s) < 2:
            continue
        smin, smax = sev[m_idx].min(), sev[m_idx].max()
        sn = (sev - smin) / (smax - smin + 1e-9)
        reg = CNN1D(1)
        pred, _ = _fit(reg, Xv[ytr_s], sn[ytr_s].astype(np.float32),
                       Xv[yte_s], sn[yte_s].astype(np.float32), task="reg", lr=1e-3)
        true = sn[yte_s]
        mae = float(np.abs(pred - true).mean())
        r2 = 1 - float(((pred - true) ** 2).sum()) / (float(((true - true.mean()) ** 2).sum()) + 1e-9)
        results["severity"][kind] = {"mae_norm": mae, "r2": r2, "n_test": len(yte_s)}
        print(f"[severity {kind}] MAE(norm)={mae:.3f}  R2={r2:.3f}  (n_test={len(yte_s)})")
        _sev_plot(true * (smax - smin) + smin, pred * (smax - smin) + smin, kind,
                  os.path.join(data_dir, "plots", f"severity_{kind}.png"))

    _example_waveforms(X, y, classes, meta, os.path.join(data_dir, "plots", "examples.png"))
    json.dump(results, open(os.path.join(data_dir, "results.json"), "w"), indent=2)
    print(f"\nresults -> {os.path.join(data_dir,'results.json')}  plots -> {data_dir}/plots/")
    return results


# ------------------------------------------------------------- plotting -------
def _per_class_acc(true, pred, n):
    out = np.full(n, np.nan)
    for c in range(n):
        m = true == c
        if m.any():
            out[c] = (pred[m] == c).mean()
    return out


def _confusion(true, pred, classes, path):
    n = len(classes)
    C = np.zeros((n, n), int)
    for t, p in zip(true, pred):
        C[t, p] += 1
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(C, cmap="Blues")
    ax.set_xticks(range(n)); ax.set_xticklabels(classes, rotation=60, ha="right", fontsize=7)
    ax.set_yticks(range(n)); ax.set_yticklabels(classes, fontsize=7)
    ax.set_xlabel("predicted"); ax.set_ylabel("true"); ax.set_title("CNN confusion (raw waveform)")
    for i in range(n):
        for j in range(n):
            if C[i, j]:
                ax.text(j, i, C[i, j], ha="center", va="center", fontsize=7,
                        color="white" if C[i, j] > C.max() / 2 else "black")
    fig.colorbar(im); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _telemetry_plot(t, path):
    fig, ax = plt.subplots(figsize=(7, 5))
    groups = ["overall", "high-stress", "healthy false-alarm"]
    A = [t["A_overall"], t.get("A_highstress") or 0, t.get("A_healthy_false_alarm") or 0]
    B = [t["B_overall"], t.get("B_highstress") or 0, t.get("B_healthy_false_alarm") or 0]
    x = np.arange(len(groups)); w = 0.36
    ax.bar(x - w / 2, A, w, label="A: waveform only", color="#d62728")
    ax.bar(x + w / 2, B, w, label="B: + temp/droop telemetry", color="#1f77b4")
    ax.set_xticks(x); ax.set_xticklabels(groups); ax.set_ylim(0, 1)
    ax.set_ylabel("rate"); ax.set_title("Telemetry fusion rejects the benign-stress confounder")
    for i in range(len(groups)):
        ax.text(x[i] - w / 2, A[i] + 0.01, f"{A[i]:.2f}", ha="center", fontsize=8)
        ax.text(x[i] + w / 2, B[i] + 0.01, f"{B[i]:.2f}", ha="center", fontsize=8)
    ax.legend(); fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _ablation_plot(abl, per_class, classes, path):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5.5))
    names = ["full", "signal", "held"]
    a1.bar(names, [abl[n] for n in names], color=["#444", "#1f77b4", "#d62728"])
    a1.set_ylabel("overall accuracy"); a1.set_ylim(0, 1); a1.set_title("Region ablation (overall)")
    for i, n in enumerate(names):
        a1.text(i, abl[n] + 0.01, f"{abl[n]:.2f}", ha="center")
    x = np.arange(len(classes)); w = 0.27
    for i, n in enumerate(names):
        a2.bar(x + (i - 1) * w, np.nan_to_num(per_class[n]), w, label=n)
    a2.set_xticks(x); a2.set_xticklabels(classes, rotation=60, ha="right", fontsize=7)
    a2.set_ylabel("per-class accuracy"); a2.set_ylim(0, 1)
    a2.set_title("Where each fault's signature lives"); a2.legend()
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _sev_plot(true, pred, kind, path):
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.scatter(true, pred, alpha=0.7)
    lo, hi = min(true.min(), pred.min()), max(true.max(), pred.max())
    ax.plot([lo, hi], [lo, hi], "k--", lw=1)
    ax.set_xlabel(f"true {kind} severity"); ax.set_ylabel("predicted")
    ax.set_title(f"Severity regression: {kind}")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def _example_waveforms(X, y, classes, meta, path):
    spu = meta["samples_per_ui"]
    fig, axes = plt.subplots(len(classes), 1, figsize=(11, 1.5 * len(classes)), sharex=True)
    t = np.arange(X.shape[1]) / spu
    for ax, c in zip(axes, classes):
        idx = np.where(y == classes.index(c))[0][0]
        ax.plot(t, X[idx], lw=0.6)
        ax.set_ylabel(c, fontsize=7, rotation=0, ha="right", va="center"); ax.set_yticks([])
    axes[-1].set_xlabel("UI"); axes[0].set_title("One raw RX waveform per fault class")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/wave")
    run(ap.parse_args().data)
