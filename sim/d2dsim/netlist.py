"""
ngspice netlist generation for the D2D interconnect (pure ngspice; no commercial
EM/AMI tools).  A line = behavioural driver (PWL swing through R_on) -> tx micro-
bump (R+L+C) -> N-segment RLGC ladder -> rx micro-bump -> RX pad C (+ light term).
Victim + two aggressors are coupled node-by-node by Cc (and optional mutual K).

Defect injection (DEEP_SIM s6.1) perturbs specific ladder elements so each run has
a known ground-truth label and position.  Two builders are provided:
  build_channel() -> transient link simulation (eye / jitter / skew / crosstalk)
  build_tdr()     -> source-matched step for reflectometry (SREL/TDR signature)
"""
import math

from .params import Config
from . import physics

K_BOLTZ = 1.380649e-23   # Boltzmann constant [J/K]


# -----------------------------------------------------------------------------
# transient (Johnson-Nyquist) resistor noise
# -----------------------------------------------------------------------------
def _noise_na(cfg, R):
    """White trnoise RMS [V] for resistor R at the die temperature.

    NA = noise_gain * sqrt(4 k T R * B_eff), with effective bandwidth B_eff =
    1/(2*tstep) (the trnoise update rate). sqrt(4kTR) is the physical thermal EMF;
    noise_gain lumps in RX-amp / supply noise. NA grows as sqrt(T) (the confounder)
    and sqrt(R) (so a resistive fault is self-revealing in its own noise)."""
    Tk = cfg.temp_c + 273.15
    beff = 1.0 / (2.0 * cfg.tstep)
    return cfg.noise_gain * math.sqrt(max(4.0 * K_BOLTZ * Tk * R * beff, 0.0))


def _emit_r(lines, cfg, name, n1, n2, R, model="", noisy=False):
    """Series resistor R{name} n1->n2 (optional .model suffix). When `noisy`, splice
    a trnoise thermal-EMF source in series via an internal node {name}z."""
    if noisy and R > 0:
        na = _noise_na(cfg, R)
        zint = f"{name}z"
        lines.append(f"R{name} {n1} {zint} {R:.6e}{model}")
        lines.append(f"V{name}n {zint} {n2} trnoise({na:.6e} {cfg.tstep:.3e} 0 0)")
    else:
        lines.append(f"R{name} {n1} {n2} {R:.6e}{model}")


# -----------------------------------------------------------------------------
# stimulus
# -----------------------------------------------------------------------------
def bits_to_pwl(bits, ui, tr, vlo, vhi, swing_scale=1.0):
    """Piecewise-linear waveform for a bit stream with finite rise/fall `tr`.

    Only emits breakpoints at transitions (holds elsewhere) -> compact PWL.
    `swing_scale` < 1 models a drooping supply reducing the launched swing.
    """
    def lvl(b):
        return vlo + (vhi - vlo) * b * swing_scale

    pts = [(0.0, lvl(bits[0]))]
    for i in range(1, len(bits)):
        if bits[i] != bits[i - 1]:
            tb = i * ui
            pts.append((tb - tr / 2.0, lvl(bits[i - 1])))
            pts.append((tb + tr / 2.0, lvl(bits[i])))
    pts.append((len(bits) * ui, lvl(bits[-1])))
    # enforce strictly increasing time (guard against tr ~ UI)
    clean = [pts[0]]
    for t, v in pts[1:]:
        if t <= clean[-1][0]:
            t = clean[-1][0] + 1e-15
        clean.append((t, v))
    return clean


def _pwl_str(pts):
    return "PWL(" + " ".join(f"{t:.6e} {v:.6e}" for t, v in pts) + ")"


