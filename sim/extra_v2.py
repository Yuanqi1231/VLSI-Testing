"""Slow v2 add-on experiments: LSTM comparison + region ablation (per-row masks).

    ~/miniconda3/envs/drl_hw2/bin/python extra_v2.py --data out/wave2

  (A) LSTM on the raw waveform, 10-class single-fault subset (vs the CNN).
  (B) REGION ablation with per-row edge/held masks (v2 bits differ per row, so
      regions are zeroed out per row instead of column-sliced): full / edge-only
      / held-only, 3 re-inits each.

Outputs: <data>/extra_v2.json, plots/region_ablation_v2.png
"""
import argparse
import json
import os

import numpy as np
import torch
import torch.nn as nn

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ml_diagnose_v2 import load_v2, strat_split_by, normalize, fit, CNN1Dv2
from why_ai_v2 import row_signal_masks


class LSTM1D(nn.Module):
    """2-layer LSTM over the (strided) waveform; final hidden state -> logits."""
    def __init__(self, n_out, hidden=64, layers=2, stride=2):
        super().__init__()
        self.stride = stride
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden, num_layers=layers,
                            batch_first=True, dropout=0.1)
        self.head = nn.Sequential(nn.Linear(hidden, 64), nn.ReLU(),
                                  nn.Linear(64, n_out))

    def forward(self, x, tel=None):
        seq = x[:, 0, ::self.stride].unsqueeze(-1)
        _, (hh, _) = self.lstm(seq)
        return self.head(hh[-1])


def per_class_acc(true, pred, n):
    out = np.full(n, np.nan)
    for c in range(n):
        mk = true == c
        if mk.any():
            out[c] = float((pred[mk] == c).mean())
    return out


def main(data_dir, epochs=60):
    X, Y, prim, single, classes, faults, sev, tel, temp, vdr, seeds, meta = load_v2(data_dir)
    spu, settle, m = meta["samples_per_ui"], meta["settle_bits"], meta["n_samples"]
    valid = np.arange(settle * spu, m)
    strata = np.array([classes[p] if p >= 0 else "mixed" for p in prim])
    tr, te = strat_split_by(strata, 0.25, seed=0)
    si = np.where(single)[0]
    tr3, te3 = strat_split_by(prim[si], 0.25, seed=0)
    tr3, te3 = si[tr3], si[te3]
    y3 = prim
    n_cls = len(classes)
    cw = (len(tr3) / (n_cls * np.maximum(
        np.bincount(y3[tr3], minlength=n_cls), 1))).astype(np.float32)
    Xn = normalize(X, tr)
    rx = Xn[:, None, valid].astype(np.float32)
    out = {}

    # ---- (A) LSTM ----
    print("[A] LSTM (10-class single-fault, waveform only)...", flush=True)
    p = fit(LSTM1D(n_cls), rx[tr3], y3[tr3], rx[te3],
            task="cls", epochs=epochs, lr=2e-3, cw=cw).argmax(1)
    out["lstm_acc"] = float((p == y3[te3]).mean())
    print(f"   LSTM acc = {out['lstm_acc']:.3f}", flush=True)

    # ---- (B) region ablation with per-row masks ----
    print("[B] region ablation (per-row masks, 3 re-inits)...", flush=True)
    sig = row_signal_masks(seeds, meta)[:, valid]      # (N, len(valid)) bool
    out["region"] = {}
    per_class = {}
    for name, mask in [("full", None), ("edge", sig), ("held", ~sig)]:
        Xr = rx.copy()
        if mask is not None:
            Xr[:, 0, :][~mask] = 0.0
        accs, last = [], None
        for s in range(3):
            p = fit(CNN1Dv2(n_cls, in_ch=1), Xr[tr3], y3[tr3], Xr[te3],
                    task="cls", epochs=epochs, cw=cw, seed=s).argmax(1)
            accs.append(float((p == y3[te3]).mean()))
            last = p
        out["region"][name] = {"mean": float(np.mean(accs)), "std": float(np.std(accs))}
        per_class[name] = per_class_acc(y3[te3], last, n_cls)
        print(f"   {name:5s}: acc = {np.mean(accs):.3f} +- {np.std(accs):.3f}", flush=True)

    # plot
    plots = os.path.join(data_dir, "plots")
    os.makedirs(plots, exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5.5))
    names = ["full", "edge", "held"]
    a1.bar(names, [out["region"][n]["mean"] for n in names],
           yerr=[out["region"][n]["std"] for n in names],
           color=["#444", "#1f77b4", "#d62728"], capsize=4)
    a1.set_ylabel("overall accuracy"); a1.set_ylim(0, 1)
    a1.set_title("v2 region ablation (overall)")
    for i, n in enumerate(names):
        a1.text(i, out["region"][n]["mean"] + 0.02,
                f"{out['region'][n]['mean']:.2f}", ha="center")
    x = np.arange(n_cls); w = 0.27
    for i, n in enumerate(names):
        a2.bar(x + (i - 1) * w, np.nan_to_num(per_class[n]), w, label=n)
    a2.set_xticks(x); a2.set_xticklabels(classes, rotation=60, ha="right", fontsize=7)
    a2.set_ylabel("per-class accuracy"); a2.set_ylim(0, 1)
    a2.set_title("Where each fault's signature lives (v2)"); a2.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(plots, "region_ablation_v2.png"), dpi=130)
    plt.close(fig)
    out["region_per_class"] = {k: np.nan_to_num(v).tolist() for k, v in per_class.items()}

    json.dump(out, open(os.path.join(data_dir, "extra_v2.json"), "w"), indent=2)
    print(f"-> {os.path.join(data_dir, 'extra_v2.json')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/wave2")
    ap.add_argument("--epochs", type=int, default=60)
    a = ap.parse_args()
    main(a.data, epochs=a.epochs)
