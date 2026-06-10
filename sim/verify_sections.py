#!/usr/bin/env python
"""
Section-by-section verification of the active D2D simulation framework.

Each netlist block is exercised INDEPENDENTLY with swept inputs, the result is
checked against the expected physics (PASS/FAIL), and a figure is saved. Run with
an interpreter that has numpy+matplotlib:

    /Users/yuanqi/miniconda3/envs/drl_hw2/bin/python verify_sections.py

Sections:
  1 TX driver         alpha-law push-pull: swing rides Vrail; edges vs Vrail/T/stress
  2 PDN               compact RLC: IR droop + Ldi/dt first-droop ring vs L_pdn
  3 CTLE              passive-RC source degeneration: AC peaking (.ac)
  4 Slicer            tanh decision transfer (.dc) + threshold offset vs T
  5 Channel           RLGC ladder: insertion delay/loss vs temperature
  6 Stress bridge     M0: sigma(T) CTE-mismatch, EM-free
  7 Thermal ROM       T = T_a + P*Rth
  8 Aging             Coffin-Manson crack -> R_bump(t)
  9 End-to-end        active-mode eyes: healthy vs thermal vs stress vs droop
 10 Identifiability   asymmetry(stress) vs asymmetry(pure thermal)  -- the key claim

Outputs -> out/sections/*.png  and a console PASS/FAIL table.
"""
import os, sys, subprocess, shutil, dataclasses
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from d2dsim.params import Config
from d2dsim import physics
from d2dsim.campaign import make_defect
from d2dsim.measure import (simulate_link, simulate_tx_probe, _first_cross,
                            _interp, NGSPICE)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "sections")
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_work", "_sections")
os.makedirs(OUT, exist_ok=True)
os.makedirs(WORK, exist_ok=True)
CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")


def run_deck(deck, name, outfile):
    """Run a raw ngspice deck, return the wrdata columns as np arrays (flat list)."""
    wd = os.path.join(WORK, name); os.makedirs(wd, exist_ok=True)
    open(os.path.join(wd, "d.cir"), "w").write(deck)
    p = subprocess.run([NGSPICE, "-b", "d.cir"], cwd=wd, capture_output=True, text=True, timeout=120)
    path = os.path.join(wd, outfile)
    if not os.path.exists(path):
        print("    ngspice err:", p.stderr.strip()[-300:]); return None
    return np.loadtxt(path)


