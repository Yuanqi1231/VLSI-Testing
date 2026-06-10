"""
Physical and electrical parameters for the pure-ngspice D2D interconnect model.

Every default is sourced from `survey/DEEP_SIM_d2d_interconnect.md` (the verified
simulation-methodology deep-dive) and `Track3_Open_Report_D2D_Link_Health.md`.
Single-ended (SE) convention throughout: Z0 = 50 ohm SE (= 100 ohm differential).

The channel is a lumped RLGC ladder (DEEP_SIM s2/s3): per-unit-length R',L',C'
split into N segments, bracketed by micro-bump R+L+C at each end (DEEP_SIM s1),
with two adjacent aggressor lanes coupled by per-node Cc (and optional mutual K)
for crosstalk (DEEP_SIM s5). Conductor R carries the Cu temperature coefficient
(tc1 = 3.9e-3 /C, DEEP_SIM s7) so temperature closes the eye *without* a defect --
the confounding that motivates multimodal fusion.
"""
from dataclasses import dataclass, field, asdict


@dataclass
class Config:
    # ---- signaling (DEEP_SIM s3/s4: UCIe-class short-reach, low-swing SE) ----
    vdd: float = 0.8           # driver full swing [V] (low-swing D2D)
    rate: float = 16e9         # data rate [GT/s]  -> UI = 62.5 ps (UCIe 16G)
    tr_frac: float = 0.30      # rise/fall time as a fraction of UI
    r_on: float = 45.0         # driver output (source) impedance [ohm], ~Z0 SE

    # ---- channel geometry (DEEP_SIM s1/s2) ----
    len_mm: float = 2.0        # interposer/RDL trace length [mm]
    n_seg: int = 20            # RLGC ladder segments (segment delay << tr)
    z0: float = 50.0           # target SE characteristic impedance [ohm]

    # per-millimetre line parameters (from Z0 + vp ~ 1.1e8 m/s, DEEP_SIM s1):
    #   L' = Z0/vp = 0.45 nH/mm ; C' = 1/(Z0*vp) = 0.18 pF/mm
    #   R' ~ 0.35 ohm/mm (RDL/interposer Cu, DC-ish; scaled by temperature)
    r_per_mm: float = 0.35     # series resistance [ohm/mm]
    l_per_mm: float = 0.45e-9  # series inductance [H/mm]
    c_per_mm: float = 0.18e-12 # shunt capacitance [F/mm]
    cc_per_mm: float = 0.030e-12  # victim<->aggressor coupling cap [F/mm] (DEEP_SIM s5)
    k_couple: float = 0.0      # inter-lane mutual inductance k (0 = cap-dominated)

    # ---- micro-bump terminals (DEEP_SIM s1 table) ----
    r_bump: float = 0.040      # 40 mOhm
    l_bump: float = 30e-12     # ~30 pH
    c_bump: float = 12e-15     # 12 fF (micro-bump 5-20 fF)

    # ---- receiver (DEEP_SIM s1) ----
    c_rx: float = 30e-15       # RX pad capacitance [F]
    r_term: float = 80.0       # light SE termination to mid-rail [ohm]; 0 = none

    # ---- temperature (DEEP_SIM s7) ----
    temp_c: float = 27.0       # global die temperature [C]
    tc1_cu: float = 3.9e-3     # Cu temperature coefficient of resistance [/C]

    # ---- benign supply droop (OBSERVABLE confounder, not a fault) ----
    # Workload-induced IR droop reported by the on-die supply monitor. It reduces
    # the launched swing (closes the eye, like attenuation faults) but is benign and
    # *observable* -- the telemetry channel a fusion model uses to reject false
    # alarms. Distinct from the supply_droop FAULT (an unexplained, larger droop).
    vdroop_benign: float = 0.0  # fractional benign swing reduction in [0,~0.1]

    # ---- aggressors / crosstalk (DEEP_SIM s5) ----
    n_agg: int = 2             # adjacent aggressor lanes (above/below)

    # ---- stimulus ----
    n_bits: int = 200          # PRBS bits per run
    prbs_order: int = 7        # PRBS7 (x^7+x^6+1)
    seed_v: int = 0b1011011    # victim LFSR seed
    seed_a1: int = 0b1110101   # aggressor-1 seed (decorrelated)
    seed_a2: int = 0b0101101   # aggressor-2 seed

    # ---- simulator timing ----
    tstep: float = 1e-12       # transient/linearize step [s] (~UI/62)
    settle_bits: int = 8       # leading bits ignored while the channel fills

    # ---- transient noise (resistor thermal EMF, time-domain trnoise) ----
    # A trnoise voltage source is placed in series with each victim resistor with
    # white RMS = noise_gain * sqrt(4 k T R / (2*tstep)).  The sqrt(4kTR) is the
    # physical Johnson-Nyquist thermal EMF; noise_gain (>1) lumps in the RX
    # amplifier + supply noise that dominate a real link, lifting the eye noise to
    # a realistic mV scale.  Because NA ~ sqrt(T), temperature raises the noise on
    # EVERY resistor (a hot but healthy link gets noisy -> the physical confounder);
    # because NA ~ sqrt(R), a resistive_open / r_drift fault makes its own segment
    # noisier (a localized noise signature).  noise_on=False -> byte-identical to
    # the legacy noiseless path.
    noise_on: bool = False
    noise_gain: float = 30.0       # lumped scale over pure conductor thermal noise
    noise_seed: int = 1            # ngspice rndseed for the trnoise RNG (per draw)

    # =====================================================================
    # ACTIVE FRONT-END (behavioural TX/RX + multiphysics fields)
    # see ../MULTIPHYSICS_DESIGN.md ; coefficients computed in physics.py and
    # inlined as numeric literals (ngspice-46 rejects .param/.func inside B).
    # =====================================================================
    active_frontend: bool = False  # False = legacy ideal PWL+RC ; True = behavioural

    # ---- latent physical fields (per-run scenario knobs) ----
    ambient_c: float = 27.0        # ambient temperature T_a [C]
    activity: float = 0.3          # switching activity alpha in [0,1] -> power
    aging_hours: float = 0.0       # field-time H [h] -> Coffin-Manson crack fraction
    warpage_um: float = 0.0        # package bow w [um] (spatial op, v2)
    stress_mpa: float = 0.0        # EXTRA mechanical stress on top of thermal [MPa]
    stress_from_thermal: bool = True  # derive CTE-mismatch stress from temp_c (M0)

    # ---- thermal ROM (T6/T7) ----
    r_th_ja: float = 0.3           # junction-ambient thermal resistance [C/W]
    c_th: float = 1e-3             # thermal capacitance -> tau=R_th*C_th [J/C]
    p_dyn_w: float = 0.0           # explicit power injection [W] (else from activity)
    c_eff_pf: float = 2.0          # effective switched capacitance [pF] for power
    i_full_a: float = 0.5          # full-activity supply current [A]

    # ---- CTE / thermomechanical stress bridge (M0) ----
    cte_mismatch: float = 14.5e-6  # delta-alpha Cu-Si [/C]
    e_eff_gpa: float = 120.0       # effective Young's modulus [GPa]
    poisson: float = 0.30
    # operating stress reference [C]: incremental thermomechanical stress relative
    # to this temperature (so healthy@T0 is stress-neutral; the constant assembly/
    # reflow residual ~ -340 MPa is a separable DC offset, not detection-relevant).
    # Set to 220.0 to model the absolute reflow residual instead.
    t_stressfree: float = 27.0

    # ---- driver alpha-law + mobility/Vth (Stage 1/3) ----
    vth: float = 0.32              # device threshold [V]
    alpha_pow: float = 1.3         # Sakurai velocity-saturation exponent
    mu_exp: float = 1.5            # mobility temperature exponent mu ~ T^-m
    dvth_dt: float = -2.0e-3       # dVth/dT [V/C]
    c_int: float = 200e-15         # driver slew capacitance [F] -> tr ~ 2.2*Ron*Cint

    # ---- piezoresistive coefficients (M1/M3, Smith/Kanda; per MPa) ----
    pi_si_p: float = 7.18e-4       # p-Si |piL<110>| -> drive [/MPa]
    pi_si_n: float = 3.16e-4       # n-Si |piL<110>| -> drive [/MPa] (OPPOSITE sign)
    pi_metal: float = 1.7e-5       # Cu gauge-factor/E [/MPa] (2nd order)
    sat_derate: float = 0.4        # saturation-region derating (0.3-0.5 physical);
                                   # set 1.0 for the un-derated triode-region split

    # ---- fatigue (M4, Coffin-Manson SAC) ----
    bump_t_life_h: float = 2000.0  # field-time to crack knee [h]

    # ---- compact PDN (V1-V3) ----
    r_pdn: float = 0.02            # PDN series resistance [ohm]
    l_pdn: float = 100e-12         # PDN series inductance [H]
    c_decap: float = 50e-9         # decoupling capacitance [F] -> f_res ~ 71 MHz

    # ---- RX front-end (Stage 2) ----
    r_ctle1: float = 400.0         # CTLE degeneration R [ohm] (0 = bypass CTLE)
    c_ctle: float = 160e-15        # CTLE degeneration C [F]
    r_ctle2: float = 1000.0        # CTLE shunt R to mid-rail [ohm]
    slicer_gain: float = 10.0      # tanh slicer gain (<=15 for convergence)
    voff0: float = 0.0             # static RX input offset [V]
    tcoff: float = 30e-6           # RX offset temperature drift [V/C]
    psij_ps_per_mv: float = 0.05   # supply-induced jitter sensitivity [ps/mV]

    # ---- derived ----
    @property
    def ui(self) -> float:
        return 1.0 / self.rate

    @property
    def tr(self) -> float:
        return self.tr_frac * self.ui

    @property
    def vp(self) -> float:
        """Phase velocity implied by L',C' [m/s]."""
        return 1.0 / (self.l_per_mm * self.c_per_mm) ** 0.5 * 1e-3

    @property
    def td_total(self) -> float:
        """One-way channel delay of the ladder [s] (excl. bumps)."""
        lseg = self.l_per_mm * self.len_mm / self.n_seg
        cseg = self.c_per_mm * self.len_mm / self.n_seg
        return self.n_seg * (lseg * cseg) ** 0.5

    def to_dict(self):
        return asdict(self)


# Defect kinds the model can inject (DEEP_SIM s6.1 taxonomy). Each maps to a
# concrete netlist perturbation in netlist.py.
DEFECT_KINDS = (
    "healthy",
    "resistive_open",        # series R at a ladder segment (weak -> hard)
    "bridge_short",          # shunt R victim<->aggressor (0..~kohm)
    "crosstalk_cap",         # increased coupling capacitance
    "bump_void_aging",       # slow series-R drift (EM/void, DEEP_SIM s8)
    "supply_droop",          # reduced/ramped driver swing (PDN droop)
    "hotspot",               # local elevated temperature on one segment
    "impedance_discontinuity",  # Z step (scaled L or C) at a segment
    "r_drift",               # distributed series-R aging (continuous severity)
    "c_drift",               # distributed shunt-C drift (continuous severity)
)
