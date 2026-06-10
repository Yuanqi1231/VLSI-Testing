"""Render pic/telemetry_value.png (slide "核心洞见：遥测的价值取决于观测的有损性").

    ~/miniconda3/envs/drl_hw2/bin/python render_telemetry_value.py

Numbers from sim/out/wave2/results_v2.json (telemetry_ablation_v2 + the zero-FA
oracle threshold sweep). Right panel includes the standalone performance of the
compressed-input-only group (binary accuracy), so the lossy regime has a headline
metric comparable to the left panel's accuracies.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 4.0),
                             gridspec_kw={"width_ratios": [1, 1.55]})

# ---- left: full-waveform regime (10-class accuracy) ----
vals = [0.789, 0.803]
bars = a1.bar(["waveform\nonly", "waveform\n+ telemetry"], vals,
              color="#1f77b4", width=0.55)
for b, v in zip(bars, vals):
    a1.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.3f}",
            ha="center", fontsize=11)
a1.set_ylim(0, 1.0)
a1.set_ylabel("diagnosis accuracy")
a1.set_title("FULL waveform: telemetry\nnearly redundant (+1.4 pt)", fontsize=11)

# ---- right: lossy-scalar regime (margin-only vs margin+telemetry) ----
groups = ["binary accuracy\n(margin only input)",
          "false alarms on\nstressed-healthy",
          "fault recall at\nZERO false alarms"]
margin_only = [0.708, 0.492, 0.465]
with_tel = [0.750, 0.093, 0.611]
x = np.arange(len(groups))
w = 0.36
b1 = a2.bar(x - w / 2, margin_only, w, color="#9e9e9e",
            label="margin threshold (scalar only)")
b2 = a2.bar(x + w / 2, with_tel, w, color="#c0392b",
            label="learned: margin + telemetry")
for bs in (b1, b2):
    for b in bs:
        a2.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.015,
                f"{b.get_height():.2f}", ha="center", fontsize=10)
a2.set_xticks(x)
a2.set_xticklabels(groups, fontsize=9)
a2.set_ylim(0, 0.9)
a2.legend(fontsize=9, loc="upper center")
a2.set_title("LOSSY scalar (runtime): telemetry\nis decisive", fontsize=11)
a2.text(0.99, 0.975, "10-class root cause from the\nscalar alone: 0.221 ≈ chance",
        transform=a2.transAxes, ha="right", va="top", fontsize=8.5,
        style="italic", color="#444444")

fig.tight_layout()
fig.savefig("pic/telemetry_value.png", dpi=150)
print("wrote pic/telemetry_value.png")
