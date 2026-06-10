"""Raw-waveform fault-diagnosis dataset generator.

Unlike campaign.py (which extracts hand-crafted eye/jitter/BER *features*), this
emits the RAW analog RX waveform v(vrxo) of each run so an ML model can learn
directly from the signal -- a post-silicon / diagnostic-mode setting (cf. Miao et
al. eye-image CNN, Usama et al. waveform AE).

Design:
  * ideal front-end + transient resistor noise (noise_on=True) -> stochastic eye.
  * the TX bit pattern (seed_v) is FIXED across every run, so the only sources of
    variation are the fault, the temperature, and the per-draw noise seed. This
    isolates what the model must learn and makes the signal/non-signal region mask
    (built from the known bits) identical for every row.
  * every run is resampled onto the SAME uniform grid (samples_per_ui samples per
    UI) by interpolation, so all waveforms share one length and one bit-phase map.

Outputs (under out/wave/):
  waveforms.csv : run_id,label,sev,temp_C,noise_seed, s0..s{M-1}
  meta.json     : grid + samples_per_ui + ui_ps + settle_bits + delay_samples +
                  bits[] (the fixed TX pattern) + class list
"""
import csv
import dataclasses
import json
import os
import shutil

from .params import Config
from .campaign import make_defect
from .measure import simulate_link, link_features, _interp
from .prbs import prbs_bits


# ---- per-class fault configs: (overrides, defect, sev_value, sev_label) -------
def build_wave_grid(quick=False):
    rows = []

    def add(kind, over, sev, lbl, **dk):
        rows.append((over, make_defect(kind, **dk), sev, lbl))

    # CRITICAL for the confounder story: faults span the SAME temperature range as
    # healthy, so high temperature is NOT a label proxy -- a hot link can be benign
    # OR faulty, and only the JOINT (margin, temp) separates them.
    ftemps = [27.0, 110.0] if quick else [27.0, 85.0, 110.0]

    # healthy across a dense temperature grid (the benign-stress class)
    for T in ([27.0, 110.0] if quick else [27.0, 45.0, 65.0, 85.0, 100.0, 110.0]):
        add("healthy", dict(temp_c=T), 0.0, f"T={T:g}C")

    # resistive_open: discrete severities x position x temp
    for T in ftemps:
        for r in ([50.0, 500.0] if quick else [20.0, 50.0, 150.0, 500.0]):
            for pos in ([10] if quick else [5, 14]):
                add("resistive_open", dict(temp_c=T), r, f"R={r:g} pos={pos} T={T:g}",
                    position=pos, r_open=r)

    # bridge_short: shunt R to aggressor
    for T in ftemps:
        for rb in ([200.0] if quick else [50.0, 200.0, 800.0, 3000.0]):
            add("bridge_short", dict(temp_c=T), rb, f"Rb={rb:g} T={T:g}",
                position=10, r_bridge=rb)

    # crosstalk_cap
    for T in ftemps:
        for f in ([4.0] if quick else [2.0, 4.0, 8.0]):
            add("crosstalk_cap", dict(temp_c=T), f, f"x{f:g} T={T:g}", xtalk_factor=f)

    # bump_void_aging (hot field operation)
    for T in ([85.0, 110.0]):
        for r in ([20.0] if quick else [5.0, 20.0, 40.0, 80.0]):
            add("bump_void_aging", dict(temp_c=T), r, f"aging R+={r:g} T={T:g}", position=5, r_open=r)

    # supply_droop
    for T in ftemps:
        for df in ([0.1] if quick else [0.05, 0.10, 0.15, 0.20]):
            add("supply_droop", dict(temp_c=T), df, f"droop={df*100:g}% T={T:g}", droop_frac=df)

    # hotspot (local hot region) at several baseline die temperatures
    for T in ftemps:
        for ht in ([150.0] if quick else [120.0, 150.0]):
            add("hotspot", dict(temp_c=T), ht, f"hot={ht:g}C T={T:g}", position=10, hot_t=ht)

    # impedance_discontinuity (Z step over a 3-segment span; wider range)
    for T in ftemps:
        for z in ([0.4, 3.0] if quick else [0.4, 0.6, 1.8, 3.0]):
            add("impedance_discontinuity", dict(temp_c=T), z, f"Z={z:g} T={T:g}", position=7, z_factor=z)

    # --- continuous drift faults: smooth severity axis (regression target) ---
    n_dr = 3 if quick else 7
    for T in ftemps:
        for i in range(n_dr):
            dr = 15.0 + (150.0 - 15.0) * i / (n_dr - 1)      # distributed series R [ohm], [15,150]
            add("r_drift", dict(temp_c=T), dr, f"dR={dr:.0f}ohm T={T:g}", drift_r=dr)
            dc_ = 0.3 + (2.5 - 0.3) * i / (n_dr - 1)         # shunt-C drift x in [0.3,2.5]
            add("c_drift", dict(temp_c=T), dc_, f"dC={dc_:.2f} T={T:g}", drift_c=dc_)

    return rows


