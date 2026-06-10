"""v2 raw-waveform dataset: a SAMPLED operating space instead of a grid.

Fixes/extensions over wave_campaign.py (v1), in response to the dataset critique:
  * temperature ~ U(27,110) C for EVERY class. v1 gave healthy three exclusive
    temperatures (45/65/100 C), so temperature support was a partial label proxy
    a telemetry-fused model could exploit; v2 removes that leak.
  * severities are CONTINUOUS (log-uniform for R-like faults), positions random.
  * the victim/aggressor PRBS seeds are random per run (workload variation).
    seed_v is stored per row so the ML side can reconstruct the TX bits and
    condition on them (pattern-invariant diagnosis / channel identification).
  * benign workload droop ~ U(0,0.12), decorrelated from the noise seed
    (v1 tied vdroop to seed index sd % 3).
  * per-run channel manufacturing variation: multiplicative factors on RLGC,
    bump parasitics, Ron, Crx, Rterm -- nuisance, NOT a label, so the model
    cannot fingerprint one nominal channel.
  * per-run TX launch jitter (RJ + DCD + SJ): a benign eye-closing nuisance.
  * MIXED_FRAC of fault rows carry TWO distinct concurrent faults; the label is
    "kindA+kindB" (sorted) -> multi-label diagnosis.
  * generation is PARALLEL (ProcessPoolExecutor, one ngspice per worker).
  * the FULL-RESOLUTION ngspice waveform (tstep grid, ~62 samples/UI) is saved
    per run under <out>/raw/w#####.f32 (little-endian float32; t0/dt/n in
    scenarios.jsonl). The CSV keeps the resampled samples_per_ui grid.

Run:  ~/miniconda3/envs/drl_hw2/bin/python run_wave2.py --n-rows 4000
"""
import argparse
import csv
import json
import math
import os
import random
import shutil
import time
from array import array
from concurrent.futures import ProcessPoolExecutor, as_completed

from .params import Config, DEFECT_KINDS
from .campaign import make_defect
from .measure import simulate_link
from .wave_campaign import _resample

SPU = 8                      # resampled samples per UI (the lossy CSV grid)
MIXED_FRAC = 0.15            # fraction of fault rows with a second concurrent fault
HEALTHY_WEIGHT = 2.0         # sampling weight of healthy vs each fault class
CLASSES = list(DEFECT_KINDS)
FAULTS = [c for c in CLASSES if c != "healthy"]


# ------------------------------------------------------------- sampling -------
def sample_defect(rng, kind):
    """One defect dict + its scalar severity, drawn from a continuous range.

    R-like severities are log-uniform (their effect is multiplicative); the rest
    uniform. Ranges match the v1 grid end-points.
    """
    def logu(a, b):
        return math.exp(rng.uniform(math.log(a), math.log(b)))

    if kind == "resistive_open":
        r = logu(20.0, 500.0)
        return make_defect(kind, position=rng.randint(2, 17), r_open=r), r
    if kind == "bridge_short":
        rb = logu(50.0, 3000.0)
        return make_defect(kind, position=rng.randint(2, 17), r_bridge=rb), rb
    if kind == "crosstalk_cap":
        f = rng.uniform(2.0, 8.0)
        return make_defect(kind, xtalk_factor=f), f
    if kind == "bump_void_aging":
        r = logu(5.0, 80.0)         # bump-region mechanism -> end segments
        return make_defect(kind, position=rng.choice([1, 2, 17, 18]), r_open=r), r
    if kind == "supply_droop":
        df = rng.uniform(0.05, 0.20)
        return make_defect(kind, droop_frac=df), df
    if kind == "hotspot":
        ht = rng.uniform(115.0, 160.0)
        return make_defect(kind, position=rng.randint(3, 16), hot_t=ht), ht
    if kind == "impedance_discontinuity":
        # exclude the near-nominal band |z-1| < 0.4 (indistinguishable from healthy)
        z = rng.uniform(0.4, 0.75) if rng.random() < 0.5 else rng.uniform(1.4, 3.0)
        return make_defect(kind, position=rng.randint(2, 15), z_factor=z), z
    if kind == "r_drift":
        dr = rng.uniform(15.0, 150.0)
        return make_defect(kind, drift_r=dr), dr
    if kind == "c_drift":
        dc = rng.uniform(0.3, 2.5)
        return make_defect(kind, drift_c=dc), dc
    return make_defect("healthy"), 0.0


