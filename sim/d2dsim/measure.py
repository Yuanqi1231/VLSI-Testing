"""
Run ngspice in batch mode and extract link telemetry from the waveforms.
Pure standard library (no numpy): the conda numpy here is broken, and keeping the
harness stdlib-only makes the benchmark trivially reproducible.

Telemetry produced (maps to the benchmark's link modality, DEEP_SIM s4/s6.2):
  eye_height_V, eye_amp_V, q_factor, ber_log10, jitter_rms_ps, jitter_pp_ps,
  eye_width_ps, delay_ps, xtalk_std_V   (+ TDR: tdr_refl_coef, tdr_pos_mm)
The voltage (droop) and temperature modalities are recorded as observable
telemetry columns by the campaign, not re-derived here.
"""
import math
import os
import shutil
import subprocess
import tempfile

from .netlist import build_channel, build_tdr, build_tx_probe
from .prbs import prbs_bits

NGSPICE = shutil.which("ngspice") or "ngspice"


# -----------------------------------------------------------------------------
# low-level: run a netlist, read a 2-column wrdata file
# -----------------------------------------------------------------------------
def _run(netlist, workdir, outfiles, timeout=120):
    os.makedirs(workdir, exist_ok=True)
    cir = os.path.join(workdir, "deck.cir")
    with open(cir, "w") as f:
        f.write(netlist)
    proc = subprocess.run([NGSPICE, "-b", "deck.cir"], cwd=workdir,
                          capture_output=True, text=True, timeout=timeout)
    data = {}
    for name in outfiles:
        path = os.path.join(workdir, name)
        if os.path.exists(path):
            data[name] = _read_wrdata(path)
        else:
            data[name] = ([], [])
    return data, proc


def _read_wrdata(path):
    """Read a single-vector wrdata file -> (t[], v[])."""
    t, v = [], []
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                a, b = float(parts[0]), float(parts[1])
            except ValueError:
                continue
            t.append(a)
            v.append(b)
    return t, v


# -----------------------------------------------------------------------------
# small stdlib numeric helpers
# -----------------------------------------------------------------------------
def _interp(t, v, x):
    """Linear interpolation of v(t) at time x (t assumed sorted ascending)."""
    if x <= t[0]:
        return v[0]
    if x >= t[-1]:
        return v[-1]
    lo, hi = 0, len(t) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if t[mid] <= x:
            lo = mid
        else:
            hi = mid
    span = t[hi] - t[lo]
    if span <= 0:
        return v[lo]
    f = (x - t[lo]) / span
    return v[lo] + f * (v[hi] - v[lo])


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def _first_cross(t, v, level, t_after, rising=True):
    """Time of the first crossing of `level` at or after t_after; None if none."""
    for i in range(1, len(t)):
        if t[i] < t_after:
            continue
        a, b = v[i - 1], v[i]
        if rising and a < level <= b or (not rising) and a > level >= b:
            if b == a:
                return t[i]
            f = (level - a) / (b - a)
            return t[i - 1] + f * (t[i] - t[i - 1])
    return None


# -----------------------------------------------------------------------------
# eye / jitter / BER from a transient bit stream (known TX bits)
# -----------------------------------------------------------------------------
def link_features(cfg, t, v, bits, mid=None):
    ui = cfg.ui
    if len(t) < 10:
        return _empty_features()
    vmin, vmax = min(v), max(v)
    if mid is None:
        mid = 0.5 * (vmin + vmax)

    # propagation delay: first victim 0->1 boundary, then RX mid-crossing
    first_rise = next((i for i in range(1, len(bits)) if bits[i] == 1 and bits[i - 1] == 0), None)
    delay = 0.0
    if first_rise is not None:
        tb = first_rise * ui
        cr = _first_cross(t, v, mid, tb, rising=True)
        if cr is not None:
            delay = cr - tb

    # sample at bit centres (shifted by delay); skip settling + last bit
    highs, lows = [], []
    lo_i = cfg.settle_bits
    hi_i = len(bits) - 2
    for i in range(lo_i, hi_i + 1):
        tc = i * ui + 0.5 * ui + delay
        s = _interp(t, v, tc)
        (highs if bits[i] == 1 else lows).append(s)

    if not highs or not lows:
        return _empty_features()

    mh, ml = _mean(highs), _mean(lows)
    sh, sl = _std(highs), _std(lows)
    eye_height = min(highs) - max(lows)         # worst-case vertical opening
    eye_amp = mh - ml
    q = eye_amp / (sh + sl) if (sh + sl) > 0 else 99.0
    ber = 0.5 * math.erfc(q / math.sqrt(2)) if q < 38 else 0.0
    ber_log10 = math.log10(ber) if ber > 0 else -300.0

    # timing: TIE of mid-crossings at transition boundaries
    tie = []
    for i in range(lo_i, hi_i + 1):
        if bits[i] != bits[i - 1]:
            tb = i * ui
            cr = _first_cross(t, v, mid, tb - 0.5 * ui, rising=(bits[i] == 1))
            if cr is not None:
                tie.append(cr - (tb + delay))
    jit_rms = _std(tie) if tie else 0.0
    jit_pp = (max(tie) - min(tie)) if tie else 0.0
    eye_width = max(ui - jit_pp, 0.0)

    return {
        "eye_height_V": eye_height,
        "eye_amp_V": eye_amp,
        "q_factor": q,
        "ber_log10": ber_log10,
        "jitter_rms_ps": jit_rms * 1e12,
        "jitter_pp_ps": jit_pp * 1e12,
        "eye_width_ps": eye_width * 1e12,
        "delay_ps": delay * 1e12,
        "v_high_mean": mh,
        "v_low_mean": ml,
        "v_high_std": sh,
        "v_low_std": sl,
    }


