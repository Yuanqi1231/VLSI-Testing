#!/usr/bin/env python
"""
Draw circuit-diagram figures for the README (matplotlib, run with drl_hw2 python):

    /Users/yuanqi/miniconda3/envs/drl_hw2/bin/python draw_schematics.py

Outputs into out/plots/:
    fig_topology.png   system view: victim + 2 aggressors, coupling, defect site
    fig_unitcell.png   the actual circuit: driver -> tx bump -> RLGC cell -> rx bump -> RX
    fig_defects.png    how each of the 8 defect classes perturbs the netlist
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, FancyArrow

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "plots")
os.makedirs(OUT, exist_ok=True)

K = "#1a1a1a"     # ink
ACC = "#1f77b4"   # accent
RED = "#d62728"
GRN = "#2a8a3e"


# ---- schematic primitives --------------------------------------------------
def wire(ax, x0, y0, x1, y1, color=K, lw=1.5):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, solid_capstyle="round", zorder=2)


def dot(ax, x, y, color=K):
    ax.plot([x], [y], "o", color=color, ms=5, zorder=4)


def res_h(ax, x0, x1, y, label=None, n=6, amp=0.09, color=K, lw=1.5, lbl_dy=0.16):
    lead = (x1 - x0) * 0.16
    a, b = x0 + lead, x1 - lead
    xs, ys = [x0, a], [y, y]
    for i in range(n):
        xs.append(a + (b - a) * (i + 0.5) / n)
        ys.append(y + amp * (1 if i % 2 == 0 else -1))
    xs += [b, x1]; ys += [y, y]
    ax.plot(xs, ys, color=color, lw=lw, zorder=3)
    if label:
        ax.text((x0 + x1) / 2, y + amp + lbl_dy, label, ha="center", va="bottom", fontsize=9, color=color)


def ind_h(ax, x0, x1, y, label=None, n=4, color=K, lw=1.5):
    lead = (x1 - x0) * 0.12
    a, b = x0 + lead, x1 - lead
    wire(ax, x0, y, a, y, color, lw); wire(ax, b, y, x1, y, color, lw)
    w = (b - a) / n
    for i in range(n):
        cx = a + w * (i + 0.5)
        ax.add_patch(Arc((cx, y), w, w * 1.5, theta1=0, theta2=180, color=color, lw=lw, zorder=3))
    if label:
        ax.text((x0 + x1) / 2, y + 0.28, label, ha="center", va="bottom", fontsize=9, color=color)


def cap_v(ax, x, ytop, ybot, label=None, plate=0.16, gap=0.10, color=K, lw=1.5):
    ymid = (ytop + ybot) / 2
    wire(ax, x, ytop, x, ymid + gap / 2, color, lw)
    ax.plot([x - plate, x + plate], [ymid + gap / 2] * 2, color=color, lw=lw)
    ax.plot([x - plate, x + plate], [ymid - gap / 2] * 2, color=color, lw=lw)
    wire(ax, x, ymid - gap / 2, x, ybot, color, lw)
    if label:
        ax.text(x + plate + 0.06, ymid, label, ha="left", va="center", fontsize=9, color=color)


def gnd(ax, x, y, color=K, lw=1.5):
    wire(ax, x, y, x, y - 0.12, color, lw)
    for i, w in enumerate([0.26, 0.16, 0.07]):
        yy = y - 0.12 - i * 0.07
        ax.plot([x - w / 2, x + w / 2], [yy, yy], color=color, lw=lw)


def src(ax, x, y, r=0.30, label=None, color=K, lw=1.5):
    ax.add_patch(plt.Circle((x, y), r, fill=True, fc="white", ec=color, lw=lw, zorder=3))
    tx = np.linspace(-r * 0.5, r * 0.5, 60)
    sq = (np.sign(np.sin(tx / (r * 0.18))) * r * 0.32) + y
    ax.plot(x + tx, sq, color=color, lw=1.2, zorder=4)
    if label:
        ax.text(x, y - r - 0.16, label, ha="center", va="top", fontsize=9, color=color)


def box(ax, x, y, w, h, label, fc="#eaf2fb", ec=ACC, fs=9):
    ax.add_patch(Rectangle((x, y), w, h, fill=True, fc=fc, ec=ec, lw=1.6, zorder=3))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, zorder=4)


def node_lbl(ax, x, y, name, dy=0.18, color="#555"):
    ax.text(x, y + dy, name, ha="center", va="bottom", fontsize=8, color=color, style="italic")


def setup(ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.axis("off")


# ---- FIGURE 1: topology ----------------------------------------------------
def fig_topology():
    fig, ax = plt.subplots(figsize=(13.5, 6.2), dpi=130)
    setup(ax, (-0.5, 14.2), (-0.4, 6.6))

    def lane(y, name, accent, defect=False):
        box(ax, 0.2, y - 0.32, 1.5, 0.64, "PRBS\ndriver", fc="#f2eafb", ec="#7a3fb0", fs=8)
        wire(ax, 1.7, y, 2.4, y)
        box(ax, 2.4, y - 0.3, 1.2, 0.6, "tx\nµbump", fc="#eaf2fb", fs=8)
        wire(ax, 3.6, y, 4.2, y)
        lfc = "#fdeceb" if defect else "#eafbef"
        box(ax, 4.2, y - 0.34, 4.0, 0.68, "RLGC ladder  ×N segments  (R+L series, C shunt)", fc=lfc, ec=(RED if defect else GRN), fs=8.5)
        if defect:
            ax.plot([6.2], [y + 0.34], marker="*", ms=20, color=RED, zorder=6)
            ax.annotate("injected\ndefect", (6.2, y + 0.34), (6.2, y + 1.15),
                        ha="center", fontsize=8, color=RED,
                        arrowprops=dict(arrowstyle="->", color=RED))
        wire(ax, 8.2, y, 8.8, y)
        box(ax, 8.8, y - 0.3, 1.2, 0.6, "rx\nµbump", fc="#eaf2fb", fs=8)
        wire(ax, 10.0, y, 10.6, y)
        box(ax, 10.6, y - 0.32, 1.5, 0.64, "RX\nCpad+term", fc="#eaf2fb", fs=8)
        ax.text(12.4, y, name, ha="left", va="center", fontsize=9, color=accent, weight="bold")

    y_a1, y_v, y_a2 = 5.2, 3.0, 0.8
    lane(y_a1, "aggressor 1", "#888")
    lane(y_v, "VICTIM", ACC, defect=True)
    lane(y_a2, "aggressor 2", "#888")

    # coupling caps (victim <-> aggressors), dashed
    for xc in (5.2, 6.9):
        for ya in (y_a1, y_a2):
            ymid = (y_v + ya) / 2
            ax.plot([xc, xc], [y_v + (0.34 if ya > y_v else -0.34), ya + (-0.34 if ya > y_v else 0.34)],
                    color="#c46", lw=1.3, ls=(0, (4, 2)), zorder=1)
        ax.text(xc, (y_v + y_a1) / 2, "Cc", fontsize=7.5, color="#c46", ha="right")

    ax.text(7.0, 6.25, "Die-to-die link  —  victim lane + 2 crosstalk aggressors over a silicon interposer",
            ha="center", fontsize=12, weight="bold")
    # modality annotations
    ax.text(13.0, 3.0, "→ v(RX):\n  eye / BER /\n  jitter / skew", fontsize=8, color=ACC, va="center")
    ax.text(0.95, 6.0, "temp .temp corner → Cu R(T) → eye drift (confounder)", fontsize=8, color="#a55")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_topology.png")); plt.close(fig)
    print("  fig_topology.png")


# ---- FIGURE 2: unit cell (the real circuit) --------------------------------
def fig_unitcell():
    fig, ax = plt.subplots(figsize=(15.5, 5.6), dpi=135)
    setup(ax, (-0.7, 18.2), (-1.4, 3.7))
    y = 1.6

    # driver: Vdrv source -> Ron -> vtxo
    src(ax, 0.2, y, 0.34)
    ax.text(0.2, y + 0.55, "Vdrv\nPWL(bits)", ha="center", va="bottom", fontsize=9)
    wire(ax, 0.2, y - 0.34, 0.2, -0.7); gnd(ax, 0.2, -0.7)   # source return to ground
    wire(ax, 0.54, y, 1.2, y)
    res_h(ax, 1.2, 2.5, y, "Ron 45Ω")
    dot(ax, 2.5, y); node_lbl(ax, 2.5, y, "vtxo")

    # tx micro-bump: Rb - Lb -> vn0 ; Cb shunt
    res_h(ax, 2.5, 3.7, y, "Rb 40mΩ", n=4, amp=0.07)
    ind_h(ax, 3.7, 5.1, y, "Lb 30pH")
    dot(ax, 5.1, y); node_lbl(ax, 5.1, y, "vn0")
    cap_v(ax, 5.1, y - 0.45, -0.7, "Cb 12fF"); gnd(ax, 5.1, -0.7)
    ax.text(3.8, y + 0.95, "tx µbump", fontsize=9, color="#666", ha="center")

    # one RLGC segment: Rseg - Lseg -> vn1 ; Cnode at vn0 and vn1
    res_h(ax, 5.1, 6.5, y, "Rseg=R'·ℓ/N", n=5, amp=0.08, color=GRN)
    ind_h(ax, 6.5, 8.1, y, "Lseg=L'·ℓ/N", color=GRN)
    dot(ax, 8.1, y); node_lbl(ax, 8.1, y, "vn1")
    cap_v(ax, 8.1, y - 0.45, -0.7, "Cnode=C'·ℓ/N", color=GRN); gnd(ax, 8.1, -0.7)
    ax.text(6.6, y + 0.95, "RLGC ladder cell  (×N=20)", fontsize=9, color=GRN, ha="center")
    # coupling cap up to aggressor stub
    wire(ax, 8.1, y, 8.1, y + 0.45, color="#c46")
    cap_v(ax, 8.1, y + 1.05, y + 0.45, "Cc", color="#c46")
    ax.text(8.1, y + 1.2, "→ aggressor", fontsize=8, color="#c46", ha="center", va="bottom")

    # ellipsis (rest of ladder)
    ax.text(9.5, y, r"$\cdots$ ×N $\cdots$", fontsize=16, ha="center", va="center")
    wire(ax, 8.1, y, 8.9, y); wire(ax, 10.1, y, 10.6, y)
    dot(ax, 10.6, y); node_lbl(ax, 10.6, y, "vnN")

    # rx micro-bump
    res_h(ax, 10.6, 11.8, y, "Rb", n=4, amp=0.07)
    ind_h(ax, 11.8, 13.2, y, "Lb")
    dot(ax, 13.2, y); node_lbl(ax, 13.2, y, "vrxo")
    ax.text(11.9, y + 0.95, "rx µbump", fontsize=9, color="#666", ha="center")

    # RX: Cpad to gnd, Rterm to Vmid rail
    cap_v(ax, 13.2, y - 0.45, -0.7, "Cpad 30fF"); gnd(ax, 13.2, -0.7)
    wire(ax, 13.2, y, 14.6, y)
    # draw Rterm vertically to Vmid
    res_v_y1 = -0.55
    xv = 14.6
    lead = 0.18
    ax.plot([xv, xv], [y, y - lead], color=K, lw=1.5)
    zz_x, zz_y = [], []
    for i in range(6):
        zz_y.append(y - lead - (y - lead - res_v_y1 - 0.0) * (i + 0.5) / 6 + 0.0)
        zz_x.append(xv + 0.09 * (1 if i % 2 == 0 else -1))
    ax.plot([xv] + zz_x + [xv], [y - lead] + zz_y + [res_v_y1], color=K, lw=1.5)
    ax.text(xv + 0.28, (y + res_v_y1) / 2, "Rterm 80Ω", fontsize=9, va="center")
    ax.plot([xv - 0.5, xv + 0.5], [res_v_y1, res_v_y1], color="#b07a1a", lw=2)
    ax.text(xv, res_v_y1 - 0.18, "Vmid = VDD/2", fontsize=8.5, color="#b07a1a", ha="center", va="top")
    ax.text(13.9, y + 0.95, "receiver", fontsize=9, color="#666", ha="center")

    ax.text(8.7, 3.35, "Per-lane signal path  (single-ended, Z₀ = 50 Ω SE,  16 GT/s, UI = 62.5 ps)",
            ha="center", fontsize=12, weight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_unitcell.png")); plt.close(fig)
    print("  fig_unitcell.png")


# ---- FIGURE 3: defect injection map ---------------------------------------
def fig_defects():
    fig, ax = plt.subplots(figsize=(14.5, 6.6), dpi=130)
    setup(ax, (-0.6, 15.0), (-2.6, 4.4))
    y = 1.4

    # driver + 4 visible cells + rx, compact
    src(ax, 0.1, y, 0.3, label="Vdrv")
    wire(ax, 0.4, y, 1.0, y)
    res_h(ax, 1.0, 2.0, y, None, n=4, amp=0.07)  # Ron
    xcells = [2.0, 4.2, 6.4, 8.6]
    for j, x0 in enumerate(xcells):
        res_h(ax, x0, x0 + 1.1, y, None, n=5, amp=0.08, color=GRN)
        ind_h(ax, x0 + 1.1, x0 + 2.2, y, None, color=GRN)
        dot(ax, x0 + 2.2, y)
        cap_v(ax, x0 + 2.2, y - 0.4, -0.6, None, color=GRN); gnd(ax, x0 + 2.2, -0.6)
        ax.text(x0 + 1.1, y - 0.95, f"seg {j}", fontsize=7.5, color="#777", ha="center")
    wire(ax, 10.8, y, 11.4, y)
    box(ax, 11.4, y - 0.3, 1.2, 0.6, "rx µbump\n+ RX", fc="#eaf2fb", fs=7.5)

    def callout(x, ytext, text, color, tx, ty):
        ax.annotate(text, (x, y + 0.12 if ty > y else y - 0.12), (tx, ty),
                    ha="center", fontsize=8.2, color=color, weight="bold",
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.4),
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=1.2))

    # 1 supply_droop @ driver
    callout(0.1, y, "supply_droop\nVdrv swing ×(1−d)", "#7a3fb0", 0.1, 3.4)
    # 2 resistive_open / aging @ seg2 series R
    callout(6.9, y, "resistive_open / bump_void_aging\n+R_open in series Rseg", RED, 6.9, 3.6)
    # 3 impedance_discontinuity @ seg1 inductor
    callout(5.3, y, "impedance_discontinuity\nLseg ×z_factor", "#b07a1a", 3.4, 3.4)
    # 4 hotspot @ seg3 resistor (per-instance temp=)
    callout(9.15, y, "hotspot\nRseg temp=Thot", "#cc5500", 11.0, 3.4)
    # 5 crosstalk_cap @ seg0 coupling
    wire(ax, 4.2, y, 4.2, y + 0.5, color="#c46")
    cap_v(ax, 4.2, y + 1.4, y + 0.5, None, color="#c46")
    callout(4.2, y + 1.4, "crosstalk_cap\nCc ×factor", "#c46", 2.0, 2.7)
    # 6 bridge_short victim node -> aggressor node (below)
    ya = -1.7
    ax.plot([2.0, 10.8], [ya, ya], color="#888", lw=1.4)
    ax.text(10.9, ya, "aggressor 1 lane", fontsize=8, color="#888", va="center")
    xv = 6.4
    ax.plot([xv, xv], [y - 0.4 - 0.2, ya], color=RED, lw=0)  # placeholder
    # vertical bridge resistor between victim node (seg1->seg2 node at 6.4) and aggressor rail
    lead = 0.2
    ax.plot([xv, xv], [-0.6 - 0.0, ya + 0.0], color="none")
    # draw zigzag vertical
    yy0, yy1 = -0.75, ya
    zz_x, zz_y = [xv], [yy0]
    for i in range(6):
        zz_y.append(yy0 + (yy1 - yy0) * (i + 0.5) / 6)
        zz_x.append(xv + 0.1 * (1 if i % 2 == 0 else -1))
    zz_x.append(xv); zz_y.append(yy1)
    ax.plot(zz_x, zz_y, color=RED, lw=1.5)
    wire(ax, xv, y - 0.4, xv, yy0, color=RED)
    callout2 = ax.annotate("bridge_short\nRbridge: victim ↔ aggressor", (xv, -1.1), (9.6, -1.9),
                           ha="center", fontsize=8.2, color=RED, weight="bold",
                           arrowprops=dict(arrowstyle="->", color=RED, lw=1.4),
                           bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=RED, lw=1.2))

    ax.text(7.0, 4.15, "Defect injection map  —  each label = a parameterised netlist perturbation (ground truth)",
            ha="center", fontsize=12, weight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_defects.png")); plt.close(fig)
    print("  fig_defects.png")


if __name__ == "__main__":
    print(f"drawing schematics -> {OUT}")
    fig_topology()
    fig_unitcell()
    fig_defects()
    print("done.")