def make_scenario(idx, master_seed, n_bits):
    """Deterministic per-row scenario: fault(s) + operating point + nuisances."""
    rng = random.Random(master_seed * 1_000_003 + idx)
    c0 = Config()
    kind = rng.choices(
        CLASSES, weights=[HEALTHY_WEIGHT if c == "healthy" else 1.0 for c in CLASSES])[0]
    if kind == "healthy":
        defects, sevs = [make_defect("healthy")], [0.0]
    else:
        d, s = sample_defect(rng, kind)
        defects, sevs = [d], [s]
        if rng.random() < MIXED_FRAC:
            k2 = rng.choice([c for c in FAULTS if c != kind])
            d2, s2 = sample_defect(rng, k2)
            defects.append(d2)
            sevs.append(s2)
    order = sorted(range(len(defects)), key=lambda i: defects[i]["kind"])
    defects = [defects[i] for i in order]
    sevs = [sevs[i] for i in order]
    label = "+".join(d["kind"] for d in defects)

    cfg_over = dict(
        n_bits=n_bits,
        temp_c=round(rng.uniform(27.0, 110.0), 2),      # continuous T for ALL classes
        vdroop_benign=round(rng.uniform(0.0, 0.12), 4),
        noise_seed=rng.randrange(1, 1 << 30),
        # workload variation: random data pattern on victim + aggressors
        seed_v=rng.randrange(1, 1 << c0.prbs_order),
        seed_a1=rng.randrange(1, 1 << c0.prbs_order),
        seed_a2=rng.randrange(1, 1 << c0.prbs_order),
        # benign TX launch jitter (nuisance)
        rj_sigma_ps=round(rng.uniform(0.2, 1.2), 3),
        dcd_ps=round(rng.uniform(-1.0, 1.0), 3),
        sj_amp_ps=round(rng.uniform(0.0, 1.2), 3),
        sj_freq_hz=round(rng.uniform(5e7, 3e8)),
        jitter_seed=rng.randrange(1 << 30),
        # per-run channel manufacturing variation (nuisance, not a label)
        r_per_mm=c0.r_per_mm * rng.uniform(0.92, 1.08),
        l_per_mm=c0.l_per_mm * rng.uniform(0.92, 1.08),
        c_per_mm=c0.c_per_mm * rng.uniform(0.92, 1.08),
        cc_per_mm=c0.cc_per_mm * rng.uniform(0.85, 1.15),
        r_bump=c0.r_bump * rng.uniform(0.85, 1.15),
        l_bump=c0.l_bump * rng.uniform(0.85, 1.15),
        c_bump=c0.c_bump * rng.uniform(0.85, 1.15),
        r_on=c0.r_on * rng.uniform(0.95, 1.05),
        c_rx=c0.c_rx * rng.uniform(0.90, 1.10),
        r_term=c0.r_term * rng.uniform(0.95, 1.05),
    )
    return dict(idx=idx, label=label, defects=defects, sevs=sevs, cfg_over=cfg_over)


# --------------------------------------------------------------- worker -------
def _worker(arg):
    """One ngspice run in a private work dir; saves the raw waveform, returns
    the resampled row. Runs in a child process."""
    scn, out_dir, work_root, noise_gain = arg
    idx = scn["idx"]
    cfg = Config(active_frontend=False, noise_on=True, noise_gain=noise_gain,
                 **scn["cfg_over"])
    defects = scn["defects"]
    wd = os.path.join(work_root, f"w{idx:05d}")
    try:
        feats, (t, v), _, proc = simulate_link(
            cfg, defects if len(defects) > 1 else defects[0], wd)
        rc, err = proc.returncode, (proc.stderr.strip()[:150] if proc.returncode else "")
    finally:
        shutil.rmtree(wd, ignore_errors=True)

    # full-resolution waveform (linearized tstep grid) -> binary float32
    raw_rel = os.path.join("raw", f"w{idx:05d}.f32")
    with open(os.path.join(out_dir, raw_rel), "wb") as f:
        array("f", v).tofile(f)
    raw = dict(file=raw_rel, n=len(v), t0=(t[0] if t else 0.0),
               dt=((t[-1] - t[0]) / (len(t) - 1) if len(t) > 1 else 0.0))

    m = cfg.n_bits * SPU
    wave = _resample(t, v, cfg.n_bits, cfg.ui, SPU) if len(t) > 5 else [0.0] * m
    eye = {k: feats[k] for k in ("eye_height_V", "eye_width_ps", "ber_log10",
                                 "jitter_rms_ps", "delay_ps")}
    return idx, scn, eye, wave, raw, rc, err