# -----------------------------------------------------------------------------
# active behavioural front-end (Stages 1-4, MULTIPHYSICS_DESIGN.md)
# -----------------------------------------------------------------------------
def _emit_tx_active(lines, cfg, p, vrm_scale=1.0, with_sso=True):
    """alpha-law push-pull TX on a compact PDN; drives node {p}txo.

    The pull-up current is drawn FROM the PDN node {p}vddtx; an explicit SSO load
    (mean activity*i_full_a) makes the rail droop observably. Pull-down sinks {p}txo
    to ground. Kp/Kn carry mu(T), Vth(T), and the OPPOSITE-sign piezo stress term,
    computed in physics.py and inlined as literals.  `with_sso=False` (the intrinsic
    edge probe) omits the data-correlated SSO load so it can't bias the edge ratio.
    """
    Kp, Kn, vth = physics.drive_conductances(cfg)
    vdd0 = cfg.vdd * vrm_scale
    a = cfg.alpha_pow
    # compact PDN: stiff VRM -> Rpdn -> Lpdn -> vddtx (decoupled by Cdec)
    lines.append(f"V{p}vrm {p}vrm 0 {vdd0:.6e}")
    lines.append(f"R{p}pdn {p}vrm {p}vddpre {cfg.r_pdn:.6e}")
    lines.append(f"L{p}pdn {p}vddpre {p}vddtx {cfg.l_pdn:.6e}")
    lines.append(f"C{p}dec {p}vddtx 0 {cfg.c_decap:.6e}")
    # SSO/aggregate-PHY load: a single behavioural lane draws too little current to
    # move the rail, so model the parallel-bus switching load explicitly -- mean =
    # activity*i_full_a (-> static IR droop = Rpdn*i_avg) with a data-correlated
    # ripple (-> Ldi/dt first-droop ring). This is what makes vdd_droop observable.
    if with_sso:
        i_avg = cfg.activity * cfg.i_full_a
        lines.append(f"B{p}sso {p}vddtx 0 I = {i_avg:.6e} + {i_avg:.6e}*(V({p}din)-0.5)")
    # slew node = driver output txo (finite edge via Cint through Ron(Vrail,T,sigma)).
    # max(...,1e-3) clamps a sub-threshold rail to ~0 conductance (driver off) instead
    # of pow() of a negative base silently returning its magnitude.
    lines.append(f"C{p}int {p}txo 0 {cfg.c_int:.6e}")
    lines.append(f"B{p}pu {p}vddtx {p}txo I = "
                 f"{Kp:.6e}*pow(max(V({p}vddtx)-{vth:.4f},1e-3),{a:g})*V({p}din)*(V({p}vddtx)-V({p}txo))")
    lines.append(f"B{p}pd {p}txo 0 I = "
                 f"{Kn:.6e}*pow(max(V({p}vddtx)-{vth:.4f},1e-3),{a:g})*(1-V({p}din))*V({p}txo)")


def _emit_rx_active(lines, cfg, p):
    """RX: pad C + passive-RC CTLE (source degeneration) + loaded tanh slicer.

    Returns the analog node the eye is measured on ({p}eq if CTLE on, else {p}rxo).
    Decision node = {p}dec.  Channel end {p}n{N} -> rx bump -> {p}rxo (emitted by
    the caller's bump code).
    """
    voff = physics.rx_offset_v(cfg)
    lines.append(f"C{p}rx {p}rxo 0 {cfg.c_rx:.6e}")
    if cfg.r_ctle1 > 0 and cfg.c_ctle > 0:
        lines.append(f"R{p}ct1 {p}rxo {p}eq {cfg.r_ctle1:.6e}")   # series R ...
        lines.append(f"C{p}ct {p}rxo {p}eq {cfg.c_ctle:.6e}")     # ... bypassed by C (HF boost)
        lines.append(f"R{p}ct2 {p}eq vmid {cfg.r_ctle2:.6e}")     # shunt to mid-rail
        eqnode = f"{p}eq"
    else:
        eqnode = f"{p}rxo"
    # SE decision threshold: rail/2 + static/T offset (no common-mode rejection)
    lines.append(f"V{p}rxs {p}vddrx 0 {cfg.vdd:.6e}")
    lines.append(f"B{p}vref {p}vref 0 V = 0.5*V({p}vddrx) + {voff:.6e}")
    # smooth comparator (gain<=15) with a resistive DC load -> good convergence
    lines.append(f"B{p}cmp {p}dec 0 V = 0.4*tanh({cfg.slicer_gain:g}*(V({eqnode})-V({p}vref)))")
    lines.append(f"R{p}dec {p}dec 0 1k")
    return eqnode


