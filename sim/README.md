# Pure-ngspice D2D Interconnect Simulation Workflow

A self-contained, **open-tool** simulator that models a **die-to-die (D2D)
chiplet link** entirely in **ngspice** and emits a **labelled, multimodal
telemetry dataset** for the runtime D2D link-health **anomaly-detection &
attribution** project (Direction 3; `../Track3_Open_Report_D2D_Link_Health.md`).
The electrical modelling follows the verified methodology in
`../survey/DEEP_SIM_d2d_interconnect.md`; the active behavioural front-end and the
EM-free multiphysics field maps follow `MULTIPHYSICS_DESIGN.md` (this folder).

The thesis the dataset is built to support: **fuse on-chip telemetry (voltage
droop, temperature, mechanical-stress proxies, aging) with link-level signals
(eye, BER, jitter, skew, TDR) to detect *and attribute* runtime defects that are
triggered by multi-physics interaction** (thermal ↔ voltage ↔ mechanical stress ↔
crosstalk). The headline novelty is a **mechanical-stress axis that is identifiable
against the thermal confounder** through the TX rise/fall asymmetry fingerprint.

> No commercial EM / AMI / FEM tools, no foundry PDK, no SPICE other than ngspice.
> The Python harness is **standard-library only** (it shells out to `ngspice`);
> only the optional plotting/verification scripts need numpy + matplotlib.

---

## TL;DR

```bash
brew install ngspice                       # the only hard dependency (ngspice >= 40)
python3 run.py selftest                    # verify the toolchain + sanity checks

python3 run.py single  --defect healthy                       # ideal link + ASCII eye
python3 run.py single  --active --defect healthy --temp 110   # behavioural multiphysics
python3 run.py probe   --active --temp 27 --stress-mpa 244    # the stress fingerprint
python3 run.py tdr     --defect resistive_open --r-open 2000 --pos 14   # reflectometry
python3 run.py campaign --out out/dataset.csv                 # 86-run labelled dataset

# figures (matplotlib interpreter — see Requirements)
PYV=/Users/yuanqi/miniconda3/envs/drl_hw2/bin/python
$PYV draw_schematics.py     # circuit diagrams  -> out/plots/fig_*.png
$PYV plot_eyes.py           # eye galleries + overview -> out/plots/
$PYV verify_sections.py     # 15 block-level checks + figures -> out/sections/
```

---

## Contents

