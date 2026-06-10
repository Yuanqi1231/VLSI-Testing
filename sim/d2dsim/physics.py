"""Physics layer: latent fields -> first-order device-parameter coefficients.

EM/FEM-free reduced-order maps (see ../MULTIPHYSICS_DESIGN.md). Every coefficient
is a *published* material/device sensitivity; this module turns a Config's latent
fields (temperature, supply droop, mechanical stress, aging) into the numeric
literals that netlist.py inlines into B-sources.  We compute the numbers HERE (in
Python) and emit them as literals because ngspice-46 rejects .param/.func/ternary
inside behavioural (B-source) expressions -- the netlist.py idiom.

Principle:  p(Phi) = p0 * [1 + s * (Phi - Phi0)]   with s from literature.
Reference operating point: T0 = 27 C, Vdd0 = Config.vdd, sigma0 = 0 MPa.
"""
import math

T0_C = 27.0
TKELVIN = 273.15


# -----------------------------------------------------------------------------
# thermal  (T6/T7/T8/T9 in the design note)
# -----------------------------------------------------------------------------
def power_w(cfg):
    """Dynamic power [W] from activity (or an explicit override p_dyn_w).

    P = alpha * C_eff * Vdd^2 * f   (switching) ; leakage left open-loop / ignored.
    """
    if cfg.p_dyn_w > 0:
        return cfg.p_dyn_w
    return cfg.activity * (cfg.c_eff_pf * 1e-12) * cfg.vdd ** 2 * cfg.rate


def t_die_from_power(cfg):
    """Junction temperature [C] = ambient + P*Rth (one-pole thermal ROM, T6).

    The scenario generator uses this to SET cfg.temp_c; the active front-end then
    reads cfg.temp_c as the authoritative die temperature (single source of truth).
    """
    return cfg.ambient_c + power_w(cfg) * cfg.r_th_ja


def mu_temp_factor(cfg):
    """mobility temperature factor  mu(T)/mu(T0) = (T/T0)^-m   (m ~ 1.5)."""
    return ((cfg.temp_c + TKELVIN) / (T0_C + TKELVIN)) ** (-cfg.mu_exp)


def vth_eff(cfg):
    """threshold voltage with linear temperature drift [V]  (dVth/dT ~ -2 mV/C)."""
    return cfg.vth + cfg.dvth_dt * (cfg.temp_c - T0_C)


def r_on_temp(cfg):
    """Driver on-resistance scaled by carrier-mobility degradation [ohm].

    Ron(T) = Ron0 * (T/T0)^mu_exp  (mu ~ T^-m, so Ron ~ T^+m). This is the dominant
    way temperature closes a matched short link's eye: the conductor R is negligible
    against Ron, so without this temperature is NOT observable in the waveform."""
    return cfg.r_on * ((cfg.temp_c + TKELVIN) / (T0_C + TKELVIN)) ** cfg.mu_exp


def r_on_passive(cfg):
    """Driver on-resistance for the PASSIVE front-end: temperature mobility
    degradation x the MEAN piezoresistive drive shift [ohm].

    The single-R driver cannot carry the opposite-sign n/p split (that fingerprint
    needs the active push-pull / the TX edge probe); what survives averaging the
    two devices is mean(dmu/mu) = (pi_p - pi_n)/2 * sigma * sat_derate, i.e.
    tensile stress slightly RAISES net drive (lowers R_on).  ~ -3% at 400 MPa.
    """
    dmu = 0.5 * (cfg.pi_si_p - cfg.pi_si_n) * cfg.sat_derate * sigma_mpa(cfg)
    return r_on_temp(cfg) / (1.0 + dmu)


def metal_stress_scale(cfg):
    """Multiplicative ohmic scale on Cu trace/bump R from stress (Cu gauge
    factor, M1): 1 + pi_metal * sigma.  Second-order (~ +0.7% at 400 MPa)."""
    return 1.0 + cfg.pi_metal * sigma_mpa(cfg)


def r_bump_warp_ohm(cfg):
    """Additive elastic corner-bump contact resistance from package bow [ohm].

    Warpage loads the corner micro-bumps (kappa = 8w/L^2); partially-contacting
    joints under that load show an elastic, REVERSIBLE contact-R increase --
    unlike bump_void_aging's permanent crack growth.  Linear scalar form:
    dR = k * w  (~ 0-3 ohm over w = 0-150 um, below the 5-80 ohm fault range).
    """
    return cfg.k_warp_bump_ohm_um * cfg.warpage_um