# -----------------------------------------------------------------------------
# one transmission line (victim or aggressor)
# -----------------------------------------------------------------------------
def _emit_line(lines, cfg, p, pwl, defect, is_victim, active=False, vrm_scale=1.0):
    """Append the SPICE cards for one lane with node prefix `p`.

    Channel-start node = f"{p}n0", channel-end node = f"{p}n{N}",
    RX-measure node    = f"{p}rxo" (or f"{p}eq" with the active CTLE).
    `active` swaps the ideal driver/RX for the behavioural front-end (victim only).
    Returns the analog RX node the eye should be measured on.
    """
    N = cfg.n_seg
    noisy = cfg.noise_on and is_victim
    # continuous distributed drifts (victim only):
    #   r_drift = TOTAL extra series R [ohm] spread over the ladder (distributed aging)
    #   c_drift = multiplicative shunt-C swell (edge slowing)
    radd = defect["drift_r"] / N if (is_victim and defect["kind"] == "r_drift") else 0.0
    cdrift = 1.0 + defect["drift_c"] if (is_victim and defect["kind"] == "c_drift") else 1.0
    Rseg = cfg.r_per_mm * cfg.len_mm / N + radd
    Lseg = cfg.l_per_mm * cfg.len_mm / N
    Cnode = cfg.c_per_mm * cfg.len_mm / N * cdrift
    Rb, Lb, Cb = cfg.r_bump, cfg.l_bump, cfg.c_bump

    # --- driver ---
    if active and is_victim:
        # 0/1 logic launch on {p}din gates the behavioural push-pull -> {p}txo
        lines.append(f"V{p}drv {p}din 0 {pwl}")
        _emit_tx_active(lines, cfg, p, vrm_scale=vrm_scale)
    else:
        # ideal PWL swing through TEMPERATURE-dependent output resistance Ron(T)
        # (mobility degradation -- the dominant way T closes a matched link's eye)
        lines.append(f"V{p}drv {p}din 0 {pwl}")
        _emit_r(lines, cfg, f"{p}on", f"{p}din", f"{p}txo",
                physics.r_on_temp(cfg), noisy=noisy)

    # --- tx micro-bump (R uses Cu tc1 so temperature scales loss) ---
    lines.append(f"R{p}bt {p}txo {p}bt1 {Rb:.6e} rcu")
    lines.append(f"L{p}bt {p}bt1 {p}n0 {Lb:.6e}")
    lines.append(f"C{p}bt {p}n0 0 {Cb:.6e}")

    # --- RLGC ladder ---
    for k in range(N):
        rseg_k = Rseg
        lseg_k = Lseg
        extra = ""  # per-instance options (e.g. hotspot temperature)

        pos = defect["position"]
        if is_victim and defect["kind"] == "resistive_open" and k == pos:
            rseg_k += defect["r_open"]                       # series R adds delay/loss
        if is_victim and defect["kind"] == "bump_void_aging" and k == pos:
            rseg_k += defect["r_open"]                       # slow drift = growing series R
        if is_victim and defect["kind"] == "impedance_discontinuity" and pos <= k < pos + 3:
            lseg_k *= defect["z_factor"]                     # Z step over a 3-segment span
        if is_victim and defect["kind"] == "hotspot" and pos - 2 <= k <= pos + 2:
            # hot region (5 segments): pinned hot AND locally degraded (void/EM self-heat).
            # local R scales with overheat so the thermal event is eye-detectable.
            extra = f" temp={defect['hot_t']:.3f}"
            rseg_k += max(0.0, (defect["hot_t"] - 90.0) * 2.0) / 5.0

        _emit_r(lines, cfg, f"{p}{k}", f"{p}n{k}", f"{p}m{k}", rseg_k,
                model=f" rcu{extra}", noisy=noisy)
        lines.append(f"L{p}{k} {p}m{k} {p}n{k+1} {lseg_k:.6e}")

    # --- shunt capacitance at every node (half at the two ends) ---
    for k in range(N + 1):
        c = Cnode * (0.5 if (k == 0 or k == N) else 1.0)
        lines.append(f"C{p}c{k} {p}n{k} 0 {c:.6e}")

    # --- rx micro-bump + light termination to mid-rail ---
    lines.append(f"R{p}br {p}n{N} {p}br1 {Rb:.6e} rcu")
    lines.append(f"L{p}br {p}br1 {p}rxo {Lb:.6e}")
    if cfg.r_term and cfg.r_term > 0:
        _emit_r(lines, cfg, f"{p}t", f"{p}rxo", "vmid", cfg.r_term, noisy=noisy)

    # --- RX front-end ---
    if active and is_victim:
        return _emit_rx_active(lines, cfg, p)     # adds pad C + CTLE + tanh slicer
    lines.append(f"C{p}rx {p}rxo 0 {cfg.c_rx:.6e}")
    return f"{p}rxo"


