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
            if "run_id" in col:
                rec["run_id"] = line[col["run_id"]]
            if "eye_height_V" in col:        # v2 stores per-run eye metrics
                rec["eye"] = (float(line[col["eye_height_V"]]),
                              float(line[col["eye_width_ps"]]),
                              float(line[col["ber_log10"]]))
            by_class[rec["label"]].append(rec)
            rows.append(rec)
    return meta, by_class, rows


def eye_fold(wave, spu, settle, dly, n_ui=2):
    """Fold the post-settle waveform into overlaid n_ui-wide traces (the eye)."""
    w = wave[settle * spu + dly:]
    seg = n_ui * spu
    n = len(w) // spu - n_ui
    return [w[i * spu:i * spu + seg] for i in range(max(n, 0))]


def raw_index(data_dir):
    """run_id -> raw-waveform record (file, n, delay_ps) from scenarios.jsonl.
    Empty dict when the dataset has no persisted raw waveforms (v1)."""
    path = os.path.join(data_dir, "scenarios.jsonl")
    idx = {}
    if not os.path.exists(path):
        return idx
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            raw = d.get("raw")
            if raw and os.path.exists(os.path.join(data_dir, raw["file"])):
                idx[d["run_id"]] = dict(file=raw["file"], n=raw["n"],
                                        delay_ps=d.get("eye", {}).get("delay_ps", 0.0))
    return idx


def eye_fold_raw(data_dir, info, meta, n_ui=2):
    """Fold one run's full-resolution (1 ps) waveform into n_ui-wide eye traces."""
    import array as _arr
    a = _arr.array("f")
    with open(os.path.join(data_dir, info["file"]), "rb") as f:
        a.fromfile(f, info["n"])
    w = np.asarray(a, np.float32)
    ui, dt = meta["ui_ps"], meta["tstep_ps"]
    seg = int(round(n_ui * ui / dt))
    segs = []
    for i in range(meta["settle_bits"], meta["n_bits"] - n_ui):
        s = int(round((i * ui + info["delay_ps"]) / dt))
        if s + seg <= len(w):
            segs.append(w[s:s + seg])
    return segs, np.arange(seg) * dt / ui


def _eye_metrics(meta, recs):
    """Median eye height / width / BER over the displayed runs, computed with the
    SAME definitions as the campaign features (measure.link_features), so the
    numbers printed on the figure match the report's tables."""
    from d2dsim.measure import link_features
    from d2dsim.params import Config
    bits = meta.get("bits")
    if bits is None:
        # v2: bits differ per row; use the per-run metrics stored in the CSV
        if recs and "eye" in recs[0]:
            hs = [r["eye"][0] for r in recs]
            ws = [r["eye"][1] for r in recs]
            bs = [r["eye"][2] for r in recs]
            return (float(np.median(hs)), float(np.median(ws)), float(np.median(bs)))
        return None
    cfg = Config(n_bits=meta["n_bits"], settle_bits=meta["settle_bits"])
    spu = meta["samples_per_ui"]
    hs, ws, bs = [], [], []
    for rec in recs:
        t = [k * cfg.ui / spu for k in range(len(rec["wave"]))]
        f = link_features(cfg, t, [float(x) for x in rec["wave"]], bits)
        hs.append(f["eye_height_V"]); ws.append(f["eye_width_ps"]); bs.append(f["ber_log10"])
    return (float(np.median(hs)), float(np.median(ws)), float(np.median(bs)))


def plot_eyes(meta, by_class, path, data_dir=None, ridx=None):
    spu, settle, dly = meta["samples_per_ui"], meta["settle_bits"], meta["delay_samples"]
    ridx = ridx or {}
    classes = sorted(c for c in by_class if "+" not in c)   # base classes only
    ncol = 3
    nrow = (len(classes) + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol, figsize=(4 * ncol, 2.6 * nrow))
    axes = np.atleast_1d(axes).ravel()
    tx = np.arange(2 * spu) / spu
    for ax, c in zip(axes, classes):
        # overlay eyes from up to 6 runs of this class (mix of temps/droops)
        shown = by_class[c][:6]
        for rec in shown:
            info = ridx.get(rec.get("run_id"))
            if info is not None:
                # full-resolution (1 ps) waveform: smooth edges, no chord artifacts
                segs, txr = eye_fold_raw(data_dir, info, meta)
                for seg in segs:
                    ax.plot(txr, seg, color="#1f77b4", alpha=0.06, lw=0.5)
                continue
            for seg in eye_fold(rec["wave"], spu, settle, dly):
                if len(seg) == 2 * spu:
                    ax.plot(tx, seg, color="#1f77b4", alpha=0.06, lw=0.6)
        met = _eye_metrics(meta, shown)
        if met is not None:
            h, wd, b = met
            ber = "<1e-30" if b <= -30 else f"1e{b:.0f}"
            ax.text(0.985, 0.04, f"H={h*1e3:.0f} mV  W={wd:.0f} ps  BER={ber}",
                    transform=ax.transAxes, ha="right", va="bottom", fontsize=6.5,
                    bbox=dict(facecolor="white", alpha=0.85, edgecolor="0.6",
                              boxstyle="round,pad=0.25", lw=0.5))
        ax.set_title(c, fontsize=9)
        ax.set_xlabel("UI", fontsize=7); ax.set_ylim(-0.05, 0.85)
        ax.tick_params(labelsize=6)
    for ax in axes[len(classes):]:
        ax.axis("off")
    src = "1 ps raw waveforms" if ridx else "resampled waveforms"
    fig.suptitle(f"Eye diagrams per fault class (folded over 2 UI, {src}); "
                 "H/W/BER = median over the overlaid runs", fontsize=12)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def plot_waveforms(meta, by_class, path):
    spu = meta["samples_per_ui"]
    classes = sorted(c for c in by_class if "+" not in c)   # base classes only
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
    # group the many "a+b" concurrent-fault labels into one bar so the
    # y-axis stays readable (v2 has 36 distinct two-fault combinations)
    grouped = defaultdict(int)
    for c, recs in by_class.items():
        grouped["concurrent (a+b)" if "+" in c else c] += len(recs)
    classes = sorted(grouped)
    counts = [grouped[c] for c in classes]
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
    ridx = raw_index(a.data)
    if ridx:
        print(f"raw waveforms found for {len(ridx)} runs -> eyes from 1 ps grid")
    plot_eyes(meta, by_class, os.path.join(outdir, "eyes.png"), data_dir=a.data, ridx=ridx)
    plot_waveforms(meta, by_class, os.path.join(outdir, "waveforms.png"))
    plot_overview(by_class, rows, os.path.join(outdir, "overview.png"))
    print(f"wrote eyes.png, waveforms.png, overview.png -> {outdir}/")