def _empty_features():
    return {k: 0.0 for k in (
        "eye_height_V", "eye_amp_V", "q_factor", "ber_log10", "jitter_rms_ps",
        "jitter_pp_ps", "eye_width_ps", "delay_ps", "v_high_mean", "v_low_mean",
        "v_high_std", "v_low_std")}


# -----------------------------------------------------------------------------
# active-front-end extras: edge asymmetry, decision BER, PDN droop
# -----------------------------------------------------------------------------
def _edge_times(cfg, t, v, bits, lo_frac=0.2, hi_frac=0.8):
    """Mean rising and falling transition times [s] of signal v at its own rails.

    Rise = t(hi_frac) - t(lo_frac) on 0->1 bits; fall = t(lo_frac) - t(hi_frac) on
    1->0 bits.  The rise/fall RATIO is the stress fingerprint: temperature scales
    both together (ratio ~ 1), stress splits them (opposite NMOS/PMOS piezo sign).
    """
    if len(t) < 10:
        return 0.0, 0.0
    vlo, vhi = min(v), max(v)
    lvl_lo = vlo + lo_frac * (vhi - vlo)
    lvl_hi = vlo + hi_frac * (vhi - vlo)
    ui = cfg.ui
    rises, falls = [], []
    for i in range(cfg.settle_bits, len(bits) - 1):
        if bits[i] == bits[i - 1]:
            continue
        t0 = (i - 0.5) * ui                       # search window start (just before edge)
        if bits[i] == 1:                          # rising edge
            a = _first_cross(t, v, lvl_lo, t0, rising=True)
            b = _first_cross(t, v, lvl_hi, t0, rising=True)
            if a is not None and b is not None and b > a:
                rises.append(b - a)
        else:                                     # falling edge
            a = _first_cross(t, v, lvl_hi, t0, rising=False)
            b = _first_cross(t, v, lvl_lo, t0, rising=False)
            if a is not None and b is not None and b > a:
                falls.append(b - a)
    return (_mean(rises) if rises else 0.0), (_mean(falls) if falls else 0.0)


def _decision_ber(cfg, t, v, bits, mid=0.0):
    """Bit-error count from the slicer decision waveform sampled at bit centres."""
    if len(t) < 10:
        return 1.0, 0
    delay = _delay_of(cfg, t, v, bits, mid)      # compute once, not per bit
    errs = n = 0
    for i in range(cfg.settle_bits, len(bits) - 2):
        s = _interp(t, v, i * cfg.ui + 0.5 * cfg.ui + delay)
        decided = 1 if s > mid else 0
        n += 1
        if decided != bits[i]:
            errs += 1
    return (errs / n if n else 1.0), errs


def _delay_of(cfg, t, v, bits, mid):
    """Slicer latency from the first 0->1 transition AFTER the channel has settled
    (>= settle_bits), so the alignment phase is taken from a filled channel."""
    fr = next((i for i in range(max(1, cfg.settle_bits), len(bits))
               if bits[i] == 1 and bits[i - 1] == 0), None)
    if fr is None:
        return 0.0
    cr = _first_cross(t, v, mid, fr * cfg.ui, rising=True)
    return (cr - fr * cfg.ui) if cr is not None else 0.0