def _emit_coupling(lines, cfg, defect):
    """Cc (and optional mutual K) between victim 'v' and aggressors 'a1','a2'."""
    N = cfg.n_seg
    xfac = defect["xtalk_factor"] if defect["kind"] == "crosstalk_cap" else 1.0
    Ccnode = cfg.cc_per_mm * cfg.len_mm / N * xfac
    aggs = [f"a{i+1}" for i in range(cfg.n_agg)]
    for a in aggs:
        for k in range(N + 1):
            c = Ccnode * (0.5 if (k == 0 or k == N) else 1.0)
            lines.append(f"Cc_{a}_{k} vn{k} {a}n{k} {c:.6e}")
        if cfg.k_couple > 0:
            for k in range(N):
                lines.append(f"Kc_{a}_{k} Lv{k} L{a}{k} {cfg.k_couple:.4f}")


# -----------------------------------------------------------------------------
# top-level builders
# -----------------------------------------------------------------------------
def build_channel(cfg, defect, bits_v, bits_a1, bits_a2,
                  rx_file="rx.dat", agg_file="agg.dat"):
    """Full transient link netlist.

    Legacy (active_frontend=False): ideal PWL driver + RC RX, writes v(vrxo).
    Active (active_frontend=True): behavioural alpha-law TX on a compact PDN +
    CTLE/tanh RX; writes the equalised eye node, plus tx.dat (driver output, for
    rise/fall asymmetry), dec.dat (slicer decision), vdd.dat (PDN rail).
    """
    active = cfg.active_frontend
    swing = 1.0 - cfg.vdroop_benign                  # benign (observable) workload droop
    vrm_scale = 1.0
    if defect["kind"] == "supply_droop":
        if active:
            vrm_scale = 1.0 - defect["droop_frac"]   # physical: lower the PDN rail
        else:
            swing *= 1.0 - defect["droop_frac"]       # fault droop on top of benign droop

    # victim launch: 0/1 logic for the active gate, else a 0..vdd analog swing
    vhi_v = 1.0 if active else cfg.vdd
    pwl_v = _pwl_str(bits_to_pwl(bits_v, cfg.ui, cfg.tr, 0.0, vhi_v, 1.0 if active else swing))
    pwl_a1 = _pwl_str(bits_to_pwl(bits_a1, cfg.ui, cfg.tr, 0.0, cfg.vdd))
    pwl_a2 = _pwl_str(bits_to_pwl(bits_a2, cfg.ui, cfg.tr, 0.0, cfg.vdd))

    L = [f"* D2D interconnect link  | defect={defect['kind']} "
         f"pos={defect.get('position')} temp={cfg.temp_c}C rate={cfg.rate/1e9:g}GT/s "
         f"front-end={'active' if active else 'ideal'}"]
    L.append(f".model rcu r (tc1={cfg.tc1_cu:.4e} tc2=0)")
    L.append(f".temp {cfg.temp_c:.3f}")
    L.append(f"Vmid vmid 0 DC {cfg.vdd/2.0:.6e}")
    if active:
        # with uic + Lpdn the PDN rail must be pre-charged or it never comes up
        vdd0 = cfg.vdd * vrm_scale
        L.append(f".ic v(vvddtx)={vdd0:.6e} v(vvddpre)={vdd0:.6e} v(vvddrx)={cfg.vdd:.6e}")

    eqnode = _emit_line(L, cfg, "v", pwl_v, defect, is_victim=True,
                        active=active, vrm_scale=vrm_scale)
    if cfg.n_agg >= 1:
        _emit_line(L, cfg, "a1", pwl_a1, defect, is_victim=False)
    if cfg.n_agg >= 2:
        _emit_line(L, cfg, "a2", pwl_a2, defect, is_victim=False)
    _emit_coupling(L, cfg, defect)

    if defect["kind"] == "bridge_short":
        pos = defect["position"]
        L.append(f"Rbrg vn{pos} a1n{pos} {defect['r_bridge']:.6e}")

    tstop = (cfg.n_bits + 2) * cfg.ui
    L += [".control", "set noaskquit"]
    if cfg.noise_on:
        L.append(f"set rndseed={int(cfg.noise_seed)}")   # seed the trnoise RNG per draw
    L += [f"tran {cfg.tstep:.3e} {tstop:.6e} uic", "linearize",
          f"wrdata {rx_file} v({eqnode})",
          f"wrdata {agg_file} v(a1rxo)"]
    if active:
        L += ["wrdata tx.dat v(vtxo)",
              "wrdata dec.dat v(vdec)",
              "wrdata vdd.dat v(vvddtx)"]
    L += ["quit", ".endc", ".end"]
    return "\n".join(L) + "\n"


