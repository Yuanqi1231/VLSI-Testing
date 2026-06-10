#!/usr/bin/env python3
"""
Command-line front-end for the pure-ngspice D2D interconnect simulator.

Examples
--------
  python3 run.py selftest                      # verify ngspice + sanity checks
  python3 run.py single --defect healthy        # one link run + ASCII eye
  python3 run.py single --defect resistive_open --r-open 500 --pos 10 --temp 85
  python3 run.py tdr --defect resistive_open --r-open 2000 --pos 14
  python3 run.py campaign --quick --out out/dataset_quick.csv
  python3 run.py campaign --out out/dataset.csv
"""
import argparse
import dataclasses
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from d2dsim.params import Config, DEFECT_KINDS
from d2dsim.measure import simulate_link, simulate_tdr, simulate_tx_probe, NGSPICE
from d2dsim.campaign import run_campaign, make_defect
from d2dsim import physics
import shutil


def _cfg_from_args(a):
    over = {}
    for k in ("temp", "rate", "len_mm", "n_seg", "n_bits"):
        v = getattr(a, k, None)
        if v is not None:
            over[{"temp": "temp_c", "rate": "rate"}.get(k, k)] = v
    if getattr(a, "active", False):
        over["active_frontend"] = True
    for k in ("activity", "aging_hours", "stress_mpa"):
        v = getattr(a, k, None)
        if v is not None:
            over[k] = v
    return dataclasses.replace(Config(), **over)


def _defect_from_args(a):
    return make_defect(a.defect, position=a.pos, r_open=a.r_open,
                       r_bridge=a.r_bridge, xtalk_factor=a.xtalk,
                       z_factor=a.zfac, hot_t=a.hot_t, droop_frac=a.droop)


def ascii_eye(cfg, t, v, bits, cols=60, rows=17, span_ui=2.0):
    """Render a folded eye diagram as text (no matplotlib needed)."""
    if len(t) < 10:
        print("(no waveform)")
        return
    ui = cfg.ui
    # estimate delay like measure.link_features (first rising edge)
    mid = 0.5 * (min(v) + max(v))
    fr = next((i for i in range(1, len(bits)) if bits[i] == 1 and bits[i - 1] == 0), None)
    delay = 0.0
    if fr is not None:
        from d2dsim.measure import _first_cross
        cr = _first_cross(t, v, mid, fr * ui, rising=True)
        if cr:
            delay = cr - fr * ui
    vmin, vmax = min(v), max(v)
    pad = 0.08 * (vmax - vmin + 1e-9)
    vmin -= pad
    vmax += pad
    grid = [[" "] * cols for _ in range(rows)]
    t0 = (cfg.settle_bits + 1) * ui + delay
    for tt, vv in zip(t, v):
        if tt < t0:
            continue
        ph = ((tt - delay) % (span_ui * ui)) / (span_ui * ui)
        c = int(ph * cols)
        r = int((vmax - vv) / (vmax - vmin) * (rows - 1))
        if 0 <= c < cols and 0 <= r < rows:
            grid[r][c] = "*" if grid[r][c] == " " else "#"
    print(f"  eye  ({span_ui:g} UI wide, {vmin*1e3:.0f}..{vmax*1e3:.0f} mV)")
    for r in range(rows):
        print("  |" + "".join(grid[r]))
    print("  +" + "-" * cols)


def cmd_single(a):
    cfg = _cfg_from_args(a)
    defect = _defect_from_args(a)
    wd = os.path.join("_work", "single")
    feats, (t, v), bits, proc = simulate_link(cfg, defect, wd)
    if proc.returncode != 0:
        print("ngspice stderr:\n" + proc.stderr[:800])
    print(f"\nD2D link  defect={defect['kind']} pos={defect['position']} "
          f"temp={cfg.temp_c:g}C rate={cfg.rate/1e9:g}GT/s UI={cfg.ui*1e12:g}ps\n")
    ascii_eye(cfg, t, v, bits)
    print()
    keys = ["eye_height_V", "eye_amp_V", "q_factor", "ber_log10",
            "jitter_rms_ps", "jitter_pp_ps", "eye_width_ps", "delay_ps", "xtalk_std_V"]
    if cfg.active_frontend:
        keys += ["ber_dec", "vdd_droop_mV"]
    for k in keys:
        val = feats.get(k, 0.0)
        unit = {"eye_height_V": " V", "eye_amp_V": " V", "xtalk_std_V": " V"}.get(k, "")
        print(f"  {k:16s} = {val:12.5g}{unit}")
    if cfg.active_frontend:
        pr, _, _ = simulate_tx_probe(cfg, defect, os.path.join("_work", "single_probe"))
        print(f"  {'t_rise_ps':16s} = {pr['t_rise_ps']:12.5g}")
        print(f"  {'t_fall_ps':16s} = {pr['t_fall_ps']:12.5g}")
        print(f"  {'drive_asym_np':16s} = {pr['drive_asym_np']:12.5g}  (=1 thermal, !=1 stress)")
        lab = physics.latent_labels(cfg, defect)
        print("  latent fields:", " ".join(f"{k}={v}" for k, v in lab.items()))


def cmd_tdr(a):
    cfg = _cfg_from_args(a)
    defect = _defect_from_args(a)
    wd = os.path.join("_work", "tdr")
    tdr, (t, v), proc = simulate_tdr(cfg, defect, wd)
    if proc.returncode != 0:
        print("ngspice stderr:\n" + proc.stderr[:800])
    print(f"\nTDR/SREL  defect={defect['kind']} pos={defect['position']} "
          f"r_open={defect['r_open']:g} z_factor={defect['z_factor']:g}")
    print(f"  reflection coefficient rho = {tdr['tdr_refl_coef']:.4f}")
    print(f"  estimated position         = {tdr['tdr_pos_mm']:.3f} mm "
          f"(channel = {cfg.len_mm:g} mm)")


