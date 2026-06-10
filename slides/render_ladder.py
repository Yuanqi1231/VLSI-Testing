"""Render pic/ladder.png (slide "主结果：哪一级观测 + 哪种模型才够用").

    ~/miniconda3/envs/drl_hw2/bin/python render_ladder.py

Observation/representation ladder on the 10-class diagnosis task (v2 dataset,
random workloads). Numbers from sim/out/wave2/results_v2.json and why_ai_v2.py.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROWS = [  # (label, accuracy, color)
    ("1-D CNN + telemetry",        0.803, "#1a5276"),
    ("1-D CNN on raw waveform",    0.789, "#1f77b4"),
    ("Handcrafted 18-D + MLP",     0.711, "#e67e22"),
    ("Handcrafted 18-D + logistic", 0.661, "#f0a04b"),
    ("Logistic on raw waveform",   0.221, "#c0392b"),
    ("Eye-margin scalar + logistic", 0.221, "#c0392b"),
]
BASE = 0.221  # majority-class baseline

fig, ax = plt.subplots(figsize=(9.6, 3.6))
y = np.arange(len(ROWS))[::-1]
for yi, (label, v, c) in zip(y, ROWS):
    ax.barh(yi, v, height=0.62, color=c)
    ax.text(v + 0.008, yi, f"{v:.3f}", va="center", fontsize=10)
ax.set_yticks(y)
ax.set_yticklabels([r[0] for r in ROWS], fontsize=10)
ax.axvline(BASE, color="0.35", ls="--", lw=1)
ax.text(BASE + 0.005, len(ROWS) - 0.45, f"majority-class baseline {BASE}",
        fontsize=8, color="0.35")
ax.set_xlim(0, 0.9)
ax.set_xlabel("10-class diagnosis accuracy (random workloads)", fontsize=10)
ax.tick_params(axis="x", labelsize=9)
fig.tight_layout()
fig.savefig("pic/ladder.png", dpi=150)
print("wrote pic/ladder.png")