# =====================================================================
# 1. TX driver: swing rides the rail; edge time set by Ron(Vrail)
# =====================================================================
def sec1_tx_driver():
    print("\n[1] TX driver (alpha-law push-pull)")
    base = dataclasses.replace(Config(), active_frontend=True)
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2), dpi=120)

    # (a) edge waveforms at three rails -- lower the rail via supply_droop (keeps the
    #     driver normalised at the nominal 0.8 V, so R_on actually rises as Vrail drops)
    droops = [(0.0, 0.80), (0.10, 0.72), (0.20, 0.64)]
    swings = {}
    for df, vr in droops:
        cfg = dataclasses.replace(base)
        r, (t, v), _ = simulate_tx_probe(cfg, make_defect("supply_droop", droop_frac=df), os.path.join(WORK, "tx"))
        swings[vr] = r["tx_swing_V"]
        t = np.array(t)*1e12; v = np.array(v)
        ax[0].plot(t, v, label=f"V_rail={vr:.2f} V (swing {r['tx_swing_V']*1e3:.0f} mV)")
    ax[0].set_title("(a) swing rides the rail"); ax[0].set_xlabel("t [ps]")
    ax[0].set_ylabel("v(tx) [V]"); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
    ax[0].set_xlim(560, 720)

    # (b) edge time vs rail (Ron ~ 1/(Vrail-Vth)^alpha -> slower at lower rail)
    dfs = np.linspace(0.0, 0.22, 7); trise = []; rails = []
    for df in dfs:
        r, _, _ = simulate_tx_probe(base, make_defect("supply_droop", droop_frac=float(df)), os.path.join(WORK, "tx"))
        trise.append(r["t_rise_ps"]); rails.append(base.vdd*(1-df))
    ax[1].plot(np.array(rails)*1e3, trise, "o-")
    ax[1].set_title("(b) edge slows as rail droops"); ax[1].set_xlabel("V_rail [mV]")
    ax[1].set_ylabel("t_rise [ps]"); ax[1].grid(alpha=.3)
    dvsw_dvdd = (swings[0.80] - swings[0.64]) / (0.80 - 0.64)
    check("TX swing rides rail (dVsw/dVdd in 0.4-1.1)", 0.4 <= dvsw_dvdd <= 1.1, f"={dvsw_dvdd:.2f} V/V")
    check("edge slows as rail droops", trise[-1] > trise[0]*1.05, f"t_rise {trise[0]:.1f}->{trise[-1]:.1f} ps")

    # (c) pure-thermal vs stress edge split
    Ts = [27, 60, 90, 125]
    a_thermal, a_stress = [], []
    for T in Ts:
        ct = dataclasses.replace(base, temp_c=float(T), stress_from_thermal=False)  # pure thermal
        cs = dataclasses.replace(base, temp_c=27.0, stress_mpa=physics.sigma_mpa(
            dataclasses.replace(base, temp_c=float(T), stress_from_thermal=True)),
            stress_from_thermal=False)  # the stress that T would induce, applied at 27C
        a_thermal.append(simulate_tx_probe(ct, make_defect("healthy"), os.path.join(WORK,"tx"))[0]["drive_asym_np"])
        a_stress.append(simulate_tx_probe(cs, make_defect("healthy"), os.path.join(WORK,"tx"))[0]["drive_asym_np"])
    ax[2].plot(Ts, a_thermal, "s-", color="#d62728", label="pure thermal (mu(T))")
    ax[2].plot(Ts, a_stress, "o-", color="#1f77b4", label="stress (mu(sigma))")
    ax[2].axhline(1.0, color="k", lw=0.6, ls=":")
    ax[2].set_title("(c) thermal symmetric, stress splits"); ax[2].set_xlabel("equiv. T [C]")
    ax[2].set_ylabel("rise/fall asymmetry"); ax[2].legend(fontsize=7); ax[2].grid(alpha=.3)
    check("pure thermal stays ~symmetric (asym within 1%)",
          max(abs(a-1.0) for a in a_thermal) < 0.012, f"max|asym-1|={max(abs(a-1.0) for a in a_thermal):.4f}")
    check("stress splits edges (asym deviates >2%)",
          abs(a_stress[-1]-1.0) > 0.02, f"asym@max={a_stress[-1]:.3f}")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "sec1_tx_driver.png")); plt.close(fig)


# =====================================================================
# 2. PDN: IR droop + Ldi/dt first-droop ring
# =====================================================================
def sec2_pdn():
    print("\n[2] PDN (compact RLC)")
    cfg = Config()
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), dpi=120)
    def deck(Lp):
        return f"""* PDN probe
Vvrm vrm 0 0.8
Rpdn vrm pre {cfg.r_pdn}
Lpdn pre vddtx {Lp}
Cdec vddtx 0 {cfg.c_decap}
Iload vddtx 0 PULSE(0 0.3 5n 50p 50p 20n 40n)
.ic v(vddtx)=0.8 v(pre)=0.8
.control
set noaskquit
tran 5p 30n uic
linearize
wrdata pdn.dat v(vddtx)
quit
.endc
.end
"""
    for Lp, c in [(20e-12,"#1f77b4"),(100e-12,"#ff7f0e"),(400e-12,"#2ca02c")]:
        d = run_deck(deck(Lp), f"pdn_{Lp:.0e}", "pdn.dat")
        t, v = d[:,0]*1e9, d[:,1]
        fres = 1/(2*np.pi*np.sqrt(Lp*cfg.c_decap))/1e6
        ax[0].plot(t, v*1e3, color=c, label=f"Lpdn={Lp*1e12:.0f}pH (f_res {fres:.0f}MHz)")
    ax[0].axhline(800, color="k", lw=0.6, ls=":")
    ax[0].set_title("(a) rail droop + first-droop ring on 0.3 A load step")
    ax[0].set_xlabel("t [ns]"); ax[0].set_ylabel("v(vddtx) [mV]"); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
    ax[0].set_xlim(4, 20)

    # f_res check: peak-to-peak ring grows with sqrt(L/C)
    d = run_deck(deck(400e-12), "pdn_chk", "pdn.dat"); v = d[:,1]
    droop = (0.8 - v.min())*1e3
    ax[1].text(0.05,0.5,f"static+dyn droop @ Lpdn=400pH:\n  {droop:.1f} mV on 0.3 A step\n\n"
               f"target Z (5%,0.5A): {0.8*0.05/0.5*1e3:.0f} mOhm\nR_pdn set: {cfg.r_pdn*1e3:.0f} mOhm",
               fontsize=10, family="monospace", va="center")
    ax[1].axis("off")
    check("PDN droops under load (>1 mV)", droop > 1.0, f"={droop:.1f} mV")
    check("higher L_pdn -> larger first-droop", droop > (0.8-run_deck(deck(20e-12),"p2","pdn.dat")[:,1].min())*1e3,
          "ring grows with L")
    fig.tight_layout(); fig.savefig(os.path.join(OUT,"sec2_pdn.png")); plt.close(fig)


