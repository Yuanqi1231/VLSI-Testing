# Multiphysics TX/RX + Field→Netlist Parametrization — Design Note

Answers two design questions for the D2D link anomaly simulator:

- **Q1.** Should the TX driver and RX receiver be modelled with **analog/active** components
  (vs the current ideal PWL source + RC), and at what fidelity?
- **Q2.** How do we map the **physical fields** (temperature, supply droop, mechanical/
  thermomechanical stress, crosstalk) to **device/netlist parameters** using only published
  literature coefficients — **no EM/FEM field solving**?

Every SPICE card below was **verified to run in this project's ngspice-46** (Homebrew, batch
`-b`) following the existing `netlist.py` idiom (numerics inlined by the Python layer — *not*
`.param`/`.func` inside behavioural sources, which this ngspice rejects; see §C). The headline
novelty claim (a stress field is identifiable against a thermal confounder via NMOS/PMOS edge
asymmetry) is demonstrated in §D.

---

## TL;DR

- **Q1 — Yes, go *behavioural-macromodel* TX/RX (B-sources + RC), not transistor/PDK, not ideal.**
  The reason is not realism for its own sake: the multiphysics confounding the detector must
  *disentangle only physically exists if several fields drive one shared knob* — the driver
  on-resistance `R_on(Vdd, T, σ)`. An ideal source + thresholdless RC has no shared knob, so
  "attribution" on that dataset is an artefact of how labels were injected, not physics. Ship the
  **minimal** active model (§A.3): an α-law push-pull whose swing rides a real PDN node, with
  opposite-sign n/p stress on drive, and a passive-RC CTLE + a low-gain loaded `tanh` slicer.
  Drop LAPLACE/FFE/DFE/clock-recovery for v1.

- **Q2 — Posit the field, multiply a netlist element by a published first-order sensitivity
  coefficient.** Same reduced-order spirit as getting RLGC from `Z0+vp` instead of an EM solve.
  Temperature → TCR / μ(T) / Vth(T); droop → a compact PDN RLC the driver references; **mechanical
  stress (the missing axis) is *bridged from the thermal field with zero FEM* via CTE-mismatch
  (`σ ≈ E·Δα·ΔT ≈ 1.5–2.5 MPa/°C`)**, then turned into electricals by the Smith/Kanda
  piezoresistive tensor and Coffin-Manson fatigue. A single coupling DAG (§B.3) drives everything
  from one latent scenario `(activity, T_ambient, aging_hours, warpage)`.

- **The experiment that matters more than any extra knob:** prove **identifiability** — train the
  detector on the fused channels, show it recovers the latent `{T, σ, droop}` labels on held-out
  runs, and show it *fails* when a tie-breaker channel is withheld (§D). Without this, an
  over-parameterised dataset is unfalsifiable.

---

# Part A — Q1: TX/RX fidelity

## A.1 Decision

| Option | Verdict | Why |
|---|---|---|
| Keep ideal PWL + linear `R_on` + RC | ✗ | No shared knob ⇒ multiphysics confounding **absent by construction**; only good for single-physics class separation. |
| **Behavioural macromodel (B-sources + RC)** | ✓ **Ship this** | Minimum fidelity at which `R_on(Vdd,T,σ)` couples Vdd/T/σ into one observable; maximum fidelity the detector consumes; pure ngspice, no PDK, reproducible. |
| Generic transistor model card | ✗ | Adds nonlinear I-V curvature the detector never sees; you must still invent W/L/Vth/μ; worse convergence; no fidelity gain over a B-source carrying the same published α/μ/Vth. |
| Full PDK | ✗ | Foundry NDA, non-reproducible, worst convergence; disallowed and unnecessary. |

## A.2 Why the ideal source + RC is insufficient (the attribution-bearing physics)

These couplings are **impossible** without an active TX/RX, and they are exactly the ones that
make different physical causes collapse onto the same link observable:

| # | Field → device parameter | Why the ideal model can't produce it | Magnitude (literature) |
|---|---|---|---|
| 1 | **PDN droop → R_on → swing *and* slew → data-dependent jitter** | Fixed `R_on` can't move with the rail; ideal source pins swing; constant edge ⇒ zero supply jitter | swing rides rail ~1 V/V; `R_on∝1/(Vdd−Vth)` ⇒ +11 % for 50 mV droop; α-law (α≈1.3) ⇒ +10–11 % t_pd for 10 % droop |
| 2 | **Temperature → μ, Vth → drive throttling** | Ideal source has no μ/Vth/overdrive | μ∝T⁻¹·⁵ ⇒ 25→125 °C drops drive 20–40 %; dVth/dT≈−2 mV/°C |
| 3 | **Mechanical stress → μ → drive (the missing axis)** | An ideal source has no mobility to perturb ⇒ stress is *unobservable* | Si piezo p≈+0.72 %/MPa, n≈−0.31 %/MPa; **opposite n/p sign is the unique stress fingerprint** |
| 4 | **RX offset Voff(T,Vdd) + threshold drift** | Thresholdless RC has no decision to bias | σ(Voff) 5–20 mV; TCoff tens of µV/°C |
| 5 | **RX input-referred noise → graded BER** | Hard RC gives BER∈{0,1}; no continuous label | 0.5–3 mV rms; BER=½·erfc((h/2−Voff)/(√2·v_n)) |
| 6 | **Catastrophic short = resistive divider; weak open = slow-to-rise** | These are dividers against `R_on` + the RX threshold — they don't exist with an ideal source | UCIe/FOWLP-BIST: short gates 200/500/600 Ω, open C<10 fF |

**Items 1, 2, 3 all act on the single knob `R_on(Vdd,T,σ)`.** That is what makes a droop event, a
hotspot event, and a stress event produce *overlapping* eye-width/height signatures — the very
confounding the thesis claims. In the ideal model these are three independent injected channels, so
the confounding is absent and attribution is ill-posed. (The corpus's joint Vdd–Temperature sensor
paper is silicon proof of exactly this degeneracy: one delay reading *cannot* separate T from Vdd.)

**Keep the passive machinery as-is** (do not rebuild): RLGC ladder, micro-bump R+L+C, impedance
discontinuities, Cc/K crosstalk, Cu-TCR on R, TDR/SREL — reflection Γ=(Zl−Z0)/(Zl+Z0) is set by
channel/termination impedance, not transistor nonlinearity. **The upgrade is surgical: replace only
the two endpoints.**

## A.3 Minimal active TX/RX — verified ngspice-46 cards

> Emitted by the Python layer with **all coefficients inlined as numeric literals** (the values
> shown are for the nominal operating point T=27 °C, σ=0, Vdd₀=0.8 V). `.param`/`.func`/ternaries
> inside `B…` expressions do **not** work here — see §C. Conductances are computed in Python:
>
> ```
> RON0=45 ; VDD0=0.8 ; VTH=0.32 ; ALPHA=1.3
> g0   = 1/RON0                                   # nominal drive conductance [S]
> muT  = ((T_die+273.15)/300)**(-1.5)             # mobility temp factor  (T8)
> Kp   = g0*muT*(1 + 7.18e-4*sigma_MPa)/(VDD0-VTH)**ALPHA    # PMOS: +stress  (M3)
> Kn   = g0*muT*(1 - 3.16e-4*sigma_MPa)/(VDD0-VTH)**ALPHA    # NMOS: -stress (opposite sign!)
> ```
> The opposite sign on `Kp` vs `Kn` is baked in at emit time — **two sign-fixed B-sources, never a
> runtime `?:`** (which breaks the operating point in this build, §C).

```spice
*==================== TX: alpha-law push-pull on a real PDN ====================
* compact PDN: droop is generated by the driver load, not hand-set
Vvrm    vrm 0 0.8
Rpdn    vrm vddpre 0.02            ; R_pdn 5-80 mOhm   (V1,V2)
Lpdn    vddpre vddtx 100p          ; L_pdn 20-500 pH  -> f_res ~ 71 MHz with Cdec (V3)
Cdec    vddtx 0 50n                ; decap 10-200 nF; size with Lpdn for tens-100s MHz f_res
*  NOTE: with `uic` + Lpdn, you MUST set .ic v(vddtx)=0.8 or the rail never charges (see §C).

* launch logic 'd' in {0,1}: the PRBS, as a finite-edge PWL (reuse bits_to_pwl)
*   Vd d 0 PWL(... your pattern ...)

* internal slewed node: edge time tr ~ 2.2*Ron*Cint ; Cint=200f -> ~20 ps (~UI/3)
Cint    vint 0 200f
Bpu     vint 0 I = 5.884e-2*pow(V(vddtx)-0.32,1.3)*V(d)*(V(vint)-V(vddtx))   ; pull-up (PMOS, +stress in Kp)
Bpd     vint 0 I = 5.884e-2*pow(V(vddtx)-0.32,1.3)*(1-V(d))*V(vint)          ; pull-down (NMOS, -stress in Kn)
*  HIGH equilibrium = V(vddtx) (swing RIDES the rail -> droop = real eye-height loss);
*  edge rate = f(V(vddtx),T,sigma) (droop/heat/stress -> slew -> data-dependent jitter).
Rlaunch vint pad 1m                ; 'pad' feeds the EXISTING micro-bump + RLGC ladder (unchanged)

*==================== RX: passive-RC CTLE + loaded tanh slicer =================
Vrxsup  vddrx 0 0.8                ; RX rail (own PDN optional)
* one-zero/one-pole CTLE as a source-degeneration RC (a real CTLE IS this) — no LAPLACE
Rctle1  rxpad rxeq 200
Cctle   rxpad rxeq 80f
Rctle2  rxeq 0 1k
* SE threshold tracks rail/2 (no CMRR) + offset(T,Vdd) baked in Python as VOFF_T
Bvref   vref 0 V = 0.5*V(vddrx)            ; + VOFF_T term if modelling offset drift (T9,V7)
* smooth slicer: gain <= ~15 and a resistive DC load on 'dec', else OP/timestep fails (§C)
Bcmp    dec 0 V = 0.4*tanh(10*(V(rxeq)-V(vref)))
Rdec    dec 0 1k
*  Decision/eye/BER/jitter are extracted in Python by folding v(dec)/v(rxeq) at bit centres
*  (exactly as measure.py already does) -> NO in-SPICE clock/latch/DFE needed for v1.
```

