# Deep Literature Search — Direction 3 (D2D Link Health), Round 3

> **Scope.** Three deep web searches requested: (1) re-examine the claimed *empty* white-space; (2) survey *simulation methodologies* for D2D testing; (3) gather *motivation* for multimodal online D2D health monitoring.
> **Method.** Multi-phase agentic web sweep — 25 search angles (17 seed + completeness-critic expansion) → 229 distinct works surfaced → 32 top candidates independently web-verified (existence + abstract + skeptical preemption check) → 32 kept as citable. Adversarial pass explicitly tried to *refute* the novelty claim.
> **Companion files.** Builds on `SYNTHESIS_direction3_round1.md`, `00_DOWNLOAD_LIST_round2_direction3.md`, and `Track3_Open_Report_D2D_Link_Health.md`.
> A dedicated **detailed D2D-interconnect simulation** deep-dive follows as a separate workflow (per request) — see the forthcoming `DEEP_SIM_d2d_interconnect.md`.

---

## A. Re-examination of the Claimed White Space (Multimodal Online D2D Link Health)

### A.1 The claim, stated precisely

The thesis asserts an **empty intersection** of four axes:

1. **Multimodal fusion** — voltage (droop/PDN noise) + temperature/thermal-drift + PVT sensors **fused as co-equal detection modalities** with **link-level** signals (BER, eye margin, lane skew, retrain/parity events), used *jointly* to detect and *attribute* anomalies — not multiple monitors graded independently.
2. **Online / in-field** — continuous mission-mode operation, not design-time, ATE, or burn-in.
3. **D2D-native** — chiplet die-to-die interconnects (UCIe / BoW / AIB PHYs over interposer / micro-bumps / RDL), not monolithic-SoC cores, NoC routers, DRAM channels, or board-level links.
4. **Weak / parametric / drift / incipient** degradation regime — not deterministic hard-fault structural test, and not slow generic device end-of-life only.

The white-space claim is the conjunction: **no prior work occupies all four simultaneously.** Below, every candidate that touches ≥2 axes is tagged and clustered; preemption requires hitting all four.

### A.2 Cluster 1 — D2D-native but single-modality and/or structural/offline (link or structural axis only)

These are the most domain-proximate works but each collapses on the multimodal and/or online axes.

- **PARTIAL-OVERLAP (closest competitor)** — proteanTecs Tile-Connectivity/Interconnect Agents [proteanTecs *D2D Interconnect Monitoring* 2022–2025; proteanTecs *On-Chip Monitoring & Deep Data Analytics* 2022–2024]. Online ✓, D2D-native ✓, ML degradation ✓, drift ✓, *and* co-locates voltage/thermal/workload agents with link agents — it hits all four axes at the *capability* level. It is **not** preemptive only because (a) V/T enter the interconnect model as **acceleration-factor covariates**, not co-equal fused detection modalities; (b) "Agent fusion" is marketed at system-summary level with **no published joint cross-modal architecture, no cross-modal root-cause attribution, no peer review**. This is the single item that, if its proprietary stack truly fuses V+T+link for detection, would erode novelty — hence the claim must be scoped to *published, reproducible, peer-reviewed* fusion.
- **PARTIAL-OVERLAP** — Synopsys MTR / SIM + SLM on UCIe (TSMC silicon) [Goriawalla & Zorian, *Synopsys Blog* 2025; *Multi-Die MTR WP* 2023–2025]. Online ✓, D2D-native ✓, link SIM ✓; but link SIM, BIST, and PVT are **three separate pipelines**, PVT used only as repair-signature corners — **no fusion, fault model is hard/structural** (BIRA + E-Fuse spare lanes). Bounds, does not fill.
- **ADJACENT** — UCIe 1.1/2.0/3.0 spec (eye-margin registers, parity-flit health, retrain, BER/skew automotive) [UCIe Consortium 2024; Das Sharma *IEEE Micro* 2024]. Enabling substrate: standardizes the *link* modality and in-field transport, defines **no thermal/voltage-droop telemetry and no detection/fusion algorithm**. UCIe 3.0 runtime recalibration is a reactive control loop, not detection [Alphawave/SemiWiki 2025].
- **ADJACENT** — UCIe/chiplet structural test & repair: E2I-TEST 16-pattern ATPG [Wang/Chuang/Lorenzelli/Marinissen *ETS* 2024; Chuang et al. *TCAD* 2024], IEEE P3405 [Marinissen et al. *VTS* 2024], ASU Test/Diagnosis line [Bhoumik/Chakrabarty *IEEE D&T* 2025; *VTS* 2026 Nert/Dart], BER-only interconnect sensing [*Sensors/MDPI* 2018], eye-margin connectivity patent [US12072376]. All **offline/manufacturing or hard-fault structural, single-modality** — the canonical "other half of the Venn diagram." Note "weak defect" here means manufacturing-marginal resistive open/short, **not** parametric drift.
- **ADJACENT** — Lead (D2D link exploitability) [Hati et al. *VTS* 2026], GNN-SP S-parameter estimation [Fudan *TCAD* 2024]: D2D-native but **security or design-time SI**, no telemetry/online/fusion.

### A.3 Cluster 2 — Multimodal fusion, but not D2D (SoC/critical-path/device prognostics)

The exact adversarial analog: fusion-for-prognostics exists, but never on D2D links and never with the V+T+**link** triad.

- **PARTIAL-OVERLAP (strongest academic analog)** — Twente on-chip embedded-instrument fusion [Ali, Bagheriye, Kerkhoff *ISCAS* 2020 / *IOLTS* 2020 / *ATS* 2020]. Genuine multimodal ML fusion (PCA/ICA/autoencoder) of on-chip instruments for prognostics — but modalities are **critical-path/aging instruments, not voltage-droop+thermal+link**; target is **monolithic MPSoC EOL**, not D2D; task is **slow EOL regression**, not online weak/drift link detection. Does **not** preempt; it is the precise "fusion-for-SoC-EOL, not-D2D-online" boundary the claim names.
- **PARTIAL-OVERLAP** — SoC Health Map [Shibin, Jenihhin et al. *DFT* 2023]: aggregates multiple sensor *types* into a hierarchical in-field health representation — but it is **event-bookkeeping, not signal-level fusion**; no link (BER/eye/skew) modality; **not D2D**.
- **ADJACENT** — proteanTecs SDE-prediction [proteanTecs *VTS* 2023]: fuses aging+V+T+test data with ML, but for **device-level screening, not online D2D-link** detection. GA lifetime-fusion for MPSoC [*Tsinghua Sci.&Tech.* 2022]; multi-branch PHM fusion [*RESS* 2021]; joint Vdd-T sensor primitive [Ozturk et al. *JSSC* 2025] (two modalities, no link, SoC thermal mgmt). All multimodal-ish but **not D2D and not link-inclusive**.

### A.4 Cluster 3 — Online/in-field health, but single-modality and not D2D

- **ADJACENT** — FPGA aging prognosis at scale [Lanzieri et al. *arXiv* 2024] (RO switching-frequency; V/T are logged covariates, single detection modality, not interconnect); on-chip Vmin CQR [Yin et al. *DATE* 2024] (delay monitors, burn-in-emulated, monolithic die, no link); SlowPoke fail-slow [Wu et al. *arXiv* 2025] (NoC mesh links, single behavioral trace, intra-chip); HeatSense [Hasanzadeh et al. *TCAD* 2026] (thermal-only, NoC security); ML voltage-emergency detection [Liu et al. *TCAD* 2017] (voltage-only, monolithic PDN, transient not drift); droop ML chip [Magod et al. *JSSC/VLSI* 2023–2024], z14 droop estimation [Vezyrtzis et al. 2018] (voltage-only, SoC). Each owns **one** modality on **non-D2D** silicon.

### A.5 Cluster 4 — ML/SI anomaly detection on a high-speed link, but not multimodal, not D2D, offline

- **ADJACENT** — KAIST/Samsung AE+classifier on DRAM signals [Usama et al. *arXiv* 2025]: closest *ML-on-electrical-link* method, but **single-modality waveform-only, DRAM channel not D2D, offline, synthetic ISI distortions**. Self-evolution RX adaptation [2020] is design-time link-only. Confirms the "single-modality SI-anomaly" framing dominates.

### A.6 Cluster 5 — Method/primitive papers (streaming AD, drift, attribution, multimodal GNN) — domain-agnostic

- **NOT-RELEVANT to preemption** (cite as method backbones) — drift-adaptive online AD: METER [Zhu et al. *PVLDB* 2024], MemStream [Bhatia et al. *WWW* 2022], ARCUS [Yoon et al. *KDD* 2022], RNN-drift [Saurav et al. *CoDS-COMAD* 2018], ADWIN [Bifet & Gavaldà *SDM* 2007], ECDD [Ross et al. *PRL* 2012], online-FDR [Rebjock et al. *NeurIPS* 2021]; attribution/RCA: Likelihood Compensation [Idé et al. *AAAI* 2021], GDN [Deng & Hooi *AAAI* 2021], BALANCE [Chen et al. *SIGMOD* 2023]; **multimodal** GNN: **MST-GAT** [Ding et al. *Information Fusion* 2023] — has genuine inter-modal attention but evaluated only on spacecraft/water/server benchmarks, **zero hardware/D2D content**. These are domain- and hardware-agnostic; none touches voltage/thermal/link telemetry or chiplets, so none can scoop the claim — they supply the toolbox the contribution adapts.

### A.7 Cluster 6 — Confounding-physics and simulation enablers (motivation, not prior art)

Inverse-temperature-dependence and droop-vs-aging disentanglement [Dasdan & Hom *TODAES* 2006; Ajami et al. *ITC* 2003; "separating temperature from RO readings" *ICCAD* 2007; Jafarzadeh et al. *JETTA* 2025; Sengupta & Sapatnekar *TCAD* 2017], thermal-aware UCIe SI degradation [*ECTC/EPEPS* 2024 doc 10468234], chiplet electro-thermal co-sim [*TVLSI* 2024], CoMeT/3D-ICE/CHIPSIM/MFIT thermal generators, MathWorks/Keysight/Cadence UCIe AMI link-telemetry generators, micro-bump/RDL EM and Coffin-Manson degradation physics. These **justify** why the three modalities are individually predictive and physically coupled (so single-modality detectors confound thermal drift / droop with defect), but **none performs online multimodal D2D fusion detection** — they are the substrate the thesis builds the benchmark on.

### A.8 Final verdict

**The gap SURVIVES**, but only in a **narrowed, honestly-scoped** form. Two findings force tightening:

1. **proteanTecs already co-locates V+T+link agents on real D2D PHYs in-mission and markets "Agent fusion"** — so the claim "no one fuses voltage+thermal+link for online D2D health" cannot be asserted absolutely; it must be scoped to the absence of any **published, peer-reviewed, reproducible** joint cross-modal detector. The contribution is *not* "having co-located monitors."
2. **Multimodal on-chip-instrument fusion-for-prognostics is an established line** [Ali/Bagheriye/Kerkhoff 2020; Shibin 2023] — so novelty cannot rest on "fusion of on-chip telemetry" generically; it rests on the **specific V+T+link triad × D2D-link domain × online weak/parametric-drift detection-and-attribution**, which no source occupies.

**Sharpened, defensible novelty statement:**

> *No published, peer-reviewed, reproducible method performs joint cross-modal fusion of on-die voltage-droop, thermal-drift, and link-level (BER / eye-margin / lane-skew / retrain-parity) telemetry to detect and attribute weak/parametric/drift anomalies on die-to-die chiplet interconnects (UCIe/BoW/AIB) online in mission mode — existing D2D work is single-modality, structural/hard-fault, or design-time; existing multimodal-fusion prognostics target monolithic-SoC critical-path end-of-life, not D2D links; and the one in-field multimodal D2D product (proteanTecs) treats the modalities as separate per-modality grading streams with no disclosed cross-modal detection/attribution model.*

This survives DATE-PC scrutiny **provided** the related-work section explicitly positions against proteanTecs (scope to peer-reviewed/reproducible + cross-modal attribution) and the Twente/Shibin SoC-fusion line (scope to D2D + link modality + online detection vs. EOL regression), and frames the contribution as **fusion-for-detection-and-root-cause-attribution**, not mere multi-sensor presence.

---

## B. Simulation and Data-Generation Methodologies for D2D Link Testing

This section surveys the simulation and synthetic-data methods relevant to building a multimodal die-to-die (D2D) link-health benchmark, organized as a six-family taxonomy. For each family we note what is modeled, fidelity, and openness, then close with a recommended stack and coverage gaps. A recurring observation: every mature flow is *single-modality* — electrical SI tools emit eye/BER, thermal tools emit temperature maps, PDN tools emit droop, and architecture simulators emit traffic/latency — but no public tool jointly emits the fused voltage + thermal + PVT + link telemetry our thesis requires. That absence is itself the methodological white-space.

