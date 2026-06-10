"""Visually inspect the raw-waveform dataset (no ML; numpy/matplotlib env).

    ~/miniconda3/envs/drl_hw2/bin/python inspect_waves.py --data out/wave

Produces under <data>/inspect/:
  eyes.png        : eye diagram (folded over 2 UI) per fault class
  waveforms.png   : a few overlaid raw RX waveforms per class
  overview.png    : class counts + (temp, vdroop) telemetry coverage
"""
import argparse
import csv
import json
import os
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load(data_dir):
    meta = json.load(open(os.path.join(data_dir, "meta.json")))
    by_class = defaultdict(list)
    rows = []
    with open(os.path.join(data_dir, "waveforms.csv")) as f:
        r = csv.reader(f)
        header = next(r)
        col = {c: i for i, c in enumerate(header)}
        s0 = col["s0"]
        for line in r:
            if len(line) <= s0 + 10:          # skip truncated last line (mid-write)
                continue
            try:
                w = np.asarray([float(x) for x in line[s0:]], np.float32)
            except ValueError:
                continue
            rec = dict(label=line[col["label"]], temp=float(line[col["temp_C"]]),
                       vdr=float(line[col["vdroop_frac"]]), sev=line[col["sev"]], wave=w)
            by_class[rec["label"]].append(rec)
            rows.append(rec)
    return meta, by_class, rows


def eye_fold(wave, spu, settle, dly, n_ui=2):
    """Fold the post-settle waveform into overlaid n_ui-wide traces (the eye)."""
    w = wave[settle * spu + dly:]
    seg = n_ui * spu
    n = len(w) // spu - n_ui
    return [w[i * spu:i * spu + seg] for i in range(max(n, 0))]


def plot_eyes(meta, by_class, path):
    spu, settle, dly = meta["samples_per_ui"], meta["settle_bits"], meta["delay_samples"]
    classes = sorted(by_class)
    ncol = 3
    nrow = (len(classes) + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol, figsize=(4 * ncol, 2.6 * nrow))
    axes = np.atleast_1d(axes).ravel()
    tx = np.arange(2 * spu) / spu
    for ax, c in zip(axes, classes):
        # overlay eyes from up to 6 runs of this class (mix of temps/droops)
        for rec in by_class[c][:6]:
            for seg in eye_fold(rec["wave"], spu, settle, dly):
                if len(seg) == 2 * spu:
                    ax.plot(tx, seg, color="#1f77b4", alpha=0.06, lw=0.6)
        ax.set_title(c, fontsize=9)
        ax.set_xlabel("UI", fontsize=7); ax.set_ylim(-0.05, 0.85)
        ax.tick_params(labelsize=6)
    for ax in axes[len(classes):]:
        ax.axis("off")
    fig.suptitle("Eye diagrams per fault class (folded over 2 UI)", fontsize=12)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def plot_waveforms(meta, by_class, path):
    spu = meta["samples_per_ui"]
    classes = sorted(by_class)
    fig, axes = plt.subplots(len(classes), 1, figsize=(12, 1.4 * len(classes)), sharex=True)
    axes = np.atleast_1d(axes)
    for ax, c in zip(axes, classes):
        recs = by_class[c][:3]
        t = np.arange(len(recs[0]["wave"])) / spu
        for rec in recs:
            ax.plot(t, rec["wave"], lw=0.5, alpha=0.8,
                    label=f"T={rec['temp']:g} vdr={rec['vdr']:g}")
        ax.set_ylabel(c, fontsize=7, rotation=0, ha="right", va="center"); ax.set_yticks([])
        ax.legend(fontsize=5, loc="upper right", ncol=3)
    axes[-1].set_xlabel("UI (first ~40 shown)")
    axes[0].set_xlim(0, 40)
    axes[0].set_title("Raw RX waveforms (3 runs per class)")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def plot_overview(by_class, rows, path):
    classes = sorted(by_class)
    counts = [len(by_class[c]) for c in classes]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5))
    a1.barh(classes, counts, color="#1f77b4")
    a1.set_xlabel("# runs"); a1.set_title("Class balance")
    for i, n in enumerate(counts):
        a1.text(n + 0.5, i, str(n), va="center", fontsize=8)
    temps = np.array([r["temp"] for r in rows]); vdrs = np.array([r["vdr"] for r in rows])
    jit = (np.random.RandomState(0).rand(len(rows)) - 0.5) * 6
    a2.scatter(temps + jit, vdrs + (np.random.RandomState(1).rand(len(rows)) - 0.5) * 0.01,
               s=12, alpha=0.4)
    a2.set_xlabel("temp_C (observable)"); a2.set_ylabel("vdroop_frac (observable)")
    a2.set_title("Telemetry coverage (the two observable confounders)")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/wave")
    a = ap.parse_args()
    meta, by_class, rows = load(a.data)
    outdir = os.path.join(a.data, "inspect")
    os.makedirs(outdir, exist_ok=True)
    print(f"{len(rows)} waveforms, {len(by_class)} classes: "
          + ", ".join(f"{c}={len(by_class[c])}" for c in sorted(by_class)))
    plot_eyes(meta, by_class, os.path.join(outdir, "eyes.png"))
    plot_waveforms(meta, by_class, os.path.join(outdir, "waveforms.png"))
    plot_overview(by_class, rows, os.path.join(outdir, "overview.png"))
    print(f"wrote eyes.png, waveforms.png, overview.png -> {outdir}/")