Verified behaviour (this deck, ngspice-46, rc=0): `pad` swings 0→0.66 V (HIGH rides the rail,
divided by the channel load), `dec` toggles ±0.4 tracking the data, rail held at 0.8 V.

## A.4 Staged roadmap & what to cut

| Stage | Add | Detector benefit | Convergence |
|---|---|---|---|
| **0 (now)** | ideal PWL + R_on + C_rx | single-physics separation only | trivial |
| **1** ★ | α-law TX swing on a real PDN node | droop closes eye via R_on **and** slew, self-couples (SSO) — *first real shared-knob* | trivial (smooth B) |
| **2** ★ | passive-RC CTLE + loaded `tanh` slicer | BER∈{0,1} → **graded BER + bathtub + timing margin** | easy (gain ≤15, load `dec`) |
| **3** ★ | μ(T), Vth(T) in the drive; RX Voff(T) | the **T↔Vdd degeneracy** (both raise R_on/shift threshold) | trivial (Python-baked) |
| **4** ★ | stress on drive (opposite n/p sign); `sigma` node | **completes the thesis** — the n/p fingerprint that separates stress from thermal | trivial |
| 5 | TX FFE / RX DFE / CTLE-peaking drift; clocked S&H | EQ-state robustness (realism hardening, *not* contribution) | **liability** — needs T-element delays, loop-breaking |

★ = the **minimal contribution-bearing set** for a 4-week project. **Cut for v1:** LAPLACE/`s_xfer`
CTLE, FFE, DFE, clock-recovery, leakage self-heating feedback loop, warpage spatial operator +
lane-adjacency map (needs a multi-lane array you don't have), full Coffin-Manson Nf (use a monotone
R-ramp, cite Coffin-Manson for its *shape*), multi-τ thermal Foster ladder (one pole is plenty at
10–30 µs telemetry cadence). Stay inside core ngspice (R/L/C/V/B/T-element) for cross-machine
reproducibility — XSPICE `s_xfer` is compiled here but flaky (timestep-too-small).

---

# Part B — Q2: physical field → netlist parameter, EM/FEM-free

## B.1 Principle

> **Latent field Φ → published first-order sensitivity coefficient s → netlist perturbation
> Δp = s·(Φ−Φ₀)·p₀ → ngspice card.**

This is the same reduced-order trick already used for the channel: there, a full 3-D Maxwell
extraction was replaced by two macroscopic numbers `(Z0, vp)` and telegrapher identities
`L'=Z0/vp`, `C'=1/(Z0·vp)`. Here a multiphysics FEM field-solve is replaced by (a) a macroscopic
field value and (b) a tabulated *material/device* sensitivity (TCR, piezoresistive π, ∂Vth/∂T, …).
The element becomes a first-order Taylor expansion about a reference point:
`p(Φ) = p₀·[1 + Σ_k s_k·(Φ_k−Φ_{k,0})]` (+ optional 2nd-order term). In ngspice this is *literally*
`.model R(tc1=… tc2=…)` for resistors, and a one-line `B`-source everywhere else.

**Legitimate because:** host elements are already lumped/linear; the coefficients are *intensive
material constants* tabulated independently of layout (so they transport without re-solving fields);
the map's *outputs* are validated by the corpus (Ma et al.'s electro-thermal co-sim raises IR drop
+27 % / +12 mV for a ~5 °C rise — the deltas a correct first-order coupling must reproduce); and it
matches the detector's observation granularity (aggregated scalar telemetry sampled every ~10–30 µs,
not raw transistor waveforms).

