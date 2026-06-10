"""Quick selftest for transient resistor noise + drift faults (Task #2)."""
import dataclasses as dc
import statistics
import sys

from d2dsim.params import Config
from d2dsim.campaign import make_defect
from d2dsim.measure import simulate_link


def held_std(cfg, t, v, bits):
    """True injected-noise RMS: residual std inside flat HELD bits after removing
    each bit's own mean (so the bimodal 0/1 spread does NOT count)."""
    ui = cfg.ui
    by_bit = {}
    for ti, vi in zip(t, v):
        bi = ti / ui
        ib = int(bi)
        frac = bi - ib
        if 2 <= ib < len(bits) - 2 and 0.4 < frac < 0.6:
            if bits[ib] == bits[ib - 1] == bits[ib + 1]:   # flat run interior
                by_bit.setdefault(ib, []).append(vi)
    resid = []
    for ib, xs in by_bit.items():
        if len(xs) >= 2:
            m = sum(xs) / len(xs)
            resid.extend(x - m for x in xs)
    return statistics.pstdev(resid) if len(resid) > 2 else 0.0


def run(label, **over):
    defect = over.pop("_defect", make_defect("healthy"))
    cfg = dc.replace(Config(), n_bits=120, **over)
    feats, (t, v), bits, proc = simulate_link(cfg, defect, f"_work/_nt_{label}")
    hs = held_std(cfg, t, v, bits)
    print(f"{label:28s} rc={proc.returncode} nsamp={len(t):5d} "
          f"eyeH={feats['eye_height_V']*1e3:6.1f}mV BER=1e{feats['ber_log10']:+.0f} "
          f"held_std={hs*1e3:6.2f}mV")
    if proc.returncode != 0:
        print("  STDERR:", proc.stderr.strip()[:200])
    return feats, hs, list(v)


print("== noiseless baseline ==")
run("noiseless_T27", noise_on=False)

print("\n== noisy: temperature scales noise (sqrt(T)) ==")
for g in (12.0, 40.0):
    _, hs27, v_a = run(f"noisy_T27_g{g:g}", noise_on=True, noise_seed=1, temp_c=27.0, noise_gain=g)
    _, hs110, _ = run(f"noisy_T110_g{g:g}", noise_on=True, noise_seed=1, temp_c=110.0, noise_gain=g)
    print(f"  gain={g:g}: noise_rms T27={hs27*1e3:.2f}mV T110={hs110*1e3:.2f}mV "
          f"ratio={hs110/hs27 if hs27 else 0:.3f} (expect ~1.13 from kT)")

print("\n== different seed -> different waveform ==")
_, _, v_a = run("noisy_T27_seed1", noise_on=True, noise_seed=1, temp_c=27.0, noise_gain=40)
_, _, v_b = run("noisy_T27_seed2", noise_on=True, noise_seed=2, temp_c=27.0, noise_gain=40)
diff = sum(abs(a - b) for a, b in zip(v_a, v_b)) / len(v_a)
print(f"  mean|seed1-seed2| = {diff*1e3:.3f}mV  (expect >0 if RNG reseeds)")

print("\n== continuous drift faults run + close the eye ==")
run("r_drift_1.5", noise_on=True, noise_seed=3, _defect=make_defect("r_drift", drift_r=1.5))
run("c_drift_1.5", noise_on=True, noise_seed=3, _defect=make_defect("c_drift", drift_c=1.5))
