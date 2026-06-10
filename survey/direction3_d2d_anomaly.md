# Direction 3: D2D Link Anomaly Detection — Literature Survey

**Scope**: AI/ML methods for detecting anomalies in chiplet / die-to-die (D2D) interconnect links — covering BER monitoring, jitter, thermal drift, voltage noise, UCIe/BoW testing, HBM and silicon-interposer testing, autoencoder / LSTM / Transformer time-series anomaly detection, statistical methods (PCA, IF, GMM), runtime monitoring of high-speed links, SerDes / PAM4 link health, BIST, and eye/margin analysis with ML.
**Venue filter**: IEEE / ACM / Springer / Elsevier (ITC, VTS, DATE, DAC, ICCAD, ETS, ATS, ISSCC, CICC, TCAD, TVLSI, TCAS, TC, JSSC, MWSCAS, ECTC, JETTA, MICRO, plus high-quality arXiv pre-prints of submitted IEEE conference work).
**Time window**: 2021 – 2026 (recent 5 years), with a small number of older foundational works included for completeness.

---

> **📌 Round-2 update (2026-06-03): Tier-1 entries verified against the actual PDFs.**
> The 11 Tier-1 papers downloaded to `papers/3/` (#1, #2, #3, #4, #6, #7, #8, #11, #12, #13, #14) were read in full; their entries below are **rewritten from ground truth** — real authors/affiliations, verified venues/DOIs, and a richer `Methods / Novelty / Evaluation / Relevance / Correction note` format (marked **✓ Status: Verified**). Several round-1 errors were fixed (e.g. **#7** was mis-dated 2021 → actually **ITC 2020**; **#8**'s round-1 abstract described the *wrong* paper — LeNet/Wide-ResNet/Inception transfer-learning — and is corrected to the real Miao et al. EPTC-2022 CNN eye-impairment classifier; **#2** had a wrong "Synopsys" affiliation → actually ASU + Intel). Entries **#5, #9, #10, #15** were *not* in the download set and remain **⚠ unverified** (web/industrial sources). See the per-entry **Correction note** fields and the **Tier-1 correction log** at the end of the Tier-1 section.
> A companion deep-reading synthesis — novelty themes, a methods taxonomy, an evaluation-methods table, and project recommendations — is in **`SYNTHESIS_direction3_round1.md`**.
> **Round-2 download list (2026-06-03):** the project focus has sharpened to *online D2D link-health evaluation by fusing multimodal on-chip telemetry (voltage / temperature / PVT + link BER/eye/skew)*. A bibliography-mined, web-verified, thesis-focused **next-download list** (Tier A/B/C + coverage-gap analysis + DATE-2027 positioning) is in **`00_DOWNLOAD_LIST_round2_direction3.md`**.

## Tier 1: Must-Read Papers (directly tackle D2D / chiplet link anomaly with ML)

### 1. Learning High-Quality Latent Representations for Anomaly Detection and Signal Integrity Enhancement in High-Speed Signals
- **Authors**: Muhammad Usama, Hee-Deok Jang, Soham Shanbhag (School of Electrical Engineering, KAIST, Daejeon, Republic of Korea); Yoo-Chang Sung, Seung-Jun Bae (DRAM Design Team, Memory Division, Samsung Electronics, Hwasung, Republic of Korea); Dong Eui Chang (KAIST, corresponding author). 6 authors, no "et al."
- **Venue**: arXiv preprint, arXiv:2506.18288v1 [cs.LG], 23 June 2025. No formal journal/conference venue printed on the PDF (Springer-style manuscript with a "Statements and Declarations" section; venue not named).
- **DOI/Link**: https://arxiv.org/abs/2506.18288 (arXiv:2506.18288). Code: github.com/Usama1002/learning-latent-representations
- **Methods**: Joint semi-supervised training of an autoencoder (Encoder R¹⁰⁰→R¹¹, Decoder R¹¹→R¹⁰⁰) and a single-layer sigmoid classifier with loss L = ‖x − x̂‖² − y·log(ŷ), where classifier gradients flow ONLY from valid (normal) data; the frozen encoder feeds three detectors (LOF, LSAnomaly, a supervised NN). A latent-space signal-integrity enhancement (Algorithm 1) nudges latent vectors toward the Fermat-Weber (geometric-median) anchor of valid latents and reconstructs while reconstruction dissimilarity stays below α=0.05.
- **Novelty**: Backpropagating classifier gradients from valid data only (vs prior work using both classes) to learn discriminative anomaly latents without overfitting scarce labeled faults; plus a Fermat-Weber-anchored latent-space remediation step that improves signal integrity, not just detection.
- **Evaluation**: Simulated 10 Gbps mobile-DRAM channel (DRAM PKG→Board→SoC), 5 test-case configs, eye-diagram (80 mV × 35 ps mask) labeling, synthetic ISI/amplitude/harmonic anomalies, 80/20 split. Baselines: contractive AE, and a both-gradients variant. Results: NN detection accuracy 95.9% (5–9% over baselines; LOF 83.7%, LSAnomaly 91.4%); Bhattacharyya distance 304.66 vs <187; latent overlap 11.29%; average eye-diagram window-area SI improvement 11.3% (up to 31.8%). No hardware/area/power numbers (pure ML study).
- **Relevance to D2D anomaly detection**: Domain-adjacent template: the package-to-package 10 Gbps channel and eye-diagram mask labeling transfer directly to D2D link SI monitoring, and the valid-only-gradient AE+classifier is a reusable recipe for learning link-anomaly latents without comprehensive labeled fault data. Caveat: it targets parallel DRAM I/O (not a UCIe/BoW/AIB D2D link), all data is simulated with synthetic anomalies, and there is no on-die sensing/DfT mechanism.
- **Correction note**: Authors were the placeholder "(DRAM SI anomaly group — memory-vendor research lab)"; now corrected to the verified 6-author KAIST + Samsung list with Dong Eui Chang as corresponding author. Old "Abstract" field replaced by structured Methods/Novelty/Evaluation; clarified it is a MOBILE-DRAM-channel (not D2D) paper using simulation + synthetic anomalies with no hardware-cost results.
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 2. OCTANE: On-Chip Telemetry-based Anomaly Notification Engine
- **Authors**: Eduardo Ortega, Arjun Hati, Jonti Talukdar, Woohyun Paik (ASU Center for Semiconductor Microelectronics, Arizona State University); Fei Su (Intel Corporation, Ann Arbor, MI); Rita Chattopadhyay (Intel Corporation, Chandler, AZ); Krishnendu Chakrabarty (Arizona State University).
- **Venue**: 2025 IEEE International Test Conference (ITC), pp. 131–140, Regular Paper. ISBN 979-8-3315-7041-5.
- **DOI/Link**: 10.1109/ITC58126.2025.00019 — https://ieeexplore.ieee.org/document/11219729/
- **Methods**: On-chip unsupervised anomaly detection using two fixed-point distance scores over telemetry feature vectors — variance-norm Euclidean d_E and a cosine-derived d_C — computed per domain (core/memory/sensor) and aggregated (mean a_M and product a_J), implemented with Kogge-Stone adders and Wallace-tree multipliers. Workload-independent feature ranking uses an entropy/discretization normalized-mutual-information index with intersection thresholding; results read/written via repurposed reserved MSR (IA32_EFER) bits. A cloud-side XGBoost classifier (OCTANE-cloud) diagnoses incidents from the compact anomaly-score vector.
- **Novelty**: Hardware/software-codesigned, compute- and memory-efficient unsupervised SLM detector with hierarchical (core/memory/sensor) scoring and workload-independent unsupervised feature ranking, paired with an anomaly-informed diagnosis stage — advancing the software-only prior SLM method E-SCOUT.
- **Evaluation**: Measured telemetry on two real Intel CPUs (i5-7600K 14 nm/181 features; i5-12600K 7 nm/460 features), PAMPAR benchmarks, injected anomalies (TRRespass/Rowhammer, Spectre, Plundervolt voltage droop). Detection metric AUCROC (>0.95 in most cases; best mean-rank vs E-SCOUT, autoencoder, iForest). Diagnosis (XGBoost) accuracy/F1 0.96/0.98, up to 0.999 combined. Hardware (OpenROAD ASAP7 7 nm synthesis): 2.59 mm² = 1.2% die-area overhead (vs E-SCOUT 4.75 mm²/2.2%); ~0.5% average power overhead, 2.6% idle, <1.45% worst-case workload.
- **Relevance to D2D anomaly detection**: Strong on-chip, low-overhead, unsupervised HW/SW-codesigned template directly portable to a per-lane/per-channel D2D link monitor: lightweight fixed-point distance scoring, hierarchical per-domain → aggregated scoring, MI-based robust feature selection, and a two-stage edge-detect + cloud-diagnose (XGBoost) architecture with a reusable PPA/AUCROC evaluation rubric. Caveat: it targets CPU MSR telemetry and security/safety anomalies, not D2D PHY signal integrity, so link-specific telemetry/stimulus would need substitution.
- **Correction note**: Authors were the placeholder "(Synopsys / academic SLM group)"; now corrected to the verified ASU (Chakrabarty group) + Intel author list — no Synopsys involvement. Venue refined to ITC 2025, pp. 131–140 with DOI; added the diagnosis half (XGBoost), the dual security/safety scope, and the verified 1.2% area / 0.5% power / >0.95 AUCROC / 0.96–0.98 diagnosis numbers. Detection is AUCROC-based (not a single "accuracy").
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 3. Defect Analysis and Built-In-Self-Test for Chiplet Interconnects in Fan-out Wafer-Level Packaging
- **Authors**: Partho Bhoumik, Christopher Bailey, Krishnendu Chakrabarty (School of Electrical, Computer and Energy Engineering / ASU Center for Semiconductor Microelectronics, Arizona State University). (Funding: NSF, in part by CHIMES.)
- **Venue**: arXiv:2503.14784v1 [eess.SY], 18 Mar 2025; carries an IEEE 2025 copyright line ("979-8-3315-2144-8/25/$31.00 ©2025 IEEE") indicating an accepted/camera-ready IEEE conference paper — specific IEEE conference name NOT printed on the PDF.
- **DOI/Link**: https://arxiv.org/abs/2503.14784 (arXiv:2503.14784)
- **Methods**: FEA/parasitic extraction (Ansys Q3D) maps Cu-pillar and RDL physical defects (cracks, opens, misalignment, bridging) to equivalent RLC circuits; package-level HSPICE fault simulation (OpenROAD ASAP7 PDK) derives defect-size-to-functional-fault thresholds. A BIST models the hexagonal bump-short problem as graph coloring (4 codewords for 12 neighbors) and uses exactly THREE test patterns {011, 110, 101} with wired-AND/wired-OR detectors, a block-partitioned bump map, and an FSM controller.
- **Novelty**: Deterministic defect-to-fault analysis flow plus a 3-pattern, graph-coloring BIST that detects and diagnoses stuck-at and bridging faults (vs prior schemes needing 16 patterns/4 codewords), with a proven diagnosability of 95.61%.
- **Evaluation**: Simulation-only (no silicon). BIST correctness proven analytically (Theorem 1: 3 patterns detect all SAFs + bridging; D ≈ 0.956). Defect thresholds e.g. signal short to VDD with R_short < 500 Ω → SA-1; critical short radial path ~3 nm (Cu bumps)/~2 nm (RDL). PPA via 45 nm Nangate synthesis on AES (+3.6–4.92% area, +3.75–6.6% power) and DES (+1.39–1.73% area, +1.15–1.57% power) for 2-/4-block configs.
- **Relevance to D2D anomaly detection**: Directly on-target — package-level BIST for chiplet interconnects (Cu pillars + RDL) in FOWLP covering opens (SAFs) and shorts (bridging), the canonical D2D anomalies. Reusable: defect taxonomy/root-cause table, the Q3D→RLC→HSPICE flow for generating labeled synthetic D2D anomaly data and defect-size thresholds (Table III as ground-truth labels), the 3-pattern detection scheme, the diagnosability metric, and PPA overhead numbers as a hardware-cost baseline. Note: this is a deterministic structural-test/BIST approach, NOT an ML anomaly detector — the structural-test baseline that learning-based D2D monitoring would be contrasted against.
- **Correction note**: Affiliation placeholder "Arizona State University authors" replaced with the verified authors Partho Bhoumik, Christopher Bailey, Krishnendu Chakrabarty. Venue corrected from "ITC/VTS-tier submission" to arXiv:2503.14784 with an IEEE 2025 camera-ready copyright line (no specific conference printed). Old abstract overstated thermo-mechanical fault simulation of CTE/warpage on functionality; clarified the actual flow is Q3D→HSPICE defect-size thresholds + a 3-pattern graph-coloring BIST (95.61% diagnosis, 45 nm Nangate PPA), and that it is structural test, not ML.
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 4. Efficient Built-In Self-Test Scheme for Inter-Die Interconnects of Chiplet-Based Chips
- **Authors**: Yi-Chun Huang, Pei-Yun Lin, Jin-Fu Li, Hong-Siang Fu (Department of Electrical Engineering, National Central University, Taoyuan, Taiwan); Yung-Ping Lee (Electronic and Optoelectronic System Research Lab., Industrial Technology Research Institute, ITRI, Hsinchu, Taiwan).
- **Venue**: 2024 IEEE International Test Conference (ITC), pp. 149–156, Regular Paper. ISBN 979-8-3315-2013-7.
- **DOI/Link**: 10.1109/ITC51657.2024.00034 — ITC 2024 proceedings (IEEE Xplore)
- **Methods**: An Alternating Row and Column Stripe (ARCS) test algorithm exploits the logical h×w 2D ubump array so the pattern count is 2·(⌈log₂h⌉+⌈log₂w⌉); a homogeneity-based compression scheme shrinks h×w-bit patterns to h-/w-bit vectors decompressed in parallel per clock by per-ubump wrapper cells. A split TX/RX BIST architecture (TX: MUX + NOR decompression; RX: NOR + XNOR-vs-golden + tri-state + OR-tree, with address-decoder/shift-register localization) supports fault detection and location modes.
- **Novelty**: Logarithmic-pattern-count ARCS algorithm plus stripe-homogeneity compression and a lightweight TX/RX wrapper, achieving TC-BCS-equivalent stuck-at + wired-OR/wired-AND detection and self-diagnosis at far lower test time and area.
- **Evaluation**: Analytical pattern/cycle derivation + TSMC 40 nm synthesis at 500 MHz (no silicon, no fault-injection). Baseline: IEEE 1500. Per-interconnect wrapper 6.05 µm² vs 16.37 µm² (63.0% saving); 32×64 array 15590 vs 33517 µm² (53.5% saving; 52.8% average). Fault-detection time 22 vs 47104 cycles (99.9% reduction); fault-location time 45100 vs 47104 cycles (nearly equal). No power numbers; fault coverage argued analytically.
- **Relevance to D2D anomaly detection**: Directly targets D2D/chiplet microbump (ubump) interconnects through a CoWoS interposer — the exact link class of Direction 3. Provides a concrete low-overhead TX/RX BIST and wrapper-cell design reusable as the on-die sensing/stimulus substrate, an RX XNOR-vs-golden + OR-tree pass/fail with per-row localization mechanism, and the D2D fault taxonomy (ubump shorts/opens, interposer-line shorts/opens → stuck-at + wired-OR/AND) as ground-truth classes. Caveat: deterministic functional test with NO ML and no weak/parametric/aging defect coverage — best cited as a low-cost test baseline an anomaly detector must complement.
- **Correction note**: Authors were already correct; the old "Abstract" misattributed the method (it does NOT enhance IEEE 1838 DWR cells and does NOT cover delay/crosstalk faults). Corrected to: ARCS algorithm + homogeneity compression + TX/RX BIST detecting stuck-at and wired-OR/wired-AND bridging only, with self-diagnosis; added verified numbers (63.0%/53.5%/52.8% area, 99.9% detection-time reduction for a 32×64 array, TSMC 40 nm/500 MHz) and clarified it is deterministic structural BIST, not ML.
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 5. Probeless Fault Isolation Capability for 2.5D/3D Chiplet Die-to-Die Interconnect
- **⚠ Verification status**: NOT in the downloaded set — entry below is from the initial round-1 sweep and has NOT been verified against a PDF (web/industrial source or pending download). Treat authors/abstract as provisional.
- **Authors**: (IEEE EPS feature)
- **Venue**: IEEE Electronics Packaging Society e-news, June 2024
- **DOI/Link**: https://eps.ieee.org/publications/enews/june-2024/1174-probeless-fault-isolation-capability-for-2-5d-3d-chiplet-die-to-die-interconnect.html
- **Abstract**: Describes a probeless fault-isolation method for D2D interconnects that works during production test and in-field without physical failure-analysis equipment. Targets the inevitable failures caused by the large number and close spacing of D2D bumps, even with interconnect redundancy.
- **Why relevant**: Defines the exact in-field diagnosis problem we want to attack with ML and gives the reference industrial workflow.
- **Recommended for download**: YES

### 6. IEEE Std P3405: New Standard-under-Development for Chiplet Interconnect Test and Repair
- **Authors**: Erik Jan Marinissen (IMEC, Belgium / TU Eindhoven, Netherlands); Vineet Pancholi (Amkor Technology, Inc., USA); Po-Yao Chuang (IMEC / NTHU, Taiwan); Martin Keim (Siemens EDA, USA).
- **Venue**: 2024 IEEE 42nd VLSI Test Symposium (VTS), Special Session paper. IEEE catalog 979-8-3503-6378-4/24/$31.00 ©2024 IEEE.
- **DOI/Link**: 10.1109/VTS60656.2024.10538776 — https://ieeexplore.ieee.org/document/10538776/
- **Methods**: Position/standards paper with three contributed sections (OSAT production-test motivation; chiplet interconnect repair logic; EDA viewpoint). It formalizes the Interconnect Repair Problem (IRP) over repair chains with spare interconnects, repair-logic relations, a defect function, and a repair-solution function; proposes Google Protocol Buffers as a language-neutral repair description format (a *.repair / ieeeP3405.proto schema); gives a worked UCIe-Advanced lane-repair example (12 repair chains); and enumerates ten EDA requirements for stack-level D2D interconnect handling.
- **Novelty**: Introduces the in-development IEEE Std P3405 for multi-vendor interoperable D2D interconnect test and repair, positioned against IEEE 1838/1687/1500/1149.1, UCIe, AIB, and HBM3, with a formal IRP definition and a Protocol-Buffers-based machine-readable repair description language.
- **Evaluation**: None — no datasets, metrics, baselines, ablations, or hardware numbers. "Evaluation" is qualitative: a worked ucie.repair example plus comparative analysis vs prior standards and a two-die EDA thought-experiment. (Cited external result: 16 test patterns suffice for all static+transition interconnect faults if physical neighbors are known.)
- **Relevance to D2D anomaly detection**: Standards/infrastructure backdrop for Direction 3: the formal IRP and repair-chain/spare-lane model define precisely what a defective D2D interconnect ("anomaly") is and how Tx/Rx repair MUXes reroute around it; the D2D defect/anomaly taxonomy (contact resistance, crosstalk, insertion/return loss, eye width/height, jitter, swing, stuck-at/transient/bridge faults) and the on-die telemetry it lists (PVT/PHI sensors, Rx eye margining, lane-repair status) are a ready feature/failure-mode source for an ML detector. Note: it proposes NO ML/anomaly-detection method — context and feature source, not a method baseline.
- **Correction note**: Authors were the placeholder "E. J. Marinissen et al. (CITR-WG, imec)"; now corrected to the verified four-author list (Marinissen, Pancholi, Chuang, Keim) with affiliations. Venue narrowed to VTS 2024 Special Session (the ETS 2024 companion is a separate Part-2 paper). Clarified this is a conference paper ABOUT the standard (no experiments/metrics), not the standard text; the old abstract's list of concrete standard features is forward-looking rather than measured.
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 7. High Speed Serial Links Risk Assessment in Industrial Post-Silicon Validation Exploiting Machine Learning Techniques
- **Authors**: Cesar A. Sánchez-Martínez, Paulo López-Meyer, Esdras Juarez-Hernandez, Aaron Desiga-Orenday, Andrés Viveros-Wacher (all Intel Corp., Zapopan, 45109 Mexico).
- **Venue**: 2020 IEEE International Test Conference (ITC), pp. 1–5, Industrial Practice track. ISBN 978-1-7281-9113-3/20, ©2020 IEEE.
- **DOI/Link**: 10.1109/ITC44778.2020.9325238 — https://ieeexplore.ieee.org/document/9325238/
- **Methods**: Supervised binary (pass/fail) classification of the post-silicon System Marginality Validation (SMV) Product-Release-Qualification risk decision for a Derivative Product, using models trained on a Base Product. Three ML models — cubic-kernel SVM, a shallow NN (163-2048-2, tanh), and Boosted Trees — over a 163-feature vector (eye width, eye height, adaptive and static Rx calibration codes) harvested via on-die DFT eye-margining hooks. Labels by 3-engineer consensus; data standardized; PCA used for an ablation.
- **Novelty**: Frames the human "compare DP vs BP margin distributions" SMV decision as supervised ML, making the DP PRQ risk call at runtime inference with BP-level accuracy; shows the full 163-feature set generalizes significantly better than a PCA-reduced 7-component subset.
- **Evaluation**: Measured silicon on a real Intel client CPU+PCH platform; SATA HSIO link. Dataset 1,275 samples × 163 features; 70/30 split, 10× random sub-sampling; metrics accuracy/sensitivity/specificity. Boosted Trees best at 94.84% (sens 94.57%, spec 95.12%); cubic SVM 93.01%; NN 92.72% (BT vs SVM/NN significant, p=0.003). PCA-reduced models drop below 88% (full vs PCA, p<1e-8). No hardware-cost reporting (offline software inference).
- **Relevance to D2D anomaly detection**: Industrial template for ML-based link risk/anomaly detection on high-speed serial links (same PHY regime as D2D). Reusable: the feature set (eye width/height + adaptive/static Rx equalizer/calibration codes from DFT hooks → D2D margining telemetry), the supervised pass/fail "link unlike golden baseline" framing, the SMV eye-margining/BER-from-margin stimulus, the SVM/NN/BT + accuracy/sensitivity/specificity + 10× sub-sampling harness, and the lesson that richer raw PHY features beat aggressive PCA. Caveats: it targets a batch PRQ qualification decision (not real-time online monitoring), the link is SATA in a PCH (not a UCIe/chiplet D2D interconnect), and the anomaly notion is supervised distribution-shift, not unsupervised novelty.
- **Correction note**: Authors were the placeholder "(Industrial post-silicon ML group)"; now corrected to the five verified Intel-Mexico authors. Year corrected from 2021 to ITC 2020. Old abstract was too vague ("learning from historical validation data"); replaced with concrete SMV/DP-from-BP framing, the 163-feature/1,275-sample setup, the three ML models, and headline numbers (BT 94.84% best); noted this is measured Intel silicon, not synthetic data.
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 8. Eye Diagram Analysis with Deep Neural Networks for Signal Integrity Applications
- **Authors**: Miao Weiyang, Chuan Seng Tan (Institute of Microelectronics, A*STAR, Singapore; and School of Electrical and Electronic Engineering, Nanyang Technological University, Singapore); Mihai D. Rotaru (Institute of Microelectronics, A*STAR).
- **Venue**: 2022 IEEE 24th Electronics Packaging Technology Conference (EPTC), pp. 212–217. ©2022 IEEE. ISBN 979-8-3503-9885-4.
- **DOI/Link**: 10.1109/EPTC56328.2022.10013173 — https://ieeexplore.ieee.org/document/10013173/
- **Methods**: A CNN (3 conv+pool blocks → dense 2048/1024 → 7-way softmax, TensorFlow) classifies the SI-impairment type of ADS-simulated eye diagrams of a multi-module memory bus into 7 classes (crosstalk, loss, reflection, and their composites). Impairments are injected via parameter sweeps (coupled-line spacing for crosstalk, loss tangent for loss, impedance mismatch for reflection); eye images are grayscaled and resized 775×543×3 → 100×70 (~60× reduction). The CNN also localizes impairments (which line carries loss/crosstalk), and a linear-regression model suggests a design parameter (coupled-line spacing/length) to reopen the eye.
- **Novelty**: Applies CNN to the "backward" problem (infer the circuit fault type from the eye image) including composite multi-impairment classes and impairment localization, coupled with a regression step that actually fixes the eye.
- **Evaluation**: Synthetic ADS eye diagrams (~100 per single-impairment class, hundreds of composite). Metric: classification accuracy by epoch — reaches 100% at 10 epochs for the 7-class task; data-volume ablation shows ≥80% of data needed for 100% accuracy. Localization: crosstalk easier with longer/uniform coupled length (100% by epoch 5); loss-location better with non-uniform line lengths. No external baseline, no precision/recall, no hardware cost.
- **Relevance to D2D anomaly detection**: Direct template for ML-based SI anomaly/fault classification on high-speed links: treat the (D2D) eye as an image and CNN-classify impairment type (crosstalk/loss/reflection/composite); the simulator-driven inject-one-fault-then-label pipeline is exactly how to build a synthetic D2D fault dataset where measured anomalies are scarce; the localization angle maps to fault localization across a multi-lane D2D PHY; the data-volume ablation guides labeled-data needs. Caveats: a memory bus (not a packaged D2D/UCIe link), jitter ignored, design-time EDA only (no in-field sensing), no area/power cost.
- **Correction note**: Authors were the placeholder "(Signal-integrity DL group)"; now corrected to Miao Weiyang, Chuan Seng Tan, Mihai D. Rotaru (A*STAR IME / NTU Singapore). Venue corrected to EPTC 2022, pp. 212–217 with DOI. The old abstract was fabricated — it claimed LeNet/Wide-ResNet/Inception-v4, Q-factor classification, and OOK/PAM4 transfer-learning speedups (>95%/60%) that do not appear in this paper; replaced with the actual single custom CNN, 7-impairment classification + localization + linear-regression eye improvement, 100% accuracy at 10 epochs, and ~60× image reduction.
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 9. Test and Diagnosis Strategies for Inter-Chiplet Interconnects
- **⚠ Verification status**: NOT in the downloaded set — entry below is from the initial round-1 sweep and has NOT been verified against a PDF (web/industrial source or pending download). Treat authors/abstract as provisional.
- **Authors**: (Inter-chiplet test team)
- **Venue**: 2024/2025 IEEE journal / TCAD-track survey
- **DOI/Link**: https://www.researchgate.net/publication/389613395
- **Abstract**: Surveys test/diagnosis strategies for inter-chiplet interconnects, including a neural-network-based test-grouping algorithm for irregular TSV layouts that accounts for crosstalk-fault influence range and hardware overhead.
- **Why relevant**: A single document that ties together TSV-fault NN classification, BIST architectures, and chiplet test grouping — gives the entire problem landscape.
- **Recommended for download**: YES

### 10. GUC GLink Test Chip Uses In-Chip Monitoring and Deep Data Analytics for High Bandwidth Die-to-Die Characterization
- **⚠ Verification status**: NOT in the downloaded set — entry below is from the initial round-1 sweep and has NOT been verified against a PDF (web/industrial source or pending download). Treat authors/abstract as provisional.
- **Authors**: GUC and proteanTecs (joint white-paper / industrial publication)
- **Venue**: proteanTecs / Semiconductor Engineering, 2022 – 2024
- **DOI/Link**: https://semiengineering.com/guc-glink-test-chip-uses-in-chip-monitoring-and-deep-data-analytics-for-high-bandwidth-die-to-die-characterization/
- **Abstract**: Documents the integration of proteanTecs' in-chip Interconnect Monitoring Agents into GUC's 5nm GLink D2D test chip, with silicon results for lane-grading, outlier detection, in-mission interconnect health monitoring, and lane repair on both ATE and in-field.
- **Why relevant**: A real silicon-validated D2D-link anomaly-detection deployment using ML-driven analytics — the strongest industrial reference.
- **Recommended for download**: YES

### 11. HeatSense: Intelligent Thermal Anomaly Detection for Securing NoC-Enabled MPSoCs
- **Authors**: Mahdi Hasanzadeh, Ahmad Patooghy (Member, IEEE) (Dept. of Computer Systems Technology, North Carolina A&T State University, Greensboro, NC); Kasem Khalil (Electrical and Computer Engineering, University of Mississippi, Oxford, MS); Cynthia Sturton (Computer Science, University of North Carolina at Chapel Hill).
- **Venue**: IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD), accepted/early-access author version, ©2026 IEEE.
- **DOI/Link**: 10.1109/TCAD.2026.3657198 — https://arxiv.org/abs/2504.11421 (arXiv preprint version)
- **Methods**: A per-router NON-ML statistical detector for Hardware-Trojan thermal-sensor spoofing in NoC-enabled MPSoCs: multi-tiered sigma thresholds (Mean ± K·std) with std approximated by bit-shift (σ_n = Mean/2ⁿ) and an Approximated Weighted Moving Average replacing the running mean; three monitored features yield a 3-level graded anomaly classification mapped to σ5/σ6/σ7 confidence intervals. A proportional, randomized port-shutdown countermeasure (4/5/all-6 ports) with staged priority reactivation provides graceful recovery. Random Forest is used only for feature-importance selection and as an ML comparison baseline.
- **Novelty**: A hardware-efficient, ML-free router-level statistical thermal-anomaly detector (bit-shift std + approximated WMA, graded multi-tier response) under a trust-separation model (untrusted third-party analog/mixed-signal thermal-sensor IP; trusted detection region with a hardware root of trust), validated on a combined CoMeT + AccessNoxim platform.
- **Evaluation**: Fully simulated (CoMeT + AccessNoxim + HotSpot; 16/32-core meshes; PARSEC). Detection accuracy up to 82% (10–15% below Random Forest ~90%/93%); precision/recall/F1/accuracy vs 5 feature sets and 7 sigma thresholds. Countermeasure reduces post-attack fluctuation from 3.00 °C to ~1.9 °C; recovery 378–2936 cycles; packet drop 1.5–3.9%. Xilinx Spartan-3 FPGA cost: up to 75% logic-resource reduction, 76.9% I/O reduction, 100% elimination of DSP48A/BUFGMUX vs ML.
- **Relevance to D2D anomaly detection**: Reusable security/anomaly-detection design for on-chip interconnect: the trust-separation threat model (untrusted analog/PHY IP, trusted detector + root of trust) maps onto multi-vendor chiplet integration; the lightweight per-router statistical detector (Mean ± K·std with bit-shift std and approximated WMA, no multipliers/LUTs) is an ASIC-friendly template for per-link in-line D2D monitoring; the multi-tier graded response and randomized graceful degradation translate to graded link throttling/lane shutdown; and the precision/recall/F1 + FPGA-overhead + recovery/packet-drop evaluation is a reusable rubric. Caveat: it monitors NoC-router thermal-sensor spoofing, not D2D-link electrical/protocol anomalies — features (router temperature, congestion) would need replacing with link-level signals (BER, lane skew, retrain events).
- **Correction note**: Authors were the placeholder "M. Hasanzadeh et al."; now corrected to the full four-author list (Hasanzadeh, Khalil, Sturton, Patooghy) with affiliations. Venue corrected from "arXiv 2504.11421, accepted at IEEE journal" to IEEE TCAD (DOI 10.1109/TCAD.2026.3657198, 2026 early access). Emphasized the method is NON-ML statistical thresholding (Random Forest is only a baseline/feature-selector) and that detection is validated only in simulation (the FPGA validates hardware overhead, not real silicon thermal detection); it is a NoC, not a D2D-link, paper.
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 12. Machine-Learning Approach in Detection and Classification for Defects in TSV-Based 3-D IC
- **Authors**: Yu-Jung Huang (Senior Member, IEEE), Shin-Chun Lin (Dept. of Electronic Engineering, I-Shou University, Kaohsiung, Taiwan); Chung-Long Pan (Dept. of Electrical Engineering, I-Shou University); Mei-Hui Guo (Dept. of Applied Mathematics, National Sun Yat-sen University, Kaohsiung, Taiwan; corresponding author).
- **Venue**: IEEE Transactions on Components, Packaging and Manufacturing Technology (TCPMT), vol. 8, no. 4, pp. 699–706, April 2018.
- **DOI/Link**: 10.1109/TCPMT.2017.2788896 — https://ieeexplore.ieee.org/document/8272475/
- **Methods**: Supervised classification of TSV void/short/open defects from HFSS-simulated two-port S-parameters (S11 return loss, S21 insertion loss, phase) over 200 MHz–20 GHz for single-die and stacked-die TSV models (plus TSV+RDL models for short/open). Classifiers: KNN (K=5) vs Random Forest, evaluated by k-fold cross-validation; void modeled as a 0–35% volume ratio.
- **Novelty**: Frames TSV void-amount and RDL short/open detection as ML over RF scattering parameters with NO image-processing step; can predict the void ratio (not just binary defect); exploits the TSV's MOS-capacitor behavior so a low-frequency (≤5 GHz) band gives the most separable, classifiable signatures.
- **Evaluation**: HFSS-simulated S-parameters only (no silicon, no public dataset). 8 void ratios + RDL short/open; KNN vs RF. Random Forest substantially outperforms KNN (RF approaching ~0.9–1.0 vs KNN ~0.2–0.4 in the 20 GHz case); low-frequency (≤5 GHz) data classifies better than wide-band (≤20 GHz); accuracy improves with CV folds, leveling near 20. Note: the paper reports accuracies only via figure curves, not a single headline percentage; no hardware-cost numbers.
- **Relevance to D2D anomaly detection**: Methodological template — the die-to-die structure here (TSV + microbumps + RDL) is the same class that carries D2D signals in 2.5D/3D chiplet packages. Reusable: use channel S-parameters (S11/S21/phase) as the ML feature vector instead of imaging; treat link health as supervised classification and even regress severity; the finding that the low-frequency band is most separable informs D2D test-stimulus frequency choice; the KNN-vs-RF + k-fold protocol is ready to reuse. Caveat: HFSS-simulated, single-link, TSV-specific void/short/open classes — a D2D project would adapt features to measured/injected link anomalies and add real silicon or fault-injection data.
- **Correction note**: Authors were the placeholder "(3D-IC test group)"; now corrected to Yu-Jung Huang, Chung-Long Pan, Shin-Chun Lin, Mei-Hui Guo (corresponding), I-Shou University / NSYSU. Venue precisely corrected to IEEE TCPMT vol. 8 no. 4, pp. 699–706, April 2018. Specified classifiers (KNN K=5, Random Forest) and HFSS-simulated S-parameter features; importantly, do NOT attribute a single accuracy figure — the paper gives accuracies only as figure curves (RF ~0.9–1.0), and data is simulation, not measured silicon.
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 13. Non-destructive Fault Diagnosis of Electronic Interconnects by Learning Signal Patterns of Reflection Coefficient in the Frequency Domain
- **Authors**: Tae Yeob Kang (Dept. of Mechanical Engineering, The University of Suwon, Hwaseong, Republic of Korea); Haebom Lee (AIMMO, Seoul); Sungho Suh (German Research Center for AI, DFKI, Kaiserslautern / Computer Science, RPTU Kaiserslautern-Landau, Germany; corresponding author, sungho.suh@dfki.de).
- **Venue**: Preprint submitted to Microelectronics Reliability (Elsevier). arXiv:2304.10207v3 [cs.LG], 4 Oct 2024 (dated October 8, 2024; original submission April 2023).
- **DOI/Link**: https://arxiv.org/abs/2304.10207 (arXiv:2304.10207)
- **Methods**: Learns the full frequency-domain reflection-coefficient (S11) magnitude pattern (0–14 GHz, measured with a VNA + GSG probes) as the input feature, instead of a single-frequency scalar. A novel Severity Rating Ensemble Learning (SREL) decomposes the joint root-cause-plus-severity problem into a bank of independent binary "baseline networks" (sigmoid outputs) whose decisions are aggregated to preserve the ordinal severity relationship; backbones tested are EfficientNet, 1DCNN-3, 1DCNN-1. Compared against softmax multiclass-CNN, Random Forest, and K-means.
- **Novelty**: First to use the full reflection-coefficient frequency PATTERN (treating discarded irregularities as features) and first to do non-destructive ROOT-CAUSE analysis (mechanical vs corrosion) plus ordinal severity via the SREL ensemble-of-binary-classifiers, with better noise robustness, fewer parameters, and faster inference than a softmax multiclass net.
- **Evaluation**: Measured hardware — fabricated Cu interconnect test vehicles (56 specimens/batch, 15 batches); 790 samples across 7 classes (Normal, M1–M3 laser-cut cracks, C1–C3 corrosion); 6:2:2 split; Gaussian noise (5/10/15 dB) for robustness. SREL+EfficientNet best at 99.3% accuracy / macro F1 0.991 (vs 98.6% best existing ML/DL: multiclass-CNN-EfficientNet and Random Forest; K-means 81.2%). SREL is most noise-robust; single-frequency baselines (DC resistance, TDR, S11@8 GHz) show no usable trend. Compute on i5-9600K + RTX 2070 Super; no on-chip area/power (bench measurement).
- **Relevance to D2D anomaly detection**: Highly relevant — non-destructive, signal-pattern-based fault diagnosis for chip-package Cu interconnects, mapping closely to D2D links. Reusable: using the FULL frequency-domain S11/reflection pattern (not a single-frequency scalar) as the ML feature (D2D bump/microbump/RDL impedance discontinuities show as reflection signatures); the SREL ensemble-of-binary-classifiers for simultaneous root-cause + ordinal-severity diagnosis of D2D anomaly types; and the multi-dB Gaussian-noise robustness protocol. Caveats: ex-situ bench VNA over 0–14 GHz (not an on-die/in-situ embedded sensor), no area/power overhead, not a real-time per-link on-chip detector.
- **Correction note**: Authors were the placeholder "(Interconnect-FD group)"; now corrected to Tae Yeob Kang, Haebom Lee, Sungho Suh (U. Suwon / AIMMO / DFKI + RPTU — a Korea-Germany collaboration). Venue clarified as a preprint submitted to Microelectronics Reliability (Elsevier), arXiv:2304.10207 v3 (Oct 2024). Added verified specifics: signal is the reflection coefficient/S11 (not S21), the named algorithm is SREL (ensemble of binary nets, not a single multiclass net), 790 samples / 7 classes, measured hardware + Gaussian-noise robustness, best accuracy 99.3% (98.6% with existing methods).
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 14. ChipletQuake: On-die Digital Impedance Sensing for Chiplet and Interposer Verification
- **Authors**: Saleh Khalaj Monfared, Maryam Saadat Safa, Shahin Tajik (all Worcester Polytechnic Institute, Worcester, MA).
- **Venue**: arXiv preprint, arXiv:2504.19418v1 [cs.CR], 28 Apr 2025. No formal conference/journal venue is printed on the PDF.
- **DOI/Link**: https://arxiv.org/abs/2504.19418 (arXiv:2504.19418)
- **Methods**: A fully on-die, fully-digital framework that sweeps the shared power-delivery network with a 2D mesh of monitoring blocks (each = a TDC delay sensor + an inverter-based current actuator) on a verifier chiplet (FPGA SLR). A frequency sweeper activates actuators across selected frequencies and records sensor traces to form an impedance signature; statistical distinguishability uses Welch's t-test (|t|>4.5) and the Wasserstein distance with bootstrap thresholds. A challenge-response protocol with a one-time key K_ver (random actuator/sensor/frequency IDs) supports remote attestation against a stored golden signature.
- **Novelty**: Claimed first fully-digital, spectral (frequency-sweep, not FFT) on-die impedance-sensing framework that verifies adjacent chiplets AND the host interposer via the shared PDN with NO direct signal interface and NO extra hardware, able to detect dormant/passive Hardware Trojans and subtle interposer tampering.
- **Evaluation**: Measured silicon on an AMD Virtex UltraScale+ VU37P HBM FPGA (three SLR chiplets on a silicon interposer); 32 monitoring blocks; T=500/1000 traces; frequency span ~100–900 MHz. Four case studies: app distinguishing (AES/FFT/CNN), interposer tampering (129 vs 133 SLLs, t up to ~5–10, Wasserstein peaks ~25), far-SLR footprinting (t ~30–35), and HT detection (Trust-Hub AES-T1100, t ~−30 to −90). Golden-vs-reference self-comparisons stay |t|<4.5. No results table, no FPR/ROC/accuracy %, no LUT/FF/area/power numbers.
- **Relevance to D2D anomaly detection**: Highly relevant — directly senses the shared interposer and adjacent-chiplet links, detecting changes in the number of interposer SLL D2D interconnects (129 vs 133), i.e. anomalies/tampering on the die-to-die interconnect fabric. Reusable: the on-die actuator+TDC mesh as a no-extra-pin probe of the D2D PDN/interposer; the frequency-sweep→impedance-signature anomaly fingerprint; the golden-vs-measured decision rule (Welch's t-test |t|>4.5 + Wasserstein with bootstrap); and the K_ver challenge-response for remote link-integrity attestation, with Trust-Hub AES-T1100 and SLL-count tampering as concrete anomaly classes. Caveat: demonstrated on FPGA SLRs over a silicon interposer rather than standardized UCIe/BoW D2D PHY links, so the mapping is by analogy.
- **Correction note**: Authors were already correct (Monfared, Saadat Safa, Tajik, WPI). Venue corrected: it is an arXiv preprint (arXiv:2504.19418v1, 28 Apr 2025) with NO peer-reviewed venue printed — the prior "Sensors 25(15), 4861, 2025 (MDPI)" citation could not be verified from the PDF and should not be asserted. Also corrected the sensing method: it is a fully-digital frequency-SWEEP (spectral) impedance method explicitly contrasted against FFT-based PDNSig, validated on an AMD VU37P FPGA (three SLRs), and it detects HTs, interposer tampering, and adjacent-chiplet design changes.
- **✓ Status**: Verified against the downloaded PDF (2026-06-03 reading pass).

### 15. The Future of Chiplet Reliability: Interconnect Failure Prediction with 100% Lane Coverage
- **⚠ Verification status**: NOT in the downloaded set — entry below is from the initial round-1 sweep and has NOT been verified against a PDF (web/industrial source or pending download). Treat authors/abstract as provisional.
- **Authors**: proteanTecs (industrial)
- **Venue**: proteanTecs technical blog / chiplet white paper, 2024
- **DOI/Link**: https://www.proteantecs.com/blog/the-future-of-chiplet-reliability-interconnect-failure-prediction-with-100-lane-coverage
- **Abstract**: Describes lane-by-lane chiplet interconnect failure prediction using on-chip Interconnect Monitoring Agents combined with deep-data analytics; predictive lane swap before failure.
- **Why relevant**: Sets the industrial benchmark for the "ideal" deployed D2D anomaly-detection workflow.
- **Recommended for download**: YES

---

## Tier-1 correction log (2026-06-03 PDF-verification pass)

What changed in each verified entry versus the round-1 sweep:

- **#1**: Placeholder author "(DRAM SI anomaly group)" → verified 6-author KAIST + Samsung list (corresponding author Dong Eui Chang); reframed from "D2D" to a domain-adjacent *simulated mobile-DRAM-channel* paper.
- **#2**: Placeholder "(Synopsys / academic SLM group)" → verified ASU (Chakrabarty group) + Intel authors; **no Synopsys involvement**; added the XGBoost cloud-diagnosis stage and verified 1.2% area / >0.95 AUCROC numbers; venue pinned to ITC 2025, pp. 131–140.
- **#3**: "Arizona State University authors" → verified Bhoumik, Bailey, Chakrabarty; corrected the method from CTE/warpage functional simulation to a Q3D→HSPICE flow + 3-pattern graph-coloring BIST (deterministic, **not** ML).
- **#4**: Authors already correct, but the **method was wrong** — it is the ARCS algorithm + TX/RX BIST detecting stuck-at + wired-OR/AND bridging (NOT IEEE-1838 DWR-cell enhancement, and NOT delay/crosstalk faults). Venue pinned to ITC 2024, pp. 149–156.
- **#6**: "E. J. Marinissen et al. (CITR-WG, imec)" → verified four authors (Marinissen, Pancholi, Chuang, Keim); narrowed venue to **VTS 2024 Special Session**; clarified it is a position paper *about* the standard with no experiments.
- **#7**: Placeholder "(Industrial post-silicon ML group)" → five verified Intel-Mexico authors; **year fixed 2021 → ITC 2020**; added concrete SMV/SATA framing with Boosted Trees 94.84% best.
- **#8**: Placeholder "(Signal-integrity DL group)" → verified Miao Weiyang, Chuan Seng Tan, Mihai D. Rotaru (A*STAR/NTU); **replaced a fabricated abstract** (LeNet/Wide-ResNet/Inception-v4, Q-factor, OOK/PAM4 transfer-learning) with the actual single CNN doing 7-impairment classification + localization + regression, 100% accuracy at 10 epochs; venue EPTC 2022.
- **#11**: "M. Hasanzadeh et al." → full four-author list (Hasanzadeh, Khalil, Sturton, Patooghy); venue fixed to **IEEE TCAD** (DOI 10.1109/TCAD.2026.3657198); clarified the method is **NON-ML statistical thresholding** (RF only a baseline/feature-selector).
- **#12**: Placeholder "(3D-IC test group)" → verified Huang, Pan, Lin, Guo (corresponding); venue fixed to **IEEE TCPMT vol. 8 no. 4 (April 2018)**; flagged that the paper reports **no single headline accuracy** (figure-curve results only, RF ≫ KNN).
- **#13**: Placeholder "(Interconnect-FD group)" → verified Kang, Lee, Suh (U. Suwon / AIMMO / DFKI+RPTU); corrected feature to **reflection coefficient / S11** (not S21) and best accuracy to 99.3% via the **SREL** ensemble on measured hardware.
- **#14**: Authors already correct, but venue corrected — it is **arXiv:2504.19418 only** (the unverifiable MDPI *Sensors* 25(15) citation was removed), and the sensing is a fully-digital frequency-**sweep** method (not FFT) on an AMD VU37P FPGA.

*Entries #5, #9, #10, #15 were not in the download set and remain unverified (see their ⚠ markers).*

---

## Tier 1b: Newly surfaced references (cited *inside* the Tier-1 papers — candidates to add)

Harvested and de-duplicated from the reference lists of the 11 read papers (the `citations_worth_chasing` of each). These fill the survey's biggest hole — **native-D2D / chiplet-interconnect test** and **electrical-signature interconnect-health sensing** — which the round-1 sweep under-covered. ★ = highest value for the recommended Direction-3 contribution. *Status: surfaced from citations, not yet independently fetched/verified.*

### Native D2D / chiplet-interconnect test (the missing anchors)
- ★ **T.-H. Wang et al., "Test and repair improvements for UCIe," IEEE ETS 2024** — closest UCIe-specific D2D test/repair work; *the* target modality. (via #3)
- ★ **P.-Y. Chuang et al., "Generating test patterns for chiplet interconnects…," IEEE TCAD 2024** — the "16 placement-aware patterns suffice" structural-test SOTA to position against. (via #3 / #6)
- **C. Cui et al., "Physical-aware interconnect testing and repairing of chiplets," IEEE ETS 2023.** (via #3)
- **S. Chakravarty, "A call to standardize chiplet interconnect testing," IEEE VTS 2022** — source of the ~95%-shorts-vs-opens statistic; and **"3D interconnect test challenge," ETS 2022** — defect taxonomy. (via #3 / #4)
- **IEEE Std 1838-2019** 3D test-access standard; **Marinissen et al., P3405 Part 2, ETS 2024.** (via #6)

### Electrical-signature + on-chip interconnect-health sensing (the feature-source anchors)
- ★ **I. Shin, K. Koo, D. Kwon, "Non-invasive on-chip interconnect health sensing based on bit error rates," Sensors 2018** — on-chip, BER-based, in-situ; the closest thing to an embedded D2D link-health monitor. (via #13)
- ★ **D. Kwon et al., "Early detection of interconnect degradation by continuous monitoring of RF impedance," IEEE TDMR 2009** — foundational continuous-impedance interconnect-health monitoring. (via #13)
- **T. Y. Kang et al., "Early detection & cause analysis of interconnect defects by ranking-CNN of S-parameter patterns," IMAPS 2019** — direct predecessor to SREL. (via #13)
- **T. Mosavirik et al., "ImpedanceVerif: on-chip impedance sensing for tamper detection," IACR TCHES 2023**; **"Silicon Echoes: frequency-selective impedance Trojan/tamper detection," TCHES 2023** — the on-die impedance lineage behind #14. (via #13 / #14)
- **C. Okoro et al., "Accelerated stress test of TSV using RF signals," IEEE T-ED 2013**; **D. H. Jung et al., "TSV defect modeling, measurement and analysis," IEEE TCPMT 2017.** (via #12)

### On-chip anomaly engines / SLM (deployment-architecture anchors)
- **E. Ortega et al., "E-SCOUT: spatial-clustering outlier detection via telemetry," IEEE ITC 2024** — the direct prior SLM baseline OCTANE (#2) beats.
- **A. Deric, D. Holcomb, "Integrity checking for zero-trust chiplet systems using between-die delay PUFs," IACR TCHES 2022**; **T. Zhang et al., "SiGuard: run-time SiP security via power-noise variation," IEEE TVLSI 2023.** (via #14)

### ML-for-anomaly-detection method references (model-design anchors)
- **L. Ruff et al., "Deep semi-supervised anomaly detection (Deep SAD)," ICLR 2020**; **D. Gong et al., "Memorizing normality (MemAE)," ICCV 2019** — AE-AD families #1 did *not* compare against; useful baselines/upgrades.
- **R. Medico et al., "Autoencoding density-based anomaly detection for SI," EPEPS 2018** and **"ML-based error detection for SI," IEEE TCPMT 2019** — closest SI-AD prior art. (via #1)
- **S. Chen et al., "Using ranking-CNN for age estimation," CVPR 2017** — theory that binary-aggregation beats softmax (underpins SREL; relevant for ordinal severity). (via #13)

> **Verify-before-citing**: #1, #13, #14, #3 are arXiv preprints (some carry IEEE copyright lines but no named venue) — confirm the final publication venue before formal citation. #11 is a 2026 IEEE TCAD early-access author version — confirm final pagination.

---

## Tier 2: Important (related methods, general SI ML, hardware time-series anomaly)

### 16. Equalization Tuning of the PCIe Physical Layer by Using Machine Learning in Industrial Post-silicon Validation
- **Authors**: (Industrial PCIe ML group)
- **Venue**: IEEE / ResearchGate 373015697, 2023
- **DOI/Link**: https://www.researchgate.net/publication/373015697
- **Abstract**: Industrial ML methodology that clusters channels (unsupervised) and trains Gaussian Process Regression (GPR) supervised models on eye-diagram margins to predict optimal PHY tuning settings.
- **Why relevant**: Demonstrates ML extracting eye-margin behavior — a feature space we will reuse for D2D anomaly detection.

### 17. PCIe Gen6 Physical Layer Equalization Tuning by Using Unsupervised and Supervised Machine Learning Techniques
- **Authors**: J. E. Rangel-Patiño, J. E. Rayas-Sánchez et al.
- **Venue**: IEEE, 2023 (RG 377091076)
- **DOI/Link**: https://www.researchgate.net/publication/377091076
- **Abstract**: Extends PCIe Gen5 ML EQ tuning to PAM4 64 GT/s; uses K-means clustering and GPR for eye-margin prediction.
- **Why relevant**: PAM4 + ML + eye-margin — directly analogous to UCIe Advanced Package PAM4 channels.

### 18. PCIe Gen5 Physical Layer Equalization Tuning by K-Means Clustering and GPR
- **Authors**: J. E. Rangel-Patiño, J. E. Rayas-Sánchez et al.
- **Venue**: IEEE 2023
- **DOI/Link**: https://www.researchgate.net/publication/372971895
- **Abstract**: Foundational paper of the PCIe ML EQ tuning series.
- **Why relevant**: Establishes a robust feature/eye representation pipeline.

### 19. NeuralEQ: Neural-Network-Based Equalizer for High-Speed Wireline Communication
- **Authors**: (NeuralEQ team)
- **Venue**: arXiv 2308.02133, 2023 (ICLR-style)
- **DOI/Link**: https://arxiv.org/abs/2308.02133
- **Abstract**: A neural network that mimics forward-backward algorithm and outperforms FFE/DFE while reducing complexity — for high-speed wireline.
- **Why relevant**: Provides a DNN-based receiver baseline whose internal features can be reused for anomaly detection.

### 20. SERDES Link Training with Edge Inference: Neural-Network-Driven Discrete Optimization
- **Authors**: (Wireline ML group, OpenReview)
- **Venue**: OpenReview (workshop), 2024
- **DOI/Link**: https://openreview.net/forum?id=OX4Tk43uwv
- **Abstract**: CNN trained on ILP-generated labels for SerDes link training; 24,000× speedup, runs on RISC-V microcontroller.
- **Why relevant**: Edge-inference link training — directly applicable to on-chiplet ML monitor design.

### 21. Self-Evolution Cascade Deep Learning Model for High-Speed Receiver Adaptation
- **Authors**: (SI/ML group)
- **Venue**: IEEE TCPMT / TCAD (Xplore 9085389), 2020/2021
- **DOI/Link**: https://ieeexplore.ieee.org/document/9085389/
- **Abstract**: Cascade DNN to model adaptive SerDes Rx behavior efficiently; replaces IBIS-AMI inner loop.
- **Why relevant**: Reference for high-fidelity link surrogate models for synthetic-data generation.

### 22. CTLE Adaptation Using Deep Learning in High-Speed SerDes Link
- **Authors**: (Wireline DL group)
- **Venue**: IEEE 2020 (Xplore 9159283)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9159283/
- **Abstract**: DNN that mimics CTLE adaptation behavior in high-speed SerDes.
- **Why relevant**: Shows that DL can model the analog adaptive front-end; useful for D2D PHY simulation.

### 23. Deep Reinforcement Learning-Based DRAM Equalizer Parameter Optimization Using Latent Representations
- **Authors**: (DRAM ML group)
- **Venue**: arXiv 2507.02365, 2025
- **DOI/Link**: https://arxiv.org/pdf/2507.02365
- **Abstract**: Uses AE-learned latent signal representations and a model-free A2C agent to optimize DRAM equalizer taps.
- **Why relevant**: A sister-paper to Paper #1 demonstrating how the same latent space can drive control as well as detection.

### 24. Predicting the Characteristics of High-Speed Serial Links Based on DNN–Transformer Cascaded Model
- **Authors**: (SI DL group, MDPI Electronics)
- **Venue**: Electronics 13(15), 3064, 2024
- **DOI/Link**: https://www.mdpi.com/2079-9292/13/15/3064
- **Abstract**: DNN + Transformer cascade that takes physical features → predicts frequency response, equalizer parameters, eye diagrams, and channel-operating-margins. Maximum relative error <2% on 3-tap TX FFE + dual-DC-gain CTLE + 12-tap DFE.
- **Why relevant**: Provides a state-of-the-art surrogate model for eye/COM prediction — ideal for synthetic anomaly training data.

### 25. LiTformer: Efficient Modeling and Analysis of High-Speed Link Transmitters Using Non-Autoregressive Transformer
- **Authors**: (HSL Transformer team)
- **Venue**: arXiv 2411.11699, 2024 (DAC-track submission)
- **DOI/Link**: https://arxiv.org/pdf/2411.11699
- **Abstract**: Non-AR Transformer for high-speed link Tx modeling considering crosstalk from multiple links. 148–456× speedup on 2-link, 404–944× on 16-link; mean relative error 0.68 – 1.25%.
- **Why relevant**: State-of-the-art surrogate for synthetic D2D Tx + crosstalk data.

### 26. Worst-case Power Integrity Prediction Using Convolutional Neural Network
- **Authors**: (PI CNN group)
- **Venue**: ACM TODAES, 2022
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3564932
- **Abstract**: CNN framework that beats commercial PI tools with 0.63 – 1.02% mean relative error and 25 – 69× speedup for worst-case power-noise prediction.
- **Why relevant**: Provides a fast surrogate for PDN-noise feature generation that couples into D2D link signal integrity.

### 27. Proactive Voltage Droop Mitigation Using Dual-Proportional-Derivative Control Based on Current and Voltage Prediction (28nm Multicore)
- **Authors**: (ISSCC 2024 paper)
- **Venue**: ISSCC 2024 (IEEE Xplore 10454398)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10454398/
- **Abstract**: Detects DC droops > 10 mV and tracks timing changes > 1 FO2 delay; integrates a dual-PD prediction control loop.
- **Why relevant**: A canonical on-die droop detector — the "voltage-noise channel" for our anomaly framework.

### 28. VDPred: Predicting Voltage Droop for Power-Efficient 3D Multi-core Processor Design
- **Authors**: (3D MC droop group)
- **Venue**: IEEE 2021 (Xplore 9426107)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9426107/
- **Abstract**: Offline-learned model for power prediction based on micro-architectural events to predict droops in a 3D multi-core SoC.
- **Why relevant**: ML droop prediction for 3D systems — relevant to chiplet PDN-induced jitter on D2D lanes.

### 29. SparseDroop: Hardware–Software Co-Design for Mitigating Voltage Droop in DNN Accelerators
- **Authors**: (DNN-Accel droop group)
- **Venue**: J. Low-Power Electronics 16(1), 2, 2025 (MDPI)
- **DOI/Link**: https://www.mdpi.com/2079-9268/16/1/2
- **Abstract**: Workload-aware voltage-droop mitigation using DNN sparsity.
- **Why relevant**: Workload-aware droop mitigation extends naturally to predictive D2D link margining.

### 30. Switching Frequency as FPGA Monitor: Studying Degradation and Ageing Prognosis at Large Scale
- **Authors**: (EU-XFEL FPGA aging group)
- **Venue**: arXiv 2412.15720, 2024 (TCAD/TVLSI submission)
- **DOI/Link**: https://arxiv.org/pdf/2412.15720
- **Abstract**: ML aging-degradation prognosis from 298 naturally aged FPGAs (EU-XFEL accelerator) using ring-oscillator switching frequency; 60-day forecasts with 0.002% relative error.
- **Why relevant**: A rare *large-scale real-world* aging-monitoring ML deployment — informs how D2D-lane aging can be predicted.

### 31. GNN4REL: Graph Neural Networks for Predicting Circuit Reliability Degradation
- **Authors**: L. Alrahis et al.
- **Venue**: IEEE TCAD, 2022 (Xplore 9852805)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9852805/
- **Abstract**: GNN that estimates the impact of process variation and aging on path delays without standard cells / STA, calibrated against 14 nm industrial data.
- **Why relevant**: GNN reliability framework that can be specialized to chiplet-interconnect graphs.

### 32. Modeling and Predicting Transistor Aging under Workload Dependency using Machine Learning
- **Authors**: (Aging ML group)
- **Venue**: arXiv 2207.04134, 2022 (TCAD submission)
- **DOI/Link**: https://arxiv.org/pdf/2207.04134
- **Abstract**: ML approach to model workload-dependent transistor aging.
- **Why relevant**: Workload-dependent aging maps to BER/timing drift on D2D lanes.

### 33. Machine Learning Approach for Fast Electromigration Aware Aging Prediction
- **Authors**: S. Dey et al.
- **Venue**: ACM TODAES, 2020/2021
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3399677
- **Abstract**: NN-based regression for fast lifetime prediction of large on-chip power grid networks.
- **Why relevant**: PDN aging fundamentally limits D2D link margins; this approach yields predictive signals.

### 34. ATPG via AI: A Survey for Machine Learning in Test Generation
- **Authors**: (Survey, 2024)
- **Venue**: blog.wangxm.com PDF, 2024 (survey of ML for ATPG)
- **DOI/Link**: https://blog.wangxm.com/wp-content/uploads/2024/12/ATPG_via_AI__A_Survey_for_Machine_Learning_in_Test_Generation.pdf
- **Abstract**: Comprehensive survey of ML-based ATPG covering classical, RL, and GNN approaches.
- **Why relevant**: Background context for ML × test/diagnosis intersection.

### 35. A Survey and Recent Advances: Machine Intelligence in Electronic Testing
- **Authors**: (Survey)
- **Venue**: J. Electronic Testing (Springer), 2024
- **DOI/Link**: https://link.springer.com/article/10.1007/s10836-024-06117-7
- **Abstract**: Survey of ML in electronic testing covering diagnosis, post-silicon validation, yield, and DfT.
- **Why relevant**: Required broad-context citation; identifies gaps for our work.

### 36. Anomaly Detection in Real-Time Multi-Threaded Processes Using Hardware Performance Counters
- **Authors**: (HPC anomaly group)
- **Venue**: IEEE TIFS, 2019/2020 (Xplore 8737990)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8737990/
- **Abstract**: Black-box HPC-time-series ML classifier for real-time anomaly detection.
- **Why relevant**: Reusable feature/training pipeline for D2D link-counter time series.

### 37. Network-on-Chip Attack Detection using Machine Learning (and related Springer chapter)
- **Authors**: (NoC security ML group)
- **Venue**: Springer, 2021 (RG 351289369)
- **DOI/Link**: https://link.springer.com/chapter/10.1007/978-3-030-69131-8_10
- **Abstract**: ML attack/anomaly detection in NoC.
- **Why relevant**: Methodologically transferable to D2D adapter-layer anomalies.

### 38. Denial-of-Service Attack Detection using Machine Learning in NoC Architectures
- **Authors**: (NoC DoS group)
- **Venue**: ACM/IEEE NoCS 2021
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3479876.3481589
- **Abstract**: Lightweight ML detection of DoS on NoC links.
- **Why relevant**: Provides traffic-pattern feature engineering for the *adapter* layer of UCIe.

### 39. Neural Network-based Online Fault Diagnosis in Wireless-NoC Systems
- **Authors**: (Wireless-NoC FD group)
- **Venue**: J. Electronic Testing (Springer), 2021
- **DOI/Link**: https://link.springer.com/article/10.1007/s10836-021-05966-w
- **Abstract**: Offline-trained FC and CNN models deployed at runtime for fault diagnosis in WiNoC; up to 81.2% fault identification.
- **Why relevant**: Direct precedent for *online* fault diagnosis with NNs in interconnect substrates.

### 40. Attack and Anomaly Prediction in Networks-on-Chip of Multiprocessor SoC-based IoT Utilizing ML
- **Authors**: (NoC + IoT ML group)
- **Venue**: Springer SOCA, 2024
- **DOI/Link**: https://link.springer.com/article/10.1007/s11761-024-00393-z
- **Abstract**: ML attack/anomaly prediction in NoC for IoT MPSoCs.
- **Why relevant**: Recent NoC ML anomaly-detection methodology; transferable features.

### 41. Hardware Trojan Detection and High-Precision Localization in NoC-Based MPSoC Using ML
- **Authors**: (ASP-DAC 2023 NoC HT group)
- **Venue**: ASP-DAC 2023 (ACM 3566097.3567922)
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3566097.3567922
- **Abstract**: ML-based hardware-Trojan localization in NoC MPSoCs.
- **Why relevant**: Localization layer useful for D2D-lane-level diagnosis.

### 42. TranAD: Deep Transformer Networks for Anomaly Detection in Multivariate Time Series
- **Authors**: (TranAD group)
- **Venue**: VLDB 2022
- **DOI/Link**: https://dl.acm.org/doi/abs/10.14778/3514061.3514067
- **Abstract**: Transformer-based AD for multivariate time series with attention-based encoders.
- **Why relevant**: Strong candidate ML architecture for multi-lane D2D telemetry anomaly detection.

### 43. CARLA: Self-supervised Contrastive Representation Learning for Time Series Anomaly Detection
- **Authors**: (CARLA group)
- **Venue**: arXiv 2308.09296, 2023
- **DOI/Link**: https://arxiv.org/pdf/2308.09296
- **Abstract**: Self-supervised contrastive AD that injects synthetic anomalies and learns deviations.
- **Why relevant**: Excellent matched method for D2D anomaly detection where labeled anomalies are scarce.

### 44. AnomalyBERT: Self-Supervised Transformer for Time-Series Anomaly Detection
- **Authors**: (AnomalyBERT)
- **Venue**: arXiv 2305.04468, 2023
- **DOI/Link**: https://arxiv.org/abs/2305.04468
- **Abstract**: BERT-style architecture trained with data-degradation scheme for unsupervised TSAD.
- **Why relevant**: Reusable as a backbone for multi-lane D2D telemetry analysis.

### 45. MT-former: Multi-Task Hybrid Transformer and Deep SVDD for Novel Anomaly Detection in Semiconductor Manufacturing
- **Authors**: (MT-former team)
- **Venue**: Light: Advanced Manufacturing, 2025
- **DOI/Link**: https://www.light-am.com/article/doi/10.37188/lam.2025.032
- **Abstract**: Hybrid Transformer encoder jointly trained on classification + reconstruction, then fine-tuned with Deep-SVDD; +8.19% AUC over Deep-SVDD on SK Hynix data.
- **Why relevant**: A direct hybrid-Transformer baseline for novel-anomaly detection in semiconductor signals.

### 46. Anomaly Detection in Semiconductor Processing using CNN with Bidirectional LSTM
- **Authors**: (Semi-process ML)
- **Venue**: RG 393588872 / IEEE, 2024
- **DOI/Link**: https://www.researchgate.net/publication/393588872
- **Abstract**: CNN-BiLSTM with XGBoost feature selection for AD in semiconductor process data.
- **Why relevant**: Spatial-temporal architecture pattern reusable on per-lane × time tensor features of D2D telemetry.

### 47. Generative Pre-Training of Time-Series Data for Unsupervised Fault Detection in Semiconductor Manufacturing (TRACE-GPT)
- **Authors**: (TRACE-GPT)
- **Venue**: arXiv 2309.11427, 2023
- **DOI/Link**: https://arxiv.org/pdf/2309.11427
- **Abstract**: Time-series AD with convolutional embedding + GPT-style Transformer decoder.
- **Why relevant**: Generative pretraining for unlabeled sensor streams — relevant for our many-lane setting.

### 48. Workload-Aware DRAM Error Prediction using Machine Learning
- **Authors**: (Workload-aware DRAM)
- **Venue**: arXiv 2003.12448 / academic paper, 2020
- **DOI/Link**: https://arxiv.org/pdf/2003.12448
- **Abstract**: Predicts DRAM single/multi-bit error rates from program features with <10.5% mean error.
- **Why relevant**: Sets the methodology for workload-conditional anomaly prediction; analogous to D2D BER prediction.

### 49. Predicting DRAM Reliability in the Field with Machine Learning
- **Authors**: (Middleware 2017 industrial track)
- **Venue**: ACM Middleware 2017 (older but foundational)
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3154448.3154451
- **Abstract**: Field-deployed ML correlates correctable errors and sensor metrics to predict uncorrectable errors weeks ahead.
- **Why relevant**: Strong field-deployment example of ML reliability prediction.

### 50. DRAM Failure Prediction in AIOps: Empirical Evaluation, Challenges and Opportunities
- **Authors**: (AIOps DRAM)
- **Venue**: arXiv 2104.15052, 2021 (DSN-track)
- **DOI/Link**: https://arxiv.org/pdf/2104.15052
- **Abstract**: AIOps evaluation of DRAM failure prediction models including imbalanced-data handling.
- **Why relevant**: Methodological lessons for label-imbalance handling, directly applicable to D2D lane failures.

### 51. Vmin Shift Prediction Using Machine Learning-Based Methodology for Automotive Products
- **Authors**: (Vmin-shift ML)
- **Venue**: IEEE 2024 (Xplore 10529430)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10529430/
- **Abstract**: ML-based Vmin shift prediction before HTOL; >20% margin reduction.
- **Why relevant**: Margin/aging prediction transferable to D2D link margin prediction.

### 52. A Siamese Deep Learning Framework for Efficient Hardware Trojan Detection Using Power Side-Channel Data
- **Authors**: (Siamese HT)
- **Venue**: Scientific Reports (Nature), 2024 (PMC 11156655)
- **DOI/Link**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11156655/
- **Abstract**: Siamese DNN on power-trace side-channel data for hardware Trojan detection.
- **Why relevant**: Useful for *power-noise channel* anomaly detection in chiplet PDNs.

### 53. Identification of Stealthy Hardware Trojans through On-Chip Temperature Sensing and Autoencoder ML
- **Authors**: (Thermal AE Trojan)
- **Venue**: IEEE 2024 (Xplore 10405958)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10405958/
- **Abstract**: Autoencoder-based ML on on-chip temperature sensors detects stealthy hardware Trojans.
- **Why relevant**: Direct example of AE + thermal time-series anomaly detection on chip — methodologically aligned with thermal-drift D2D detection.

### 54. RF Analog Hardware Trojan Detection Through Electromagnetic Side-Channel (Classification AE)
- **Authors**: (RF Trojan AE)
- **Venue**: Academia.edu / IEEE, 2023
- **DOI/Link**: https://www.academia.edu/99231969
- **Abstract**: Classification autoencoder for analog/RF HT detection; >90% accuracy on single-tone and BLE.
- **Why relevant**: Analog/RF AE deployment template for D2D PHY analog observables.

### 55. Using Machine Learning for Anomaly Detection on a System-on-Chip under Gamma Radiation
- **Authors**: (SoC radiation AD)
- **Venue**: Nuclear Engineering and Technology (Elsevier), 2022/2024 (arXiv 2201.01588)
- **DOI/Link**: https://arxiv.org/pdf/2201.01588
- **Abstract**: One-Class SVM, IF, and Elliptic Envelope ML algorithms on FPGA board sensor data; OC-SVM achieves recall 0.95 under gamma exposure (monitoring VDDR3 = DDR memory voltage).
- **Why relevant**: A rare paper that combines IF / OC-SVM / EE on *actual silicon sensor streams* (including DDR voltage) — a strong methodological precedent.

---

## Tier 3: Supplementary (chiplet test architecture, surveys, foundational SerDes / HBM)

### 56. The Survey of Chiplet-based Integrated Architecture: An EDA perspective
- **Authors**: (Chiplet EDA survey)
- **Venue**: arXiv 2411.04410, 2024
- **DOI/Link**: https://arxiv.org/abs/2411.04410
- **Abstract**: EDA-perspective survey of chiplet integration, including test/repair.
- **Why relevant**: Broad context survey.

### 57. Special Session: Test Challenges in a Chiplet Marketplace
- **Authors**: (Special session)
- **Venue**: IEEE conference 2020 (Xplore 9107636)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9107636/
- **Abstract**: Identifies open chiplet-test challenges and DfT strategies.
- **Why relevant**: Foundational problem statement.

### 58. Applying IEEE Test Standards to Multidie Designs
- **Authors**: (IEEE standards survey)
- **Venue**: IEEE D&T (Xplore 9815874)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9815874/
- **Abstract**: Survey of 1149.1, 1149.6, 1500, 1838 applied to chiplet/multidie packages.
- **Why relevant**: Standard-compliance baseline for any D2D-test paper.

### 59. IEEE 1838-2019 Standard for Test Access Architecture for 3D Stacked ICs
- **Authors**: IEEE
- **Venue**: IEEE Standard, 2019/2020 (Xplore 9036129)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9036129
- **Abstract**: Standard for serial PTAP, optional flexible parallel ports for stacked dies.
- **Why relevant**: Mandatory architectural reference.

### 60. Bunch of Wires (BoW): An Open Inter-Chiplet Communication Link
- **Authors**: R. Farjadrad, M. Kuemerle et al.
- **Venue**: IEEE Micro, 2020/2021 (Xplore 9271827)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9271827/
- **Abstract**: BoW open D2D PHY spec for organic / advanced packaging.
- **Why relevant**: Alternative to UCIe; must understand both substrates.

### 61. Signal and Power Integrity Design and Analysis for Bunch-of-Wires (BoW) Interface for Chiplet Integration (ECTC 2023)
- **Authors**: IBM Research
- **Venue**: ECTC 2023
- **DOI/Link**: https://research.ibm.com/publications/signal-and-power-integrity-design-and-analysis-for-bunch-of-wires-bow-interface-for-chiplet-integration-on-advanced-packaging
- **Abstract**: Detailed SI/PI analysis of BoW chiplet interface on advanced packaging.
- **Why relevant**: SI/PI baseline for BoW; provides simulated feature spaces.

### 62. UCIe 2.0 / UCIe Specification 2024 (Property of UCIe Consortium)
- **Authors**: UCIe Consortium (D. Das Sharma et al.)
- **Venue**: UCIe Consortium release, August 2024
- **DOI/Link**: https://files.futurememorystorage.com/proceedings/2024/20240808_SPOS-301-1_UCIe_Consortium_Das_Sharma.pdf
- **Abstract**: UCIe 2.0 adds DFx architecture (UDA), management fabric for testing/telemetry/debug, periodic parity-flit injection + checking, periodic retrain to capture eye margin.
- **Why relevant**: Defines the on-chip mechanisms our ML anomaly detector will consume.

### 63. A 4nm 1.15 TB/s HBM3 Interface with Resistor-Tuned Offset-Calibration and In-Situ Margin-Detection
- **Authors**: (HBM3 ISSCC)
- **Venue**: ISSCC 2023 (Xplore 10067736)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10067736/
- **Abstract**: 4 nm HBM3 PHY with in-situ margin-detection.
- **Why relevant**: In-situ margin sensors — the foundational instrumentation for ML AD on HBM channels.

### 64. Using In-Chip Monitoring and Deep Data Analytics for High Bandwidth Memory (HBM) Reliability and Safety
- **Authors**: proteanTecs
- **Venue**: Semiconductor Engineering / proteanTecs white paper, 2024
- **DOI/Link**: https://semiengineering.com/using-in-chip-monitoring-and-deep-data-analytics-for-high-bandwidth-memory-hbm-reliability-and-safety/
- **Abstract**: Parametric lane grading + outlier detection on HBM subsystem with per-pin in-mission monitoring.
- **Why relevant**: Direct industrial precedent on HBM lane-level ML monitoring.

### 65. proteanTecs U.S. Patent for HBM Signal Quality and Reliability Monitoring
- **Authors**: proteanTecs
- **Venue**: USPTO + proteanTecs press, 2023/2024
- **DOI/Link**: https://www.proteantecs.com/news/proteantecs-granted-us-patent-for-high-bandwidth-memory-hbm-signal-quality-and-reliability-monitoring
- **Abstract**: Patent describes HBM lane-by-lane signal-quality monitoring agents.
- **Why relevant**: Documents the deployable monitoring agent architecture.

### 66. Robust Detection, Segmentation, and Metrology of HBM 3D Scans Using an Improved Semi-Supervised Deep Learning Approach
- **Authors**: (HBM CV group)
- **Venue**: MDPI Sensors 23(12), 5470, 2023
- **DOI/Link**: https://www.mdpi.com/1424-8220/23/12/5470
- **Abstract**: Semi-supervised CV for HBM bump / void / pad segmentation in 3D scans.
- **Why relevant**: Imaging-domain HBM defect ML.

### 67. Artificial Intelligence Deep Learning for 3D IC Reliability Prediction
- **Authors**: (3D IC reliability)
- **Venue**: Sci. Rep. (Nature), 2022
- **DOI/Link**: https://www.nature.com/articles/s41598-022-08179-z
- **Abstract**: CNN on 3D X-ray tomographic images of solder interconnects; 89.9% accuracy.
- **Why relevant**: ML-enabled physical inspection precedent for 3D-IC bumps/interconnects.

### 68. Deep Learning Powered 3D X-Ray Nanotomography for Failure Analysis of Advanced Semiconductor Packages
- **Authors**: (3D X-ray DL)
- **Venue**: 2025 (RG 398217700)
- **DOI/Link**: https://www.researchgate.net/publication/398217700
- **Abstract**: DL pipeline on 3D X-ray nanotomography for FA of advanced packages.
- **Why relevant**: ML-driven FA for chiplet packages.

### 69. AI-Empowered 3D X-Ray Analysis of Solder Joint Fatigue After Board-Level Vibration Testing
- **Authors**: TU Delft / others
- **Venue**: TU Delft, 2025
- **DOI/Link**: https://research.tudelft.nl/en/publications/ai-empowered-3d-x-ray-analysis-of-solder-joint-fatigue-after-boar/
- **Abstract**: YOLOv11-based deep-learning crack detection for solder joints under vibration.
- **Why relevant**: Physical-reliability DL precedent.

### 70. Detection and Diagnosis of Multi-Fault for TSVs in 3D IC (Ring-Osc + LSSVM)
- **Authors**: (TSV multi-fault)
- **Venue**: J. Electronic Testing (Springer), 2020 (RG 347255818)
- **DOI/Link**: https://link.springer.com/article/10.1007/s10836-020-05916-y
- **Abstract**: Ring-oscillator-based stimulus + LSSVM classifier for TSV multi-fault diagnosis.
- **Why relevant**: Classical RO + ML pattern reusable for D2D-bump diagnosis.

### 71. Test-Path Scheduling for Interposer-Based 2.5D ICs Using Orthogonal Learning-Based Differential Evolution
- **Authors**: (2.5D test scheduling)
- **Venue**: Mathematics (MDPI), 13(16), 2679, 2025
- **DOI/Link**: https://www.mdpi.com/2227-7390/13/16/2679
- **Abstract**: Test-path scheduling using OLDE; reduces test time on 2.5D ICs.
- **Why relevant**: Scheduling layer for ML-driven test orchestration.

### 72. Boundary-Scan-Based Interconnect Testing Design for Silicon Interposer in 2.5D ICs
- **Authors**: (Boundary-scan 2.5D)
- **Venue**: Elsevier MEJ, 2019
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0167926019303621
- **Abstract**: Boundary-scan-based interconnect test for silicon interposer.
- **Why relevant**: Classical DfT baseline.

### 73. ChiplDR-style Test Architecture for D2D Interconnects (UCIe Compliance and Debug Testing)
- **Authors**: USPTO 12353305 (compliance/debug D2D)
- **Venue**: USPTO patent, 2024
- **DOI/Link**: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12353305
- **Abstract**: Compliance and debug testing for D2D interconnects with BIST FSM controlling TX/RX.
- **Why relevant**: Patent-level implementation reference.

### 74. High-Speed Channel Modeling with Deep Neural Network for Signal Integrity Analysis
- **Authors**: (Google Research SI)
- **Venue**: Google Research / IEEE
- **DOI/Link**: https://research.google/pubs/high-speed-channel-modeling-with-deep-neural-network-for-signal-integrity-analysis/
- **Abstract**: DNN regression models that predict eye-diagram metrics from channel parameters.
- **Why relevant**: Foundational surrogate-model paper for SI ML.

### 75. High-Speed Channel Modeling With Machine Learning Methods for Signal Integrity Analysis
- **Authors**: (Google / academic SI)
- **Venue**: IEEE TCPMT (Xplore 8245823)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8245823/
- **Abstract**: LR, SVR, DNN regressions predict eye-height/width.
- **Why relevant**: Reference baseline for eye-metric regression.

### 76. A Data-Efficient Training Model for Signal Integrity Analysis based on Transfer Learning
- **Authors**: (SI TL)
- **Venue**: IEEE 2020 (Xplore 8953103)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8953103/
- **Abstract**: Transfer learning achieves same SI prediction accuracy with 64% less labeled data.
- **Why relevant**: Useful for D2D anomaly model adaptation across packaging variants.

### 77. Application and Prospect of Artificial Intelligence Methods in Signal Integrity Prediction and Optimization of Microsystems
- **Authors**: (AI SI survey)
- **Venue**: PMC, 2023
- **DOI/Link**: https://pmc.ncbi.nlm.nih.gov/articles/PMC9958958/
- **Abstract**: Survey of AI in SI prediction/optimization.
- **Why relevant**: Required general survey.

### 78. Jitter Decomposition Meets Machine Learning: 1D-Convolutional Neural Network Approach
- **Authors**: (Jitter 1D-CNN)
- **Venue**: IEEE, 2021 (RG 349601560)
- **DOI/Link**: https://www.researchgate.net/publication/349601560
- **Abstract**: 1D-CNN decomposes jitter histograms.
- **Why relevant**: Jitter is a key D2D anomaly observable.

### 79. Modeling and Analysis Techniques of Jitter Enhancement Across High-Speed Interconnect Systems
- **Authors**: (Jitter analysis)
- **Venue**: Academia.edu / IEEE, 2023
- **DOI/Link**: https://www.academia.edu/111007346
- **Abstract**: Jitter Impulse Response models for >20 Gbps interconnects.
- **Why relevant**: Physics baseline that feeds ML feature design.

### 80. Methodology for Signal Waveform, Eye Diagram, and BER Bathtub Prediction (USPTO 11621808)
- **Authors**: (Industrial method)
- **Venue**: USPTO 11621808
- **DOI/Link**: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11621808
- **Abstract**: ML correlates waveforms and predicts BER bathtubs / eye diagrams.
- **Why relevant**: Industrial template for predictive ML BER.

### 81. Data-driven PAM4 SerDes Modeling with Conditional GAN (Tektronix)
- **Authors**: Y. Choi et al. (Tektronix)
- **Venue**: DesignCon / Tek paper, 2022
- **DOI/Link**: https://download.tek.com/document/PAPER_Track14_data_driven_pam4_serdes_modeling_choi.pdf
- **Abstract**: cGAN learns PAM4 BER contour outputs indistinguishable from measurements.
- **Why relevant**: Demonstrates GANs as a feasible *synthetic-data* engine for D2D PAM4 anomaly augmentation.

### 82. START: Self-Adapting Tool for Automated Receiver Test Based on AI (Reinforcement Learning PAM-4 Sequence Discovery)
- **Authors**: (START RL Rx test)
- **Venue**: Springer 2024 (chapter 5 of Springer book)
- **DOI/Link**: https://link.springer.com/chapter/10.1007/978-3-031-62495-7_5
- **Abstract**: RL discovers error-prone PAM-4 sequences for high-speed receiver testing.
- **Why relevant**: Active-test stimulus generation; complementary to anomaly detection.

### 83. SAFE-SiP: Secure Authentication Framework for System-in-Package Using MPC
- **Authors**: (SAFE-SiP)
- **Venue**: arXiv 2505.09002, 2025 (security venue)
- **DOI/Link**: https://arxiv.org/pdf/2505.09002
- **Abstract**: MPC-based authentication for SiP chiplets, addressing supply-chain trust.
- **Why relevant**: Adjacent security/trust layer for D2D systems.

### 84. ToSHI: Toward Secure Heterogeneous Integration
- **Authors**: (ToSHI security)
- **Venue**: IACR ePrint 2022/984
- **DOI/Link**: https://eprint.iacr.org/2022/984.pdf
- **Abstract**: Security framework for heterogeneous integration / chiplets.
- **Why relevant**: Adjacent security framework.

### 85. Fast Thermal Analysis for Chiplet Design Based on Graph Convolution Networks (ASP-DAC)
- **Authors**: (Chiplet thermal GCN)
- **Venue**: ASP-DAC 2022
- **DOI/Link**: ASP-DAC 2022 proceedings
- **Abstract**: GCN-based thermal analysis for chiplet floorplans.
- **Why relevant**: Thermal-drift feature generator.

### 86. Thermal Modeling of Chiplet-Based Packaging with a 2.5D TSV Interposer
- **Authors**: (Chiplet thermal)
- **Venue**: IEEE 2022 (RG 360965825)
- **DOI/Link**: https://www.researchgate.net/publication/360965825
- **Abstract**: Thermal modeling of 2.5D chiplet TSV interposer packaging.
- **Why relevant**: Physics for thermal-drift effects on D2D SI.

### 87. Predicting Future-System Reliability with a Component-Level DRAM Fault Model
- **Authors**: (Component-level DRAM reliability)
- **Venue**: ACM/IEEE SC '23
- **DOI/Link**: https://dl.acm.org/doi/fullHtml/10.1145/3613424.3614294
- **Abstract**: Component-level DRAM fault model + reliability projection.
- **Why relevant**: Reliability baseline framing relevant to HBM stacks.

### 88. HBM Shifts Testing Left to Preserve AI Chip Yield
- **Authors**: (Semiconductor Engineering article)
- **Venue**: Semiconductor Engineering 2024
- **DOI/Link**: https://semiengineering.com/hbm-shifts-testing-left-to-preserve-ai-chip-yield/
- **Abstract**: HBM testing strategy in AI chip context.
- **Why relevant**: Industry context.

### 89. LLM-Assisted Analytics in Semiconductor Test (Invited)
- **Authors**: (Invited LLM-for-test paper)
- **Venue**: ACM/IEEE MLCAD 2024
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3670474.3685974
- **Abstract**: LLM-driven analytics for semiconductor test data.
- **Why relevant**: Emerging directions; future work.

### 90. A Survey on Machine and Deep Learning in Semiconductor Industry: Methods, Opportunities, and Challenges
- **Authors**: (Survey 2023)
- **Venue**: Springer Cluster Computing, 2023
- **DOI/Link**: https://link.springer.com/article/10.1007/s10586-023-04115-6
- **Abstract**: Broad ML/DL survey across the semiconductor industry.
- **Why relevant**: Required survey citation.

### 91. CITaR'24 / CITaR'25 — IEEE International Workshop on Chiplet Interconnect Test and Repair (Workshop Program)
- **Authors**: ETS organizing committee (E. J. Marinissen et al.)
- **Venue**: ETS 2024 / 2025
- **DOI/Link**: https://www.ieee-ets.org/past_events/ets24/files/CITaR24program.pdf
- **Abstract**: Workshop on chiplet interconnect test and repair.
- **Why relevant**: Venue-level reference; latest research agenda.

### 92. Adaptive Equalization for 32 Gbps SerDes Receivers Using Floating DFE
- **Authors**: (Adaptive EQ SerDes)
- **Venue**: ACM ICIT 2024
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3718391.3718421
- **Abstract**: Adaptive EQ algorithm for 32 Gbps SerDes.
- **Why relevant**: Classical adaptive baseline for D2D PHY.

### 93. Machine Learning Models for Accelerating Post-Silicon Chip Validation
- **Authors**: B. P. Nanan
- **Venue**: Medium / industrial summary, 2024
- **DOI/Link**: https://medium.com/@preethishnananbotlagunta/machine-learning-models-for-accelerating-post-silicon-chip-validation-265226dc75fe
- **Abstract**: ML models that accelerate post-silicon validation tasks including high-speed link tuning.
- **Why relevant**: Industrial practice context.

### 94. Application of Machine Learning Techniques in Post-Silicon Debugging and Bug Localization
- **Authors**: (JETTA 2018, foundational)
- **Venue**: Springer JETTA, 2018
- **DOI/Link**: https://dl.acm.org/doi/10.1007/s10836-018-5716-y
- **Abstract**: ML for post-silicon bug localization.
- **Why relevant**: Foundational reference.

### 95. Real-Time Machine Learning for Embedded Anomaly Detection
- **Authors**: (Embedded RT-ML)
- **Venue**: arXiv 2512.19383, 2025
- **DOI/Link**: https://arxiv.org/pdf/2512.19383
- **Abstract**: Compares IF and OC-SVM for embedded anomaly detection under hardware constraints.
- **Why relevant**: Resource/latency trade-offs for on-die deployment of D2D anomaly detection.

### 96. fSEAD: Composable FPGA-based Streaming Ensemble Anomaly Detection Library
- **Authors**: (fSEAD)
- **Venue**: ACM TRETS, 2023
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3568992
- **Abstract**: FPGA-based ensemble AD library, with dynamic partial reconfiguration for runtime swapping.
- **Why relevant**: Reference FPGA deployment of streaming anomaly detection.

### 97. F-SE-LSTM: Time Series Anomaly Detection with Frequency Domain Information
- **Authors**: (F-SE-LSTM)
- **Venue**: arXiv 2412.02474, 2024
- **DOI/Link**: https://arxiv.org/html/2412.02474v1
- **Abstract**: LSTM AD method using frequency-domain features.
- **Why relevant**: Eye-diagram & jitter histograms have natural frequency-domain analogs.

### 98. Decomposition-based Multi-Scale Transformer Framework for Time Series Anomaly Detection (TransDe)
- **Authors**: (TransDe)
- **Venue**: arXiv 2504.14206, 2025
- **DOI/Link**: https://arxiv.org/pdf/2504.14206
- **Abstract**: Decomposition-based multi-scale Transformer AD for multivariate TS.
- **Why relevant**: Multi-lane multivariate D2D telemetry maps directly.

### 99. Anomaly Detection on Time Series Sensor Data Using Deep LSTM-Autoencoder
- **Authors**: (LSTM-AE TS sensor)
- **Venue**: IEEE 2023 (Xplore 10293676)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10293676/
- **Abstract**: Deep LSTM-AE for time-series sensor anomaly detection.
- **Why relevant**: Foundational architecture for time-series sensor AD.

### 100. ATPG-via-AI Survey (2024) — reproducer entry for completeness
- (See #34 for primary listing.)

---

## Key Datasets & Benchmarks

There is currently **no public, standardized benchmark for D2D (chiplet) link anomaly detection**. The available evaluation substrates are scattered:

- **proteanTecs / GUC GLink 5 nm test-chip silicon data (industrial, restricted)** — eye-margin, BER, per-lane SI degradation. Documented in #10 and #15 but not publicly released.
- **UCIe Compliance Vectors (UCIe Consortium)** — parity-flit error injection and retrain margin scan defined in the UCIe 2.0 spec (#62). Synthetic only.
- **Open Compute Project BoW reference designs** — design data used by IBM Research for BoW SI/PI characterization (#61); useful for simulated training data.
- **EU-XFEL FPGA aging dataset (298 devices, long-term ring-oscillator readings)** — used in #30; closest publicly available large-scale aging dataset.
- **Semiconductor wafer / process datasets (SK Hynix, etc.)** used in #45 and #47 — adjacent domain.
- **TSV S-parameter synthetic datasets** generated by EM simulators in #12 and #13 — common practice in the chiplet-test ML literature.
- **DRAM-error AIOps datasets** (#48, #49, #50) — adjacent benchmark for workload-aware failure prediction.

**Practical implication**: nearly every D2D-anomaly paper uses *simulator-generated synthetic data* (Ansys Q3D, EM solvers, IBIS-AMI, or Hi-Speed-Link surrogates such as #21, #24, #25, #81). A *publicly released D2D anomaly-detection benchmark* would itself be a strong contribution.

---

## Identified Research Gaps

1. **No public benchmark for D2D-lane anomaly detection.** Existing work either uses proprietary industrial silicon data (proteanTecs / GUC, HBM PHY) or unreleased simulation outputs. Creating an open synthetic-+-emulated D2D-anomaly benchmark (with UCIe / BoW-like signatures) would be highly publishable.

2. **Most ML on high-speed links targets *design optimization* (EQ tuning, channel modeling), not *runtime anomaly detection*.** Papers #16–#25, #74–#76 are EQ / channel surrogates. There is a clear gap for unsupervised TSAD applied to D2D telemetry streams *during mission mode*.

3. **No paper jointly fuses BER, eye-margin, jitter, thermal, and PDN-noise channels for chiplet D2D.** Each modality is studied in isolation (#11 thermal, #27/#28 droop, #18/#16 eye, #78/#79 jitter). A multi-modal Transformer or contrastive model unifying these would be a strong contribution.

4. **Workload-aware anomaly detection on D2D PHY is unexplored.** DRAM workload-aware error prediction exists (#48), but no analog exists for chiplet links where workload modulates self-induced PDN noise and crosstalk.

5. **On-die / on-edge deployment of D2D anomaly detection is nascent.** OCTANE (#2) and HeatSense (#11) are the only credible examples; the throughput and memory budgets of a UCIe adapter for an OCTANE-style detector are unstudied.

6. **Synthetic-data realism gap.** GAN/Transformer SerDes surrogates (#24, #25, #81) achieve excellent regression accuracy but have not been validated for generating *realistic anomalies* (latent defects, soft failures, intermittent crosstalk).

7. **IEEE P3405 + ML.** P3405 (#6) and #4 standardize chiplet test/repair but do not yet incorporate ML-based diagnosis. Specifying an ML-friendly extension (telemetry feature format, label distribution) would be a publishable systems contribution.

8. **Lack of causal / explainable models.** All TSAD work cited is black-box. For root-cause analysis (e.g., "which lane / which bump / which thermal hotspot") the literature lacks causal anomaly-attribution methods for D2D links.

9. **Aging / wear-out prediction for D2D PHY.** Aging ML exists for transistors (#32), interconnects (#33), and FPGAs (#30), but no targeted study of D2D-lane aging exists. Combining #30's methodology with chiplet telemetry would be a strong incremental angle.

10. **Federated / privacy-preserving learning across chiplets from multiple vendors.** UCIe envisions multi-vendor chiplets, but no work explores federated anomaly detection across vendor-owned data shards.

---

## Notes on Sources / Filtering

- Approximately 100 candidate entries were initially identified; the list above keeps the 95+ most directly useful. Several patent-only matches (USPTO) were retained where they were the only available documentation of an industrial method (e.g., #73, #80).
- Older-than-2021 foundational papers (#36, #49, #58, #94) are retained because they are still standard citations and continue to be referenced in the recent venue program (ITC/VTS/ETS).
- The proteanTecs corpus (#10, #15, #64, #65) is the dominant industrial reference for D2D anomaly monitoring; multiple entries are included because each documents a distinct facet (GLink characterization, lane-coverage prediction, HBM, patent).
- Surveys (#9, #34, #35, #56, #77, #90) are deliberately included to satisfy the "background section" of an IEEE-style paper.