**Where it breaks (honest boundaries):** large excursions (ΔT>100 °C needs the `tc2` term);
exponential fields (leakage doubles per ~10 °C — use the native `exp`, not a Taylor); mechanism
saturation (stress→drive is >10 % in triode but collapses in saturation — derate 0.3–0.5×);
many-to-one non-identifiability (the *point* — §B.4); coupled fields (stress is *derived from* T, can't
be swept independently — §B.3); spatial structure (warpage is a 2-D field — needs a distribution
operator, cut for v1).

## B.2 Master table (load-bearing rows; coefficients literature-cited)

Reference point T₀=27 °C, Vdd₀=0.8 V, σ₀=0 MPa, stress-free T_sf≈220 °C. Latent **nodes**: `tdie`
(1 V = 1 °C), `sigma` (**1 V = 1 MPa** — fixed convention; bake the Pa↔MPa ×1e6 into each coefficient
in Python), `vddtx` (PDN node). Drive `tdie`/`sigma` from a **stiff V/PWL source**, never a high-Z
"info" node (§C M2).

### Thermal

| Field | Mechanism | Param | Formula | Coefficient | ngspice | Conf |
|---|---|---|---|---|---|---|
| T of Cu | Cu TCR | `r_per_mm`, `r_bump` | R(T)=R₀[1+α·ΔT+β·ΔT²] | α=3.9e-3/°C, β≈6e-7/°C² | `.model RCU R(tc1=3.9e-3 tc2=6e-7)` | high |
| T of W TSV | W TCR | TSV R | R(T)=R₀[1+α_W·ΔT] | α_W=4.5e-3/°C | `.model RW R(tc1=4.5e-3)` | high |
| T of SnAg bump | solder TCR | `r_bump` | R(T)=R₀[1+α_sol·ΔT] | α_sol≈4.5e-3/°C | `.model RBUMP R(tc1=4.5e-3)` | med |
| T of dielectric | TCDk → C → Z0,t_pd | `c_per_mm` | C(T)=C₀[1+TCDk·ΔT] | TCDk ≈ +22e-6/°C (low-loss); ±100–200e-6 FR4 | `.model CD C(tc1=22e-6)` | med |
| T of dielectric | TCDf → tanδ → loss | new shunt G | tanδ(T)=tanδ₀[1+TCDf·ΔT]; G=2πfC·tanδ | tanδ↑ tens of % /100 °C | `Gn n 0 g={…}` (numeric) | med |
| **power P → T** | thermal ROM | `temp_c` / `temp=` | T_j=T_a+P·R_th | R_th 0.15–0.5 °C/W sinked … 5–30 passive | `Bp tdie 0 I={P}` `Rth tdie tamb 0.3` | high |
| P(t) → T(t) | thermal RC lag | `Cth` on `tdie` | C_th·Ṫ=P−(T−T_a)/R_th | τ=R_th·C_th ~ 1 ms (die) | add `Cth tdie 0 {τ/Rth}` | med |
| **T → mobility** | μ∝T⁻ᵐ → R_on↑ slew↓ | drive `Kp/Kn` | g_on(T)=g₀(T/T₀)⁻ᵐ | m≈1.5 (acoustic phonon) | baked in `Kp/Kn` (A.3) | high |
| T → Vth | Vth↓ → overdrive, RX thr | drive / RX `Vref` | Vth(T)=Vth₀+(∂Vth/∂T)·ΔT | ∂Vth/∂T=−2.0 mV/°C | baked in `Vref`/overdrive | high |
| T → leakage | near-exponential | load on `vddtx` | I_off=I₀·2^(ΔT/10) | doubling /8–10 °C (d ln I/dT≈0.069) | `Bleak vddtx 0 I={…}` (open-loop) | med |

### Voltage / PDN