def build_tx_probe(cfg, defect, probe_file="txp.dat"):
    """Isolated single-edge probe of the behavioural TX (no PRBS / no ISI).

    Drives one clean 0->1->0 pulse into a fixed load (tx bump + Z0 to mid-rail,
    approximating the channel input impedance) so the intrinsic pull-up vs
    pull-down edge times -- the stress fingerprint -- can be measured cleanly.
    Returns (netlist, t_rise_start, t_fall_start) window hints.
    """
    ui = cfg.ui
    tr = cfg.tr
    t_hi = 10 * ui            # rising edge
    t_lo = 30 * ui            # falling edge (well separated -> isolated)
    tstop = 40 * ui
    pts = [(0.0, 0.0), (t_hi - tr / 2, 0.0), (t_hi + tr / 2, 1.0),
           (t_lo - tr / 2, 1.0), (t_lo + tr / 2, 0.0), (tstop, 0.0)]
    pwl = _pwl_str(pts)

    vdd0 = cfg.vdd
    if defect["kind"] == "supply_droop":
        vdd0 = cfg.vdd * (1.0 - defect["droop_frac"])

    L = [f"* D2D TX edge probe | temp={cfg.temp_c}C sigma-bridge on drive"]
    L.append(f".model rcu r (tc1={cfg.tc1_cu:.4e} tc2=0)")
    L.append(f".temp {cfg.temp_c:.3f}")
    L.append(f"Vmid vmid 0 DC {cfg.vdd/2.0:.6e}")
    L.append(f".ic v(vvddtx)={vdd0:.6e} v(vvddpre)={vdd0:.6e}")
    L.append(f"Vvdrv vdin 0 {pwl}")
    _emit_tx_active(L, cfg, "v", vrm_scale=(vdd0 / cfg.vdd), with_sso=False)
    # fixed load: tx bump + Z0 resistor to mid-rail + a light cap (channel-like)
    L.append(f"Rvbt vtxo vbt1 {cfg.r_bump:.6e} rcu")
    L.append(f"Lvbt vbt1 vld {cfg.l_bump:.6e}")
    L.append(f"Rvld vld vmid {cfg.z0:.6e}")
    L.append(f"Cvld vld 0 {cfg.c_bump + cfg.c_per_mm*cfg.len_mm/cfg.n_seg:.6e}")

    L += [".control", "set noaskquit",
          f"tran {cfg.tstep/2:.3e} {tstop:.6e} uic", "linearize",
          f"wrdata {probe_file} v(vtxo)",
          "quit", ".endc", ".end"]
    return "\n".join(L) + "\n", t_hi, t_lo


