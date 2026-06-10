#!/usr/bin/env python
"""
Render eye diagrams and a dataset overview with matplotlib.

The d2dsim harness is pure-stdlib (it shells out to ngspice), but this plotting
script needs numpy+matplotlib.  Run it with an interpreter that has them, e.g.:

    /Users/yuanqi/miniconda3/envs/drl_hw2/bin/python plot_eyes.py

Outputs (into out/plots/):
    eye_<case>.png        one real overlaid-trace eye per representative case
    eye_gallery.png       3x3 contact sheet of all cases
    dataset_overview.png  class separability + the aging degradation trajectory
    README.md             index that embeds the figures with captions
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from d2dsim.params import Config
from d2dsim.measure import simulate_link, simulate_tx_probe, _first_cross
from d2dsim.campaign import make_defect
from d2dsim import physics

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "plots")
os.makedirs(OUT, exist_ok=True)
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_work", "_plotwork")

# (key, title, defect, cfg-overrides) ---------------------------------------
CASES = [
    ("healthy_27C", "Healthy  (T=27 C)", make_defect("healthy"), {}),
    ("healthy_110C", "Healthy  (T=110 C, thermal confounder)", make_defect("healthy"), {"temp_c": 110.0}),
    ("resistive_open_500", "Resistive open  R=500 ohm @ seg10", make_defect("resistive_open", position=10, r_open=500.0), {}),
    ("bridge_short_200", "Bridge short  R=200 ohm (lane1)", make_defect("bridge_short", position=10, r_bridge=200.0), {}),
    ("crosstalk_x8", "Crosstalk  Cc x8", make_defect("crosstalk_cap", xtalk_factor=8.0), {}),
    ("aging_R80", "Micro-bump aging  R+80 ohm @ seg5 (T=85C)", make_defect("bump_void_aging", position=5, r_open=80.0), {"temp_c": 85.0}),
    ("supply_droop_20", "Supply droop  -20% swing", make_defect("supply_droop", droop_frac=0.20), {}),
    ("hotspot_150", "Hotspot  150 C @ seg10", make_defect("hotspot", position=10, hot_t=150.0), {}),
    ("impedance_z1p6", "Impedance step  Lx1.6 @ seg7", make_defect("impedance_discontinuity", position=7, z_factor=1.6), {}),
]

# ACTIVE behavioural front-end cases (multiphysics). Each rides the SAME driver
# knob R_on(Vdd,T,sigma), so temperature, mechanical stress and supply droop all
# couple physically -- the confounding the detector must disentangle. Annotated
# with the active-only telemetry (decision BER, observed PDN droop, and the TX
# rise/fall asymmetry that is ~1 for temperature but != 1 for mechanical stress).
ACTIVE_CASES = [
    ("a_healthy_27C", "Healthy  (active, T=27 C)  — asym baseline",
     make_defect("healthy"), {}),
    ("a_thermal_pure_110C", "Pure thermal  T=110 C  (mu(T)+Vth(T) only)  — symmetric",
     make_defect("healthy"), {"temp_c": 110.0, "stress_from_thermal": False}),
    ("a_thermal_cte_110C", "Thermal+CTE stress  T=110 C  (full coupled model)",
     make_defect("healthy"), {"temp_c": 110.0}),
    ("a_stress_244", "Mechanical stress  +244 MPa @ 27 C  (isolated)  — antisymmetric",
     make_defect("healthy"), {"stress_mpa": 244.0, "stress_from_thermal": False}),
    ("a_droop_20", "Supply droop  -20% PDN rail",
     make_defect("supply_droop", droop_frac=0.20), {}),
    ("a_open_500", "Resistive open  R=500 ohm @ seg10",
     make_defect("resistive_open", position=10, r_open=500.0), {}),
]


def get_waveform(defect, over):
    import dataclasses
    cfg = dataclasses.replace(Config(), **over)
    feats, (t, v), bits, proc = simulate_link(cfg, defect, WORK)
    return cfg, np.array(t), np.array(v), bits, feats


def fold(cfg, t, v, bits, span_ui=2.0):
    """Return a list of (x_ps, y_V) traces folded over span_ui."""
    ui = cfg.ui
    mid = 0.5 * (v.min() + v.max())
    fr = next((i for i in range(1, len(bits)) if bits[i] == 1 and bits[i - 1] == 0), None)
    delay = 0.0
    if fr is not None:
        cr = _first_cross(list(t), list(v), mid, fr * ui, rising=True)
        if cr:
            delay = cr - fr * ui
    traces = []
    k0 = cfg.settle_bits + 1
    for k in range(k0, len(bits) - 2):
        ts = k * ui + delay
        m = (t >= ts) & (t < ts + span_ui * ui)
        if m.sum() > 2:
            traces.append(((t[m] - ts) * 1e12, v[m]))
    return traces, delay, mid


def draw_eye(ax, cfg, traces, mid, feats, title):
    ax.set_facecolor("#0a0a1c")
    for x, y in traces:
        ax.plot(x, y * 1e3, color="#39d7d7", alpha=0.06, lw=1.0)
    ui_ps = cfg.ui * 1e12
    ax.axhline(mid * 1e3, color="#8a8aa0", lw=0.7, ls="--", alpha=0.7)
    for c in (0.5 * ui_ps, 1.5 * ui_ps):
        ax.axvline(c, color="#6a6a85", lw=0.6, ls=":", alpha=0.6)
    ax.set_xlim(0, 2 * ui_ps)
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("time within 2 UI [ps]", fontsize=8)
    ax.set_ylabel("v(RX) [mV]", fontsize=8)
    ax.tick_params(labelsize=7)
    txt = (f"eyeH={feats['eye_height_V']*1e3:.0f} mV   "
           f"BER=1e{feats['ber_log10']:.0f}\n"
           f"jit={feats['jitter_rms_ps']:.2f} ps   Q={feats['q_factor']:.0f}")
    ax.text(0.98, 0.03, txt, transform=ax.transAxes, fontsize=7,
            ha="right", va="bottom", color="#e8e860",
            bbox=dict(fc="#0a0a1c", ec="#39d7d7", alpha=0.6, pad=2))


def main():
    cache = {}
    # individual eyes
    for key, title, defect, over in CASES:
        cfg, t, v, bits, feats = get_waveform(defect, over)
        traces, delay, mid = fold(cfg, t, v, bits)
        cache[key] = (cfg, traces, mid, feats, title)
        fig, ax = plt.subplots(figsize=(4.6, 3.2), dpi=130)
        draw_eye(ax, cfg, traces, mid, feats, title)
        fig.tight_layout()
        fig.savefig(os.path.join(OUT, f"eye_{key}.png"))
        plt.close(fig)
        print(f"  eye_{key}.png  (eyeH={feats['eye_height_V']*1e3:.0f}mV "
              f"BER=1e{feats['ber_log10']:.0f})")

    # 3x3 contact sheet
    fig, axes = plt.subplots(3, 3, figsize=(13.5, 9.6), dpi=120)
    for ax, (key, *_rest) in zip(axes.ravel(), CASES):
        cfg, traces, mid, feats, title = cache[key]
        draw_eye(ax, cfg, traces, mid, feats, title)
    fig.suptitle("Pure-ngspice D2D link eye diagrams  (16 GT/s, UI=62.5 ps, 2 mm interposer channel)",
                 fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(os.path.join(OUT, "eye_gallery.png"))
    plt.close(fig)
    print("  eye_gallery.png")

    active_eyes()
    overview()
    write_index()


def draw_eye_active(ax, cfg, traces, mid, feats, asym, title):
    """Like draw_eye but annotates the active-front-end telemetry + stress asym."""
    ax.set_facecolor("#0a0a1c")
    for x, y in traces:
        ax.plot(x, y * 1e3, color="#ffae5c", alpha=0.06, lw=1.0)
    ui_ps = cfg.ui * 1e12
    ax.axhline(mid * 1e3, color="#8a8aa0", lw=0.7, ls="--", alpha=0.7)
    for c in (0.5 * ui_ps, 1.5 * ui_ps):
        ax.axvline(c, color="#6a6a85", lw=0.6, ls=":", alpha=0.6)
    ax.set_xlim(0, 2 * ui_ps)
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("time within 2 UI [ps]", fontsize=8)
    ax.set_ylabel("v(eq) [mV]", fontsize=8)
    ax.tick_params(labelsize=7)
    txt = (f"eyeH={feats['eye_height_V']*1e3:.0f} mV   "
           f"BERdec={feats.get('ber_dec', 0):.0e}\n"
           f"droop={feats.get('vdd_droop_mV', 0):.1f} mV   "
           f"asym={asym:.3f}")
    ax.text(0.98, 0.03, txt, transform=ax.transAxes, fontsize=7,
            ha="right", va="bottom", color="#ffe08a",
            bbox=dict(fc="#0a0a1c", ec="#ffae5c", alpha=0.6, pad=2))


def active_eyes():
    """Eye gallery for the behavioural multiphysics front-end (--active)."""
    import dataclasses
    cache = {}
    for key, title, defect, over in ACTIVE_CASES:
        cfg = dataclasses.replace(Config(), active_frontend=True, **over)
        feats, (t, v), bits, proc = simulate_link(cfg, defect, WORK)
        pr, _, _ = simulate_tx_probe(cfg, defect, WORK + "_probe")
        asym = pr.get("drive_asym_np", 0.0)
        t, v = np.array(t), np.array(v)
        traces, delay, mid = fold(cfg, t, v, bits)
        cache[key] = (cfg, traces, mid, feats, asym, title)
        fig, ax = plt.subplots(figsize=(4.6, 3.2), dpi=130)
        draw_eye_active(ax, cfg, traces, mid, feats, asym, title)
        fig.tight_layout()
        fig.savefig(os.path.join(OUT, f"eyeA_{key}.png"))
        plt.close(fig)
        sig = physics.sigma_mpa(cfg)
        print(f"  eyeA_{key}.png  (eyeH={feats['eye_height_V']*1e3:.0f}mV "
              f"BERdec={feats.get('ber_dec', 0):.0e} sigma={sig:.0f}MPa asym={asym:.3f})")

    # 2x3 contact sheet
    fig, axes = plt.subplots(2, 3, figsize=(13.8, 7.2), dpi=120)
    for ax, (key, *_rest) in zip(axes.ravel(), ACTIVE_CASES):
        cfg, traces, mid, feats, asym, title = cache[key]
        draw_eye_active(ax, cfg, traces, mid, feats, asym, title)
    fig.suptitle("Active behavioural front-end eyes  (alpha-law TX on a compact PDN + CTLE/tanh RX)  "
                 "—  asym=rise/fall: ~1 thermal, !=1 stress",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(os.path.join(OUT, "eye_active_gallery.png"))
    plt.close(fig)
    print("  eye_active_gallery.png")


def overview(csv_path=None):
    csv_path = csv_path or os.path.join(os.path.dirname(OUT), "dataset.csv")
    if not os.path.exists(csv_path):
        print("  (no dataset.csv -> skip overview; run: python3 run.py campaign)")
        return
    rows = list(csv.DictReader(open(csv_path)))
    labels = sorted(set(r["label"] for r in rows))
    cmap = plt.get_cmap("tab10")
    colors = {lab: cmap(i % 10) for i, lab in enumerate(labels)}

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.2), dpi=120)

    # A: separability -- eye height vs RMS jitter, coloured by label
    for lab in labels:
        rs = [r for r in rows if r["label"] == lab]
        xs = [float(r["eye_height_V"]) * 1e3 for r in rs]
        ys = [float(r["jitter_rms_ps"]) for r in rs]
        axA.scatter(xs, ys, s=46, color=colors[lab], label=lab,
                    edgecolor="k", linewidth=0.4, alpha=0.85)
    axA.set_xlabel("eye height [mV]")
    axA.set_ylabel("RMS jitter [ps]")
    axA.set_title("Telemetry separability (per labelled run)")
    axA.grid(alpha=0.3)
    axA.legend(fontsize=7, ncol=2, framealpha=0.9)

    # B: aging degradation trajectory (R+ vs eye height & jitter)
    ag = [r for r in rows if r["label"] == "bump_void_aging"]
    def rplus(r):
        m = re.search(r"R\+=([0-9.]+)", r["severity"])
        return float(m.group(1)) if m else 0.0
    ag.sort(key=rplus)
    rr = [rplus(r) for r in ag]
    eh = [float(r["eye_height_V"]) * 1e3 for r in ag]
    jt = [float(r["jitter_rms_ps"]) for r in ag]
    axB.plot(rr, eh, "o-", color="#1f77b4", label="eye height [mV]")
    axB.set_xlabel("injected micro-bump series resistance  R+ [ohm]  (aging)")
    axB.set_ylabel("eye height [mV]", color="#1f77b4")
    axB.tick_params(axis="y", labelcolor="#1f77b4")
    axB.set_title("Incipient aging trajectory @ seg5, T=85 C")
    axB.grid(alpha=0.3)
    axB2 = axB.twinx()
    axB2.plot(rr, jt, "s--", color="#d62728", label="RMS jitter [ps]")
    axB2.set_ylabel("RMS jitter [ps]", color="#d62728")
    axB2.tick_params(axis="y", labelcolor="#d62728")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "dataset_overview.png"))
    plt.close(fig)
    print("  dataset_overview.png")


def write_index():
    has_sch = os.path.exists(os.path.join(OUT, "fig_unitcell.png"))
    lines = ["# Eye-diagram gallery (pure-ngspice D2D link)\n",
             "Generated by `plot_eyes.py`. 16 GT/s, UI = 62.5 ps, 2 mm interposer "
             "channel, victim + 2 crosstalk aggressors. See `../../README.md` for the "
             "full circuit/netlist documentation.\n"]
    if has_sch:
        lines += ["## Circuit model (drawn by `draw_schematics.py`)\n",
                  "System view\n\n![topology](fig_topology.png)\n",
                  "Per-lane netlist unit cell\n\n![unitcell](fig_unitcell.png)\n",
                  "Defect-injection map\n\n![defects](fig_defects.png)\n"]
    lines += ["## Contact sheet (ideal PWL front-end)\n", "![gallery](eye_gallery.png)\n",
              "## Active behavioural front-end (multiphysics)\n", "![active](eye_active_gallery.png)\n",
              "## Dataset overview\n", "![overview](dataset_overview.png)\n",
              "## Individual eyes — ideal front-end\n"]
    for key, title, *_ in CASES:
        lines.append(f"**{title}**\n\n![{key}](eye_{key}.png)\n")
    lines.append("## Individual eyes — active behavioural front-end\n")
    for key, title, *_ in ACTIVE_CASES:
        lines.append(f"**{title}**\n\n![{key}](eyeA_{key}.png)\n")
    with open(os.path.join(OUT, "README.md"), "w") as f:
        f.write("\n".join(lines))
    print("  README.md")


if __name__ == "__main__":
    print(f"rendering plots -> {OUT}")
    main()
    print("done.")