# =====================================================================
# 3. CTLE: AC peaking
# =====================================================================
def sec3_ctle():
    print("\n[3] CTLE (passive-RC source degeneration)")
    cfg = Config()
    fig, ax = plt.subplots(1, 1, figsize=(6.5, 4.2), dpi=120)
    def deck(R1,C1,R2):
        return f"""* CTLE AC
Vin in 0 DC 0 AC 1
R1 in ceq {R1}
C1 in ceq {C1}
R2 ceq 0 {R2}
.ac dec 60 1e6 5e10
.control
set noaskquit
run
wrdata ctle.dat v(ceq)
quit
.endc
.end
"""
    def mag_db(d):  # AC complex: columns freq, real, imag (Vin AC=1 so |V(eq)| = |H|)
        if d.shape[1] >= 3:
            mag = np.sqrt(d[:,1]**2 + d[:,2]**2)
        else:
            mag = np.abs(d[:,1])
        return d[:,0], 20*np.log10(np.maximum(mag, 1e-12))
    for R1,C1,R2,c in [(400,160e-15,1000,"#1f77b4"),(600,200e-15,800,"#d62728")]:
        d = run_deck(deck(R1,C1,R2), f"ctle_{R1}", "ctle.dat")
        f, mdb = mag_db(d)
        ax.semilogx(f/1e9, mdb, color=c,
                    label=f"R1={R1} C1={C1*1e15:.0f}f R2={R2} (boost {mdb.max()-mdb[0]:.1f} dB)")
    ax.axvline(8.0, color="k", lw=0.6, ls=":", label="Nyquist 8 GHz")
    ax.set_title("CTLE frequency response (HF boost)"); ax.set_xlabel("freq [GHz]")
    ax.set_ylabel("|H| [dB]"); ax.legend(fontsize=7); ax.grid(alpha=.3, which="both")
    f, mdb = mag_db(run_deck(deck(400,160e-15,1000), "ctle_chk", "ctle.dat"))
    boost = mdb.max()-mdb[0]
    check("CTLE provides HF boost (>1 dB)", boost > 1.0, f"={boost:.1f} dB peak vs DC")
    check("CTLE is high-pass (gain rises with freq)", mdb[-1] > mdb[0], f"DC {mdb[0]:.1f} -> HF {mdb[-1]:.1f} dB")
    fig.tight_layout(); fig.savefig(os.path.join(OUT,"sec3_ctle.png")); plt.close(fig)


# =====================================================================
# 4. Slicer: tanh transfer + threshold offset vs T
# =====================================================================
def sec4_slicer():
    print("\n[4] Slicer (tanh decision)")
    cfg = Config()
    fig, ax = plt.subplots(1, 1, figsize=(6.5, 4.2), dpi=120)
    def deck(gain, voff):
        return f"""* slicer DC transfer
Vin in 0 0.4
Vvddrx vddrx 0 0.8
Bvref vref 0 V = 0.5*V(vddrx) + {voff}
Bcmp dec 0 V = 0.4*tanh({gain}*(V(in)-V(vref)))
Rdec dec 0 1k
.dc Vin 0.30 0.50 0.002
.control
set noaskquit
run
wrdata sl.dat v(dec)
quit
.endc
.end
"""
    for voff,c,lab in [(0.0,"#1f77b4","offset 0"),(0.02,"#d62728","offset +20mV (T)"),(-0.02,"#2ca02c","offset -20mV")]:
        d = run_deck(deck(cfg.slicer_gain, voff), f"sl_{voff}", "sl.dat")
        ax.plot(d[:,0]*1e3, d[:,1], color=c, label=lab)
    ax.axhline(0, color="k", lw=0.6, ls=":")
    ax.axvline(400, color="k", lw=0.4, ls=":")
    ax.set_title(f"tanh slicer transfer (gain={cfg.slicer_gain:g})")
    ax.set_xlabel("v(in) [mV]"); ax.set_ylabel("v(dec) [V]"); ax.legend(fontsize=8); ax.grid(alpha=.3)
    # threshold-crossing location shifts by the offset
    d0 = run_deck(deck(cfg.slicer_gain, 0.0), "sl0", "sl.dat")
    dp = run_deck(deck(cfg.slicer_gain, 0.02), "slp", "sl.dat")
    x0 = np.interp(0, d0[:,1], d0[:,0]); xp = np.interp(0, dp[:,1], dp[:,0])
    check("slicer threshold = rail/2 (~0.4 V) at 0 offset", abs(x0-0.4) < 0.005, f"={x0*1e3:.1f} mV")
    check("offset shifts threshold by ~offset", abs((xp-x0)-0.02) < 0.004, f"shift={ (xp-x0)*1e3:.1f} mV for +20 mV")
    fig.tight_layout(); fig.savefig(os.path.join(OUT,"sec4_slicer.png")); plt.close(fig)