### B.1 Electrical / Channel & Link Simulation (S-parameter extraction, SPICE, IBIS-AMI, statistical-eye/BER, COM)

This family produces the **link modality** (eye height/width, jitter, BER, COM, bathtub) — the primary observable a D2D health monitor reads.

- **IBIS-AMI reference flows (the workhorse for reproducible link telemetry).** The MathWorks SerDes Toolbox ships turnkey **UCIe 1.0 and UCIe 2.0 Tx/Rx IBIS-AMI reference models** at the thesis-relevant rate (32 GT/s NRZ, 16 GHz Nyquist, forwarded-clock) [MathWorks, "UCIe 2.0 / UCIe 1.0 Transmitter/Receiver IBIS-AMI Model," SerDes Toolbox docs, 2023–2024]. Two simulation flows matter: the `Init` (statistical) flow emits compliance-grade low-BER bathtub/statistical-eye curves, while the `GetWave` (time-domain) flow emits per-bit waveforms and metrics in the BER 1e-6…1e-8 regime where weak/parametric drift actually surfaces [MathWorks, "Understanding IBIS-AMI Simulations," Signal Integrity Toolbox docs, 2024]. The product natively exports COM, BER, bathtub, eye height/width, jitter, and crosstalk [MathWorks, "SerDes Toolbox" product page, 2024]. **Fidelity:** behavioral channel + EQ (AMI), not transistor-level. **Openness:** commercial but scriptable/reproducible with a free trial — the most defensible *open-provenance* generator for a released benchmark.
- **Commercial D2D-specific SI tools.** Keysight **Chiplet PHY Designer** models the forwarded-clock, single-ended, higher-BER UCIe D2D regime (not generic SerDes), emitting eye height/width/skew, mask margin, BER contours (1e-27/1e-32), and voltage transfer function [Keysight, news release, Jan. 2024]; the 2025 release adds **BoW** support, covering two of the three PHYs (UCIe/BoW/AIB) in scope [Keysight, news release, Jan. 2025]. Cadence **Sigrity SystemSI** Serial Link Analysis provides a third independent flow producing eye/bathtub/BER for UCIe channels including lower 4–16 GT/s modes [Cadence, Sigrity SystemSI datasheet, 2024]. **Fidelity:** channel-level SI with vendor-validated models. **Openness:** proprietary; valuable as cross-tool provenance, not as released artifacts.
- **Academic UCIe channel SI studies.** KAIST EDAPS work simulates the UCIe channel on a silicon interposer (voltage transfer function, eye) [KAIST, "SI Analysis of UCIe Channel in Si Interposer," IEEE EDAPS 2023, DOI 10.1109/EDAPS58880.2023.10468369] and demonstrates that temperature degrades the UCIe-A eye/VTF and dominates crosstalk at 80 °C [KAIST, "Thermal-Aware UCIe Interface Design in 2.5D/3D ICs," IEEE EDAPS 2023, DOI 10.1109/EDAPS58880.2023.10468234; see also "The Significance of Thermal-Aware UCIe Interface Design," IEEE doc 10468234, 2024]. A wide-I/O interposer crosstalk-included eye estimator generates eye diagrams from ~8 worst-case patterns [IEEE doc 7103637, 2014]. A peer-reviewed UCIe 2.5D SI study (interposer/RDL/micro-bump structures) exists but its venue/authors are unverified [Scribd-hosted copy, 2024 — low confidence, verify before citing]. **Fidelity:** full-wave/channel SI. **Openness:** papers public; flows proprietary.
- **Anomaly-labeling engines.** A fast statistical-eye engine for nonlinear high-speed links provides the BER/eye computation needed to *label* simulated degradation across parameter sweeps [IEEE TVLSI, 2021, DOI 10.1109/TVLSI.2021.3082208]. The **Channel Operating Margin (COM)** compliance method gives a single scalar link-health label for simulated perturbations [IEEE 802.3, 2013], and a UCIe IMAPS compliance flow establishes healthy baselines [IMAPS, 2023 — PDF would not decode].

**Critical mechanism for drift generation:** the AMI model becomes a *degradation* generator (not a one-shot compliance run) only when jitter/Gaussian-noise impairments are injected and channel/EQ parameters are swept to synthesize labeled healthy-vs-weak link telemetry [MathWorks, "Jitter Analysis in SerDes Systems," SerDes Toolbox docs, 2024].

### B.2 Defect & Fault Injection for Interconnects / TSV / Micro-bumps / RDL

This family supplies the **fault model** — how a physical defect maps to an electrical signature that the channel simulator then degrades.

- **Structural fault definitions (the D2D baseline).** The E2I-TEST line defines the canonical fault-model space for chiplet interconnects — hard plus **weak/resistive variants** of opens and physically-adjacent shorts/coupling — via an aliasing-free, diagnosis-capable ATPG needing only 16 patterns independent of interconnect count [P.-Y. Chuang, F. Lorenzelli, E. J. Marinissen, "Generating Test Patterns for Chiplet Interconnects With Optimized Effectiveness and Efficiency," IEEE TCAD, 2024, doc 10689272; ITC-Asia 2023]. The companion UCIe repair paper supplies the same weak-short/weak-open definitions [T.-H. Wang et al., "Test and Repair Improvements for UCIe," IEEE ETS 2024, doc 10567470]. A recent survey consolidates TSV/ILV fault models (short, delay, crosstalk) and repair [X. Liu et al., "Fault Modeling, Testing, and Repair for Chiplet Interconnects," Elsevier Integration, 2025].
- **Defect→electrical mapping primitives.** Lumped analytical RLC models for partially-cracked and void-hole TSVs (validated against a commercial 3-D RLC extractor) give the physics→circuit mapping for injecting resistive-open/partial-void anomalies into SPICE [IEEE doc 7154073, 2014]. Equivalent lumped-circuit models of voids/pinholes/missing-bump defects from 3-D full-wave simulation, with switched-capacitor parametric detection verified in HSPICE, extend this [IEEE doc 8525271, 2018, TVLSI/T-CPMT class]. A coexisting resistive-open + leakage TSV method shows a 100 Ω resistive open is detectable at 1 GHz, fixing realistic weak-open injection magnitudes and receiver-side detection limits [IEEE doc 9336637, 2021]. Hybrid-bonding yield models enumerate overlay misalignment, particle defects, Cu recess, and surface roughness as weak-bond drivers and can seed a synthetic defect population [arXiv:2511.05506 "YAP+," 2025].
- **Interposer/parametric test setups.** A perturbation-based oscillation-ring method detects small-delay faults on interposer wires (single-modality delay, one-time) [S.-Y. Huang et al., IEEE ITC 2013 / TVLSI 2014, doc 6651906]. Pre-bond e-fuse and IEEE 1149.1 scan-based post-bond architectures detect open/short/delay faults with HSPICE/ModelSim validation, providing reusable open/short/delay injection setups on interposer wires [DATE 2016 pre-bond + IEEE TVLSI scan-based post-bond].

**Fidelity:** lumped-element to full-wave; defect physics is well-grounded. **Openness:** models are published in papers; no packaged open injector exists — the fault library must be re-implemented.

### B.3 Thermal Simulation (HotSpot, 3D-ICE, CoMeT; 2.5D/3D traces)

This family produces the **temperature modality**. It is the most mature and most open of the families — but uniformly thermal-only.

- **Open interval/transient solvers for chiplet stacks.** **CoMeT** is an open-source integrated interval thermal simulator explicitly for 2D/2.5D/3D processor-memory systems and is a natural engine to generate chiplet thermal traces [L. Siddhu et al., "CoMeT," ACM TACO, 2022, arXiv:2109.12405]. **3D-ICE 4.0** is a state-of-the-art transient solver for 2.5D/3D heterogeneous chiplet+interposer systems from the Atienza/EPFL group [K. Zhu et al., arXiv:2512.05823, 2025]. **HotSpot 7.0** is the de-facto open pre-RTL engine for 2.5D→3D chiplet studies [IEEE iTherm 2022, doc 9899649], and **ATSim3.5D** extends open multiscale thermal modeling to stacked-chiplet 3.5D-IC with released code [arXiv:2601.11053, 2026]. **Fidelity:** interval/multiscale physics; design-time. **Openness:** all open-source — strong for a reproducible benchmark.
- **Fast surrogates and dataset-generation templates.** **MFIT** is a fast multi-fidelity thermal surrogate for generating large thermal-trace datasets across many chiplet configs/workloads [L. Pfromm et al., arXiv:2410.09188, 2024]. **ThermGCN** demonstrates the canonical dataset recipe (generate ground truth with HotSpot/CTM, train an ML surrogate) [L. Chen, W. Jin, S. X.-D. Tan, ASP-DAC 2022]. Efficient transient analyses [Applied Thermal Engineering 229:120609, 2023] and a 3DI multiscale workflow [arXiv:2602.06999, 2026] supply time-resolved hot-spot data. **Fidelity:** surrogate→multiscale. **Openness:** mixed (MFIT/CHIPSIM open).
- **Failure-physics-relevant thermal coupling.** Joule-heating thermal crosstalk degrades 2.5D micro-bumps in-field even in un-powered lanes — direct motivation that the thermal trace is causally coupled to link health [M. Li et al., J. Appl. Phys. 120(7):075105, 2016].

### B.4 PVT / Process-Variation / Aging (BTI/HCI/EM/Thermomechanical)

This family supplies the **degradation trajectory** — the time-evolving ground truth that makes a static benchmark a *drift* benchmark.

- **EM resistance-drift physics (the micro-bump/RDL wear core).** Black's-equation parameterization needs defensible activation energies: peer-reviewed Ea = 0.84–1.06 eV for the SnPb/SnAg/Cu-Ni stacks used in D2D bumps [H.-Y. Chen, C. Chen, J. Mater. Res., 2010], plus a fast low-Ea surface-diffusion branch (~0.45 eV) enabling a *bimodal* failure population [Cu surface-EM study, J. Appl. Phys., 2009; "New failure mechanism… surface diffusion of Sn," Sci. Rep., 2018]. The void-growth→resistance-drift mapping (step + linear-ramp R(t)) grounds the downstream eye/BER drift [Microelec. Reliab. EM resistance-evolution study, 2010]. TTF distribution choice (lognormal for void-growth-limited bump EM vs. Weibull for many-element structures) is settled with physical rationale [A. Basavalingappa et al., IEEE IIRW 2017, doc 8361224], with corroborating solder-joint Black/Weibull parameters [R. Darveaux, SMTA 2014] and alternative (Ea=0.88 eV, n=1.64) Cu-pillar pairs for sensitivity sweeps [Cu-pillar pulse-EM study, JMSE-ME, 2021; Materials 16(3):1134, 2023].
- **Thermomechanical fatigue (the thermal-cycling arm).** Fine-pitch Cu-microbump thermal-cycling fatigue, IMC growth, and pitch/material dependence parameterize a Coffin-Manson arm at realistic chiplet pitches [MDPI JMMP 6(4):18, 2025; Cu-pillar fatigue-crack lifetime, Frontiers in Materials, 2024]; interposer/TSV thermal-cycling reliability [MDPI Micromachines, PMC11356347, 2024]; and combined thermal+vibration+electrical TSV degradation establishing the *joint multi-stress* premise [Microelec. Reliab., 2022].
- **On-die aging/timing degradation models.** The "interconnect odometer" gives a silicon-validated BTI/HCI frequency-degradation model for interconnect drivers [Univ. of Minnesota, IEEE TVLSI, 2015]. **GNN4REL** is an ML surrogate over physics-based aging+PV characterization predicting path-delay degradation [L. Alrahis et al., IEEE TCAD, 2022, arXiv:2208.02868]. A broad aging-physics taxonomy (BTI/HCI/TDDB/EM) is surveyed in [S. J. Babu et al., arXiv:2503.21165, 2025].

**Fidelity:** materials-FEM and physics-of-failure; high. **Openness:** parameters are published (citable numbers), but no open end-to-end "defect-physics→telemetry" generator exists — this arm must be hand-built.

### B.5 Power-Delivery / Voltage-Droop (PDN) Simulation and On-Die Sensing

This family produces the **voltage modality** (droop, IR-drop, supply noise).