| Field | Mechanism | Param | Formula | Coefficient | ngspice | Conf |
|---|---|---|---|---|---|---|
| Vdd(t) | compact PDN replaces stiff rail | new `vddtx` RLC | v=V_nom−R·i−L·di/dt; f_res=1/(2π√LC) | Z_tgt=Vdd·ripple%/I_max; 0.8 V/5 %/0.5 A→80 mΩ | `Rpdn/Lpdn/Cdec` (A.3) | high |
| static IR | ohmic DC drop | `R_pdn` | ΔV=R_pdn·I_avg | ≤~10 mV well-designed | DC term of load | high |
| dynamic Ldi/dt | first-droop ring at f_res | `L_pdn`,`C_dec` | ΔV≈L·di/dt; resonant ≈√(L/C)·I_step | budget 5–10 % Vdd | `Istep vddtx 0 PULSE(…)` | high |
| droop → swing | SE HIGH rides rail | TX swing tied to V(vddtx) | V_hi=V(vddtx)·divider; dV_sw/dVdd≈1 | ~1 V/V | `Bpu/Bpd` use V(vddtx) (A.3) | high |
| droop → R_on | overdrive sets R_on | drive `Kp/Kn` | R_on∝1/(Vdd−Vth) | +11 % per 50 mV (overdrive 0.5 V) | `pow(V(vddtx)-0.32,1.3)` (A.3) | high |
| droop → delay/jitter | Sakurai α-law | TX edge | t_pd=K·C_L·Vdd/(Vdd−Vth)^α | α≈1.3 | emerges from `Kp/Kn` + Cint | high |
| RX droop → Voff | SE slicer vs Vdd/2, no CMRR | RX `Vref` | V_ref=V(vddrx)/2 | 0.5–1.0 V/V (SE); <0.03 differential | `Bvref vref 0 V=0.5*V(vddrx)` | med |
| supply noise → PSIJ | ripple modulates edge | clock/edge | T_jit=S·ΔV | **S=0.05 ps/mV** (0.01–0.1; *not* 2!) | modulate sample instant in Python | high |

### Mechanical / thermomechanical stress (the missing axis — fully built)

| Field | Mechanism | Param | Formula | Coefficient | ngspice | Conf |
|---|---|---|---|---|---|---|
| **T → σ (the bridge — no FEM)** | CTE-mismatch | drives `sigma` node | σ=E/(1−ν)·Δα·(T−T_sf) | Δα: Si 2.5, Cu 17, SAC 22, EMC 8–10, glass 3.3 ppm/°C; E_Cu 120 GPa, ν 0.3 → **≈1.5–2.5 MPa/°C** | `Bsig sigma 0 V=2.6*(V(tdie)-25)` (MPa) | high |
| σ in Si | Si piezoresistance | Si R / channel μ | ΔR/R=π_L·σ_L+π_T·σ_T | (100)⟨110⟩: p-Si π_L=+71.8, n-Si π_L=−31.2 (×1e-11/Pa) → **p-Si ≈ 0.72 %/MPa** | baked: `1/(R0*(1+7.18e-4*sig_MPa))` | high |
| σ in Cu | metal gauge factor | `r_per_mm`,`r_bump` | ΔR/R=GF·σ/E | GF≈2 → ≈1.7e-5/MPa (~1000× < Si; ≤ TCR, 2nd-order) | `R={R0*(1+1.7e-5*sig_MPa)}` | high |
| **σ → drive (KOZ μ)** | strained-Si Δμ | TX `Kp/Kn` | Δμ/μ=−π_eff·σ, **opposite n/p sign** | pMOS≈0.07–0.1 %/MPa, nMOS≈0.03–0.036 %/MPa; **derate 0.3–0.5× in saturation** | `Kp`:(1+7.18e-4σ), `Kn`:(1−3.16e-4σ) | med |
| cyclic σ → R_bump(t) | Coffin-Manson fatigue | `r_bump` over field-time | N_f=C·Δε_p^(1/c); a(N)=N/N_f; R(N)=R₀/(1−a) | c=−0.5…−0.7; ε_f'≈0.30; crack→R +20 mΩ@20 %, +200 mΩ near open | `R={R0/(1-a)}`, a from Python ramp | med |
| warpage w → σ_corner | global CTE bow (spatial) | per-bump σ (corner>centre) | κ=8w/L²; σ_corner=E_sol·k_w·w | w 30–200 µm → corner 45–450 MPa | **cut for v1** (needs array) | med |

### Crosstalk / activity

| Field | Mechanism | Param | Coefficient | ngspice |
|---|---|---|---|---|
| aggressor activity | capacitive (+ inductive) coupling | `cc_per_mm`,`k_couple`,`n_agg` | RDL coupling ≈0.092 fF/µm; hex 12 / rect 8 aggressors | `Cc{i} vic agg{j} {…}` (have it) |
| loss/ISI | shared-substrate tanδ→G | shunt G per cell | tanδ 0.002–0.02 | `Gn n 0 g={…}` |
| Z discontinuity | local Z step → reflection | `z_factor` on seg L/C | Γ=(Zl−Z0)/(Zl+Z0); **DC-R a poor proxy** | scale `l_per_mm`/`c_per_mm` (have it) |

## B.3 Coupling DAG — one scenario drives everything coherently