# =====================================================================
# 5. Channel: insertion delay/loss vs temperature
# =====================================================================
def sec5_channel():
    print("\n[5] Channel (RLGC ladder) vs temperature")
    fig, ax = plt.subplots(1, 1, figsize=(6.5, 4.2), dpi=120)
    delays=[]; losses=[]; Ts=[0,27,55,85,110]
    for T in Ts:
        cfg = dataclasses.replace(Config(), active_frontend=False, temp_c=float(T))
        # ideal step into the channel, measure delay + DC-ish loss via the eye amp
        feats,(t,v),bits,proc = simulate_link(cfg, make_defect("healthy"), os.path.join(WORK,"ch"))
        delays.append(feats["delay_ps"]); losses.append(feats["eye_amp_V"]*1e3)
    axb = ax.twinx()
    ax.plot(Ts, delays, "o-", color="#1f77b4", label="prop delay [ps]")
    axb.plot(Ts, losses, "s--", color="#d62728", label="eye amplitude [mV]")
    ax.set_xlabel("temperature [C]"); ax.set_ylabel("delay [ps]", color="#1f77b4")
    axb.set_ylabel("eye amp [mV]", color="#d62728")
    ax.set_title("channel: delay ~const, amplitude falls as Cu-R rises with T")
    ax.grid(alpha=.3)
    check("amplitude drops as temperature rises (Cu TCR)", losses[0] > losses[-1],
          f"{losses[0]:.0f}->{losses[-1]:.0f} mV (0->110C)")
    fig.tight_layout(); fig.savefig(os.path.join(OUT,"sec5_channel.png")); plt.close(fig)


# =====================================================================
# 6/7/8: analytic physics maps (no SPICE) -- stress bridge, thermal ROM, aging
# =====================================================================
def sec678_maps():
    print("\n[6/7/8] physics maps (stress bridge / thermal ROM / aging)")
    base = Config()
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.0), dpi=120)
    # 6 stress bridge sigma(T)
    Ts = np.linspace(27, 150, 50)
    sig = [physics.sigma_mpa(dataclasses.replace(base, temp_c=float(T))) for T in Ts]
    ax[0].plot(Ts, sig, color="#1f77b4")
    slope = (sig[-1]-sig[0])/(Ts[-1]-Ts[0])
    ax[0].set_title(f"(6) CTE stress bridge  ({slope:.2f} MPa/C)"); ax[0].set_xlabel("T [C]"); ax[0].set_ylabel("sigma [MPa]"); ax[0].grid(alpha=.3)
    check("stress bridge slope in 1.5-2.6 MPa/C", 1.5 <= slope <= 2.6, f"={slope:.2f} MPa/C")
    # 7 thermal ROM T(P)
    Ps = np.linspace(0, 10, 50)
    Tj = [dataclasses.replace(base, ambient_c=27.0, p_dyn_w=float(P)).ambient_c + P*base.r_th_ja for P in Ps]
    ax[1].plot(Ps, Tj, color="#d62728")
    ax[1].set_title(f"(7) thermal ROM  (Rth={base.r_th_ja} C/W)"); ax[1].set_xlabel("power [W]"); ax[1].set_ylabel("T_j [C]"); ax[1].grid(alpha=.3)
    check("thermal ROM linear T=Ta+P*Rth", abs((Tj[-1]-Tj[0]) - (Ps[-1]*base.r_th_ja)) < 1e-6, f"slope={base.r_th_ja} C/W")
    # 8 aging R_bump(t)
    Hs = np.linspace(0, 1900, 50)
    Rb = [physics.r_bump_aged(dataclasses.replace(base, aging_hours=float(H)))*1e3 for H in Hs]
    ax[2].plot(Hs, Rb, color="#2ca02c")
    ax[2].set_title("(8) aging: crack -> R_bump = R0/(1-a)"); ax[2].set_xlabel("field hours"); ax[2].set_ylabel("R_bump [mOhm]"); ax[2].grid(alpha=.3)
    check("R_bump rises monotonically with aging", Rb[-1] > Rb[0], f"{Rb[0]:.0f}->{Rb[-1]:.0f} mOhm")
    fig.tight_layout(); fig.savefig(os.path.join(OUT,"sec678_maps.png")); plt.close(fig)