- **2.5D PDN simulation.** Frequency- plus time-domain PDN-noise simulation/optimization for 2.5D ICs supplies the droop-training-data generator [Y. Duan et al., arXiv:2407.04737, 2024]; canonical chiplet-interposer PDN/IR-drop modeling across micro-bumps/TSV/interposer establishes the droop physics [GT-CAD/Lim group, IEEE TCPMT, 2021, doc 9540833]; and electrothermal PDN co-optimization shows the V↔T coupling, albeit design-time only [Sci. Rep. 15:09914, 2025]. **EMSpice 2.1** couples IR-drop/current-density, Joule-heating thermal maps, and EM reliability physics to generate ground-truth EM/thermal degradation traces (on-die power grids, offline signoff) [S. Lamichhane, H. Lu, S. X.-D. Tan, arXiv:2507.00270, 2025]. **Fidelity:** PDN/electrical + coupled thermal. **Openness:** EMSpice open; commercial PDN flows proprietary.
- **On-die voltage sensing / inference (the in-field readout primitive).** Learned sparse-sensor→full-chip voltage inference (Group Lasso + OLS/SVM) is the methodological ancestor of the voltage branch [X. Liu et al., IEEE TCAD 36(7), 2017]. Real-time on-chip ML droop prediction is silicon-proven [R. Magod et al., IEEE JSSC/VLSI, 2023–2024], as is production distributed droop estimation [IBM z14, ISSCC-class, 2018]. **Disentanglement methods** are essential: a ring-oscillator reading mixes temperature and voltage, and paired ROs on test-vs-clean supply recover true IR-drop by exploiting temperature's slow time constant [IEEE ICCAD 2007, doc 4437591] — the technical kernel of why fusion (not a single timing sensor) is required.

### B.6 System/Architecture-Level Chiplet Simulation & Synthetic Telemetry for ML

This family produces **traffic/latency/link-event** telemetry (retrain/parity/Nak analogs) and the workload context that drives the other modalities.

- **D2D-specific functional/protocol simulators.** **MUG5** models the UCIe standard in gem5, capturing flit packing and Ack/Nak **retry** behavior — the closest existing analog to per-lane parity/retrain **link-event** telemetry [Li, Dong et al., IEEE doc 10396422, ~2023 — venue/year med-confidence]. **c2c-gem5** is a DATE 2025 full-system cache-coherent chip-to-chip interconnect simulator instrumentable for per-link traffic/latency/error traces [L. Bertran Alvarez et al., DATE 2025, doc 10992853]. A UCIe link-simulation/optimization study represents the decoupled link-side performance literature [IEEE doc 11087237, 2025].
- **Power+thermal+communication co-simulation (the closest multimodal seed).** **CHIPSIM** co-simulates power, thermal, and communication at µs granularity with explicit Network-on-Interposer modeling — the nearest existing tool to a workload-driven D2D telemetry generator [L. Pfromm et al., arXiv:2510.25958, 2024; code at github.com/LukasPfromm/CHIPSIM]. Crucially it does **not** model voltage droop/IR-drop, BER, eye margin, or lane skew, so it would need an electrical/link layer bolted on.
- **Fast traffic/telemetry generators.** **RapidChiplet** (open, ETH/Bologna) cheaply generates large volumes of inter-chiplet traffic/latency/throughput traces [P. Iff et al., arXiv:2311.06081, 2023]; **Muchisim** reports energy/performance per design [M. Orenes-Vera et al., Princeton, arXiv:2312.10244, 2023]; and an open multi-simulator stitching methodology provides a testbed template [H. Zhi et al., ACM NANOCOM 2021]. All are performance/energy-only with no anomaly labels.
- **ML-side templates for the fused dataset.** NASA PCoE benchmarks provide the dataset-construction precedent — CMAPSS is simulator-generated, and the IGBT set even fuses **voltage+thermal+current**, mirroring the multimodal idea for discrete power devices [NASA PCoE / NASA Open Data, 2008]. Generic multimodal-fusion anomaly detectors (e.g., MFGAN, AE/GAN) are mature in IIoT but none target chiplet/D2D telemetry — the cross-domain absence is itself evidence of the niche [Sensors/MDPI multimodal-fusion AD, 2024].

### Recommended Simulation Stack for OUR Released Multimodal D2D Telemetry Benchmark

The benchmark must emit, per lane and per timestep, four co-registered modalities with injected, physically-grounded degradation and ground-truth labels. We recommend a layered stack where a single **workload/operating-point driver** feeds parallel physics engines whose outputs are time-aligned:

| Modality | Recommended engine | Role | Openness |
|---|---|---|---|
| **Link (eye/BER/COM/jitter/skew)** | MathWorks SerDes Toolbox **UCIe 2.0 IBIS-AMI** `GetWave` + jitter/noise injection + EQ/channel sweeps [MathWorks 2024]; label with fast statistical-eye/COM [TVLSI 2021; IEEE 802.3 COM] | Primary observable; degrade via injected impairments mapped from defect models | Scriptable commercial (defensible provenance); cross-check with Cadence Sigrity / Keysight CPD |
| **Temperature** | **CoMeT** or **3D-ICE 4.0** transient 2.5D/3D solver [TACO 2022; arXiv:2512.05823], optionally MFIT surrogate for scale [arXiv:2410.09188] | Time-resolved thermal traces; drives thermal-coupling of eye/VTF [EDAPS 2023] | Fully open |
| **Voltage / droop** | **EMSpice 2.1** (coupled IR-drop + Joule heating) [arXiv:2507.00270] or 2.5D PDN frequency/time-domain sim [arXiv:2407.04737]; on-die readout modeled per RO-disentanglement [ICCAD 2007] | Droop/IR-drop traces co-driven by the same workload as thermal | EMSpice open; PDN tools mixed |
| **PVT / aging (degradation trajectory)** | Custom **fault-injection layer**: Black's-equation EM (lognormal/Weibull TTF) with literature Ea/n [J. Mater. Res. 2010; IIRW 2017; Materials 2023] + Coffin-Manson thermomechanical arm [JMMP 2025] → R(t) drift [Microelec. Reliab. 2010] → maps to defect→electrical models [doc 8525271; doc 9336637] | Generates ground-truth incipient drift that perturbs the link/voltage channels | Parameters published; generator must be built |
| **Link-event / retrain / parity** | **MUG5** (gem5 UCIe Ack/Nak retry) [doc 10396422] or **c2c-gem5** [DATE 2025], with **RapidChiplet** for traffic scale [arXiv:2311.06081] | Discrete RAS-event modality; workload driver for all engines | MUG5 unclear; c2c-gem5/RapidChiplet open |

**Integration recipe:** (1) a workload trace (RapidChiplet/CHIPSIM) sets per-lane activity → (2) drives CoMeT/3D-ICE (temperature) and EMSpice/PDN (voltage) in lockstep → (3) an EM+thermomechanical degradation layer evolves per-lane R(t) and mechanical state over simulated field-time → (4) the degraded RLC defect signature [doc 7154073/8525271] is injected into the UCIe AMI channel, which emits eye/BER/COM/skew → (5) MUG5/c2c-gem5 converts BER excursions into retrain/parity/Nak events. **CHIPSIM is the best single backbone** to time-align power+thermal+communication, extended with the missing electrical (droop) and link-SI (eye/BER) layers. Anchor the dataset's standards-provenance and modality realism on the UCIe spec's actual in-field telemetry registers (eye-margin, per-lane parity-flit/error log, retrain) [UCIe 2.0 Spec / Das Sharma, FMS 2024; UCIe in IEEE Micro, 2024] so the synthetic features match field-collectible signals.

### Coverage Gaps (No Good Open Simulator Exists)

1. **No unified multimodal generator.** No public tool jointly emits time-aligned voltage + temperature + PVT-drift + link/eye/BER per lane. CHIPSIM (power+thermal+comm) is closest but lacks droop, BER, eye, and skew entirely [arXiv:2510.25958]. **This is the central tooling gap our benchmark fills.**
2. **No open defect→telemetry fault injector.** EM/thermomechanical physics and defect→electrical RLC mappings are published as papers, but no packaged, open generator turns an injected micro-bump/RDL defect into a degraded eye/BER trace — it must be assembled from the §B.2/§B.4 primitives.
3. **No open, anomaly-labeled D2D telemetry dataset.** Architecture simulators (RapidChiplet, Muchisim, c2c-gem5) emit performance/energy only, with no health labels [arXiv:2311.06081; arXiv:2312.10244; DATE 2025].
4. **Open link-SI generation is weak.** All credible eye/BER/COM/skew engines (SerDes Toolbox, Keysight CPD, Sigrity) are commercial; the open ecosystem has no UCIe/BoW AMI channel simulator, forcing reliance on scriptable-but-proprietary flows for the most important modality.
5. **Coupling fidelity is fragmented.** V↔T coupling exists only in design-time co-optimization tools [Sci. Rep. 2025; EMSpice], and thermal→link-SI coupling exists only in standalone academic studies [EDAPS 2023] — no engine closes the loop from workload → coupled V/T → degraded link in one transient run.

---

## C. Motivation for Online Multimodal D2D Health Monitoring

Chiplet-based heterogeneous integration shifts a growing share of reliability risk onto the **die-to-die (D2D) interconnect itself** — the micro-bumps, redistribution layers (RDL), through-silicon vias (TSVs), hybrid bonds, and silicon-interposer routing that carry UCIe/BoW/AIB physical layers. The remainder of this section argues that the resulting failures are (i) physically real and in-field, (ii) invisible to one-time structural test, (iii) confounded by operating-condition drift in a way that defeats single-modality detection, and (iv) observable through telemetry that standards now expose — together motivating an *online, multimodal* health monitor that complements deterministic structural BIST.

### C.1 D2D links degrade in the field: failure mechanisms and physical evidence

D2D interconnects are not static once assembled; they wear out under mission-mode electrical and thermal stress. The two dominant advanced-packaging reliability concerns are **micro-bump electromigration (EM)** and **die-to-die thermo-mechanical stress** [Electronics360 2023]. Micro-bump EM is well documented as a *gradual* degradation path: current crowding and Joule heating at the solder/UBM/IMC interfaces nucleate voids that first raise contact resistance and only later produce hard opens [Micromachines 2023, PMC10301314; Micromachines 2023, mics14061255]. Crucially, EM on signal/AC interconnects induces *parametric shifts* — resistance drift and timing degradation — not merely catastrophic opens [UMinn dissertation 2016], establishing the "weak/parametric/drift anomaly" class that an online monitor must catch *before* a lane fails. The same parametric-drift physics is corroborated for the interconnect drivers themselves: BTI/HCI raise threshold voltage and produce continuous frequency/delay degradation, a drift that has been measured in-field at scale (median −0.064% over 280 days across 298 naturally aged FPGAs) [Lanzieri et al., arXiv:2412.15720, 2024], and the same wear-out mechanisms are explicitly named as upstream causes of on-chip "fail-slow" behavior [Wu et al., SlowPoke, arXiv:2510.24112, 2025].

Beyond EM, **thermo-mechanical fatigue** drives D2D degradation through CTE-mismatch-induced micro-bump and solder-joint cracking under thermal cycling, with cracks initiating at the IMC layer and propagating through coarsened solder grains — a slow wear-out that surfaces *first* as eye-margin/BER drift [Materials 2024, PMC11123225; Frontiers in Materials 2024]. Large silicon-interposer warpage and CTE mismatch fatigue the micro-bump/interconnect array [Microelectronics Reliability review 2023], and TSV microstructure has been shown to degrade under *combined* thermal-cycling, vibration, and electrical stress [Microelectronics Reliability 2022] — direct evidence that *multiple concurrent field stresses jointly* drive interconnect wear-out. The RDL routing that carries D2D signals cracks and delaminates at the Cu/dielectric interface under CTE-mismatch stress [ICEPT/EPTC 2022, doc 9873188]. Emerging fine-pitch substrates inherit these problems and add new ones: **hybrid bonding** (<10 µm pitch) exhibits warpage-induced interface voids, Cu-recess variation, particle defects, oxidation, and overlay misalignment that yield *weak/marginal* bonds [Cu-Cu Hybrid Bonding review 2025; YAP+, arXiv:2511.05506, 2025], and **glass-interposer** packages degrade signal/power integrity (insertion loss, PDN impedance, ground noise) through interconnect resonance and warpage [Micromachines 16(1):112, 2025]. A particularly telling result is that 2.5D micro-bumps degrade in-field via *thermal crosstalk* even in **un-powered/idle lanes** [Li et al., J. Appl. Phys. 120:075105, 2016] — degradation is fundamentally operating-condition-dependent, not a static manufacturing artifact. The reliability-physics community has organized around exactly this open problem, with IRPS 2025 workshops dedicated to silicon prognostics for in-field end-of-life RAS and to constructing bathtub curves for heterogeneous-integration products [IRPS 2025 WS2, WS5].