# -----------------------------------------------------------------------------
# mechanical / thermomechanical stress  (M0/M1/M3 in the design note)
# -----------------------------------------------------------------------------
def sigma_mpa(cfg):
    """Mechanical stress [MPa] = CTE-mismatch thermomechanical (from temp)
    + package-warpage corner stress + extra.

    sigma_cte  = E/(1-nu) * dAlpha * (T - T_sf)  [Pa] -> /1e6 -> MPa   (M0, no FEM)
    sigma_warp = k_w * w   (M5 scalar form: kappa = 8w/L^2 -> corner stress ~ w)
    plus cfg.stress_mpa (an explicit override / extra term).
    """
    s = cfg.stress_mpa + cfg.k_warp_mpa_um * cfg.warpage_um
    if cfg.stress_from_thermal:
        E = cfg.e_eff_gpa * 1e9
        s += (E / (1.0 - cfg.poisson)) * cfg.cte_mismatch * (cfg.temp_c - cfg.t_stressfree) / 1e6
    return s


# -----------------------------------------------------------------------------
# driver alpha-law conductances  (Stage 1/3/4)
# -----------------------------------------------------------------------------
def drive_conductances(cfg):
    """(Kp, Kn, vth) prefactors for the alpha-law push-pull B-sources.

    g_on(Vrail) = K * (Vrail - vth)^alpha , normalised so g_on = 1/r_on at the
    nominal point (Vdd0, T0, sigma=0).  PMOS gets +piezo, NMOS gets -piezo: the
    OPPOSITE SIGN is the stress fingerprint (separates stress from temperature,
    which scales both equally through mu_temp_factor).
    """
    sig = sigma_mpa(cfg)
    muT = mu_temp_factor(cfg)
    vth = vth_eff(cfg)
    g0 = 1.0 / cfg.r_on
    denom = (cfg.vdd - cfg.vth) ** cfg.alpha_pow          # normalise at nominal
    dmu_p = cfg.pi_si_p * cfg.sat_derate * sig            # PMOS: + with stress
    dmu_n = cfg.pi_si_n * cfg.sat_derate * sig            # NMOS: - with stress
    Kp = g0 * muT * (1.0 + dmu_p) / denom
    Kn = g0 * muT * (1.0 - dmu_n) / denom
    return Kp, Kn, vth


def r_on_eff(cfg, vrail=None):
    """Effective driver on-resistance [ohm] at a given rail (default nominal),
    averaged over the two devices -- a diagnostic, not used in emission."""
    if vrail is None:
        vrail = cfg.vdd
    Kp, Kn, vth = drive_conductances(cfg)
    gp = Kp * (vrail - vth) ** cfg.alpha_pow
    gn = Kn * (vrail - vth) ** cfg.alpha_pow
    return 2.0 / (gp + gn)


# -----------------------------------------------------------------------------
# receiver offset  (T9/V7)
# -----------------------------------------------------------------------------
def rx_offset_v(cfg):
    """Additive RX threshold offset [V] = static offset + temperature drift.

    The netlist adds this to V(vddrx)/2 (the rail-referenced SE decision level).
    """
    return cfg.voff0 + cfg.tcoff * (cfg.temp_c - T0_C)


# -----------------------------------------------------------------------------
# aging  (M4 -- simplified monotone crack fraction; Coffin-Manson sets the shape)
# -----------------------------------------------------------------------------
def r_bump_aged(cfg):
    """Micro-bump series R after aging [ohm]: crack fraction a -> R0/(1-a)."""
    if cfg.aging_hours <= 0:
        return cfg.r_bump
    a = min(0.95, cfg.aging_hours / cfg.bump_t_life_h)
    return cfg.r_bump / (1.0 - a)


# -----------------------------------------------------------------------------
# labels for the dataset (the hidden ground-truth latent fields)
# -----------------------------------------------------------------------------
def pdn_droop_mv(cfg):
    """Static PDN IR-droop estimate [mV] (the dynamic ring is in the simulation)."""
    i_avg = cfg.activity * cfg.i_full_a
    return cfg.r_pdn * i_avg * 1e3


def total_droop_mv(cfg, defect=None):
    """Total latent supply droop [mV] = activity IR droop + supply_droop defect offset.

    Both the activity component and the defect offset reduce the rail through the
    SAME node the driver references, so the label is consistent with the simulated
    observable (vdd_droop_mV).
    """
    d = pdn_droop_mv(cfg)
    if defect is not None and defect.get("kind") == "supply_droop":
        d += defect.get("droop_frac", 0.0) * cfg.vdd * 1e3
    return d


def latent_labels(cfg, defect=None):
    """The hidden ground-truth fields a scenario realises (dataset target columns)."""
    return {
        "field_T_C": round(cfg.temp_c, 3),
        "field_sigma_MPa": round(sigma_mpa(cfg), 3),
        "field_droop_mV": round(total_droop_mv(cfg, defect), 4),
        "field_aging_a": round(min(0.95, cfg.aging_hours / cfg.bump_t_life_h) if cfg.aging_hours > 0 else 0.0, 4),
    }