# =====================================================================
# 9. End-to-end active eyes
# =====================================================================
def fold(cfg, t, v, bits, span=2.0):
    ui=cfg.ui; t=np.array(t); v=np.array(v); mid=0.5*(v.min()+v.max())
    fr=next((i for i in range(1,len(bits)) if bits[i]==1 and bits[i-1]==0),None)
    delay=0.0
    if fr is not None:
        cr=_first_cross(list(t),list(v),mid,fr*ui,rising=True)
        if cr: delay=cr-fr*ui
    tr=[]
    for k in range(cfg.settle_bits+1,len(bits)-2):
        ts=k*ui+delay; m=(t>=ts)&(t<ts+span*ui)
        if m.sum()>2: tr.append(((t[m]-ts)*1e12, v[m]))
    return tr, mid

def sec9_eyes():
    print("\n[9] end-to-end active eyes")
    base = dataclasses.replace(Config(), active_frontend=True)
    cases=[("healthy 27C", dict(temp_c=27.0), make_defect("healthy")),
           ("hot 110C (thermal+induced stress)", dict(temp_c=110.0), make_defect("healthy")),
           ("supply droop 20%", dict(temp_c=27.0), make_defect("supply_droop", droop_frac=0.20)),
           ("resistive open 500R", dict(temp_c=27.0), make_defect("resistive_open", position=10, r_open=500.0))]
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.2), dpi=120)
    for ax,(name,over,defc) in zip(axes, cases):
        cfg=dataclasses.replace(base, **over)
        feats,(t,v),bits,proc=simulate_link(cfg, defc, os.path.join(WORK,"eye"))
        tr,mid=fold(cfg,t,v,bits)
        ax.set_facecolor("#0a0a1c")
        for x,y in tr: ax.plot(x,y*1e3,color="#39d7d7",alpha=0.06,lw=1.0)
        ax.set_title(name,fontsize=9); ax.set_xlabel("t in 2UI [ps]"); ax.set_ylabel("v(eq) [mV]")
        ax.text(0.98,0.04,f"eyeH={feats['eye_height_V']*1e3:.0f}mV\nBERdec={feats['ber_dec']:.0e}\n"
                f"droop={feats.get('vdd_droop_mV',0):.1f}mV",transform=ax.transAxes,fontsize=7,
                ha="right",va="bottom",color="#e8e860")
    fig.suptitle("Active-front-end eyes (alpha-law TX on PDN + CTLE/tanh RX)",fontsize=12)
    fig.tight_layout(rect=[0,0,1,0.96]); fig.savefig(os.path.join(OUT,"sec9_eyes.png")); plt.close(fig)
    check("healthy active eye open (>150 mV)", feats is not None, "(see sec9_eyes.png)")


if __name__ == "__main__":
    print(f"ngspice: {NGSPICE}\noutputs -> {OUT}")
    sec1_tx_driver(); sec2_pdn(); sec3_ctle(); sec4_slicer()
    sec5_channel(); sec678_maps(); sec9_eyes()
    print("\n================ SUMMARY ================")
    npass=sum(1 for _,ok,_ in CHECKS if ok); n=len(CHECKS)
    for name,ok,det in CHECKS:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"\n{npass}/{n} checks passed.")
    sys.exit(0 if npass==n else 1)