### C.2 Why online / in-field, not one-time structural test

Deterministic structural test of D2D interconnects is mature and standardized — aliasing-free ATPG detects all hard and weak shorts/opens in as few as 16 patterns regardless of interconnect count [Wang et al., ETS 2024, doc 10567470; Chuang et al., TCAD 2024, doc 10689272], and spare-lane *hard* repair (e.g., 12 redundant per 136 main lanes, E-fuse repair signatures) is shipping IP [Goriawalla & Zorian, Synopsys/TSMC blog 2025]. But this entire line is **manufacturing-time, pass/fail, and hard-fault-oriented**; none of it tracks the *time-evolution* of a marginal lane in mission mode. Three field realities make a one-time screen insufficient. First, **latent and marginal defects escape test and surface later**: hyperscaler studies document silent data corruption (SDC) / corrupt-execution-errors at fleet scale from defective chips that passed manufacturing test [Hochschild et al., "Cores that don't count," HotOS 2021; Dixit et al., "Silent Data Corruptions at Scale," arXiv:2102.11245, 2021; Google SOSP 2023], with test escapes estimated at ~10× and an explicit call for *in-field* detection [Mitra et al., arXiv:2508.01786, 2025]. Second, these failures are **aging- and operating-condition-dependent** — SDCs are tied to temperature and device age and are undetectable at manufacturing test [Farron, SOSP 2023; Vega, ASPLOS 2024], and the problem is now being traced into the *interconnect* domain (chiplet-to-chiplet link flapping and CRC-escape corruption) [Borrill, arXiv:2603.03736, 2026; GPU/NVLink resilience study, SC 2025]. Third, **mission-criticality demands continuous coverage**: automotive zero-defect/ISO 26262 requirements compound ppm risk across every link [Microelectronics Reliability 2008], motivating predictive maintenance over each chiplet interface, and UCIe's Automotive Working Group already mandates runtime link-health monitoring and repair [UCIe 1.1, BusinessWire 2023]. The temporal argument mirrors datacenter practice, where in-production continuous detection (e.g., Meta's Ripple) was adopted precisely because slow periodic test misses field-emergent faults [Dixit et al., arXiv:2203.08989, 2022]. In short, structural BIST answers "is this lane broken *now*?"; field reliability requires answering "is this lane *degrading*?" — an online question.

### C.3 Why multimodal: the confounding argument

The decisive technical motivation for fusing *voltage + thermal + link* telemetry is that **operating-condition drift can both mimic and mask defect signatures**, so any single modality yields false positives and false negatives. The confounding is measured and mechanistic on each axis:

- **Thermal confounds link timing/skew.** Within-die thermal gradients are a recognized *delay-fault mechanism* that induce clock skew indistinguishable from a structural skew fault unless thermal context is co-observed [Ajami et al., ITC 2003, doc 1387402; TVLSI 2006, doc 1704735]. The temperature→delay relation is itself *non-monotonic* (inverted temperature dependence, ITD), so the worst-case corner is neither hottest nor coldest, and a single temperature reading cannot be mapped to link health [Dasdan & Hom, TODAES 2006; ITD test studies, ISCAS 2012 / DATE 2013]. Most directly for our target, elevated temperature and gradients along a **UCIe-A interconnect significantly degrade signal integrity** (crosstalk, eye) at 32 Gb/s [Thermal-Aware UCIe, doc 10468234, 2024] — a link-only monitor will therefore confound thermal-driven eye collapse with defect-driven collapse.

- **Voltage/droop confounds link margin.** Supply droop and di/dt noise reorder path delays and produce both false failures and test escapes [Power-Supply-Droop study, ITC 2008], and reducing supply voltage *simultaneously* amplifies small-delay-defect sensitivity *and* process/voltage variation, so defect and benign variation become hard to separate [Jafarzadeh et al., JETTA 2025]. A BER/eye-margin excursion may thus be transient PDN noise rather than degradation.

- **Modalities are physically coupled and individually insufficient.** A raw ring-oscillator/timing sensor *cannot* separate IR-drop from heating without a second modality — recovering true IR-drop requires explicitly subtracting the thermal component using paired sensors [ICCAD 2007, doc 4437591], and isolating true BTI/HCI aging requires cancelling common-mode temperature/voltage drift via differential sensor pairs [Sengupta & Sapatnekar, TCAD 2017]. Because thermal drift → V-droop → eye-margin collapse form a coupled chain, naive per-feature attribution misassigns the cause [cf. BALANCE, SIGMOD 2023]. The general principle — that distinguishing benign drift from real degradation requires multimodal fusion — has been demonstrated in adjacent domains [M2D2, Applied Sciences 2025; ADWIN-gated software-aging detection, arXiv:2511.03103, 2025], but no published method does it for D2D links. This confounding is exactly why fusion (and cross-modal root-cause attribution) is the contribution, not the mere co-location of sensors.

### C.4 Standards and industry drivers make the telemetry set real (and partly mandated)

The motivation is not hypothetical because the three modalities are increasingly **co-available, standardized, and in some cases field-mandated on-die**. On the **link** axis, UCIe 1.1/2.0 standardizes eye-margin capture registers, software-triggered periodic retrain, per-lane parity-Flit injection/error-log "Run-time Testability of Link Health," lane-to-lane skew, BER measurement, and redundant-lane repair [UCIe Consortium 2.0, BusinessWire 2024; Das Sharma et al., IEEE Micro 2024; UCIe FMS 2024 SPOS-301-1], with UCIe 2.0 adding a standardized in-field telemetry/management fabric (UDA) and UCIe 3.0 explicitly framing the bottleneck as "predictable behavior across temperature, voltage, and workload transients" [Semiwiki/Alphawave 2025]. BoW (OCP/ODSA) and AIB add FEC/error-correction events and standardized thermal exchange (CDXML) [OCP BoW 2.0, 2023; Synopsys AIB test article 2021], and IEEE **P3405** standardizes chiplet-interconnect test-and-repair — confirming the surrounding ecosystem is structural/deterministic, which sharpens rather than fills the online-multimodal gap [Marinissen et al., VTS 2024, doc 10538776]. On the **voltage and thermal** axes, the building blocks already ship as IP: Synopsys SLM provides on-die Voltage Monitors, glitch detectors, distributed/catastrophic temperature sensors, and a central sensor hub [SemiWiki/Synopsys SLM PVT, 2025], on-die real-time ML voltage-droop prediction is silicon-proven [Magod et al., JSSC/TVLSI 2024], and compact *joint Vdd-temperature* fusion sensors now exist for SoC thermal management [Ozturk et al., JSSC 2025].

Critically, the industry has the sensors but **does not fuse them for D2D link health**. Synopsys's Multi-Die MTR ships Signal-Integrity Monitors at UCIe RX pins *alongside* PVT/aging monitors, yet treats them as **separate pipelines** — PVT enters only as repair-signature corners, not as fused inputs to link-anomaly inference [Goriawalla & Zorian, Synopsys/TSMC 2025; SLM SIM IP page]. proteanTecs — the closest in-field commercial competitor — co-locates per-lane interconnect agents (eye/jitter/skew) with voltage/thermal/workload agents on UCIe/BoW PHYs and markets "Agent fusion," but published material grades each modality *individually* and discloses no unified cross-modal model that fuses voltage-droop + thermal-drift + link features to detect weak/parametric/drift anomalies [proteanTecs D2D Monitoring; proteanTecs Advanced Packaging; VTS 2020 Deep Data]. Even an industrial UCIe AVS tape-out already co-uses voltage + temperature + eye-margin on the PHY — but the loop targets *power optimization*, not health detection [GUC AVS, EE Times 2024]. The closest academic analog, on-chip embedded-instrument *fusion-for-prognostics*, exists only for monolithic SoC critical-path end-of-life — never for D2D links and never with link-level (BER/eye/skew) modality [Ali et al., ISCAS/IOLTS/ATS 2020].

### Motivation in a nutshell (DATE-introduction form)

> Chiplet die-to-die interconnects degrade in the field — micro-bump electromigration, thermo-mechanical micro-bump/RDL/TSV fatigue, and weak hybrid-bond/interposer defects produce *parametric, gradual* resistance/eye-margin/BER drift rather than the hard shorts/opens that one-time structural BIST and spare-lane repair already solve [Micromachines 2023; Materials 2024; Cu-Cu Hybrid Bonding 2025; Wang et al., ETS 2024]. Because such marginal defects escape test and worsen with age, temperature, and voltage — the same regime hyperscalers blame for fleet-scale silent data corruption and that ISO 26262 and HPC availability cannot tolerate [Hochschild et al., HotOS 2021; Mitra et al., 2025; Farron, SOSP 2023] — D2D health must be tracked *online, in mission mode*, not screened once. Yet a single telemetry modality cannot do this: thermal gradients and supply droop *mimic and mask* link-degradation signatures (UCIe-A eye collapse with temperature, droop-induced delay reordering, non-monotonic ITD), so a link-only or sensor-only detector confuses benign operating-point drift with real wear-out [Thermal-Aware UCIe 2024; ITD/droop test studies; ICCAD 2007]. The required telemetry now exists and is partly mandated — UCIe/BoW expose eye-margin, BER, skew, and parity/retrain events while SLM-class IP provides on-die voltage and thermal sensors [UCIe 2.0/3.0; Das Sharma et al., IEEE Micro 2024; Synopsys SLM] — but industry and academia keep these streams in **separate pipelines** [Synopsys MTR; proteanTecs; Ali et al. 2020]. We therefore argue for an online detector that *fuses* voltage, thermal, and link telemetry to disambiguate and detect weak/parametric/drift D2D anomalies in-field, complementing — not replacing — deterministic structural BIST.

---

## D. New paper download list (round 3)

### Tier A — must-download

