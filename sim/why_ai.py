"""Why is a learned model necessary? Two non-ML / shallow baselines for contrast.

Run:  ~/miniconda3/envs/drl_hw2/bin/python why_ai.py --data out/wave

(1) RULE baseline in the lossy regime: the natural test-engineer alternative to ML
    is a single eye-margin threshold "flag faulty if margin < tau". We give the rule
    every advantage -- we tune tau on the TEST set itself (an oracle upper bound for
    any single-threshold rule) -- and show it still cannot separate benign high-stress
    healthy links from faults, because they OVERLAP in margin. We report:
      * best-accuracy threshold: its accuracy and the false-alarm it is forced to incur
      * the threshold that first reaches zero healthy false-alarm: the recall it destroys
    Contrast with the learned 2-D (margin, temperature) boundary.

(2) HAND-CRAFTED-FEATURE baseline for the 10-class diagnosis: instead of the raw
    1024-pt waveform, extract a small vector of standard eye features (mean level,
    eye margin, std, max slew, and their edge/held-region versions) and train the
    SAME logistic and a small MLP on them. This isolates "did learning a
    representation from the raw signal help, vs. classic feature engineering?".
"""
import argparse
import json
import os

import numpy as np
import torch
import torch.nn as nn

from ml_diagnose import load_data, region_masks, strat_split, _logreg

torch.manual_seed(0)
np.random.seed(0)


# ----------------------------------------------------------------- (1) rule ----
def rule_baseline(X, valid, y, classes, temp, vdr, tr, te):
    h = classes.index("healthy")
    mar = (np.percentile(X[:, valid], 90, axis=1)
           - np.percentile(X[:, valid], 10, axis=1)).astype(np.float32)  # eye margin [V]
    yb = (y != h).astype(np.int64)                                       # 1 = faulty
    mte, yte = mar[te], yb[te]
    hmask = yte == 0
    sh = hmask & ((temp[te] >= 85) | (vdr[te] >= 0.05))                  # stressed healthy

    # sweep every candidate threshold; predict faulty if margin < tau
    taus = np.unique(mte)
    best = None
    zero_fa = None
    for tau in taus:
        pred = (mte < tau).astype(int)
        acc = (pred == yte).mean()
        fa = (pred[hmask] == 1).mean() if hmask.any() else 0.0
        rec = (pred[yte == 1] == 1).mean()
        fa_sh = (pred[sh] == 1).mean() if sh.any() else float("nan")
        if best is None or acc > best["acc"]:
            best = {"tau_mV": float(tau * 1e3), "acc": float(acc), "healthy_FA": float(fa),
                    "stressed_healthy_FA": float(fa_sh), "fault_recall": float(rec)}
        if fa == 0.0 and (zero_fa is None or rec > zero_fa["fault_recall"]):
            zero_fa = {"tau_mV": float(tau * 1e3), "acc": float(acc),
                       "fault_recall": float(rec), "healthy_FA": 0.0}
    return {"best_accuracy_threshold": best, "first_zero_FA_threshold": zero_fa}


# ------------------------------------------------- (2) hand-crafted features ----
def _feat(Xsub):
    """A small vector of standard eye/signal features over a set of samples."""
    mean = Xsub.mean(1)
    margin = np.percentile(Xsub, 90, 1) - np.percentile(Xsub, 10, 1)
    std = Xsub.std(1)
    slew = np.abs(np.diff(Xsub, axis=1)).max(1)
    p10 = np.percentile(Xsub, 10, 1)
    p90 = np.percentile(Xsub, 90, 1)
    return np.stack([mean, margin, std, slew, p10, p90], axis=1)


def handcrafted_baseline(X, valid, sig, non, y, classes, tr, te):
    # eye features on full / edge / held regions -> 18-D engineered vector
    F = np.concatenate([_feat(X[:, valid]), _feat(X[:, sig]), _feat(X[:, non])], axis=1).astype(np.float32)
    counts = np.bincount(y[tr], minlength=len(classes))
    cw = (len(y[tr]) / (len(classes) * np.maximum(counts, 1))).astype(np.float32)

    # logistic on engineered features
    pred_lr = _logreg(F[tr], y[tr], F[te], n_cls=len(classes), cw=cw)
    acc_lr = float((pred_lr == y[te]).mean())

    # small MLP on the SAME engineered features (shallow learning, no conv)
    mu, sd = F[tr].mean(0), F[tr].std(0) + 1e-9
    Fn = (F - mu) / sd
    net = nn.Sequential(nn.Linear(F.shape[1], 64), nn.ReLU(),
                        nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, len(classes)))
    opt = torch.optim.Adam(net.parameters(), lr=2e-3, weight_decay=1e-4)
    lf = nn.CrossEntropyLoss(weight=torch.tensor(cw))
    Xt, yt = torch.tensor(Fn[tr]), torch.tensor(y[tr])
    for _ in range(400):
        opt.zero_grad(); lf(net(Xt), yt).backward(); opt.step()
    with torch.no_grad():
        pred_mlp = net(torch.tensor(Fn[te])).argmax(1).numpy()
    acc_mlp = float((pred_mlp == y[te]).mean())
    return {"n_features": F.shape[1], "logistic_on_features_acc": acc_lr,
            "mlp_on_features_acc": acc_mlp}


def main(data_dir):
    X, y, classes, sev, tel, temp, meta = load_data(data_dir)
    valid, sig, non = region_masks(meta)
    tr, te = strat_split(y, 0.25, seed=0)
    vdr = tel[:, 1] / 10.0

    out = {}
    out["rule_lossy"] = rule_baseline(X, valid, y, classes, temp, vdr, tr, te)
    out["handcrafted_10class"] = handcrafted_baseline(X, valid, sig, non, y, classes, tr, te)

    print("\n=== (1) single eye-margin RULE in the lossy regime (oracle-tuned tau) ===")
    b = out["rule_lossy"]["best_accuracy_threshold"]
    z = out["rule_lossy"]["first_zero_FA_threshold"]
    print(f"  best-accuracy tau = {b['tau_mV']:.0f} mV : acc={b['acc']:.3f}  "
          f"healthy-FA={b['healthy_FA']:.3f}  stressed-healthy-FA={b['stressed_healthy_FA']:.3f}  "
          f"recall={b['fault_recall']:.3f}")
    if z:
        print(f"  to force healthy-FA=0 -> tau={z['tau_mV']:.0f} mV : recall collapses to "
              f"{z['fault_recall']:.3f} (acc={z['acc']:.3f})")
    else:
        print("  NO threshold achieves healthy-FA=0 without flagging every link.")
    print("  (cf. learned margin+temp boundary: acc=0.732, FA=0.000, recall=0.720)")

    print("\n=== (2) hand-crafted eye-feature baselines (10-class) ===")
    hc = out["handcrafted_10class"]
    print(f"  {hc['n_features']}-D engineered features:")
    print(f"    logistic = {hc['logistic_on_features_acc']:.3f}")
    print(f"    MLP      = {hc['mlp_on_features_acc']:.3f}")
    print("  (cf. raw-waveform logistic=0.702, raw-waveform CNN=0.803)")

    json.dump(out, open(os.path.join(data_dir, "why_ai.json"), "w"), indent=2)
    print(f"\n-> {os.path.join(data_dir, 'why_ai.json')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/wave")
    main(ap.parse_args().data)
