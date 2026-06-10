"""Why-AI baselines on the v2 dataset (fast experiments; LSTM/region in extra_v2).

    ~/miniconda3/envs/drl_hw2/bin/python why_ai_v2.py --data out/wave2

  (A) RULE: oracle-tuned single threshold on the eye-margin scalar vs a learned
      (margin, temp, droop) boundary -- both evaluated at their best-accuracy and
      first-zero-FA operating points (binary healthy-vs-faulty, all rows).
  (B) HANDCRAFTED: 18-D eye features (mean/margin/std/slew/p10/p90 over
      full/edge/held regions, per-row masks from each row's own PRBS bits) ->
      logistic + small MLP, 10-class on the single-fault subset; vs the CNN.
  (C) RAW-WAVEFORM LOGISTIC: 10-class logistic on the raw waveform (single-fault
      subset) -- the linear baseline for the diagnosis table.
  (D) SCALAR ROOT-CAUSE: 10-class from the margin scalar (+telemetry).

Outputs: <data>/why_ai_v2.json
"""
import argparse
import json
import os

import numpy as np
import torch.nn as nn

from d2dsim.prbs import prbs_bits
from ml_diagnose_v2 import (load_v2, strat_split_by, normalize, fit,
                            LogisticML, CNN1Dv2)


def row_signal_masks(seeds, meta):
    """Per-row edge-region mask (+-0.5 UI around each transition of that row's
    own bits, shifted by the nominal RX delay)."""
    spu, nb, m = meta["samples_per_ui"], meta["n_bits"], meta["n_samples"]
    dly, order = meta["delay_samples"], meta["prbs_order"]
    w = spu // 2
    cache = {}
    out = np.zeros((len(seeds), m), dtype=bool)
    for i, s in enumerate(seeds):
        if s not in cache:
            bits = prbs_bits(order, nb, int(s))
            mk = np.zeros(m, dtype=bool)
            for b in range(1, len(bits)):
                if bits[b] != bits[b - 1]:
                    c = b * spu + dly
                    mk[max(0, c - w):min(m, c + w + 1)] = True
            cache[s] = mk
        out[i] = cache[s]
    return out


def region_feats(X, mask):
    """6 stats per region: mean, p90-p10, std, mean|dv|, p10, p90 (row-wise mask)."""
    Xm = np.where(mask, X, np.nan)
    mean = np.nanmean(Xm, 1)
    std = np.nanstd(Xm, 1)
    p10 = np.nanpercentile(Xm, 10, 1)
    p90 = np.nanpercentile(Xm, 90, 1)
    d = np.abs(np.diff(X, axis=1))
    dmask = mask[:, 1:] & mask[:, :-1]
    slew = np.nanmean(np.where(dmask, d, np.nan), 1)
    return np.stack([mean, p90 - p10, std, slew, p10, p90], 1)


def operating_points(score, yb):
    """Sweep thresholds on a 'more faulty when larger' score: return best-acc and
    first-zero-FA (max recall subject to FA=0) operating points."""
    ths = np.unique(score)
    best = {"acc": -1.0}
    zfa = {"recall": 0.0, "acc": None}
    for t in ths:
        pred = (score >= t).astype(int)
        acc = float((pred == yb).mean())
        fa = float(pred[yb == 0].mean())
        rec = float(pred[yb == 1].mean())
        if acc > best["acc"]:
            best = {"acc": acc, "FA": fa, "recall": rec}
        if fa == 0.0 and rec > zfa["recall"]:
            zfa = {"recall": rec, "acc": acc}
    return best, zfa