# -----------------------------------------------------------------------------
# public entry points
# -----------------------------------------------------------------------------
def simulate_link(cfg, defect, workdir):
    """Build + run the link netlist, return (features, waveform) and raw bits."""
    bits_v = prbs_bits(cfg.prbs_order, cfg.n_bits, cfg.seed_v)
    bits_a1 = prbs_bits(cfg.prbs_order, cfg.n_bits, cfg.seed_a1)
    bits_a2 = prbs_bits(cfg.prbs_order, cfg.n_bits, cfg.seed_a2)
    deck = build_channel(cfg, defect, bits_v, bits_a1, bits_a2)
    want = ["rx.dat", "agg.dat"]
    if cfg.active_frontend:
        want += ["tx.dat", "dec.dat", "vdd.dat"]
    data, proc = _run(deck, workdir, want)
    t, v = data["rx.dat"]
    feats = link_features(cfg, t, v, bits_v)
    # crosstalk-induced victim noise proxy = larger of the two rail std's
    feats["xtalk_std_V"] = max(feats["v_high_std"], feats["v_low_std"])

    if cfg.active_frontend:
        # decision-based BER from the slicer (reliable from the PRBS run)
        td, vd = data.get("dec.dat", ([], []))
        ber_dec, n_err = _decision_ber(cfg, td, vd, bits_v, mid=0.0)
        feats["ber_dec"] = ber_dec
        feats["n_err"] = n_err
        # observed PDN droop (min rail vs nominal)
        tv, vv = data.get("vdd.dat", ([], []))
        feats["vdd_min_V"] = min(vv) if vv else 0.0
        feats["vdd_droop_mV"] = (cfg.vdd - min(vv)) * 1e3 if vv else 0.0
    return feats, (t, v), bits_v, proc


def _edge_1090(t, v, t_start, vlo, vhi, rising):
    """10-90% (rising) / 90-10% (falling) transition time about t_start [s]."""
    l10 = vlo + 0.1 * (vhi - vlo)
    l90 = vlo + 0.9 * (vhi - vlo)
    if rising:
        a = _first_cross(t, v, l10, t_start, rising=True)
        b = _first_cross(t, v, l90, t_start, rising=True)
    else:
        a = _first_cross(t, v, l90, t_start, rising=False)
        b = _first_cross(t, v, l10, t_start, rising=False)
    return (b - a) if (a is not None and b is not None and b > a) else 0.0


def simulate_tx_probe(cfg, defect, workdir):
    """Isolated single-edge TX probe -> intrinsic rise/fall times + n/p asymmetry.

    Edge times are measured relative to the LOCALLY settled low/high (sampled in
    the flat hold regions), so they reflect driver strength only -- not ISI or the
    global min/max.  The rise/fall ratio is the stress fingerprint.
    """
    deck, t_hi, t_lo = build_tx_probe(cfg, defect, "txp.dat")
    data, proc = _run(deck, workdir, ["txp.dat"])
    t, v = data["txp.dat"]
    if len(t) < 10:
        return {"t_rise_ps": 0.0, "t_fall_ps": 0.0, "drive_asym_np": 0.0,
                "tx_swing_V": 0.0}, (t, v), proc
    ui = cfg.ui
    v_lo = _interp(t, v, t_hi - 2 * ui)        # settled low just before the rise
    v_hi = _interp(t, v, t_lo - 2 * ui)        # settled high just before the fall
    tr = _edge_1090(t, v, t_hi - 0.5 * ui, v_lo, v_hi, rising=True)
    tf = _edge_1090(t, v, t_lo - 0.5 * ui, v_lo, v_hi, rising=False)
    return {
        "t_rise_ps": round(tr * 1e12, 4),
        "t_fall_ps": round(tf * 1e12, 4),
        "drive_asym_np": round(tr / tf, 5) if tf > 0 else 0.0,
        "tx_swing_V": round(v_hi - v_lo, 5),
    }, (t, v), proc


def simulate_tdr(cfg, defect, workdir):
    """Build + run the TDR netlist, return reflection coefficient and position."""
    deck, t0 = build_tdr(cfg, defect, "tdr.dat")
    data, proc = _run(deck, workdir, ["tdr.dat"])
    t, v = data["tdr.dat"]
    if len(t) < 10:
        return {"tdr_refl_coef": 0.0, "tdr_pos_mm": 0.0}, (t, v), proc
    incident = cfg.vdd / 2.0                     # matched-source launch level
    t_inc = t0 + cfg.tr
    guard = 2e-12
    # Early window only: the first few round trips, so the reflection arrival
    # (not the slow DC tail of a fully-open line charging to VS) sets position.
    win_end = t_inc + 5.0 * cfg.td_total
    seg = [(tt, vv) for tt, vv in zip(t, v) if t_inc + guard < tt <= win_end]
    if not seg:
        return {"tdr_refl_coef": 0.0, "tdr_pos_mm": 0.0}, (t, v), proc
    peak, tpk = max((abs(vv - incident), tt) for tt, vv in seg)
    rho = 2.0 * peak / cfg.vdd                    # measured dev = rho * incident
    pos_mm = cfg.vp * (tpk - t_inc) / 2.0 * 1e3   # round-trip -> one-way distance
    return {"tdr_refl_coef": round(rho, 4), "tdr_pos_mm": pos_mm}, (t, v), proc
