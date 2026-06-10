"""Render per-root-cause-group eye diagrams for the slides (from 1 ps raw waves).

    ~/miniconda3/envs/drl_hw2/bin/python render_group_eyes.py --data out/wave2

Each group page in the deck gets one figure: healthy reference + the classes
sharing that eye signature. Fault runs are picked at the severe end of their
range so the signature is didactically clear (the dataset itself stays
continuous-severity; this is presentation only).
"""
import argparse
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from inspect_waves import load, raw_index, eye_fold_raw, _eye_metrics

# (panel title, class, severity sort, optional filter on the rec)
# sort: "desc" = larger sev more severe, "asc" = smaller sev more severe
GROUPS = {
    "eye_grp_attenuation": [
        ("healthy", "healthy", None, None),
        ("resistive_open", "resistive_open", "desc", None),
        ("bump_void_aging", "bump_void_aging", "desc", None),
        ("hotspot", "hotspot", "desc", None),
        ("r_drift", "r_drift", "desc", None),
    ],
    "eye_grp_droop": [
        ("healthy", "healthy", None, None),
        ("supply_droop", "supply_droop", "desc", None),
    ],
    "eye_grp_cdrift": [
        ("healthy", "healthy", None, None),
        ("c_drift", "c_drift", "desc", None),
    ],
    "eye_grp_xtalk": [
        ("healthy", "healthy", None, None),
        ("crosstalk_cap", "crosstalk_cap", "desc", None),
        ("bridge_short", "bridge_short", "asc", None),
    ],
    "eye_grp_impedance": [
        ("healthy", "healthy", None, None),
        ("imp. disc. ($z<1$)", "impedance_discontinuity", "asc",
         lambda r: float(r["sev"]) < 1.0),
        ("imp. disc. ($z>1$)", "impedance_discontinuity", "desc",
         lambda r: float(r["sev"]) > 1.0),
    ],
}
NCOL = {"eye_grp_attenuation": 3}


def pick_runs(by_class, cls, sort, filt, ridx, n=6):
    recs = [r for r in by_class.get(cls, [])
            if r.get("run_id") in ridx and (filt is None or filt(r))]
    if sort == "desc":
        recs.sort(key=lambda r: -float(r["sev"]))
    elif sort == "asc":
        recs.sort(key=lambda r: float(r["sev"]))
    return recs[:n]


def render(name, panels, meta, by_class, ridx, data_dir, outdir):
    ncol = NCOL.get(name, len(panels))
    nrow = (len(panels) + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.6 * ncol, 2.7 * nrow))
    axes = np.atleast_1d(axes).ravel()
    for ax, (title, cls, sort, filt) in zip(axes, panels):
        recs = pick_runs(by_class, cls, sort, filt, ridx)
        for rec in recs:
            segs, tx = eye_fold_raw(data_dir, ridx[rec["run_id"]], meta)
            for seg in segs:
                ax.plot(tx, seg, color="#1f77b4", alpha=0.05, lw=0.5)
        met = _eye_metrics(meta, recs)
        if met is not None:
            h, wd, b = met
            ber = "<1e-30" if b <= -30 else f"1e{b:.0f}"
            ax.text(0.98, 0.03, f"H={h*1e3:.0f} mV  W={wd:.0f} ps  BER={ber}",
                    transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
                    bbox=dict(facecolor="white", alpha=0.9, edgecolor="0.6",
                              boxstyle="round,pad=0.25", lw=0.5))
        ax.set_title(title, fontsize=12,
                     color="#2ca02c" if cls == "healthy" else "#c03030")
        ax.set_xlabel("UI", fontsize=8)
        ax.set_ylim(-0.05, 0.85)
        ax.tick_params(labelsize=7)
    for ax in axes[len(panels):]:
        ax.axis("off")
    fig.tight_layout()
    path = os.path.join(outdir, name + ".png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print("wrote", path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="out/wave2")
    ap.add_argument("--out", default="../slides/pic")
    a = ap.parse_args()
    meta, by_class, rows = load(a.data)
    ridx = raw_index(a.data)
    print(f"{len(rows)} rows, raw waves for {len(ridx)} runs")
    for name, panels in GROUPS.items():
        render(name, panels, meta, by_class, ridx, a.data, a.out)
