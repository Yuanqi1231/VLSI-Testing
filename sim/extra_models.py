"""Two add-on experiments requested for the report:

  (A) LSTM sequence classifier on the raw RX waveform, as a second AI model
      alongside the 1-D CNN (the waveform is a time series; an LSTM reads it
      sample-by-sample and keeps a recurrent state).

  (B) ROOT-CAUSE vs BINARY: can a conventional single scalar (the eye margin)
      assign the 10-way root-cause class, or only a healthy/faulty bit? We fit a
      multinomial classifier on (i) the eye-margin scalar alone, (ii) margin +
      telemetry, and (iii) the full waveform (CNN), and compare 10-class accuracy
      and macro-F1. This quantifies the claim "conventional methods are limited to
      binary detection; the learned model recovers the root cause."

Run:  ~/miniconda3/envs/drl_hw2/bin/python extra_models.py --data out/wave
"""
import argparse
import json
import os

import numpy as np
import torch
import torch.nn as nn

from ml_diagnose import (load_data, region_masks, strat_split, normalize,
                         to_cnn, _fit, _logreg, CNN1D, acc)

torch.manual_seed(0)
np.random.seed(0)


# --------------------------------------------------------------- (A) LSTM ------
class LSTM1D(nn.Module):
    """LSTM over the waveform. Input (N,1,T) -> (N,T,1); the last hidden state of a
    2-layer LSTM is mapped to the class logits. Optionally fuses scalar telemetry."""
    def __init__(self, n_out, n_tel=0, hidden=64, layers=2, stride=2):
        super().__init__()
        self.stride = stride
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden, num_layers=layers,
                            batch_first=True, dropout=0.1)
        self.head = nn.Sequential(nn.Linear(hidden + n_tel, 64), nn.ReLU(),
                                  nn.Linear(64, n_out))

    def forward(self, x, tel=None):
        seq = x[:, 0, ::self.stride].unsqueeze(-1)      # (N, T/stride, 1)
        out, (h, _) = self.lstm(seq)
        f = h[-1]                                       # last layer's final hidden state
        if tel is not None:
            f = torch.cat([f, tel], dim=1)
        return self.head(f)


def macro_f1(true, pred, n):
    f1s = []
    for c in range(n):
        tp = np.sum((pred == c) & (true == c))
        fp = np.sum((pred == c) & (true != c))
        fn = np.sum((pred != c) & (true == c))
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if (prec + rec) else 0.0)
    return float(np.mean(f1s))


# ----------------------------------------- (B) root-cause from a scalar --------
def scalar_rootcause(X, valid, y, classes, temp, vdr, tr, te):
    n = len(classes)
    mar = (np.percentile(X[:, valid], 90, axis=1)
           - np.percentile(X[:, valid], 10, axis=1)).astype(np.float32)
    counts = np.bincount(y[tr], minlength=n)
    cw = (len(y[tr]) / (n * np.maximum(counts, 1))).astype(np.float32)
    majority = float((y[te] == np.bincount(y[tr]).argmax()).mean())

    F1 = mar[:, None]
    F3 = np.stack([mar, temp / 100.0, vdr * 10.0], axis=1).astype(np.float32)
    p1 = _logreg(F1[tr], y[tr], F1[te], n_cls=n, cw=cw)
    p3 = _logreg(F3[tr], y[tr], F3[te], n_cls=n, cw=cw)
    return {
        "majority_class_acc": majority,
        "margin_scalar": {"acc": float((p1 == y[te]).mean()), "macro_f1": macro_f1(y[te], p1, n)},
        "margin_plus_telemetry": {"acc": float((p3 == y[te]).mean()), "macro_f1": macro_f1(y[te], p3, n)},
    }


def main(data_dir):
    X, y, classes, sev, tel, temp, meta = load_data(data_dir)
    valid, sig, non = region_masks(meta)
    n = len(classes)
    tr, te = strat_split(y, 0.25, seed=0)
    Xn = normalize(X, tr)
    Xv = to_cnn(Xn[:, valid])
    counts = np.bincount(y[tr], minlength=n)
    cw = (len(y[tr]) / (n * np.maximum(counts, 1))).astype(np.float32)
    vdr = tel[:, 1] / 10.0

    out = {}

    # (A) LSTM (waveform only) and LSTM (+telemetry)
    print("[LSTM] training (this is the slow one)...")
    torch.manual_seed(0)
    lstm = LSTM1D(n)
    pL, tL = _fit(lstm, Xv[tr], y[tr], Xv[te], y[te], epochs=60, lr=2e-3, cw=cw)
    torch.manual_seed(0)
    lstmB = LSTM1D(n, n_tel=tel.shape[1])
    pLB, tLB = _fit(lstmB, Xv[tr], y[tr], Xv[te], y[te],
                    Ttr=tel[tr].astype(np.float32), Tte=tel[te].astype(np.float32),
                    epochs=60, lr=2e-3, cw=cw)
    out["lstm_waveform_acc"] = acc(pL, tL)
    out["lstm_waveform_macro_f1"] = macro_f1(tL, pL, n)
    out["lstm_plus_telemetry_acc"] = acc(pLB, tLB)
    print(f"   LSTM waveform-only  acc = {out['lstm_waveform_acc']:.3f}  "
          f"macroF1 = {out['lstm_waveform_macro_f1']:.3f}")
    print(f"   LSTM + telemetry    acc = {out['lstm_plus_telemetry_acc']:.3f}")

    # CNN macro-F1 for a fair side-by-side (acc already in results.json)
    torch.manual_seed(0)
    cnn = CNN1D(n)
    pC, tC = _fit(cnn, Xv[tr], y[tr], Xv[te], y[te], cw=cw)
    out["cnn_waveform_acc"] = acc(pC, tC)
    out["cnn_waveform_macro_f1"] = macro_f1(tC, pC, n)
    print(f"   CNN  waveform-only  acc = {out['cnn_waveform_acc']:.3f}  "
          f"macroF1 = {out['cnn_waveform_macro_f1']:.3f}")

    # (B) root-cause from a single scalar
    out["rootcause_from_scalar"] = scalar_rootcause(X, valid, y, classes, temp, vdr, tr, te)
    rc = out["rootcause_from_scalar"]
    print("\n[root-cause vs binary]  10-class accuracy / macro-F1:")
    print(f"   majority-class floor      : acc={rc['majority_class_acc']:.3f}")
    print(f"   eye-margin scalar only    : acc={rc['margin_scalar']['acc']:.3f}  "
          f"F1={rc['margin_scalar']['macro_f1']:.3f}")
    print(f"   margin + telemetry        : acc={rc['margin_plus_telemetry']['acc']:.3f}  "
          f"F1={rc['margin_plus_telemetry']['macro_f1']:.3f}")
    print(f"   CNN on full waveform      : acc={out['cnn_waveform_acc']:.3f}  "
          f"F1={out['cnn_waveform_macro_f1']:.3f}")

    json.dump(out, open(os.path.join(data_dir, "extra_models.json"), "w"), indent=2)
    print(f"\n-> {os.path.join(data_dir, 'extra_models.json')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/wave")
    main(ap.parse_args().data)