def build_tdr(cfg, defect, tdr_file="tdr.dat"):
    """Source-matched step into the victim channel; record the launch node so
    that reflections from an injected discontinuity appear (SREL/TDR, DEEP_SIM s6.2a).
    RX end is left high-impedance (pad C only)."""
    t0 = 5 * cfg.ui
    pts = [(0.0, 0.0), (t0, 0.0), (t0 + cfg.tr, cfg.vdd)]
    pwl = _pwl_str(pts)

    L = [f"* D2D TDR | defect={defect['kind']} pos={defect.get('position')}"]
    L.append(f".model rcu r (tc1={cfg.tc1_cu:.4e} tc2=0)")
    L.append(f".temp {cfg.temp_c:.3f}")
    L.append(f"Vstep vsrc 0 {pwl}")
    L.append(f"Rsrc vsrc vn0in {cfg.z0:.6e}")     # source matched to Z0
    L.append(f"Cbt vn0 0 {cfg.c_bump:.6e}")
    L.append(f"Rbt vn0in vbt1 {cfg.r_bump:.6e} rcu")
    L.append(f"Lbt vbt1 vn0 {cfg.l_bump:.6e}")

    N = cfg.n_seg
    Rseg = cfg.r_per_mm * cfg.len_mm / N
    Lseg = cfg.l_per_mm * cfg.len_mm / N
    Cnode = cfg.c_per_mm * cfg.len_mm / N
    for k in range(N):
        rseg_k, lseg_k = Rseg, Lseg
        if defect["kind"] in ("resistive_open", "bump_void_aging") and k == defect["position"]:
            rseg_k += defect["r_open"]
        if defect["kind"] == "impedance_discontinuity" and k == defect["position"]:
            lseg_k *= defect["z_factor"]
        L.append(f"Rv{k} vn{k} vm{k} {rseg_k:.6e} rcu")
        L.append(f"Lv{k} vm{k} vn{k+1} {lseg_k:.6e}")
    for k in range(N + 1):
        c = Cnode * (0.5 if (k == 0 or k == N) else 1.0)
        L.append(f"Cc{k} vn{k} 0 {c:.6e}")
    L.append(f"Rbr vn{N} vbr1 {cfg.r_bump:.6e} rcu")
    L.append(f"Lbr vbr1 vrxo {cfg.l_bump:.6e}")
    L.append(f"Crx vrxo 0 {cfg.c_rx:.6e}")

    tstop = t0 + 6 * cfg.td_total + 20 * cfg.ui
    L += [
        ".control", "set noaskquit",
        f"tran {cfg.tstep/2:.3e} {tstop:.6e} uic",
        "linearize",
        f"wrdata {tdr_file} v(vn0in)",
        "quit", ".endc", ".end",
    ]
    return "\n".join(L) + "\n", t0