def cmd_probe(a):
    a.active = True
    cfg = _cfg_from_args(a)
    defect = _defect_from_args(a)
    pr, _, proc = simulate_tx_probe(cfg, defect, os.path.join("_work", "probe"))
    if proc.returncode != 0:
        print("ngspice stderr:\n" + proc.stderr[:800])
    print(f"\nTX edge probe  temp={cfg.temp_c:g}C  sigma={physics.sigma_mpa(cfg):.1f} MPa")
    print(f"  t_rise = {pr['t_rise_ps']:.3f} ps")
    print(f"  t_fall = {pr['t_fall_ps']:.3f} ps")
    print(f"  drive_asym_np (rise/fall) = {pr['drive_asym_np']:.4f}   (=1 thermal-symmetric, !=1 stress)")
    print(f"  tx swing = {pr['tx_swing_V']*1e3:.1f} mV")


def cmd_campaign(a):
    cfg = Config()
    if a.rate is not None:
        cfg = dataclasses.replace(cfg, rate=a.rate)
    out = a.out or ("out/dataset_quick.csv" if a.quick else "out/dataset.csv")
    run_campaign(cfg, out, quick=a.quick, with_tdr=not a.no_tdr,
                 keep_waveforms=a.keep_waveforms)


def cmd_selftest(a):
    print(f"ngspice: {NGSPICE}")
    if not shutil.which("ngspice"):
        print("FAIL: ngspice not on PATH (brew install ngspice)")
        return 1
    cfg = Config()
    fh, _, _, p1 = simulate_link(cfg, make_defect("healthy"), "_work/_st_h")
    fo, _, _, p2 = simulate_link(cfg, make_defect("resistive_open", position=10, r_open=2000.0),
                                 "_work/_st_o")
    td, _, p3 = simulate_tdr(cfg, make_defect("resistive_open", position=14, r_open=5000.0), "_work/_st_t")
    print(f"  healthy   : eye_height={fh['eye_height_V']*1e3:.1f} mV  BER=1e{fh['ber_log10']:.0f}")
    print(f"  open 2kohm: eye_height={fo['eye_height_V']*1e3:.1f} mV  BER=1e{fo['ber_log10']:.0f}")
    print(f"  TDR(open) : rho={td['tdr_refl_coef']:.3f} pos={td['tdr_pos_mm']:.2f} mm")
    ok = True
    checks = [
        ("ngspice link run ok", p1.returncode == 0 and p2.returncode == 0),
        ("healthy eye open (>50mV)", fh["eye_height_V"] > 0.05),
        ("defect closes eye vs healthy", fo["eye_height_V"] < fh["eye_height_V"]),
        ("defect worsens BER vs healthy", fo["ber_log10"] >= fh["ber_log10"]),
        ("TDR sees a reflection (rho>0.02)", td["tdr_refl_coef"] > 0.02),
    ]
    for name, cond in checks:
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and cond
    print("\nSELFTEST", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Pure-ngspice D2D interconnect simulator")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_common(p):
        p.add_argument("--defect", choices=DEFECT_KINDS, default="healthy")
        p.add_argument("--pos", type=int, default=10, help="ladder segment index")
        p.add_argument("--r-open", dest="r_open", type=float, default=0.0)
        p.add_argument("--r-bridge", dest="r_bridge", type=float, default=1e9)
        p.add_argument("--xtalk", type=float, default=1.0)
        p.add_argument("--zfac", type=float, default=1.0)
        p.add_argument("--hot-t", dest="hot_t", type=float, default=27.0)
        p.add_argument("--droop", type=float, default=0.0)
        p.add_argument("--temp", type=float, default=None)
        p.add_argument("--rate", type=float, default=None)
        p.add_argument("--len-mm", dest="len_mm", type=float, default=None)
        p.add_argument("--n-seg", dest="n_seg", type=int, default=None)
        p.add_argument("--n-bits", dest="n_bits", type=int, default=None)
        # active behavioural front-end (MULTIPHYSICS_DESIGN.md)
        p.add_argument("--active", action="store_true", help="behavioural TX/RX + multiphysics fields")
        p.add_argument("--activity", type=float, default=None, help="switching activity 0..1 (PDN load)")
        p.add_argument("--stress-mpa", dest="stress_mpa", type=float, default=None, help="extra mechanical stress [MPa]")
        p.add_argument("--aging-hours", dest="aging_hours", type=float, default=None, help="field-time [h] -> bump R drift")

    ps = sub.add_parser("single", help="one link run + ASCII eye")
    add_common(ps)
    ps.set_defaults(func=cmd_single)

    pt = sub.add_parser("tdr", help="one TDR/SREL run")
    add_common(pt)
    pt.set_defaults(func=cmd_tdr)

    pp = sub.add_parser("probe", help="active TX intrinsic edge probe (rise/fall asymmetry)")
    add_common(pp)
    pp.set_defaults(func=cmd_probe)

    pc = sub.add_parser("campaign", help="full fault-injection dataset")
    pc.add_argument("--quick", action="store_true")
    pc.add_argument("--out", default=None)
    pc.add_argument("--no-tdr", action="store_true")
    pc.add_argument("--keep-waveforms", action="store_true")
    pc.add_argument("--rate", type=float, default=None)
    pc.set_defaults(func=cmd_campaign)

    pst = sub.add_parser("selftest", help="verify ngspice + sanity checks")
    pst.set_defaults(func=cmd_selftest)

    a = ap.parse_args()
    rc = a.func(a)
    sys.exit(rc or 0)


if __name__ == "__main__":
    main()