```
   LATENT SCENARIO:  activity α(t)   ambient T_a   aging hours H   warpage w
        │                 │              │              │
        ▼                 │              │              │
   P = α·C·Vdd²·f + I_off(T)·Vdd         │              │      (power; leakage = optional open-loop)
        │  (R_th, τ)       │              │              │
        ▼                 ▼              │              │
   T_die = T_a + P·R_th  (RC lag τ=R_th·C_th)           │
        │                                │              │
        ├──► R(T),G(T),C(T) of channel   │              │      (T1–T5: eye/loss/Z0 drift)
        │                                │              │
        ▼  (M0: CTE bridge — heat MAKES stress)         │
   σ = E/(1−ν)·Δα·(T_die − T_sf)  ≈ 2.6 MPa/°C          │
        │                                │              │
        ├──► ΔR/R = π·σ  on Si & Cu R    │              │      (M1,M2)
        └──► Δμ/μ = −π_eff·σ  on drive (opposite n/p)   │      (M3: the stress fingerprint)
                              │                          │
   i_load(t)=α·toggling ─► PDN: Vdd(t)=V_nom−R_pdn·i−L·di/dt (ring @ f_res)   (V1–V3)
                              └──► swing↓, R_on↑, t_pd↑, PSIJ, RX Vref offset  (V4–V8)
        │
   H ─► a(H)=H/t_life ─► R_bump(H)=R_bump0/(1−a)  (knee→open)                  (M4)
   w ─► σ_corner > σ_centre ─► selects which bump fatigues/opens first         (M5, v2)
```