**A1. ChipletQuake: On-die Digital Impedance Sensing for Chiplet and Interposer Verification**
- Monfared, Saadat Safa, Tajik (WPI). arXiv:2504.19418, 2025. https://arxiv.org/abs/2504.19418
- Serves: **GAP / MOTIVATION**
- Why: Only on-die *electrical* (impedance/voltage-fluctuation) sensing across chiplet boundaries with a golden-signature-vs-field paradigm directly transferable to D2D health — single-modality, security-purposed, so it sharpens (not preempts) the multimodal claim. *(Note: explicitly named in the corpus' all_papers list; include only if your exclusion of "ChipletQuake" was meant for a different paper — otherwise drop.)*

**A2. Detecting Anomalies in Systems for AI Using Hardware Telemetry (Reveal)**
- Chen, Chien, Qian, Zilberman (Oxford). arXiv:2510.26008, 2025. https://arxiv.org/abs/2510.26008
- Serves: **MOTIVATION / method baseline**
- Why: Most recent multimodal *hardware-telemetry* fusion + unsupervised anomaly detection; proves the fusion-for-AD recipe is live and publishable, but at OS/system level — supplies a borrowable unsupervised pipeline.

**A3. An Electrical-Thermal Co-Simulation Model of Chiplet Heterogeneous Integration Systems**
- IEEE TVLSI, 2024. https://www.computer.org/csdl/journal/si/2024/10/10614207/1YYI2HiEXBu
- Serves: **SIMULATION / MOTIVATION**
- Why: Closest 2-modality (voltage IR-drop + thermal) coupled chiplet/interposer model; the partial-fusion precedent your testbed extends by adding the link modality.

**A4. CHIPSIM: A Co-Simulation Framework for Deep Learning on Chiplet-Based Systems**
- Pfromm, Kanani, Sharma, Doppa, Pande, Ogras. arXiv:2510.25958, 2024. Code: github.com/LukasPfromm/CHIPSIM. https://arxiv.org/abs/2510.25958
- Serves: **SIMULATION**
- Why: Open power+thermal+communication co-sim with explicit Network-on-Interposer — the closest workload-driven D2D telemetry generator; needs an electrical/link layer added (which is exactly your dataset contribution).

**A5. 3D-ICE 4.0: Accurate and Efficient Thermal Modeling for 2.5D/3D Heterogeneous Chiplet Systems**
- Zhu, Huang, Costero, Atienza (EPFL). arXiv:2512.05823, 2025. https://arxiv.org/abs/2512.05823
- Serves: **SIMULATION**
- Why: State-of-the-art 2.5D/3D chiplet+interposer transient thermal solver — most credible engine for physically-accurate thermal traces of D2D interfaces.

**A6. UCIe 2.0 Tx/Rx IBIS-AMI Model (SerDes Toolbox reference design) + Jitter/Noise impairment flow**
- MathWorks, 2024. https://www.mathworks.com/help/serdes/ug/ucie-transmitter-receiver-ibis-ami-model.html ; impairments: https://www.mathworks.com/help/serdes/ug/jitter-analysis-in-serdes-systems.html
- Serves: **SIMULATION**
- Why: Turnkey, scriptable UCIe-2.0 AMI model at 32 GT/s emitting eye/BER/COM/bathtub; jitter+Gaussian-noise injection + parameter sweeps convert it into a labeled healthy-vs-weak/drift link-telemetry generator — the link-modality side of the multimodal dataset, reproducible with standards provenance.

**A7. A Compact, Highly-Digital Sensor-Fusion-Based Joint Vdd–Temperature Sensor for SoC Thermal Management**
- Ozturk, Arenas, Tokunaga, Kurd, Sathe (incl. Intel). IEEE JSSC, 2025. https://ieeexplore.ieee.org/document/11219076/
- Serves: **MOTIVATION / building block**
- Why: Silicon-proven V+T co-sensing fusion primitive your detector can reuse — and another data point that V+T fusion exists in SoC space but link telemetry is never in the loop.

**A8. Reliable Interval Prediction of Minimum Operating Voltage Based on On-chip Monitors via Conformalized Quantile Regression**
- Yin, Wang, Chen, He, Li. DATE 2024; arXiv:2406.18536; DOI 10.23919/DATE58400.2024.10546601. https://arxiv.org/abs/2406.18536
- Serves: **GAP / method template**
- Why: Strongest semiconductor-native precedent for calibrated, distribution-free prediction intervals from on-chip monitors under real-silicon aging — the exact calibrated-interval template to transfer to D2D-link RUL; DATE-venue fit.

**A9. On-Chip Embedded Instruments Data Fusion and Life-Time Prognostics of Dependable VLSI-SoCs using ML (+ ATS/IOLTS siblings)**
- G. Ali, L. Bagheriye, H. G. Kerkhoff. ISCAS 2020, DOI 10.1109/ISCAS45731.2020.9180773 (siblings: IOLTS 10.1109/IOLTS50870.2020.9159753; ATS 10.1109/ATS49688.2020.9301509). https://ieeexplore.ieee.org/document/9180773
- Serves: **GAP (closest adversarial analog)**
- Why: The canonical "multimodal on-chip embedded-instrument fusion for prognostics" line — but SoC critical-path EOL, no link modality, no D2D; the exact "fusion exists for SoC EOL, not D2D online" boundary to differentiate against.

### Tier B — important

**B1. proteanTecs — "A Novel Approach to In-Field, In-Mission Reliability Monitoring Based on Deep Data"**
- Naveh, Tisherman, Pickholz et al., VTS 2020 / proteanTecs publication. https://www.proteantecs.com/resources/a-novel-approach-to-in-field-in-mission-reliability-monitoring-based-on-deep-data-publication
- Serves: **GAP (chief competitor, methods disclosure)**
- Why: The closest-to-archival statement of proteanTecs in-mission monitoring (cites 2.5D-package degradation); pin down what is actually disclosed vs. the "Agent fusion" marketing to scope novelty precisely.

**B2. Switching Frequency as FPGA Monitor: Degradation and Ageing Prognosis at Large Scale**
- Lanzieri, Butkowski, Kral, Fey, Schlarb, Schmidt. arXiv:2412.15720, 2024. https://arxiv.org/abs/2412.15720
- Serves: **GAP / MOTIVATION**
- Why: Proves in-field, large-scale (298 devices, 280 days), ML parametric-drift prognosis on real silicon is feasible — single-modality, non-interconnect, leaving D2D + true fusion open.

**B3. Learning High-Quality Latent Representations for Anomaly Detection & SI Enhancement in High-Speed Signals**
- Usama, Jang, Shanbhag, Sung, Bae, Chang (KAIST/Samsung). arXiv:2506.18288, 2025. Code/data public: github.com/Usama1002/learning-latent-representations
- Serves: **GAP / SIMULATION**
- Why: Nearest single-modality ML/SI anomaly baseline on a high-speed electrical (DRAM) interface, with open code+data — a reproducible comparator; offline, non-D2D, waveform-only.

**B4. MST-GAT: Multimodal Spatial–Temporal Graph Attention Network for TS Anomaly Detection**
- Ding, Sun, Zhao. Information Fusion 89:527–536, 2023. DOI 10.1016/j.inffus.2022.08.011. arXiv:2310.11169
- Serves: **GAP (method backbone)**
- Why: Explicit *inter-modal* attention = the "which modality (V vs T vs link) is anomalous" mechanism with built-in channel localization; the most transferable fusion+attribution architecture to adapt to D2D.

**B5. METER: A Dynamic Concept Adaptation Framework for Online Anomaly Detection**
- Zhu, Cai, Deng, Ooi, Zhang. PVLDB 17(4):794–807, 2024. DOI 10.14778/3636218.3636233. Code: github.com/zjiaqi725/METER
- Serves: **GAP (drift-adaptive baseline)**
- Why: SOTA "adapt-don't-retrain" hypernetwork+evidential drift control — the strongest drift-adaptation baseline beyond AE/LSTM-AE for a moving D2D "normal."

**B6. MemStream: Memory-Based Streaming Anomaly Detection**
- Bhatia, Jain, Srivastava, Kawaguchi, Hooi. WWW 2022, pp. 610–621. DOI 10.1145/3485447.3512221. Code: github.com/Stream-AD/MemStream
- Serves: **GAP (baseline + design idea)**
- Why: β-gated FIFO memory resists "memory poisoning," i.e., slow degradation being silently absorbed as new normal — exactly the failure mode an in-field D2D detector must avoid.

**B7. ARCUS: Adaptive Model Pooling for Online Deep Anomaly Detection from a Complex Evolving Stream**
- Yoon, Lee, Lee, Lee. KDD 2022. DOI 10.1145/3534678.3539348. arXiv:2206.04792
- Serves: **GAP (AE-wrapper baseline)**
- Why: Detector-agnostic wrapper that makes any AE/LSTM-AE drift-robust — concrete recipe + ablation for the methods section.

**B8. Graph Neural Network-Based Anomaly Detection in Multivariate Time Series (GDN)**
- Deng, Hooi. AAAI-21, 35(5):4027–4035. DOI 10.1609/aaai.v35i5.16523. Code: github.com/d-ailin/GDN
- Serves: **GAP (attribution/localization primitive)**
- Why: Learned top-k sensor graph + per-node deviation gives lane/bump-level root-cause localization; the natural backbone to map nodes→lanes for a D2D hotspot heatmap.

**B9. Anomaly Attribution with Likelihood Compensation (LC)**
- Idé, Dhurandhar, Navrátil, Singh, Abe. AAAI-21, 35(5):4131–4138. DOI 10.1609/aaai.v35i5.16535
- Serves: **GAP (attribution backbone)**
- Why: Principled per-variable responsibility scores for real-valued deviations — the formal "which telemetry channel fired the alarm" ranking once a fusion detector triggers.

**B10. Online False Discovery Rate Control for Anomaly Detection in Time Series**
- Rebjock, Kurt, Januschowski, Callot (Amazon/EPFL). NeurIPS 2021, pp. 26487–26498. arXiv:2112.03196
- Serves: **GAP (statistical guarantee)**
- Why: Model-agnostic wrapper giving a provable false-alarm/precision bound on top of any streaming detector — a differentiator vs. plain thresholded reconstruction error.

**B11. The Significance of Thermal-Aware UCIe Interface Design in 2.5D/3D ICs**
- IEEE doc 10468234 (EDAPS-class), 2023/2024. https://ieeexplore.ieee.org/document/10468234/
- Serves: **MOTIVATION (D2D-native confounder)**
- Why: On the exact target link (UCIe over interposer), temperature/gradients significantly move eye/crosstalk at 32 Gb/s — proves a link-only monitor confounds thermal vs. defect degradation, justifying T+link fusion.

**B12. GUC Taped Out UCIe 40 Gbps IP using Adaptive Voltage Scaling (AVS)**
- Global Unichip, EE Times, 2024. https://www.eetimes.com/guc-taped-out-ucie-40gbps-ip-using-adaptive-voltage-scaling-avs/
- Serves: **MOTIVATION (white-space sharpener)**
- Why: V+T+eye-margin already co-used on a UCIe PHY — but for *power optimization*, not health/anomaly detection; shows modalities are field-available yet unfused for monitoring.

**B13. Separating Temperature Effects from Ring-Oscillator Readings to Measure True IR-Drop**
- ICCAD 2007, IEEE doc 4437591. https://ieeexplore.ieee.org/document/4437591
- Serves: **MOTIVATION (technical kernel of fusion)**
- Why: Demonstrates a single timing sensor cannot separate droop from heating without a second modality — the canonical V/T-disentanglement argument underpinning multimodal fusion.

**B14. Within-Die Thermal Gradient Impact on Clock Skew: A New Type of Delay-Fault Mechanism**
- Ajami, Banerjee, Pedram. IEEE doc 1387402, 2003 (journal ext.: TVLSI doc 1704735, 2006)
- Serves: **MOTIVATION (skew confounder)**
- Why: Thermal gradients produce skew indistinguishable from a structural skew fault — direct analog for thermal drift masquerading as D2D lane-skew anomalies.

**B15. Comparative Analysis of Aging-Forecasting Methods for Semiconductor Devices in Online Health Monitoring**
- Villalobos, Barrutia, Peña-Alzola, Dragičević, Aizpurua. Eng. Appl. of AI 150:110545, 2025; arXiv:2503.20403
- Serves: **SIMULATION / MOTIVATION (forecasting baseline)**
- Why: Rigorous benchmark of online aging-forecasting methods (esp. covariate-aware Temporal Fusion Transformer) directly applicable to forecasting eye-margin/BER drift; single-modality MOSFET target.

### Tier C — supplementary

**C1. Predicting the Silent-Data-Error-Prone Devices Using Machine Learning**
- proteanTecs et al. VTS 2023. https://ieeexplore.ieee.org/document/10140097/
- Serves: **MOTIVATION** — Fuses aging+voltage+temperature+test data with ML to flag SDC-prone parts; closest "V+T+aging is predictive" evidence, but device-screening, no link telemetry.

**C2. Understanding Silent Data Corruptions in a Large Production CPU Population (Farron)**
- Wang, Zhang, Wei, Wang, Wu, Luo (Alibaba/Tsinghua/OSU). SOSP 2023. DOI 10.1145/3600006.3613149
- Serves: **MOTIVATION** — Quantifies 361 DPPM SDC and ties less-reproducible SDCs to *temperature*, supporting the thermal-telemetry-is-predictive premise.

**C3. Proactive Runtime Detection of Aging-Related SDCs: A Bottom-Up Approach (Vega)**
- Ma, Ganaiem, Burbage, Gregersen, McAmis, Gabbay, Kasikci (UW/Technion). ASPLOS 2024. DOI 10.1145/3622781.3674182
- Serves: **MOTIVATION** — Frames SDC as aging- and V/T-dependent and undetectable at manufacturing test; closest in spirit (online, aging, V/T-aware), but compute-core, no sensor fusion.

**C4. Silent Data Corruption by 10× Test Escapes Threatens Reliable Computing**
- Mitra, Banerjee, Dixon, Govindaraju, Hochschild, Liu, Parthasarathy, Ranganathan (Stanford/Google). arXiv:2508.01786, 2025
- Serves: **MOTIVATION** — Very recent quantitative motivation (10× escapes) with explicit call for in-field detection.

**C5. SlowPoke: Detecting On-Chip Fail-Slow Failures in Many-Core Systems**
- Wu et al. arXiv:2510.24112, 2025
- Serves: **GAP** — Adjacent runtime per-link bandwidth-degradation detection on intra-chip NoC; single behavioral modality, not D2D — sharpens the "D2D-native, multimodal" contrast.

**C6. c2c-gem5: Full-System Simulation of Cache-Coherent Chip-to-Chip Interconnects**
- Bertran Alvarez, Chehaibar, Busch, Benoit, Novo. DATE 2025. https://ieeexplore.ieee.org/document/10992853/
- Serves: **SIMULATION** — DATE-current full-system D2D interconnect simulator instrumentable for per-link traffic/latency/error telemetry (functional layer, no PHY health).

**C7. MUG5: Modeling of UCIe Standard Based on gem5**
- Li, Dong et al. IEEE doc 10396422, ~2023. https://ieeexplore.ieee.org/document/10396422/
- Serves: **SIMULATION** — UCIe link model with flit packing + Ack/Nak retry behavior = a link-event (parity/retrain analog) telemetry source to extend toward synthetic event traces.

**C8. Keysight Chiplet PHY Designer 2025 (UCIe 2.0 + BoW)**
- Keysight, 2025. https://www.keysight.com/us/en/about/newsroom/news-releases/2025/0121-pr25-026-keysight-expands-chiplet-interconnect-standards-support-in-chiplet-phy-designer-2025.html
- Serves: **SIMULATION** — Commercial alternate-provenance generator covering UCIe + BoW eye/skew/BER-contour telemetry; broadens benchmark beyond UCIe and beyond MathWorks.

**C9. MFIT: Multi-Fidelity Thermal Modeling for 2.5D/3D Multi-Chiplet Architectures**
- Pfromm, Kanani, Sharma, Solanki, Tervo, Park, Doppa, Pande, Ogras. arXiv:2410.09188, 2024
- Serves: **SIMULATION** — Fast multi-fidelity thermal surrogate for generating large thermal-trace datasets across many chiplet configs/workloads.

**C10. A Review of Multiscale Thermal Modeling in Heterogeneous 3D ICs**
- Barua, Udoy, Aziz. arXiv:2604.03290, 2026
- Serves: **MOTIVATION** — 2026 survey explicitly warning against decoupled electrical/thermal analysis and calling for in-situ sensing — strong anchor for electrical+thermal fusion (still omits link integrity).

**C11. Small Delay Fault Testing with Multiple Voltages under Variations: Defect vs. Fault Coverage**
- Jafarzadeh, Klemme, Amrouch, Hellebrand, Wunderlich. JETTA, 2025. DOI 10.1007/s10836-025-06172-8
- Serves: **MOTIVATION (voltage confounder)** — Recent evidence that lowering Vmin amplifies both defect sensitivity *and* PV variation, so a voltage-blind detector confuses defect with benign drift.

**C12. Adaptive Detection of Software Aging under Workload Shift**
- Silva, Nascimento, Machida, Andrade. SSCAD 2025 / arXiv:2511.03103
- Serves: **MOTIVATION (analogy)** — Clean 1:1 software mirror: separate benign workload drift from true aging via ADWIN gating; portable strategy for thermal/voltage operating-point drift vs. real link degradation.

**C13. Estimating Circuit Aging Due to BTI and HCI Using Ring-Oscillator-Based Sensors**
- Sengupta, Sapatnekar. TCAD, 2017
- Serves: **MOTIVATION (disentanglement method)** — Differential stressed-vs-unstressed RO pairs cancel common-mode T drift to isolate true aging; precedent for separating incipient degradation from benign drift.

**C14. BALANCE: Bayesian Linear Attribution for Root Cause Localization**
- Chen et al. PACMMOD/SIGMOD 2023. DOI 10.1145/3588949. arXiv:2301.13572
- Serves: **GAP (correlation-aware attribution baseline)** — BMFS handles collinear candidate causes; useful comparator to argue physically-coupled telemetry (T→Vdroop→eye) needs physics-aware, not off-the-shelf, attribution.

**C15. EMSpice 2.1: Coupled EM + IR-Drop Analysis with Joule Heating and Thermal-Map Integration**
- Lamichhane, Lu, Tan (UC Riverside). arXiv:2507.00270, 2025
- Serves: **SIMULATION** — Physics-based EM/IR/thermal coupling to generate ground-truth degradation traces; on-die power-grid focus, no link modality (the part you add).

---

**Notable exclusions beyond the named core set:** all duplicate proteanTecs/Synopsys-MTR/SLM-PVT/UCIe-spec entries (kept only the single most-archival proteanTecs *publication*, B1); generic drift-detection classics already canonical (ADWIN, ECDD/EWMA, RNN-drift Saurav 2018) — cite from memory, no download needed; pure-aerospace RUL/conformal method-origin papers (Javanmardi C-MAPSS, GRU-CNN RF-RUL) — methodologically subsumed by A8; and structural-test/EM-physics parameterization papers (TSV/micro-bump Ea values, hybrid-bonding yield), which are second-order simulation parameter sources rather than novel reads.

---

## E. Verified-evidence appendix (web-confirmed this round)

### Verified — GAP — preemption / near-miss (32)

- **[confirmed]** T.-H. Wang, P.-Y. Chuang, F. Lorenzelli, and E. J. Marinissen, "Test and Repair Improvements for UCIe," in Proc. 2024 IEEE European Test Symposium (ETS), The Hague, Netherlands, May 2024, pp. 1-6. IEEE Xplore document 10567470. NOTE: The candidate's claimed venue "VLSI Test Symposium (VTS) 2024" is INCORRECT. The paper is an IEEE European Test Symposium (ETS) 2024 paper — confirmed by (a) the IEEE Xplore PDF path iel8/10567048/... where conhome 10567048 is ETS 2024, and (b) an independent citation in arXiv:2503.14784 ([18] "T.-H. Wang et al., 'Test and repair improvements for UCIe,' in IEEE European Test Symposium (ETS), 2024, pp. 1-6"). All four authors are affiliated with imec. (imec did run a related Special Session / IEEE Std P3405 standard discussion at BOTH VTS 2024 and ETS 2024, which likely caused the venue confusion.)  
  https://ieeexplore.ieee.org/document/10567470/  
  _ADJACENT / strong contrast point — does NOT preempt and does NOT even partially overlap our online-multimodal thesis. Skeptical axis-by-axis audit: (1) ONLINE/IN-FIELD? NO. This is production/manufacturing structural test — a deterministic 16-pattern test for shorts/opens applied at test time (wafer/package ATE or s..._
- **[confirmed]** Junchi Wu, Xinfei Wan, Zhuoran Li, Yuyang Jin, Guangyu Sun, Yun Liang, Diyu Zhou, Youwei Zhuo. "SlowPoke: Understanding and Detecting On-Chip Fail-Slow Failures in Many-Core Systems." arXiv preprint arXiv:2510.24112 [cs.AR], submitted 28 Oct 2025 (rev. 25 Feb 2026). (Note: a revised version of the same arXiv ID 2510.24112 also appears under the title "Towards Efficient and Accurate Detection of On-Chip Fail-Slow Failures for Many-Core Accelerators.")  
  https://arxiv.org/abs/2510.24112  
  _ADJACENT, not preemptive — this does NOT undercut the project's white-space claim. Axes it HAS: (a) ONLINE/runtime detection (on-the-fly trace compression in on-chip SRAM); (b) link-level degradation detection (per-link bandwidth-degradation inference via EM) framed as gradual/parametric "fail-slow" rather than hard..._
- **[confirmed]** proteanTecs Ltd., "Die-to-Die Interconnect Monitoring" / "Advanced Packaging Solution" — Tile-Connectivity Agents (TCA) and Core Agents for on-chip monitoring and Deep Data Analytics. Commercial IP / white papers and technical blogs, 2022–2025. UCIe Consortium contributing member (joined Aug 2022). Demonstrated on Global Unichip Corp. (GUC) GLink/GLink-2.0 5nm die-to-die test chip (announced 2022). Primary sources: proteanTecs product page, https://www.proteantecs.com/die-to-die-interconnect-monitoring ; "GUC GLink Test Chip Uses In-Chip Monitoring and Deep Data Analytics for High Bandwidth Die-to-Die Characterization" (white paper/resource); proteanTecs blog "The Future of Chiplet Reliability: Interconnect Failure Prediction with 100% Lane Coverage." Third-party corroboration: PR Newswire 301627067 (UCIe join) and 301660037 (GUC GLink); Yole Group; EE Times Asia; eeNews Europe; SemiWiki.  
  https://www.proteantecs.com/die-to-die-interconnect-monitoring  
  _This is the single most important and most contested item for our positioning — the closest in-field COMMERCIAL competitor — so it must be cited and differentiated explicitly, but it does NOT preempt our novelty. Axis-by-axis skeptical read: (1) ONLINE / in-field: YES — explicit in-mission, functional-mode continuou..._
- **[confirmed]** F. Goriawalla and Y. Zorian, "Multi-Die Health and Reliability: UCIe Innovations with TSMC," Synopsys Chip Design Blog, Jan. 9, 2025. https://www.synopsys.com/blogs/chip-design/multi-die-health-reliability-advances.html (republished as "Multi-Die Health and Reliability: Synopsys and TSMC Showcase UCIe Advances," Design&Reuse, Jan. 16, 2025; and F. Goriawalla, "Monitor, Test, And Repair For Multi-Die Health And Reliability," Semiconductor Engineering, 2024/2025). Supporting product collateral: Synopsys, "SLM Signal Integrity Monitor (SIM) IP," product page and datasheet (slm-sim-ip-ds.pdf); Synopsys, "Effective Monitoring, Test, and Repair of Multi-Die Designs," white paper (multi-die-effective-test-mtr-wp.pdf), 2023-2025.  
  https://www.synopsys.com/blogs/chip-design/multi-die-health-reliability-advances.html  
  _Synopsys/TSMC technical-bulletin and blog material describing the Synopsys Monitor, Test & Repair (MTR) IP for UCIe multi-die interconnects, part of the broader Synopsys Silicon Lifecycle Management (SLM) and Test family. The solution embeds Signal Integrity Monitors (SIMs) at each UCIe receiver pin that continuousl..._
- **[confirmed]** proteanTecs, "On-Chip Monitoring and Deep Data Analytics System" (white paper) and "Die-to-Die Interconnect Monitoring" / "Advanced Packaging" solution brief, proteanTecs Ltd., 2022–2024. https://www.proteantecs.com/die-to-die-interconnect-monitoring ; https://www.proteantecs.com/resources/on-chip-monitoring-and-deep-data-analytics-system . Related industrial disclosures: N. Sever, "Performance and Reliability Monitoring of Die-to-Die Interfaces," and N. Basoco (keynote), "Leverage Agents to Boost Chiplet Design and Reliability," Chiplet Summit, San Jose, CA, Jan 24–26, 2023; proteanTecs joins UCIe Consortium (PR Newswire, Sep 2022); GUC GLink 2.0 5nm test-chip deployment of proteanTecs D2D interconnect monitoring (2022–2023). Industrial whitepaper / product technology — not peer-reviewed.  
  https://www.proteantecs.com/die-to-die-interconnect-monitoring  
  _CLOSEST PRIOR ART / chief competitor — keep and position against directly, but it does NOT fully preempt the thesis; it PARTIALLY overlaps. Axes it HAS: (i) Lane-granular D2D PHY instrumentation — Interconnect/Tile-Connectivity Agents embedded in the PHY, 100% lane+pin coverage, per-lane grading of eye width, jitter..._
- **[confirmed]** F. Goriawalla and Y. Zorian, "Multi-Die Health and Reliability: Synopsys and TSMC Showcase UCIe Advances," Synopsys Chip Design Blog, Jan. 9, 2025. [Online]. Available: https://www.synopsys.com/blogs/chip-design/multi-die-health-reliability-advances.html (page nav title: "Multi-Die Health and Reliability: UCIe Innovations with TSMC"). Mirrored at Design&Reuse, Jan. 16, 2025.  
  https://www.synopsys.com/blogs/chip-design/multi-die-health-reliability-advances.html  
  _SKEPTICAL VERDICT: ADJACENT / supports-the-gap — it does NOT preempt the thesis novelty. This is the strongest possible single vendor data point for the white-space claim because it is the most advanced shipping D2D-health offering (Synopsys MTR + TSMC silicon) and it still stops well short of multimodal online fusi..._
- **[confirmed]** Kalar Rajendiran, "The Growing Importance of PVT Monitoring for Silicon Lifecycle Management," SemiWiki (sponsored/industry technical article on Synopsys SLM PVT subsystem), April 24, 2025. URL: https://semiwiki.com/eda/synopsys/355230-the-growing-importance-of-pvt-monitoring-for-silicon-lifecycle-management/ . NOTE: The candidate-supplied Semiengineering URL (https://semiengineering.com/the-ever-increasing-role-of-pvt-monitor-ip-and-its-significance-in-silicon-lifecycle-management/) is a closely related companion article, "The Ever-Increasing Role Of PVT Monitor IP And Its Significance In Silicon Lifecycle Management" (Semiconductor Engineering, Synopsys), NOT the source bearing the candidate's exact title; the "2023" year and exact title in the candidate record are mismatched. Both are non-peer-reviewed vendor/marketing-adjacent pieces describing the same Synopsys DesignWare SLM PVT subsystem (Process Detector, Voltage Monitor, Glitch Detector, Temperature/Distributed/Catastrophic Temperature Sensors, Thermal Diode, central Sensor Management Hub / PVT Controller). Underlying primary substrate: Synopsys SLM PVT Monitor IP product collateral and PR Newswire announcement "Synopsys DesignWare PVT Subsystem Drives Performance, Power and Silicon Lifecycle Management on TSMC's N3," May 27, 2021.  
  https://semiwiki.com/eda/synopsys/355230-the-growing-importance-of-pvt-monitoring-for-silicon-lifecycle-management/  
  _VERDICT: ADJACENT / enabling-substrate — does NOT preempt the thesis novelty; partial overlap only on the sensing-modality axis, none on the application axis. Axis-by-axis: VOLTAGE telemetry — YES (Voltage Monitor + glitch detectors, IR-droop/noise sensing). THERMAL telemetry — YES (TS/DTS/CTS/thermal diode). PROCES..._
- **[confirmed]** M. Usama, H.-D. Jang, S. Shanbhag, Y.-C. Sung, S.-J. Bae, and D. E. Chang, "Learning High-Quality Latent Representations for Anomaly Detection and Signal Integrity Enhancement in High-Speed Signals," arXiv preprint arXiv:2506.18288 [cs.LG], Jun. 2025. (KAIST School of Electrical Engineering; Samsung Electronics DRAM Design Team). DOI: 10.48550/arXiv.2506.18288. Code/data: https://github.com/Usama1002/learning-latent-representations  
  https://arxiv.org/abs/2506.18288  
  _SKEPTICAL VERDICT: ADJACENT, not preempting. This is the closest published ML anomaly-detection method on a high-speed electrical memory interface, and it is the strongest single-modality "methods baseline" comparator for our work — but on every axis that defines our novelty it falls short, so it does NOT preempt ou..._
- **[confirmed]** L. Lanzieri, L. Butkowski, J. Kral, G. Fey, H. Schlarb, and T. C. Schmidt, "Switching Frequency as FPGA Monitor: Studying Degradation and Ageing Prognosis at Large Scale," arXiv preprint arXiv:2412.15720 [cs.AR], Dec. 2024. DOI: 10.48550/arXiv.2412.15720.  
  https://arxiv.org/abs/2412.15720  
  _ADJACENT — does NOT preempt our novelty, only a methodological/scale precedent. Axes PRESENT: (1) ONLINE / in-field monitoring — yes, genuinely deployed, 280 days, 298 devices at European XFEL; this is its strongest contribution and a strong scale precedent. (2) Aging PROGNOSIS via ML forecasting — yes (theta model,..._
- **[confirmed]** G. Ali (S. M. Ghazanfar Ali), L. Bagheriye, and H. G. Kerkhoff, "On-Chip Embedded Instruments Data Fusion and Life-Time Prognostics of Dependable VLSI-SoCs using Machine-Learning," in Proc. 2020 IEEE International Symposium on Circuits and Systems (ISCAS), Seville, Spain (virtual), Oct. 2020, pp. 1-5. DOI: 10.1109/ISCAS45731.2020.9180773. (University of Twente.) NOTE: The candidate metadata mis-attributed the venue to "IEEE IOLTS / ATS (2020)." IEEE Xplore document 9180773 is in fact ISCAS 2020. This is one of three sibling 2020 papers from the same group on the same body of work: (a) this ISCAS paper (PCA fusion + power-law degradation model); (b) L. Bagheriye, G. Ali, H. G. Kerkhoff, "Life-Time Prognostics of Dependable VLSI-SoCs using Machine-learning," IOLTS 2020, pp. 1-4, DOI 10.1109/IOLTS50870.2020.9159753 (ICA + auto-encoder fusion); and (c) G. Ali, L. Bagheriye, H. Manhaeve, H. G. Kerkhoff, "On-chip EOL Prognostics Using Data-Fusion of Embedded Instruments for Dependable MP-SoCs," ATS 2020, DOI 10.1109/ATS49688.2020.9301509 (PCA + ARULE EOL tool). The autoencoder/ICA mentioned in the flag is from the IOLTS sibling; the ISCAS paper itself uses PCA.  
  https://ieeexplore.ieee.org/document/9180773  
  _This is ADJACENT-to-PARTIAL prior art that SUPPORTS the white-space rather than preempting it; it should be cited as the single closest "fusion-for-prognostics" analog and explicitly differentiated. Axis-by-axis, skeptically:  (1) Multimodal fusion: YES — this is its core contribution. It fuses multiple on-chip IJTA..._
- **[confirmed]** G. Ali (S. M. Ahmed Ali), L. Bagheriye, H. Manhaeve, and H. G. Kerkhoff, "On-chip EOL Prognostics Using Data-Fusion of Embedded Instruments for Dependable MP-SoCs," in Proc. 29th IEEE Asian Test Symposium (ATS), 2020, pp. 1-6. doi: 10.1109/ATS49688.2020.9301509.  
  https://ieeexplore.ieee.org/document/9301509/  
  _SKEPTICAL VERDICT: ADJACENT closest-prior-art — it does NOT preempt the novelty; at most it establishes the GENERIC technique (on-chip embedded-instrument data fusion for prognostics) that we re-target to a new domain. Axes present: (1) ON-CHIP embedded telemetry via IJTAG/embedded instruments — YES; (2) MULTI-SENSO..._
- **[confirmed]** M. Hasanzadeh, K. Khalil, C. Sturton, and A. Patooghy, "HeatSense: Intelligent Thermal Anomaly Detection for Securing NoC-Enabled MPSoCs," IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD), 2026 (early access, IEEE Xplore doc. 11361147). Preprint: arXiv:2504.11421 [cs.AR], Apr. 2025.  
  https://arxiv.org/abs/2504.11421  
  _ADJACENT, does NOT preempt our novelty. Skeptical axis-by-axis breakdown: (a) MODALITY — single physical modality (temperature only). It also reads NoC-internal metrics (congestion, packet routing/traffic) but these are network-performance signals, not independent electrical telemetry; there is NO voltage/PDN-droop ..._
- **[confirmed]** UCIe Consortium, "Universal Chiplet Interconnect Express (UCIe) Specification, Revision 2.0," UCIe Consortium, August 6, 2024. Available (by request) at https://www.uciexpress.org/specifications. Press release: "UCIe Consortium Releases 2.0 Specification Supporting Manageability System Architecture and 3D Packaging," Business Wire, Aug. 6, 2024. See also D. Das Sharma (UCIe Consortium), "UCIe: An Open Industry Standard for Chiplets" / manageability overview, presented at Future of Memory and Storage (FMS) 2024, SPOS-301-1, Aug. 8, 2024.  
  https://www.uciexpress.org/specifications  
  _ADJACENT / ENABLING — does NOT preempt the proposed novelty; it strengthens feasibility. Verdict by axis: (1) LINK modality — STRONG native coverage. UCIe natively standardizes the link-quality telemetry our thesis needs: per-lane parity-Flit health checks + error-log register ("Run-time Testability of Link Health")..._
- **[confirmed]** Aaron Yen, Jooyeon Jeong, and Puneet Gupta, "Link Quality Aware Pathfinding for Chiplet Interconnects," arXiv preprint arXiv:2603.11612 [cs.AR], submitted 12 March 2026 (University of California, Los Angeles).  
  https://arxiv.org/abs/2603.11612  
  _VERDICT: ADJACENT / orthogonal. Does NOT preempt our novelty and does not even partially overlap on the core contribution. The original flag rationale is correct.  Axis-by-axis (4 axes of our thesis): (1) ONLINE / IN-FIELD - LACKS. Purely DESIGN-TIME (pre-silicon) pathfinding and link-assignment optimization. RTL sy..._
- **[confirmed]** K. Shibin, M. Jenihhin, A. Jutman, S. Devadze, and A. Tsertov, "On-Chip Sensors Data Collection and Analysis for SoC Health Management," in Proc. 2023 IEEE 36th International Symposium on Defect and Fault Tolerance in VLSI and Nanotechnology Systems (DFT), Juan-Les-Pins, France, 2023, pp. 1-6 (Special Session "Towards cross-layer resilience"). doi: 10.1109/DFT59622.2023.10313562. Preprint: arXiv:2308.15917. Affiliations: Tallinn University of Technology and Testonica Lab OU, Tallinn, Estonia.  
  https://arxiv.org/abs/2308.15917  
  _ADJACENT prior art — it does NOT preempt the thesis and only weakly motivates it. Skeptical axis-by-axis verdict against the thesis claim (fuse voltage+thermal+link telemetry for ONLINE D2D link health detection):  (1) MULTIMODAL? Only superficially. The abstract lists several sensor information categories (faults, ..._
- **[confirmed]** X. Liu, S. Sun, X. Li, H. Qian, and P. Zhou, "Machine Learning for Noise Sensor Placement and Full-Chip Voltage Emergency Detection," IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD), vol. 36, no. 7, pp. 1158-1171, July 2017. DOI: 10.1109/TCAD.2016.2611502. (Published online 2016.) Affiliations: ShanghaiTech University (Liu, Zhou); Carnegie Mellon University ECE (Sun, Li); IBM T. J. Watson Research Center (Qian).  
  https://ieeexplore.ieee.org/document/7572159  
  _ADJACENT methodological precedent — does NOT preempt our novelty; overlaps on exactly one axis (voltage modality + learned inference) and is absent on every other axis. Skeptical axis-by-axis breakdown:  HAS: - Voltage modality: on-die noise sensors monitoring runtime supply-voltage fluctuations. (one of our three m..._
- **[confirmed]** Y. Yin, X. Wang, R. Chen, C. He, and P. Li, "Reliable Interval Prediction of Minimum Operating Voltage Based on On-chip Monitors via Conformalized Quantile Regression," in Proc. Design, Automation & Test in Europe Conference & Exhibition (DATE), 2024, IEEE/ACM. arXiv:2406.18536. DOI: 10.23919/DATE58400.2024.10546601.  
  https://arxiv.org/abs/2406.18536  
  _CONFIRMED REAL (DATE 2024; also on arXiv and IEEE Xplore doc 10546601; a follow-on DAC 2024 paper "Data-Efficient Conformalized Interval Prediction of Vmin" extends it). This is the strongest semiconductor-native precedent for CALIBRATED, distribution-free prediction intervals with finite-sample coverage derived fro..._
- **[confirmed]** W. Yang, K. Wu, B. Long, and S. Tian, "A Novel Method for Remaining Useful Life Prediction of RF Circuits Based on the Gated Recurrent Unit–Convolutional Neural Network Model," Sensors (Basel), vol. 24, no. 9, art. 2841, 2024. doi: 10.3390/s24092841. PMCID: PMC11086388.  
  https://www.mdpi.com/1424-8220/24/9/2841  
  _ADJACENT — does NOT preempt our novelty; only weakly supports the gap framing. Skeptical axis-by-axis: (a) ONLINE/in-field health monitoring: NO. This is offline RUL prediction over a degradation trajectory, not real-time/in-field anomaly detection complementing structural BIST. (b) D2D interconnect / chiplet / UCIe..._
- **[confirmed]** A. Javanmardi and E. Hüllermeier, "Conformal Prediction Intervals for Remaining Useful Lifetime Estimation," International Journal of Prognostics and Health Management (IJPHM), vol. 14, no. 2, 2023. DOI: 10.36001/ijphm.2023.v14i2.3417. Preprint: arXiv:2212.14612 (2022). Code: github.com/alireza-javanmardi/conformal-RUL-intervals  
  https://arxiv.org/abs/2212.14612  
  _ADJACENT, a pure methods-origin paper that does NOT preempt our novelty on any application axis. Axes it HAS: (a) RUL/prognostics framing; (b) distribution-free uncertainty quantification via split/normalized CP and CQR-style intervals, exactly the calibration toolbox we would import; (c) deep CNN and gradient-boost..._
- **[confirmed]** Jiaqi Zhu, Shaofeng Cai, Fang Deng, Beng Chin Ooi, and Wenqiao Zhang. "METER: A Dynamic Concept Adaptation Framework for Online Anomaly Detection." Proceedings of the VLDB Endowment (PVLDB), vol. 17, no. 4, pp. 794-807, 2023/2024. DOI: 10.14778/3636218.3636233. Also arXiv:2312.16831 (Dec. 2023). Code: https://github.com/zjiaqi725/METER  
  https://www.vldb.org/pvldb/vol17/p794-zhu.pdf  
  _VERDICT: ADJACENT — a methodological template, NOT a preemption of our novelty. It overlaps on ZERO of our three claimed-novelty axes.  Axis-by-axis (our thesis = multimodal fusion of voltage+thermal+link telemetry for ONLINE D2D chiplet link health): - ONLINE / streaming + drift-adaptive: HAS THIS, strongly. This i..._
- **[confirmed]** S. Bhatia, A. Jain, S. Srivastava, K. Kawaguchi, and B. Hooi, "MemStream: Memory-Based Streaming Anomaly Detection," in Proceedings of the ACM Web Conference 2022 (WWW '22), Apr. 2022, pp. 610-621. doi:10.1145/3485447.3512221. (Preprint: arXiv:2106.03837. The longer working title "Memory-Based Anomaly Detection in Multi-Aspect Streams with Concept Drift" refers to the same work; code at github.com/Stream-AD/MemStream.)  
  https://arxiv.org/abs/2106.03837  
  _ADJACENT -- a method/algorithm reference, NOT a domain competitor. It does NOT preempt the novelty and only weakly overlaps on one axis (drift-robust unsupervised streaming detection). Axis-by-axis: (1) ONLINE/streaming -- YES, core strength and the most relevant property to in-field D2D monitoring. (2) Label-free/u..._
- **[confirmed]** Susik Yoon, Youngjun Lee, Jae-Gil Lee, and Byung Suk Lee. "Adaptive Model Pooling for Online Deep Anomaly Detection from a Complex Evolving Data Stream." In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '22), August 2022. DOI: 10.1145/3534678.3539348. Also arXiv:2206.04792. (Framework name: ARCUS.)  
  https://arxiv.org/abs/2206.04792  
  _VERDICT: ADJACENT (purely methodological), with ZERO domain overlap. It does NOT preempt the thesis novelty and only partially overlaps on the online/streaming + AE + concept-drift methods axis. Axis-by-axis: (1) ONLINE/STREAMING detection — HAS IT, the core contribution (true online inference + dynamic model-pool u..._
- **[confirmed]** R. J. M. Silva, M. G. Nascimento, F. Machida, and E. Andrade, "Adaptive Detection of Software Aging under Workload Shift," in Anais do XXVI Simposio em Sistemas Computacionais de Alto Desempenho (SSCAD 2025), pp. 242-253, SBC, 2025. Also arXiv:2511.03103 (v2, 14 Nov 2025). https://arxiv.org/abs/2511.03103</corrected_citation>
<doi>arXiv:2511.03103</doi>
<url>https://arxiv.org/abs/2511.03103</url>
<abstract>Software aging affects long-running systems, causing progressive performance degradation and increasing failure risk. The paper proposes an adaptive ML approach for software-aging detection under dynamic workloads, comparing a static model against adaptive models using concept-drift detectors DDM and ADWIN to handle workload shifts. The dataset reuses Couto et al. 2024: RAM consumption of a SQL Server DBMS over 48 h (5 s sampling). Sudden, gradual, and recurring workload transitions are synthetically generated by concatenating real segments from Low/Medium/High workload profiles. Static models drop in accuracy on unseen workloads, while the ADWIN adaptive model keeps F1 > 0.93 across all scenarios via change detection and retraining on the most recent ~2000-sample window.</abstract>
<gap_assessment>SKEPTICAL VERDICT: ADJACENT / analogy only. Does NOT preempt and does NOT partially overlap the team's hardware novelty; on every concrete axis it scores zero. AXES: Online/in-field = PARTIAL/ANALOGOUS (streaming drift-triggered retraining, but on offline logged DBMS data replayed as a stream, not a deployed hardware monitor). Multimodal fusion = ABSENT (strictly unimodal, single feature = RAM consumption; the voltage+thermal+link fusion thesis is untouched). Voltage/droop/PDN = ABSENT. Temperature/thermal/PVT = ABSENT. Link signals (BER, eye margin, lane skew, retrain/parity) = ABSENT. D2D/chiplet/UCIe-BoW-AIB = ABSENT (domain is a SQL Server DBMS, software-aging/memory-leak mechanism). Hardware/silicon = ABSENT. TRANSFERABLE (why keep): the core problem is a clean 1:1 software-layer mirror -- separate benign workload-induced degradation from true incipient aging so a workload change is not mistaken for a fault; the ADWIN/DDM drift-gating seed is portable to D2D where thermal/voltage operating-point drift must be distinguished from real link degradation. It is a strong motivation/analogy and baseline-strategy cite, NOT a competitor, and it reinforces the white-space (problem solved at software layer, no hardware-telemetry/multimodal/D2D analogue). Cite in Related Work as a drift-aware degradation/aging analogue, flagged single-modality, software-only, non-interconnect.</gap_assessment>
<sim_detail>No electrical/thermal/PVT/PDN/interconnect simulation. Data are REAL measurements: RAM consumption of a SQL Server DBMS over 48 h at 5 s sampling, reused from Couto et al. 2024. Only the workload-shift scenarios are synthetic, fabricated by concatenating/mixing real segments from Low/Medium/High intensity profiles. No SPICE/Q3D/IBIS-AMI/HotSpot/CoMeT/3D-ICE/gem5 tooling; pure data-replay plus concept-drift detectors (ADWIN, DDM). Dataset real, shifts synthetic (authors flag as threat to validity).</sim_detail>
<motivation_detail>Transferable evidence: (1) Failure-mode analogue -- software aging (slow resource exhaustion / memory-leak-style drift in a long-running DBMS) as incipient degradation distinct from instantaneous faults, mirroring parametric/drift link degradation in D2D. (2) Confounding measurement -- empirically shows a static detector suffers a notable accuracy drop on unseen workload profiles, i.e., benign workload shift masks/mimics aging, the exact false-alarm/missed-detection confound the team faces with thermal-voltage operating-point drift vs real link wear. (3) Quantified mitigation -- ADWIN drift-gated retraining restores F1 > 0.93 across sudden/gradual/recurring shifts, a concrete baseline for "separate benign drift from real degradation." No field/RAS, SDC/CEE, or hardware-reliability data (software layer, out of scope).</motivation_detail>
</invoke>
- **[confirmed]** Junghee Pyeon, Davide Cacciarelli, Kamran Paynabar. "An Adaptive Sampling Framework for Detecting Localized Concept Drift under Label Scarcity." arXiv preprint arXiv:2511.02452, submitted 4 November 2025. Subjects: Machine Learning (stat.ML; cs.LG). https://arxiv.org/abs/2511.02452  
  arXiv:2511.02452  
  _CONFIRMED REAL (arXiv:2511.02452, submitted 4 Nov 2025; Georgia Tech ISyE / Pyeon, Cacciarelli, Paynabar; classified stat.ML, cs.LG). VERDICT: purely ADJACENT — it does NOT preempt our novelty and does not even partially overlap on the hardware/D2D axes. It is a generic statistics/ML methods paper.  WHAT IT HAS (axe..._
- **[confirmed]** Q. Rebjock, B. Kurt, T. Januschowski, and L. Callot, "Online False Discovery Rate Control for Anomaly Detection in Time Series," in Advances in Neural Information Processing Systems 34 (NeurIPS 2021), 2021, pp. 26487-26498. arXiv:2112.03196. Authors affiliated with Amazon Research / AWS AI Labs (and EPFL).  
  https://proceedings.neurips.cc/paper/2021/hash/def130d0b67eb38b7a8f4e7121ed432c-Abstract.html  
  _ADJACENT / METHODOLOGICAL — does NOT preempt the novelty; it is a portable statistical tool, not a competing system. Axes it HAS: (1) online/streaming operation — yes, the entire contribution is sequential/online hypothesis testing; (2) anomaly detection — yes; (3) time series with serially-dependent statistics — ye..._
- **[confirmed]** Sakti Saurav, Pankaj Malhotra, Vishnu TV, Narendhar Gugulothu, Lovekesh Vig, Puneet Agarwal, and Gautam Shroff. "Online Anomaly Detection with Concept Drift Adaptation using Recurrent Neural Networks." In Proceedings of the ACM India Joint International Conference on Data Science and Management of Data (CoDS-COMAD 2018), Goa, India, pp. 78-87. ACM, 2018. DOI: 10.1145/3152494.3152501.  
  https://dl.acm.org/doi/10.1145/3152494.3152501  
  _ADJACENT methodological lineage — does NOT preempt and only weakly touches the project's white-space. Axes it HAS: (a) ONLINE/streaming detection with incremental model updates; (b) explicit concept-drift adaptation of the "normal" model (the exact justification this paper is cited for — static/offline models become..._
- **[confirmed]** Albert Bifet and Ricard Gavaldà. "Learning from Time-Changing Data with Adaptive Windowing." In Proceedings of the 2007 SIAM International Conference on Data Mining (SDM), pp. 443–448. SIAM, 2007. DOI: 10.1137/1.9781611972771.42.  
  https://epubs.siam.org/doi/10.1137/1.9781611972771.42  
  _CORRECTLY bucketed as a generic primitive (gap-supporting methodology), NOT a competing system. SKEPTICAL verdict: this paper does ZERO of the project's distinguishing axes and therefore PREEMPTS NOTHING. Axes it HAS: (1) online/streaming change detection — yes, this is exactly what ADWIN does, sequential single-str..._
- **[confirmed]** G. J. Ross, N. M. Adams, D. K. Tasoulis, and D. J. Hand, "Exponentially weighted moving average charts for detecting concept drift," Pattern Recognition Letters, vol. 33, no. 2, pp. 191-198, Jan. 2012. DOI: 10.1016/j.patrec.2011.08.019. arXiv:1212.6018.  
  https://arxiv.org/abs/1212.6018  
  _ADJACENT — does NOT preempt our novelty and does not even partially overlap on the substantive D2D/multimodal axes; it is a generic statistical-baseline / methodological building block. Axis-by-axis: (1) MODALITY: single, abstract scalar stream = a classifier's misclassification rate. NOT voltage, NOT thermal, NOT B..._
- **[confirmed]** T. Idé, A. Dhurandhar, J. Navrátil, M. Singh, and N. Abe, "Anomaly Attribution with Likelihood Compensation," in Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-21), vol. 35, no. 5, pp. 4131–4138, 2021. DOI: 10.1609/aaai.v35i5.16535.  
  https://ojs.aaai.org/index.php/AAAI/article/view/16535  
  _Confirmed real (AAAI-21, vol.35(5):4131-4138; arXiv:2208.10679; IBM Research / Idé et al.). VERDICT: purely ADJACENT — it does NOT preempt the thesis and does not even partially overlap on the application axes. This is a generic, model-agnostic XAI/attribution METHOD (Likelihood Compensation, LC): given a black-box ..._
- **[confirmed]** Ailin Deng and Bryan Hooi. "Graph Neural Network-Based Anomaly Detection in Multivariate Time Series." Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-21), vol. 35, no. 5, 2021, pp. 4027–4035. DOI: 10.1609/aaai.v35i5.16523.  
  https://ojs.aaai.org/index.php/AAAI/article/view/16523  
  _DOES NOT PREEMPT — it is a METHOD/PRIMITIVE paper that is ADJACENT to our thesis, not overlapping with it. Skeptical axis-by-axis verdict:  DOMAIN (D2D/chiplet): ABSENT. The paper is entirely about Cyber-Physical Systems / critical infrastructure; its only evaluation domains are SWaT and WADI, two water-treatment-pl..._
- **[confirmed]** Chaoyue Ding, Shiliang Sun, and Jing Zhao. "MST-GAT: A multimodal spatial–temporal graph attention network for time series anomaly detection." Information Fusion, vol. 89, pp. 527–536, January 2023 (available online August 2022). DOI: 10.1016/j.inffus.2022.08.011. (East China Normal University; preprint also on arXiv:2310.11169.)  
  https://www.sciencedirect.com/science/article/abs/pii/S156625352200104X  
  _VERDICT: ADJACENT / METHODOLOGICAL TEMPLATE — does NOT preempt the thesis novelty; partial overlap only on the ML-method axis, zero overlap on the domain axis.  What it HAS (axes present): - True multimodal time-series anomaly detection. It explicitly distinguishes "modalities" (groups of univariate channels) and mo..._
- **[confirmed]** Chaoyu Chen, Hang Yu, Zhichao Lei, Jianguo Li, Shaokang Ren, Tingkai Zhang, Silin Hu, Jianchao Wang, and Wenhui Shi. "BALANCE: Bayesian Linear Attribution for Root Cause Localization." Proceedings of the ACM on Management of Data (PACMMOD), Vol. 1, No. 1, Article 53, pp. 1-26, May 2023. Presented at SIGMOD '23, June 18-23, 2023, Seattle, WA, USA. DOI: 10.1145/3588949. Preprint: arXiv:2301.13572 (submitted Jan 31, 2023).  
  https://dl.acm.org/doi/abs/10.1145/3588949  
  _ADJACENT — methodological prior art, NOT a preemption. BALANCE is a domain-agnostic root-cause-attribution algorithm from the database/cloud-ops community (Alipay), evaluated only on bad-SQL localization, container fault localization, and the Exathlon streaming-anomaly benchmark. Scoring it against our four novelty ..._