def main(data_dir):
    X, Y, prim, single, classes, faults, sev, tel, temp, vdr, seeds, meta = load_v2(data_dir)
    spu, settle, m = meta["samples_per_ui"], meta["settle_bits"], meta["n_samples"]
    valid = np.arange(settle * spu, m)
    h = classes.index("healthy")
    strata = np.array([classes[p] if p >= 0 else "mixed" for p in prim])
    tr, te = strat_split_by(strata, 0.25, seed=0)          # same split as ml v2
    out = {}

    # margins
    mar = (np.percentile(X[:, valid], 90, axis=1)
           - np.percentile(X[:, valid], 10, axis=1)).astype(np.float32)
    yb = (Y.sum(1) > 0).astype(np.int64)

    # ---- (A) rule vs learned boundary, both oracle-tuned on the test set ----
    rule_best, rule_zfa = operating_points(-mar[te], yb[te])   # faulty = small margin
    F3 = np.stack([mar, temp / 100.0, vdr * 10.0], 1).astype(np.float32)
    cwb = np.array([0.5 * len(tr) / max((yb[tr] == c).sum(), 1) for c in (0, 1)], np.float32)
    lo = fit(LogisticML(3, 2), F3[tr, None, :], yb[tr], F3[te, None, :],
             task="cls", epochs=200, lr=0.05, cw=cwb)
    score = lo[:, 1] - lo[:, 0]
    lrn_best, lrn_zfa = operating_points(score, yb[te])
    out["rule_vs_learned"] = {
        "rule_margin_only": {"best": rule_best, "zero_FA": rule_zfa},
        "learned_margin_tel": {"best": lrn_best, "zero_FA": lrn_zfa}}
    print("[A] rule vs learned (binary, oracle operating points):")
    print(f"   rule    best acc={rule_best['acc']:.3f} (FA={rule_best['FA']:.3f}) "
          f"| zero-FA recall={rule_zfa['recall']:.3f}")
    print(f"   learned best acc={lrn_best['acc']:.3f} (FA={lrn_best['FA']:.3f}) "
          f"| zero-FA recall={lrn_zfa['recall']:.3f}")

    # ---- single-fault subset for 10-class ----
    si = np.where(single)[0]
    tr3, te3 = strat_split_by(prim[si], 0.25, seed=0)
    tr3, te3 = si[tr3], si[te3]
    y3 = prim
    n_cls = len(classes)
    cw = (len(tr3) / (n_cls * np.maximum(
        np.bincount(y3[tr3], minlength=n_cls), 1))).astype(np.float32)

    # ---- (B) 18-D handcrafted eye features ----
    print("[B] handcrafted 18-D features (10-class, single-fault):")
    sig = row_signal_masks(seeds, meta)
    vm = np.zeros(m, bool); vm[valid] = True
    F = np.concatenate([region_feats(X, np.broadcast_to(vm, X.shape)),
                        region_feats(X, sig & vm),
                        region_feats(X, ~sig & vm)], 1).astype(np.float32)
    mu, sd = F[tr3].mean(0), F[tr3].std(0) + 1e-9
    Fn = (F - mu) / sd
    p = fit(LogisticML(F.shape[1], n_cls), Fn[tr3, None, :], y3[tr3],
            Fn[te3, None, :], task="cls", epochs=300, lr=0.05, cw=cw).argmax(1)
    out["handcrafted_logistic_acc"] = float((p == y3[te3]).mean())
    mlp = nn.Sequential(nn.Flatten(), nn.Linear(F.shape[1], 64), nn.ReLU(),
                        nn.Linear(64, n_cls))
    mlp.forward_orig = mlp.forward
    class Wrap(nn.Module):
        def __init__(s, mod): super().__init__(); s.m = mod
        def forward(s, x, tel=None): return s.m(x)
    p = fit(Wrap(mlp), Fn[tr3, None, :], y3[tr3], Fn[te3, None, :],
            task="cls", epochs=300, lr=2e-3, cw=cw).argmax(1)
    out["handcrafted_mlp_acc"] = float((p == y3[te3]).mean())
    print(f"   logistic={out['handcrafted_logistic_acc']:.3f}  "
          f"mlp={out['handcrafted_mlp_acc']:.3f}")

    # ---- (C) raw-waveform logistic, 10-class ----
    Xn = normalize(X, tr)
    rx = Xn[:, None, valid].astype(np.float32)
    p = fit(LogisticML(len(valid), n_cls), rx[tr3], y3[tr3], rx[te3],
            task="cls", epochs=120, lr=1e-2, cw=cw).argmax(1)
    out["raw_logistic_acc"] = float((p == y3[te3]).mean())
    print(f"[C] raw-waveform logistic (10-class) = {out['raw_logistic_acc']:.3f}")

    # ---- (D) root cause from the scalar ----
    maj = float((y3[te3] == np.bincount(y3[tr3]).argmax()).mean())
    F1 = mar[:, None].astype(np.float32)
    p1 = fit(LogisticML(1, n_cls), F1[tr3, None, :], y3[tr3], F1[te3, None, :],
             task="cls", epochs=300, lr=0.05, cw=cw).argmax(1)
    p3 = fit(LogisticML(3, n_cls), F3[tr3, None, :], y3[tr3], F3[te3, None, :],
             task="cls", epochs=300, lr=0.05, cw=cw).argmax(1)
    out["rootcause_from_scalar"] = {
        "majority_floor": maj,
        "margin_only_acc": float((p1 == y3[te3]).mean()),
        "margin_tel_acc": float((p3 == y3[te3]).mean())}
    print(f"[D] root-cause from scalar: majority={maj:.3f}  "
          f"margin={out['rootcause_from_scalar']['margin_only_acc']:.3f}  "
          f"margin+tel={out['rootcause_from_scalar']['margin_tel_acc']:.3f}")

    json.dump(out, open(os.path.join(data_dir, "why_ai_v2.json"), "w"), indent=2)
    print(f"-> {os.path.join(data_dir, 'why_ai_v2.json')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/wave2")
    main(ap.parse_args().data)