1. [Installation](#installation)
2. [How the D2D interconnect is modeled](#how-the-d2d-interconnect-is-modeled)
   — topology · unit cell · element provenance · defect injection · telemetry
3. [Active behavioural front-end (multiphysics) `--active`](#active-behavioural-front-end-multiphysics----active)
4. [Eye diagrams](#eye-diagrams)
5. [Command-line reference](#command-line-reference)
6. [Usage examples (exhaustive)](#usage-examples-exhaustive)
7. [Python API](#python-api)
8. [Dataset schema](#dataset-schema-outdatasetcsv)
9. [Directory & output structure](#directory--output-structure)
10. [ngspice-46 gotchas (for extenders)](#ngspice-46-gotchas-for-extenders)
11. [Notes & honest limits](#notes--honest-limits)

---

## Installation

### Dependency overview

| Component | Needed for | Minimum |
|---|---|---|
| **ngspice** | everything (the simulator core) | ≥ 40 (tested on **v46**) |
| **Python 3** (stdlib only) | `run.py`, the `d2dsim` package, the campaign | ≥ 3.8 |
| **numpy + matplotlib** | `plot_eyes.py`, `verify_sections.py`, `draw_schematics.py` | numpy ≥ 1.21, matplotlib ≥ 3.4 |

The simulator core and the dataset campaign need **only ngspice + a stock Python
3** — no `pip install` at all. numpy/matplotlib are needed *only* for the optional
figure scripts.

### Step 1 — install ngspice (the one hard dependency)

| Platform | Command | Resulting binary |
|---|---|---|
| **macOS (Homebrew)** | `brew install ngspice` | `/opt/homebrew/bin/ngspice` (Apple Si) · `/usr/local/bin/ngspice` (Intel) |
| **Debian / Ubuntu** | `sudo apt-get update && sudo apt-get install -y ngspice` | `/usr/bin/ngspice` |
| **Fedora / RHEL** | `sudo dnf install -y ngspice` | `/usr/bin/ngspice` |
| **conda (any OS)** | `conda install -c conda-forge ngspice` | `$CONDA_PREFIX/bin/ngspice` |
| **from source** | `./configure --with-ngshared=no && make && sudo make install` | `/usr/local/bin/ngspice` |

> The harness finds ngspice via `shutil.which("ngspice")`, so as long as it is on
> your `PATH` you do not need to configure anything. Confirm:
>
> ```bash
> ngspice --version      # expect "ngspice-46" or newer
> ```

### Step 2 — Python for the core (no packages required)

`python3 --version` (≥ 3.8) is enough to run `selftest`, `single`, `tdr`, `probe`,
and the full `campaign`. The `d2dsim` package imports only `math`, `csv`,
`subprocess`, `dataclasses`, … from the standard library.

### Step 3 — numpy + matplotlib for the figures (optional)

Pick **one** of the following. All three give a working `numpy`+`matplotlib`
interpreter; substitute its path for `python3` when running the plot/verify scripts.

```bash
# (a) Use the existing conda env on this machine (numpy 1.26 + matplotlib 3.10):
/Users/yuanqi/miniconda3/envs/drl_hw2/bin/python plot_eyes.py

# (b) Fresh conda env (recommended for a clean setup):
conda create -n d2dsim python=3.11 numpy matplotlib -y
conda activate d2dsim
python plot_eyes.py

# (c) pip + venv (no conda):
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install numpy matplotlib
python plot_eyes.py
```

> ⚠️ On this machine the conda **base** env's numpy is broken (`import numpy`
> fails), so do **not** use base for plotting — use `drl_hw2` (option a) or a fresh
> env (b/c). The pure-stdlib core (`run.py …` without plotting) is unaffected.

A one-shot `requirements.txt` for option (c):

```text
numpy>=1.21
matplotlib>=3.4
```

### Step 4 — verify the toolchain

```text
$ python3 run.py selftest
ngspice: /opt/homebrew/bin/ngspice
  healthy   : eye_height=480.7 mV  BER=1e-300
  open 2kohm: eye_height=-106.4 mV  BER=1e-0
  TDR(open) : rho=0.996 pos=1.62 mm
  [PASS] ngspice link run ok
  [PASS] healthy eye open (>50mV)
  [PASS] defect closes eye vs healthy
  [PASS] defect worsens BER vs healthy
  [PASS] TDR sees a reflection (rho>0.02)

SELFTEST PASSED
```

If `selftest` prints `FAIL: ngspice not on PATH`, revisit Step 1 (`brew install
ngspice` / `apt-get install ngspice`).

---

## How the D2D interconnect is modeled

### 1. System view — victim lane + 2 crosstalk aggressors

![D2D link topology](out/plots/fig_topology.png)

A die-to-die link carries many parallel single-ended lanes across a silicon
interposer. We simulate one **victim** lane plus the two **adjacent aggressor**
lanes (the dominant crosstalk neighbours). Each lane is the same chain —
PRBS driver → tx micro-bump → an `N`-segment RLGC transmission-line ladder →
rx micro-bump → receiver — and the victim is coupled to each aggressor by a
per-node coupling capacitance `Cc`. A defect is injected at one victim segment;
the observable is the victim RX waveform, from which the link telemetry (eye,
BER, jitter, skew, reflection) is measured. A global temperature corner scales the
copper resistance and closes the eye *without* a defect — the **confounder** that
motivates multimodal fusion. (DEEP_SIM §1, §5, §7)

### 2. The per-lane circuit (the netlist unit cell)

![Per-lane circuit](out/plots/fig_unitcell.png)

Every element above is one ngspice card. The lumped **RLGC ladder** (DEEP_SIM
§2–§3) discretises the distributed line into `N` π-sections: a series `R+L` per
segment with a shunt `C` at each node. It is bracketed by the **micro-bump**
`R+L+C` lumps (DEEP_SIM §1) at both ends. Mapping schematic → card (node names
in *italics*):

| Schematic element | ngspice card(s) | meaning |
|---|---|---|
| Driver swing | `Vvdrv vdin 0 PWL(…)` | ideal bit waveform 0→VDD with finite rise/fall (from the PRBS) |
| Driver output Z | `Rvon vdin vtxo 45` | source resistance Rₒₙ ≈ Z₀ (SE) |
| tx micro-bump | `Rvbt`,`Lvbt`,`Cvbt` | 40 mΩ + 30 pH series, 12 fF shunt at *vn0* |
| RLGC cell ×N | `Rv{k} vn{k} vm{k}`, `Lv{k} vm{k} vn{k+1}`, `Cvc{k} vn{k} 0` | Rseg=R′·ℓ/N, Lseg=L′·ℓ/N, Cnode=C′·ℓ/N |
| crosstalk coupling | `Cc_a{n}_{k} vn{k} a{n}n{k}` | per-node victim↔aggressor capacitance |
| rx micro-bump | `Rvbr`,`Lvbr` → *vrxo* | receive-side bump |
| RX load | `Cvrx vrxo 0 30f`, `Rvt vrxo vmid 80` | pad capacitance + light termination to mid-rail |
| Cu temperature | `.model rcu r (tc1=3.9e-3)` + `.temp` | every conductor R scales with the die-temperature corner |

**Annotated netlist excerpt** (`N=3`, one aggressor, shortened — the real default
is `N=20`, two aggressors; a `resistive_open` of 500 Ω is injected at segment 1,
visible as the enlarged `Rv1`):

```spice
.model rcu r (tc1=3.9000e-03 tc2=0)     ; Cu tempco -> R(T)
.temp 27.000                            ; die-temperature corner (modality + confounder)
Vmid vmid 0 DC 0.4                       ; mid-rail for the light RX termination
Vvdrv vdin 0 PWL(0 0 … 1.25e-08 0.8)     ; victim PRBS bit waveform (0..VDD)
Rvon  vdin vtxo 45                       ; driver output resistance Ron
Rvbt  vtxo vbt1 0.04  rcu                ; ── tx micro-bump: R + L + C ──
Lvbt  vbt1 vn0  3e-11
Cvbt  vn0  0    1.2e-14
Rv0 vn0 vm0 0.2333 rcu                    ; ── RLGC ladder segment 0 ──
Lv0 vm0 vn1 3.0e-10
Rv1 vn1 vm1 500.23 rcu                    ; segment 1  (+500 Ω resistive_open injected here)
Lv1 vm1 vn2 3.0e-10
Rv2 vn2 vm2 0.2333 rcu                    ; segment 2
Lv2 vm2 vn3 3.0e-10
Cvc0 vn0 0 6e-14                          ; shunt C at each ladder node (half at the ends)
Cvc1 vn1 0 1.2e-13
Cvc2 vn2 0 1.2e-13
Cvc3 vn3 0 6e-14
Rvbr vn3 vbr1 0.04 rcu                    ; ── rx micro-bump ──
Lvbr vbr1 vrxo 3e-11
Cvrx vrxo 0 3e-14                         ; RX pad capacitance
Rvt  vrxo vmid 80                         ; RX light termination to mid-rail
*  … aggressor lane a1 built identically …
Cc_a1_0 vn0 a1n0 1e-14                    ; victim<->aggressor coupling, per node
Cc_a1_1 vn1 a1n1 2e-14
.control
  tran 1p 625p uic                        ; transient
  linearize                               ; resample onto a uniform time grid
  wrdata rx.dat  v(vrxo)                   ; dump victim RX  -> eye/BER/jitter
  wrdata agg.dat v(a1rxo)                  ; dump aggressor RX
.endc
```

### 3. Element values & provenance

All defaults live in `d2dsim/params.py` (`Config` dataclass), sourced from
`../survey/DEEP_SIM_d2d_interconnect.md`:

| Quantity | Symbol | Default | Source |
|---|---|---|---|
| SE characteristic impedance | Z₀ | 50 Ω | DEEP_SIM §1 (100 Ω diff) |
| Data rate / UI | — | 16 GT/s / 62.5 ps | UCIe-16G (DEEP_SIM §3) |
| Driver swing / output Z | VDD / Rₒₙ | 0.8 V / 45 Ω | low-swing D2D (DEEP_SIM §4) |
| Trace length / segments | ℓ / N | 2 mm / 20 | segment delay ≪ rise time |
| Series resistance | R′ | 0.35 Ω/mm | RDL/interposer Cu (DEEP_SIM §1) |
| Series inductance | L′ | 0.45 nH/mm | = Z₀/vₚ |
| Shunt capacitance | C′ | 0.18 pF/mm | = 1/(Z₀·vₚ) |
| Coupling capacitance | Cc′ | 0.03 pF/mm | adjacent-lane (DEEP_SIM §5) |
| Micro-bump R / L / C | — | 40 mΩ / 30 pH / 12 fF | DEEP_SIM §1 table |
| RX pad C / termination | Cpad / Rterm | 30 fF / 80 Ω→mid | DEEP_SIM §1 |
| Cu tempco | tc1 | 3.9e-3 /°C | DEEP_SIM §7 |

`L′` and `C′` are back-solved from the target Z₀ and the phase velocity
`vₚ = 1/√(L′C′) ≈ 1.1×10⁸ m/s`; the harness then splits them into `N` segments
(`Rseg = R′·ℓ/N`, etc.). `N=20` keeps each segment's delay (~0.9 ps) far below the
~19 ps rise time so the ladder behaves as a transmission line, not a lump.

### 4. Defect injection — the ground-truth labels

![Defect injection map](out/plots/fig_defects.png)

Each label is a **parameterised perturbation of specific cards** (DEEP_SIM §6.1),
so every run carries an exact ground-truth label, position, and severity:

| Label | Netlist perturbation | CLI knob |
|---|---|---|
| `healthy` | nominal | — |
| `resistive_open` | `+R_open` added to `Rv{k}` series resistance | `--r-open --pos` |
| `bump_void_aging` | same as open, swept as a slow R(t) drift trajectory | `--r-open --pos` (campaign sweeps it) |
| `bridge_short` | shunt `Rbrg vn{k} a1n{k}` victim↔aggressor | `--r-bridge --pos` |
| `crosstalk_cap` | `Cc` × factor on the coupling caps | `--xtalk` |
| `impedance_discontinuity` | `Lseg` × z_factor at one segment (Z step) | `--zfac --pos` |
| `hotspot` | per-instance `temp=Thot` on one segment's R | `--hot-t --pos` |
| `supply_droop` | victim driver swing × (1 − droop_frac) [ideal] / PDN rail × (1 − droop_frac) [active] | `--droop` |

### 5. From waveform to telemetry

`measure.py` runs ngspice, reads the `wrdata` dump, and — because the TX bit
sequence is known — folds the RX waveform at the bit centres to get **eye height /
amplitude**, the high/low means and σ for the **Q-factor** and **BER = ½·erfc(Q/√2)**,
the mid-rail crossing **TIE** for **RMS/pp jitter and eye width**, the first-edge
**propagation delay** (→ lane skew), and the aggressor-induced **crosstalk noise**.
A separate source-matched step (`build_tdr`) gives a **TDR/SREL** reflection
coefficient and an estimated defect **position** (DEEP_SIM §4, §6.2). All of this
is pure standard library — no numpy.

---

## Active behavioural front-end (multiphysics)  `--active`

By default the link uses an **ideal** PWL driver through a linear `R_on` and a
trivial RC receiver — fine for single-physics class separation, but the multiphysics
fields cannot couple through it. Setting `active_frontend=True` (CLI `--active`)
swaps the two endpoints for **behavioural macromodels** so temperature, supply
droop and mechanical stress all act on the *same* driver knob `R_on(Vdd,T,σ)` —
the physical confounding an anomaly detector must disentangle.

> **Why behavioural and not ideal/PDK?** The multiphysics confounding only *exists*
> if several latent fields drive one shared device parameter. An ideal source +
> thresholdless RC has no shared knob, so "attribution" would be a label-injection
> artefact; a transistor/PDK model is out of scope (no foundry models, 4-week
> budget). The behavioural macromodel is the minimal contribution-bearing middle.
> Full rationale + every literature coefficient: **`MULTIPHYSICS_DESIGN.md`**. The
> field→parameter maths lives in **`d2dsim/physics.py`** (coefficients computed in
> Python and inlined as numeric literals — ngspice-46 rejects `.param`/`.func`/
> ternary inside `B`-sources).

What the active path adds (`netlist._emit_tx_active` / `_emit_rx_active`):

- **TX** — an α-law push-pull (`g_on(Vrail)=K·(Vrail−vth)^α`, normalised to
  `R_on=45 Ω` at the nominal point) whose **swing rides a compact PDN node**
  (`Rpdn/Lpdn/Cdec` + an activity-scaled SSO load → real IR + Ldi/dt droop), with
  `μ(T)`, `Vth(T)` and an **opposite-sign NMOS/PMOS piezoresistive** stress term
  baked into the conductance.
- **RX** — a passive-RC **CTLE** (HF boost) + a loaded `tanh` **slicer** referenced
  to `V(vddrx)/2`+offset(T); decisions/BER are extracted in Python.
- **Latent fields** — `temperature`, `supply droop`, **mechanical stress (bridged
  from the thermal field via CTE-mismatch, σ ≈ 2.5 MPa/°C, no FEM)**, and
  Coffin-Manson aging — emitted as hidden ground-truth `field_*` labels.
- **Extra telemetry** — `ber_dec`, `vdd_droop_mV`, and a dedicated isolated-edge
  probe (`simulate_tx_probe`) giving `t_rise/t_fall` and `drive_asym_np`.

### The field → device-parameter maps (`d2dsim/physics.py`)

Every coefficient is a *published* first-order material/device sensitivity — the
same spirit as RLGC-from-(Z₀,vₚ). `p(Φ) = p₀·[1 + s·(Φ − Φ₀)]`.

| Latent field Φ | Acts on | Map (physics.py) | Coefficient (default) |
|---|---|---|---|
| Temperature `T` | mobility | `mu_temp_factor` | `μ ∝ T^−1.5` |
| Temperature `T` | threshold | `vth_eff` | `dVth/dT = −2 mV/°C` |
| Temperature `T` | **→ stress** | `sigma_mpa` (CTE) | `σ = E/(1−ν)·Δα·(T−T_sf)` ≈ **2.49 MPa/°C** |
| Stress `σ` | drive (PMOS/NMOS) | `drive_conductances` | `π_p=+7.18e-4`, `π_n=−3.16e-4` /MPa × `sat_derate=0.4` |
| Activity `α` | power → `T` | `power_w`,`t_die_from_power` | `T = T_a + P·R_th`, `R_th=0.3 °C/W` |
| Activity `α` | PDN droop | SSO load + `pdn_droop_mv` | `I = α·I_full`, `R_pdn=20 mΩ` |
| Aging `H` | bump R (label) | `r_bump_aged` | `R0/(1−a)`, `a=H/2000 h` |

The **opposite sign** of `π_p`/`π_n` is the crux: temperature scales pull-up and
pull-down together (rise/fall asymmetry stays ≈ 1), whereas mechanical stress
splits them (asymmetry departs from 1, sign-bearing). That is what makes the
mechanical-stress axis **identifiable against the thermal confounder**.

### The identifiability fingerprint (verified)

`drive_asym_np = t_rise / t_fall` from the isolated TX edge probe:

| Scenario | command | `drive_asym_np` | interpretation |
|---|---|---|---|
| baseline | `probe --active --temp 27` | **0.9994** | symmetric (no stress) |
| pure mobility, +83 °C | `verify_sections.py` sec 1c (`stress_from_thermal=False`) | **≈ 0.999** | temperature alone → **symmetric** |
| +244 MPa stress @ 27 °C | `probe --active --temp 27 --stress-mpa 244` | **0.9742** | stress → **antisymmetric** |
| +110 °C, CTE-coupled | `single --active --temp 110` | **0.978** | heat *induces* ~206 MPa → splits |

So a hot link does show asymmetry — but it is attributable to the *stress* the
heat induces (via CTE), not to temperature per se; the pure-mobility component
stays symmetric. The detector reads `drive_asym_np` (with sign) as a stress
channel that the eye/BER/jitter channels alone cannot supply.

### Section-by-section verification (`verify_sections.py`)

Each block is exercised **independently** with swept inputs, checked against the
expected physics (PASS/FAIL), and rendered to `out/sections/*.png`. **All 15
checks pass:**

| Fig | Block | Representative check (as-run) |
|---|---|---|
| `sec1_tx_driver.png` | α-law TX | swing rides rail; edge slows 18.9→21.5 ps as rail droops; pure-thermal `max\|asym−1\|=0.0006`; stress `asym=0.974` |
| `sec2_pdn.png` | compact PDN | droop 28.2 mV on a 0.3 A step; first-droop ring grows with `L_pdn` |
| `sec3_ctle.png` | RC-CTLE | +2.9 dB HF boost vs DC; high-pass |
| `sec4_slicer.png` | tanh slicer | threshold = rail/2 = 400 mV; +20 mV offset → +20 mV shift |
| `sec5_channel.png` | RLGC ladder | amplitude falls as Cu-R rises with T |
| `sec678_maps.png` | physics maps | stress bridge **2.49 MPa/°C**; thermal ROM 0.3 °C/W linear; aging R 40→800 mΩ |
| `sec9_eyes.png` | end-to-end | active eyes: healthy / thermal / droop / open |

```text
$ /Users/yuanqi/miniconda3/envs/drl_hw2/bin/python verify_sections.py
  ...
15/15 checks passed.
```

---

## Eye diagrams

Two galleries are produced by `plot_eyes.py` into `out/plots/`.

### Ideal front-end — all 8 defect classes

![passive eye gallery](out/plots/eye_gallery.png)

A 3×3 contact sheet (`eye_gallery.png`); individual eyes are `eye_<case>.png`.
Healthy is wide open (eyeH ≈ 481 mV, BER < 1e-300); each defect closes it
characteristically. Example single-eye render (`run.py single`, ASCII):

```text
$ python3 run.py single --defect healthy
D2D link  defect=healthy pos=10 temp=27C rate=16GT/s UI=62.5ps

  eye  (2 UI wide, -59..799 mV)
  |#####                    ##########                    #####
  |############################################################
  |#####   ## #*           ############ ##  #            ######
  | ###                     ####  ####                     ###
  |####                      ########                       ###
  |###                        ######                         ##
  |##                          ####                          ##
  | ...
  eye_height_V     =      0.48073 V
  q_factor         =         40.3
  ber_log10        =         -300
  jitter_rms_ps    =       1.7668
  eye_width_ps     =       55.923
  delay_ps         =       22.868
  xtalk_std_V      =    0.0062719 V
```

### Active behavioural front-end — the multiphysics story

![active eye gallery](out/plots/eye_active_gallery.png)

`eye_active_gallery.png` is a 2×3 sheet annotated with the active-only telemetry
(`eyeH`, decision `BER`, observed PDN `droop`, and `asym = t_rise/t_fall`). The
six panels are arranged to tell the identifiability story:

| Panel | eyeH | σ (MPa) | `asym` | reads as |
|---|---|---|---|---|
| healthy 27 °C | 347 mV | 0 | 0.999 | baseline |
| **pure thermal 110 °C** (`stress_from_thermal=False`) | 350 mV | 0 | **0.999** | temperature alone → **symmetric** |
| thermal+CTE 110 °C (full model) | 351 mV | 206 | **0.978** | heat-induced stress splits edges |
| **mechanical stress +244 MPa** @ 27 °C | 349 mV | 244 | **0.974** | isolated stress → **antisymmetric** |
| supply droop −20 % | 209 mV | 0 | 1.000 | rail collapse, edges stay symmetric |
| resistive open 500 Ω | −74 mV | 0 | 0.999 | eye closed, intrinsic driver fine |

Individual active eyes are `eyeA_a_*.png`. The index `out/plots/README.md` embeds
every figure with captions.

---

## Command-line reference

```
python3 run.py <subcommand> [options]
```

| Subcommand | Purpose |
|---|---|
| `selftest` | verify ngspice on PATH + 5 sanity checks |
| `single` | one link run → ASCII eye + telemetry (`--active` adds multiphysics extras) |
| `probe` | active TX **isolated-edge** probe → `t_rise/t_fall` + `drive_asym_np` (implies `--active`) |
| `tdr` | one TDR/SREL run → reflection coefficient + estimated position |
| `campaign` | full fault-injection grid → labelled CSV dataset |

**Common options** (apply to `single`, `tdr`, `probe`):

| Flag | Default | Meaning |
|---|---|---|
| `--defect {kind}` | `healthy` | one of the 8 `DEFECT_KINDS` |
| `--pos N` | `10` | ladder segment index for positional defects |
| `--r-open Ω` | `0` | series R for `resistive_open` / `bump_void_aging` |
| `--r-bridge Ω` | `1e9` | shunt R for `bridge_short` (smaller = harder short) |
| `--xtalk ×` | `1.0` | coupling-cap multiplier for `crosstalk_cap` |
| `--zfac ×` | `1.0` | `Lseg` multiplier for `impedance_discontinuity` |
| `--hot-t °C` | `27` | local segment temperature for `hotspot` |
| `--droop frac` | `0.0` | supply-droop fraction (0.2 = −20 %) |
| `--temp °C` | model | global die temperature corner |
| `--rate GT/s` | `16e9` | data rate (sets UI). Pass in Hz, e.g. `--rate 24e9` |
| `--len-mm`, `--n-seg`, `--n-bits` | model | channel length / ladder segments / PRBS length |
| `--active` | off | behavioural TX/RX + multiphysics fields |
| `--activity 0..1` | `0.3` | switching activity → PDN load (active) |
| `--stress-mpa` | `0` | extra mechanical stress on the drive (active) |
| `--aging-hours` | `0` | field-time → Coffin-Manson crack fraction **label** (active) |

**Campaign options:** `--quick` (small grid), `--out PATH`, `--no-tdr`,
`--keep-waveforms`, `--rate`.

---

## Usage examples (exhaustive)

### `single` — one link + ASCII eye (ideal front-end)

```bash
python3 run.py single --defect healthy                                  # wide-open reference eye
python3 run.py single --defect resistive_open --r-open 500 --pos 10 --temp 85
python3 run.py single --defect bridge_short   --r-bridge 200 --pos 10   # victim<->aggressor short
python3 run.py single --defect crosstalk_cap  --xtalk 8                 # 8x coupling
python3 run.py single --defect impedance_discontinuity --zfac 1.6 --pos 7
python3 run.py single --defect hotspot        --hot-t 150 --pos 10      # local hot segment
python3 run.py single --defect supply_droop   --droop 0.2              # -20% launched swing
python3 run.py single --defect healthy --temp 110                       # thermal confounder, no defect
python3 run.py single --defect healthy --rate 24e9                      # 24 GT/s corner
python3 run.py single --defect resistive_open --r-open 500 --pos 10 --n-seg 40 --n-bits 400
```

A closed-eye example (defect dominates the channel):

```text
$ python3 run.py single --defect resistive_open --r-open 500 --pos 10 --temp 85
  eye_height_V     =    -0.082886 V     # negative => eye closed
  q_factor         =       0.7664
  ber_log10        =      -0.6542        # BER ~ 0.22
  xtalk_std_V      =     0.037398 V
```

### `single --active` — behavioural multiphysics front-end

```bash
python3 run.py single --active --defect healthy --temp 110              # heat: mu(T)+Vth(T)+CTE stress
python3 run.py single --active --defect supply_droop --droop 0.2        # PDN rail collapse
python3 run.py single --active --defect healthy --stress-mpa 244        # injected mechanical stress
python3 run.py single --active --defect healthy --activity 0.8          # heavy SSO -> larger droop
python3 run.py single --active --defect resistive_open --r-open 500 --pos 10
```

The active path prints the extra telemetry **and the hidden latent fields**:

```text
$ python3 run.py single --active --defect healthy --temp 110
  eye_height_V     =      0.35139 V
  ber_log10        =      -14.851
  ber_dec          =            0
  vdd_droop_mV     =       8.0022
  t_rise_ps        =       18.591
  t_fall_ps        =        19.01
  drive_asym_np    =      0.97795  (=1 thermal, !=1 stress)
  latent fields: field_T_C=110.0 field_sigma_MPa=206.314 field_droop_mV=3.0 field_aging_a=0.0
```

### `probe` — the TX stress fingerprint (A/B at fixed temperature)

```bash
python3 run.py probe --active --temp 27                  # asym 0.9994  (no stress)
python3 run.py probe --active --temp 27 --stress-mpa 244 # asym 0.9742  (stress splits edges)
python3 run.py probe --active --temp 125                 # asym 0.9741  (CTE-induced ~244 MPa)
```

```text
$ python3 run.py probe --active --temp 27 --stress-mpa 244
TX edge probe  temp=27C  sigma=244.0 MPa
  t_rise = 18.621 ps
  t_fall = 19.115 ps
  drive_asym_np (rise/fall) = 0.9742   (=1 thermal-symmetric, !=1 stress)
  tx swing = 424.8 mV
```

### `tdr` — reflectometry / defect localisation

```bash
python3 run.py tdr --defect resistive_open --r-open 2000 --pos 14
python3 run.py tdr --defect impedance_discontinuity --zfac 1.6 --pos 7
python3 run.py tdr --defect healthy                       # no reflection (rho ~ 0)
```

```text
$ python3 run.py tdr --defect resistive_open --r-open 2000 --pos 14
TDR/SREL  defect=resistive_open pos=14 r_open=2000 z_factor=1
  reflection coefficient rho = 0.9685
  estimated position         = 1.625 mm (channel = 2 mm)
```

### `campaign` — build the labelled dataset

```bash
python3 run.py campaign --out out/dataset.csv            # full grid: 86 runs (~40 s)
python3 run.py campaign --quick                          # small grid -> out/dataset_quick.csv
python3 run.py campaign --out out/ds.csv --no-tdr        # skip the TDR pass (faster)
python3 run.py campaign --keep-waveforms                 # keep every run's deck + .dat
python3 run.py campaign --rate 24e9 --out out/ds_24g.csv # whole grid at 24 GT/s
```

```text
$ python3 run.py campaign --out out/dataset.csv
[  1/86] run0000 healthy                eyeH= 481.2mV  BER=1e-300  jit=1.8ps  rho=1.022
[ 17/86] run0016 resistive_open         eyeH= 353.4mV  BER=1e-29   jit=2.8ps  rho=0.980
[ 70/86] run0069 bump_void_aging        eyeH= 249.1mV  BER=1e-11   jit=4.5ps  rho=0.953
...
Wrote 86 rows x 18 cols -> out/dataset.csv
```

### Figure generation

```bash
PYV=/Users/yuanqi/miniconda3/envs/drl_hw2/bin/python
$PYV draw_schematics.py      # fig_topology / fig_unitcell / fig_defects  -> out/plots/
$PYV plot_eyes.py            # eye_gallery + eye_active_gallery + per-case eyes + overview
$PYV verify_sections.py      # 15 block checks + sec*.png  -> out/sections/
```

`plot_eyes.py`'s `dataset_overview.png` needs `out/dataset.csv` (run the campaign
first); it skips the overview gracefully if absent.

---

## Python API

The `d2dsim` package is importable for notebooks / custom sweeps. Everything is
pure stdlib; `Config` is a frozen-ish dataclass you mutate with
`dataclasses.replace`.

```python
import dataclasses
from d2dsim.params import Config
from d2dsim.campaign import make_defect
from d2dsim.measure import simulate_link, simulate_tdr, simulate_tx_probe
from d2dsim import physics

# 1) one ideal link run --------------------------------------------------------
cfg = Config(temp_c=85.0)
defect = make_defect("resistive_open", position=10, r_open=500.0)
feats, (t, v), bits, proc = simulate_link(cfg, defect, workdir="_work/api")
print(feats["eye_height_V"], feats["ber_log10"], feats["jitter_rms_ps"])

# 2) active behavioural front-end + latent ground truth ------------------------
acfg = dataclasses.replace(Config(), active_frontend=True, temp_c=110.0)
feats, _, _, _ = simulate_link(acfg, make_defect("healthy"), "_work/api_active")
print(feats["ber_dec"], feats["vdd_droop_mV"])
print(physics.latent_labels(acfg))          # {'field_T_C':110.0,'field_sigma_MPa':206.3,...}

# 3) the stress fingerprint directly -------------------------------------------
probe, _, _ = simulate_tx_probe(
    dataclasses.replace(Config(), active_frontend=True, stress_mpa=244.0,
                        stress_from_thermal=False),
    make_defect("healthy"), "_work/api_probe")
print(probe["drive_asym_np"])               # ~0.974  (stress != 1)

# 4) inspect the field -> parameter maps without running SPICE -----------------
print(physics.sigma_mpa(Config(temp_c=110.0)))      # CTE-bridged stress [MPa]
print(physics.drive_conductances(Config(stress_mpa=244.0, stress_from_thermal=False)))

# 5) a custom mini-campaign ----------------------------------------------------
from d2dsim.campaign import run_campaign
run_campaign(Config(), "out/my_dataset.csv", quick=True)
```

Key entry points: `simulate_link` (eye/BER/jitter + active extras),
`simulate_tdr` (reflectometry), `simulate_tx_probe` (edge asymmetry),
`physics.*` (field→parameter maps & labels), `campaign.run_campaign`
(dataset builder), `netlist.build_channel/build_tdr/build_tx_probe` (raw deck
generation), `prbs.prbs_bits` (PRBS streams).

---

## Dataset schema (`out/dataset.csv`)

86 rows × 18 columns (full grid). Label distribution: `resistive_open` ×36,
`healthy` ×15, `bridge_short` ×8, `supply_droop` ×8, `crosstalk_cap` ×6,
`bump_void_aging` ×6, `impedance_discontinuity` ×4, `hotspot` ×3.

| group | columns |
|---|---|
| identity / label | `run_id`, `label`, `position`, `severity` |
| **observable confounders** | `temp_C`, `vdroop_frac`, `rate_GTps` |
| link modality | `eye_height_V`, `eye_amp_V`, `q_factor`, `ber_log10`, `jitter_rms_ps`, `jitter_pp_ps`, `eye_width_ps`, `delay_ps`, `xtalk_std_V` |
| reflectometry | `tdr_refl_coef`, `tdr_pos_mm` |

```text
run_id,label,position,severity,temp_C,vdroop_frac,rate_GTps,eye_height_V,...,tdr_refl_coef,tdr_pos_mm
run0000,healthy,10,T=0C seed=0x5b,0.0,0.0,16.0,0.481176,...,1.0215,2.375
run0050,resistive_open,17,R_open=2000ohm pos=17 T=85C,85.0,0.0,16.0,-0.039254,...,0.9793,1.9583
run0078,supply_droop,10,droop=20% T=85C,85.0,0.2,16.0,0.380045,...,1.0195,2.375
```

`label` is the hidden target; `temp_C` / `vdroop_frac` are **observable**
telemetry channels — a detector must use them to avoid mistaking a benign
thermal/droop excursion for a defect (the multimodal-fusion premise).

> **Note on the active multiphysics columns.** The default campaign uses the ideal
> front-end (so the CSV schema above is stable and reproducible). The active-only
> observables (`ber_dec`, `vdd_droop_mV`, `drive_asym_np`) and the hidden
> `field_*` labels are produced per-run by `simulate_link`/`simulate_tx_probe`/
> `physics.latent_labels` (see the [Python API](#python-api)); wire them into a
> campaign variant when you want the multiphysics dataset.

---

## Directory & output structure

```
sim/
├── d2dsim/                 the package (pure stdlib)
│   ├── params.py           Config dataclass + physical defaults (cited to DEEP_SIM)
│   ├── prbs.py             maximal-length LFSR PRBS bit streams
│   ├── physics.py          latent fields -> device-parameter coefficients (EM-free)
│   ├── netlist.py          ngspice deck generation (ideal + active front-end, TDR, probe)
│   ├── measure.py          run ngspice, parse wrdata, extract eye/jitter/BER/TDR/asym
│   └── campaign.py         fault-injection grid -> labelled dataset
├── run.py                  CLI: single | tdr | probe | campaign | selftest
├── plot_eyes.py            matplotlib eye galleries (ideal + active) + overview
├── verify_sections.py      15 block-level checks + section figures (active front-end)
├── draw_schematics.py      matplotlib circuit diagrams for this README
├── MULTIPHYSICS_DESIGN.md  the active-front-end + field-mapping design note
├── proto/active_txrx_min.cir   minimal verified active TX/RX prototype deck
│
├── out/                    ← DELIVERABLES (keep these)
│   ├── dataset.csv             one row per run: label + observable telemetry
│   ├── plots/                  eye galleries, schematics, overview + index README
│   │   ├── fig_topology / fig_unitcell / fig_defects .png   circuit diagrams
│   │   ├── eye_gallery.png          3x3 ideal-front-end eyes (all 8 classes)
│   │   ├── eye_active_gallery.png   2x3 active multiphysics eyes (the identifiability story)
│   │   ├── eye_<case>.png / eyeA_a_<case>.png   individual eyes
│   │   └── dataset_overview.png     class separability + aging trajectory
│   └── sections/               verify_sections.py block figures (sec1..sec9)
│
└── _work/                  ← SCRATCH (safe to delete; regenerated on demand)
    ├── run0000/                one kept campaign run: deck.cir + rx/agg/tdr .dat
    └── single/ tdr/ probe/ …   last-run decks + waveform dumps
```

* **`out/`** is what you keep and share. **`_work/`** holds the raw ngspice decks
  (`deck.cir`) and waveform dumps (`rx.dat`=victim RX, `agg.dat`=aggressor,
  `tx.dat`/`dec.dat`/`vdd.dat`=active driver/slicer/rail, `tdr.dat`=reflectometry).
  The campaign deletes per-run scratch as it goes, keeping only `run0000` as a
  worked example you can open in ngspice. Delete `_work/` anytime — it is rebuilt.

---

## ngspice-46 gotchas (for extenders)

The behavioural cards were hardened against real ngspice-46 behaviour (the
synthesized "textbook" HSPICE/PSpice cards **fail** here):

- `.param` / `.func` / ternary **inside** `B`-source expressions, `E…LAPLACE`, and
  `E…delay` are all rejected → **inline numeric literals computed in Python**
  (`physics.py` → `netlist.py`).
- `B … I=` sources current **out of** `n+`; a wrong sign on the pull-up/pull-down
  blows the rail up to ±1e8 V. The pull-up draws from `vddtx`, the pull-down sinks
  `txo`.
- `uic` + a PDN inductor → the rail starts at 0 and never charges. Pre-charge with
  `.ic v(vvddtx)=… v(vvddpre)=… v(vvddrx)=…`.
- `pow()` of a sub-threshold (negative) base silently returns the magnitude →
  clamp with `pow(max(V(rail)−vth, 1e-3), α)` so an off driver stays off.
- A node literally named `eq` is parsed as the `.eq.` operator (and `vdb()/vm()`
  choke on it in `wrdata`) → name CTLE nodes `ceq`/`veq`, not `eq`.
- `tanh` slicer needs gain ≤ ~15 **and** a resistive DC load for convergence.

---

## Notes & honest limits

* This is a **first-experiment, channel-level + behavioural-endpoint** model: a
  lumped RLGC ladder, an α-law push-pull on a compact PDN, and reduced-order
  field maps. It generates *labelled, physically-plausible* telemetry — **not** a
  sign-off-accurate S-parameter / IBIS-AMI / FEM flow. Board-level signature
  magnitudes (e.g. ±20 % Z → eye-% rules) are templates to rescale (DEEP_SIM §6.2).
* The temperature→stress CTE bridge is **incremental** about `t_stressfree=27 °C`
  (so healthy@27 is stress-neutral); the constant assembly/reflow residual
  (~ −340 MPa) is a separable DC offset, not detection-relevant. Set
  `t_stressfree=220` to model the absolute reflow residual instead.
* `--aging-hours` currently sets the **Coffin-Manson crack-fraction label** and the
  physics-map plot; the *observable* aging trajectory in the dataset is the
  `bump_void_aging` series-R drift (`physics.r_bump_aged` is not yet wired into the
  active bump resistance — a one-line extension, analogous to the SSO-droop fix).
* `tdr_refl_coef` is a raw peak-deviation ratio and can slightly exceed 1.0 from
  ringing/overshoot; it is a feature, not a calibrated ρ.
* Deliberately **cut for the 4-week budget** (see `MULTIPHYSICS_DESIGN.md`):
  LAPLACE/s-domain CTLE, FFE/DFE, in-SPICE clock recovery, leakage self-heating
  loop, warpage spatial operator, multi-τ thermal ladder, mutual-K crosstalk sweep.

---

*Provenance: electrical model `../survey/DEEP_SIM_d2d_interconnect.md`; active
front-end + field maps `MULTIPHYSICS_DESIGN.md`; project framing
`../Track3_Open_Report_D2D_Link_Health.md`. Open-tool, reproducible: ngspice +
Python stdlib.*