# ----------------------------------------------------------------- main -------
def run_v2(out_dir="out/wave2", n_rows=4000, n_bits=160, workers=None,
           master_seed=20260610, noise_gain=30.0, work_root="_work_wave2",
           verbose=True):
    os.makedirs(os.path.join(out_dir, "raw"), exist_ok=True)
    workers = workers or max(1, (os.cpu_count() or 4) - 2)
    base = Config(n_bits=n_bits)
    m = n_bits * SPU

    # nominal RX latency from a healthy 27C nominal-channel run -> region masks
    cfg0 = Config(active_frontend=False, noise_on=True, noise_gain=noise_gain,
                  n_bits=n_bits, temp_c=27.0, noise_seed=1)
    f0, _, _, _ = simulate_link(cfg0, make_defect("healthy"),
                                os.path.join(work_root, "_cal"))
    shutil.rmtree(os.path.join(work_root, "_cal"), ignore_errors=True)
    delay_samples = int(round(f0["delay_ps"] * 1e-12 / (base.ui / SPU)))

    scns = [make_scenario(i, master_seed, n_bits) for i in range(n_rows)]
    csv_path = os.path.join(out_dir, "waveforms.csv")
    header = (["run_id", "label", "sev", "temp_C", "vdroop_frac", "noise_seed",
               "seed_v", "eye_height_V", "eye_width_ps", "ber_log10"]
              + [f"s{i}" for i in range(m)])
    t_start = time.time()
    n_done = n_fail = 0
    with open(csv_path, "w", newline="") as cf, \
         open(os.path.join(out_dir, "scenarios.jsonl"), "w") as jf, \
         ProcessPoolExecutor(max_workers=workers) as ex:
        w = csv.writer(cf)
        w.writerow(header)
        futs = [ex.submit(_worker, (s, out_dir, work_root, noise_gain)) for s in scns]
        for fut in as_completed(futs):
            try:
                idx, scn, eye, wave, raw, rc, err = fut.result()
            except Exception as e:                      # ngspice timeout/crash
                n_fail += 1
                print(f"[worker error] {type(e).__name__}: {e}", flush=True)
                continue
            o = scn["cfg_over"]
            w.writerow([f"w{idx:05d}", scn["label"], f"{scn['sevs'][0]:g}",
                        f"{o['temp_c']:g}", f"{o['vdroop_benign']:g}",
                        o["noise_seed"], o["seed_v"],
                        f"{eye['eye_height_V']:.5f}", f"{eye['eye_width_ps']:.2f}",
                        f"{eye['ber_log10']:.1f}"] + [f"{x:.5f}" for x in wave])
            jf.write(json.dumps(dict(
                run_id=f"w{idx:05d}", label=scn["label"], sevs=scn["sevs"],
                defects=scn["defects"], cfg_over=o, raw=raw, eye=eye,
                ngspice_rc=rc, ngspice_err=err)) + "\n")
            n_done += 1
            if rc != 0:
                n_fail += 1
            if verbose and n_done % 25 == 0:
                el = time.time() - t_start
                rate = n_done / el
                print(f"[{n_done:5d}/{n_rows}]  {rate*60:5.1f} runs/min  "
                      f"ETA {((n_rows - n_done) / rate) / 60:5.1f} min  "
                      f"fails={n_fail}", flush=True)
            if n_done % 200 == 0:
                cf.flush(); jf.flush()

    meta = {
        "version": 2, "samples_per_ui": SPU, "n_bits": n_bits, "n_samples": m,
        "ui_ps": base.ui * 1e12, "tstep_ps": base.tstep * 1e12,
        "settle_bits": base.settle_bits, "delay_samples": delay_samples,
        "noise_gain": noise_gain, "n_rows": n_done, "n_fail": n_fail,
        "master_seed": master_seed, "workers": workers,
        "prbs_order": base.prbs_order,        # bits per row = prbs_bits(order, n_bits, seed_v)
        "multi_label": True, "mixed_frac": MIXED_FRAC,
        "healthy_weight": HEALTHY_WEIGHT,
        "telemetry": ["temp_C", "vdroop_frac"],
        "classes": CLASSES,
        "raw_format": "little-endian float32, v(rxo) on the linearized tstep grid; "
                      "per-run t0/dt/n in scenarios.jsonl",
        "notes": "continuous T/severity for all classes; random PRBS per run; "
                 "per-run channel variation + TX jitter (nuisances); "
                 "15% of fault rows have two concurrent faults (label 'a+b')",
    }
    with open(os.path.join(out_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    if verbose:
        el = time.time() - t_start
        print(f"\nWrote {n_done} rows ({n_fail} ngspice failures) in {el/60:.1f} min "
              f"-> {csv_path}")
    return csv_path


def build_cli():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="out/wave2")
    ap.add_argument("--n-rows", type=int, default=4000)
    ap.add_argument("--n-bits", type=int, default=160)
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--seed", type=int, default=20260610)
    ap.add_argument("--noise-gain", type=float, default=30.0)
    return ap


def main(argv=None):
    a = build_cli().parse_args(argv)
    run_v2(out_dir=a.out, n_rows=a.n_rows, n_bits=a.n_bits, workers=a.workers,
           master_seed=a.seed, noise_gain=a.noise_gain)


if __name__ == "__main__":
    main()