Evaluate top-to-bottom per run. **The key structural insight (from CHIPSIM's three-domain
decomposition and Ma et al.'s self-consistent loop): one scalar — local power — drives the entire
cascade.** Everything downstream is a deterministic function of `{P(t), T_a, H, w, geometry}`, so a
single latent scenario produces a *physically self-consistent* multimodal row.

## B.4 Scenario generator + new `Config` fields

```python
def realize(scenario) -> (Config-overrides, defect-dict, ground-truth-labels):
    P       = alpha*Ceff*vdd**2*rate + Ioff0*exp(0.0693*(T_a-25))*vdd   # leakage open-loop
    T_die   = T_a + P*r_th_ja                                            # thermal ROM (one pole)
    sigma   = (e_eff_gpa*1e9/(1-poisson))*cte_mismatch*(T_die-t_stressfree)/1e6  # -> MPa  (M0)
    Nf      = cm_C*(cte_mismatch*dT_cycle)**(1/cm_c)
    a       = min(0.95, (aging_hours/hours_per_cycle)/Nf)               # crack fraction (M4)
    r_bump_H= r_bump0/(1-a)
    Vdroop  = r_pdn*alpha*i_full + l_pdn*di_dt_peak                     # static + first-droop
    # Python bakes Kp,Kn,muT,Vth(T),Vref(T,Vdd) numeric literals into the netlist (A.3)
    return overrides(temp_c=T_die, r_bump=r_bump_H, ...),
           labels(field_T_C=T_die, field_sigma_MPa=sigma, field_droop_mV=Vdroop, field_crack_a=a)
```

**Reuse as-is:** `temp_c`, `r_bump`, `cc_per_mm`/`k_couple`/`n_agg`, `r_per_mm`, `tc1_cu`.
**New `Config` fields** (all literature-cited defaults, no PDK):

```python
# latent fields (per-run scenario knobs)
ambient_c=27.0; activity=0.3; aging_hours=0.0; warpage_um=0.0; stress_mpa=0.0  # MPa override
# thermal ROM
r_th_ja=0.3; c_th=1e-3; p_dyn_w=0.0
# CTE / stress bridge (M0)
cte_mismatch=14.5e-6; e_eff_gpa=120.0; poisson=0.30; t_stressfree=220.0
# piezoresistive (M1/M3, Smith/Kanda) — units 1/MPa after ×1e6
pi_si_p=7.18e-4; pi_si_n=3.16e-4; pi_metal=1.7e-5; sat_derate=0.4
# fatigue (M4, Coffin-Manson SAC)
cm_c=-0.6; cm_epsf=0.30; bump_t_life_h=2000.0
# PDN + driver (V1–V8, A.3)
r_pdn=0.02; l_pdn=100e-12; c_decap=50e-9; vth=0.32; alpha_pow=1.3
dvth_dt=-2.0e-3; psij_ps_per_mv=0.05
```

**New `campaign` columns:** hidden ground truth `field_T_C`, `field_sigma_MPa`, `field_droop_mV`,
`field_crack_a`; keep the *observable* (sensor-corrupted, §B.4) `temp_C`/`vdroop_frac`; add the
tie-breaker channels of §B.5.

## B.5 Identifiability — the deliberate collisions and their tie-breakers

The map is **many-to-one on purpose** — that is the scientific content (detect *and* attribute).
Each collision is broken by a specific auxiliary channel the dataset must emit:

| Collision | Shared param | Degenerate signature | Tie-breaker channel |
|---|---|---|---|
| Thermal vs aging | series R↑ | DC-R rise, TDR damping | on-die **T sensor** + drift *direction* (thermal reversible/ms; aging monotone/hours) |
| **Thermal vs stress** | series R↑ / drive | R rise / eye close | **n-vs-p drive asymmetry** (stress splits rise/fall; thermal symmetric — §D) + Si-vs-Cu R ratio |
| Droop vs hotspot | R_on↑, slew↓ | eye-width closes, jitter↑ | **PDN-V waveform** (droop = ns–µs, f_res ring) + Cu-TCR R + leakage (thermal = ms–s) |
| Stress-μ vs droop | drive/swing↓ | eye-height↓, BER↑ | **voltage sensor** (droop only) + n/p asymmetry (stress only) |
| Vth(T) vs RX offset vs bridge | decision threshold bias | '1'-vs-'0' BER asymmetry | T sensor (Vth drifts −2 mV/°C); bridge is *static, T-independent* |
| Loss(G↑) vs crosstalk vs Z-step | eye closure / ISI | reduced eye | **TDR/SREL** (localized Z step) + aggressor-pattern conditioning + thermal node |

**Minimal observable-confounder column set:** `temp_C` (have), `vdroop`/PDN-V waveform (extend),
`tdr_refl_coef`+`tdr_pos_mm` (have), **`drive_asym_np`** (NEW — only observable with an active TX),
`activity`/`i_avg` (NEW), **drift-rate (time-derivative) of every slow feature** (NEW — "rate of
change is the attribution key").

**Sensor-realism corruption** (so tie-breakers are honest, joint Vdd–T sensor coefficients): T
channel = truth ± 1.2 °C (3σ) + 0.4 °C/V Vdd cross-coupling; V channel = truth ± 3 mV + 1 mV/V T
cross-coupling; both sampled every 10–30 µs (slow scalar stream, not per-UI). This makes the problem
well-posed *only via multimodal fusion* — which is the thesis.

---

# Part C — ngspice-46 implementation gotchas (verified, must-fix)

These were tested against this project's ngspice-46 and **fail**; the synthesized "textbook" cards
must be rewritten in the `netlist.py` idiom (Python-inlined numerics).

| # | Fails in ngspice-46 | Fix |
|---|---|---|
| C1 | `E … LAPLACE {V(n)} {H(s)}` — **does not exist** (PSpice/HSPICE only) | passive 1z/1p **RC CTLE** (Rs/Cs/Rl), as in A.3. Drop LAPLACE entirely. |
| C2 | `E… delay {V(x)} td=…` / `{...}` braces | 1-UI delay via lossless **T-element** `T1 a 0 b 0 Z0=50 TD=62.5p` + term, or skip (v1 needs no delay). |
| C3 | `.param`/`.func` symbols inside `B…` expressions — **`Undefined parameter`** | **inline numeric literals from Python** (f-strings), exactly as `netlist.py` does for R_on/bumps. |
| C4 | `(pn>0)?a:b` ternary in `.func`, and `?:` on a DC node breaks OP | n/p sign is **compile-time constant** — emit **two sign-baked B-sources** (`+pi_p` up, `−pi_n` down). |
| C5 | `tanh` slicer at gain 50/20 — **timestep too small** | gain **≤ 8–15**, add `Rdec dec 0 1k` DC path, run `.tran … uic` (don't force `op`). |
| C6 | self-referential latch `…?…:V(dout)` = algebraic loop | break with a T-element-delayed copy; or **omit the latch** (extract decisions in Python) for v1. |
| C7 | `Lpdn` + `uic` → rail starts at 0, never charges in a short window | **`.ic v(vddtx)=0.8`** (and `vddpre`,`vddrx`). |
| C8 | `Lpdn a a 0` (degenerate short), `Cdec=200p` (f_res ~GHz, 1000× off), `KPSIJ=2p` (40× off), `Cint` edge-time arithmetic 22× off | real series `Lpdn=100p`; `Cdec=50n` → f_res≈71 MHz; PSIJ `0.05 ps/mV`; `Cint=200f` → ~20 ps edge. |
| C9 | `sigma` node Pa-vs-MPa unit collision between the two synthesis docs | **one convention: `sigma` in MPa (1 V=1 MPa)**; bake ×1e6 Pa-conversion into each coefficient in Python. |
| C10 | latent `tdie`/`sigma` as high-Z "info" nodes → `gmin`/OP grief | drive from a **stiff V/PWL source** (low source-R). |

Plus: `B` current sources push current **out** of the `n+` node — pull-up uses
`I=…*(V(vint)−V(vddtx))`, pull-down uses `I=…*V(vint)` (getting these backwards is positive
feedback → numerical blow-up; verified).

---

# Part D — The experiment that matters: identifiability

Adding ~8 couplings (Q1) and ~40 coefficients (Q2) raises a fair reviewer question: *with this many
free coefficients, can the labels still be identified, or can any eye/BER signature be explained by
**some** latent setting?* The forward map + a tie-breaker table are **not** evidence the inverse is
identifiable. **Do this before generating the full dataset:**

1. **Forward demo (done, as-built).** The n/p stress fingerprint emerges in pure ngspice-46 from
   the integrated `simulate_tx_probe` with literature coefficients — pure temperature scales rise &
   fall *together*, stress *splits* them. Two numbers matter: the **idealised unloaded** ratio
   (a single Cint, no channel load, `sat_derate=1.0`) and the **as-built** ratio (the shipped probe:
   bump R+L + Z₀ load, physical `sat_derate=0.4`). The load and saturation-derate dilute the split
   but it stays clearly above the symmetric thermal baseline:

   | Field | as-built `drive_asym_np` (shipped) | idealised unloaded |
   |---|---|---|
   | healthy / baseline | 0.9994 | 1.000 |
   | **pure thermal 125 °C** (μ(T), no stress) | 0.9995 | 1.000 |
   | **stress +244 MPa** (or 125 °C induced) | **0.974** | 0.819 |
   | **stress −244 MPa** | **1.026** | 1.18 |

   So `drive_asym_np` (rise/fall ratio) discriminates stress (≠1, sign-bearing) from thermal (≈1).
   The ±2.6 % as-built split is subtle but, in the clean probe, well separated from the 0.05 %
   thermal baseline. *(Raise `sat_derate` toward 1.0 for the larger triode-region split; the shipped
   default 0.4 is the physical saturation value.)* The earlier 0.819 figure was the idealised 1/g
   prediction, not what the loaded simulator produces.

2. **Inverse / leakage check.** Train the detector on the fused channels; show it recovers the
   latent `{T, σ, droop}` labels on held-out runs **better than chance**, and a confusion/mutual-
   information matrix that the three are separable.
3. **Ablation (the falsifiable claim).** Withhold one tie-breaker channel at a time
   (`drive_asym_np`, PDN-V, T sensor) and show attribution **degrades to the confounded baseline** —
   i.e. the channel is *load-bearing*, not decoration. A coefficient earns its place only if removing
   it measurably changes a channel the detector consumes *and* its effect is not rank-degenerate with
   another knob given the observables.

**Minimal honest contribution = Stage 1+2+3+4 (one genuine confound: `R_on` shared by Vdd/T/σ; one
discriminating fingerprint per cause) + this identifiability experiment.** Everything beyond is
realism hardening — add only if the minimal version already shows clean identifiability.

---

## References (corpus + literature, as gathered)

Ma et al., "Electrical-Thermal Co-Simulation Model of Chiplet Heterogeneous Integration," *IEEE
TVLSI* 32(10), 2024 (Cu α=3.93e-3/K; +27 % IR; R_ja). Smith, *Phys. Rev.* 1954 / Kanda, *IEEE TED*
1982 (Si piezoresistive tensor). Sakurai & Newton, *IEEE JSSC* 1990 (α-power-law delay). Coffin
1954 / Manson 1953; Engelmaier 1983 (solder LCF). Smith & Bogatin (PDN target impedance). Filanovsky
2001 (Vth(T), μ(T)). FOWLP-BIST arXiv:2503.14784 (defect→R/C fits). Kang et al. arXiv:2304.10207
(reflection-coefficient fault diagnosis; DC-R poor proxy). ChipletQuake arXiv:2504.19418 (on-die
impedance sensing). HeatSense (thermal anomaly thresholds). Joint Vdd–Temperature Sensor (T/V sensor
accuracy + T↔Vdd degeneracy). proteanTecs / deep-data in-field prognostics (fusion feature set;
rate-of-change attribution). UCIe Test&Repair / Physical-aware testing (PHY driver/RX, lane repair).

*Generated from workflow `wf_5936b647-798` (17 agents: 10 corpus miners + 4 literature researchers +
2 synthesis architects + 1 adversarial critic). All cards re-verified against ngspice-46.*