def _resample(t, v, n_bits, ui, spu):
    """Interpolate v(t) onto k*ui/spu for k in [0, n_bits*spu) -> fixed-length list."""
    m = n_bits * spu
    dt = ui / spu
    return [_interp(t, v, k * dt) for k in range(m)]


def run_wave_campaign(out_dir="out/wave", quick=False, seeds=6, samples_per_ui=8,
                      n_bits=128, noise_gain=30.0, work_root="_work_wave", verbose=True):
    os.makedirs(out_dir, exist_ok=True)
    base = Config(active_frontend=False, noise_on=True, noise_gain=noise_gain,
                  n_bits=n_bits)
    bits_v = prbs_bits(base.prbs_order, base.n_bits, base.seed_v)
    grid = build_wave_grid(quick=quick)
    spu = samples_per_ui
    m = n_bits * spu
    benign_droops = [0.0, 0.05, 0.10]              # OBSERVABLE benign workload droop

    # nominal RX latency (samples) from a healthy 27C run -> shifts the region mask
    cfg0 = dataclasses.replace(base, temp_c=27.0, noise_seed=1)
    f0, (t0, v0), _, _ = simulate_link(cfg0, make_defect("healthy"), f"{work_root}/_cal")
    delay_samples = int(round(f0["delay_ps"] * 1e-12 / (base.ui / spu)))

    csv_path = os.path.join(out_dir, "waveforms.csv")
    header = (["run_id", "label", "sev", "temp_C", "vdroop_frac", "noise_seed"]
              + [f"s{i}" for i in range(m)])
    n_total = len(grid) * seeds
    idx = 0
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for (over, defect, sev, lbl) in grid:
            for sd in range(seeds):
                vdr = benign_droops[sd % len(benign_droops)]
                cfg = dataclasses.replace(base, noise_seed=1000 + sd,
                                          vdroop_benign=vdr, **over)
                rid = f"w{idx:04d}"
                wd = os.path.join(work_root, rid)
                feats, (t, v), _, proc = simulate_link(cfg, defect, wd)
                if proc.returncode != 0 and verbose:
                    print(f"[{rid}] ngspice rc={proc.returncode}: {proc.stderr.strip()[:100]}")
                wave = _resample(t, v, n_bits, base.ui, spu) if len(t) > 5 else [0.0] * m
                w.writerow([rid, defect["kind"], f"{sev:g}", f"{cfg.temp_c:g}",
                            f"{vdr:g}", cfg.noise_seed] + [f"{x:.5f}" for x in wave])
                if verbose and idx % 20 == 0:
                    print(f"[{idx+1:4d}/{n_total}] {rid} {defect['kind']:<22} "
                          f"{lbl:<16} T={cfg.temp_c:g} vdr={vdr:g} "
                          f"eyeH={feats['eye_height_V']*1e3:5.0f}mV BER=1e{feats['ber_log10']:+.0f}")
                shutil.rmtree(wd, ignore_errors=True)
                idx += 1

    meta = {
        "samples_per_ui": spu, "n_bits": n_bits, "n_samples": m,
        "ui_ps": base.ui * 1e12, "tstep_ps": base.tstep * 1e12,
        "settle_bits": base.settle_bits, "delay_samples": delay_samples,
        "noise_gain": noise_gain, "seeds": seeds, "n_rows": idx,
        "benign_droops": benign_droops, "telemetry": ["temp_C", "vdroop_frac"],
        "bits": list(bits_v),
        "classes": sorted({d["kind"] for (_, d, _, _) in grid}),
    }
    with open(os.path.join(out_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    if verbose:
        print(f"\nWrote {idx} waveforms x {m} samples -> {csv_path}")
        print(f"meta -> {os.path.join(out_dir, 'meta.json')}  (delay_samples={delay_samples})")
    return csv_path
