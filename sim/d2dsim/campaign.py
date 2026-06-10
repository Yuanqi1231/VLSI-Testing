"""
Fault-injection campaign: enumerate {defect kind x severity x position x corner},
run each through ngspice, and write a labelled multimodal-telemetry dataset
(one row per run) ready for an anomaly detector.

Observable telemetry columns include temp_C and vdroop_frac (the confounders are
*observable*, the defect label is the hidden target) -- this is the multimodal
fusion setup of Track3_Open_Report_D2D_Link_Health.md.
"""
import csv
import dataclasses
import os
import shutil

from .params import Config
from .measure import simulate_link, simulate_tdr


def default_defect():
    return dict(kind="healthy", position=10, r_open=0.0, r_bridge=1e9,
                xtalk_factor=1.0, z_factor=1.0, hot_t=27.0, droop_frac=0.0,
                drift_r=0.0, drift_c=0.0)


def make_defect(kind, **kw):
    d = default_defect()
    d["kind"] = kind
    d.update(kw)
    return d


# ---- the campaign grid (modest by default; --quick trims further) -----------
def build_grid(quick=False):
    """Return a list of (Config-overrides, defect, severity_label) tuples."""
    temps_all = [0.0, 27.0, 55.0, 85.0, 110.0]
    rows = []

    # healthy across temperature corners and a few data seeds (normal variety)
    seeds = [0b1011011] if quick else [0b1011011, 0b1100101, 0b0011011]
    htemps = [27.0, 85.0] if quick else temps_all
    for T in htemps:
        for s in seeds:
            rows.append((dict(temp_c=T, seed_v=s), make_defect("healthy"),
                         f"T={T:g}C seed={s:#x}"))

    opens = [50.0, 500.0] if quick else [5.0, 20.0, 50.0, 150.0, 500.0, 2000.0]
    opos = [10] if quick else [3, 10, 17]
    otemps = [27.0] if quick else [27.0, 85.0]
    for T in otemps:
        for pos in opos:
            for r in opens:
                rows.append((dict(temp_c=T), make_defect("resistive_open", position=pos, r_open=r),
                             f"R_open={r:g}ohm pos={pos} T={T:g}C"))

    bridges = [200.0, 3000.0] if quick else [50.0, 200.0, 800.0, 3000.0]
    for T in ([27.0] if quick else [27.0, 85.0]):
        for rb in bridges:
            rows.append((dict(temp_c=T), make_defect("bridge_short", position=10, r_bridge=rb),
                         f"R_bridge={rb:g}ohm T={T:g}C"))

    xf = [4.0] if quick else [2.0, 4.0, 8.0]
    for T in ([27.0] if quick else [27.0, 85.0]):
        for f in xf:
            rows.append((dict(temp_c=T), make_defect("crosstalk_cap", xtalk_factor=f),
                         f"xtalk_x{f:g} T={T:g}C"))

    aging = [10.0, 80.0] if quick else [2.0, 5.0, 10.0, 20.0, 40.0, 80.0]
    for r in aging:
        rows.append((dict(temp_c=85.0), make_defect("bump_void_aging", position=5, r_open=r),
                     f"aging R+={r:g}ohm pos=5 T=85C"))

    droops = [0.1, 0.2] if quick else [0.05, 0.10, 0.15, 0.20]
    for T in ([27.0] if quick else [27.0, 85.0]):
        for df in droops:
            rows.append((dict(temp_c=T), make_defect("supply_droop", droop_frac=df),
                         f"droop={df*100:g}% T={T:g}C"))

    for ht in ([150.0] if quick else [110.0, 130.0, 150.0]):
        rows.append((dict(temp_c=27.0), make_defect("hotspot", position=10, hot_t=ht),
                     f"hotspot={ht:g}C pos=10"))

    zf = [0.6, 1.6] if quick else [0.6, 0.8, 1.25, 1.6]
    for z in zf:
        rows.append((dict(temp_c=27.0), make_defect("impedance_discontinuity", position=7, z_factor=z),
                     f"Zfac={z:g} pos=7"))

    return rows


COLUMNS = [
    "run_id", "label", "position", "severity",
    # observable confounder telemetry
    "temp_C", "vdroop_frac", "rate_GTps",
    # link modality
    "eye_height_V", "eye_amp_V", "q_factor", "ber_log10",
    "jitter_rms_ps", "jitter_pp_ps", "eye_width_ps", "delay_ps", "xtalk_std_V",
    # reflectometry modality
    "tdr_refl_coef", "tdr_pos_mm",
]


def run_campaign(base_cfg, out_csv, quick=False, with_tdr=True,
                 keep_waveforms=False, work_root="_work", verbose=True):
    grid = build_grid(quick=quick)
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    rows_out = []
    n = len(grid)
    for idx, (over, defect, sev) in enumerate(grid):
        cfg = dataclasses.replace(base_cfg, **over)
        rid = f"run{idx:04d}"
        wd = os.path.join(work_root, rid)
        feats, _, _, proc = simulate_link(cfg, defect, wd)
        if proc.returncode != 0 and verbose:
            print(f"[{rid}] ngspice rc={proc.returncode}: {proc.stderr.strip()[:120]}")
        tdr = {"tdr_refl_coef": 0.0, "tdr_pos_mm": 0.0}
        if with_tdr:
            tdr, _, _ = simulate_tdr(cfg, defect, wd)

        row = {
            "run_id": rid, "label": defect["kind"], "position": defect["position"],
            "severity": sev, "temp_C": cfg.temp_c,
            "vdroop_frac": defect["droop_frac"], "rate_GTps": cfg.rate / 1e9,
            "tdr_refl_coef": round(tdr["tdr_refl_coef"], 6),
            "tdr_pos_mm": round(tdr["tdr_pos_mm"], 4),
        }
        for k in ("eye_height_V", "eye_amp_V", "q_factor", "ber_log10",
                  "jitter_rms_ps", "jitter_pp_ps", "eye_width_ps", "delay_ps",
                  "xtalk_std_V"):
            row[k] = round(feats[k], 6)
        rows_out.append(row)
        if verbose:
            print(f"[{idx+1:3d}/{n}] {rid} {defect['kind']:<22} "
                  f"eyeH={feats['eye_height_V']*1e3:6.1f}mV  "
                  f"BER=1e{feats['ber_log10']:.0f}  jit={feats['jitter_rms_ps']:.1f}ps  "
                  f"rho={tdr['tdr_refl_coef']:.3f}")
        if not keep_waveforms and os.path.isdir(wd) and idx != 0:
            shutil.rmtree(wd, ignore_errors=True)

    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows_out:
            w.writerow({c: r.get(c, "") for c in COLUMNS})
    if verbose:
        print(f"\nWrote {len(rows_out)} rows x {len(COLUMNS)} cols -> {out_csv}")
    return rows_out
