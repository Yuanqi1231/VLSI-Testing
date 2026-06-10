# Direction 3 — Reading Synthesis (Round 1): D2D / Chiplet Die-to-Die Link Anomaly Detection

Based on the **11 Tier-1 papers** read for `papers/3/`. Note up front: **none of the 11 is a "native" UCIe/BoW/AIB D2D-link anomaly detector** — they are domain-*adjacent* (DRAM/SATA channels, TSV/RDL/microbump interconnects, NoC routers, interposer PDN, FPGA SLRs). That is the opportunity: the methods, fault taxonomies, and evaluation rubrics transfer cleanly, but the exact "ML anomaly detection on a standardized D2D PHY link" cell is **empty**. This synthesis is written to help the team pick a credible, non-over-engineered contribution.

> **IDs are the ground-truth `paper_id`s (1,2,3,4,6,7,8,11,12,13,14)** — they are not contiguous; that's expected.

## The 11 papers

| # | Short name | Venue/Year | Category | One-liner |
|---|-----------|-----------|----------|-----------|
| 1 | Usama et al. — Latent-rep AE+classifier for DRAM SI | arXiv 2506.18288 (2025) | SI/eye ML | Joint autoencoder+classifier, gradients backprop'd **only from valid data**, learns discriminative latents for DRAM-channel anomaly detection **and** latent-space signal-integrity enhancement. |
| 2 | OCTANE — On-chip telemetry anomaly engine | IEEE ITC 2025 | on-chip-anomaly-engine | HW/SW-co-designed, fixed-point unsupervised distance-scoring SLM engine on real Intel CPUs; per-domain (core/mem/sensor) scores + XGBoost cloud diagnosis of Spectre/Rowhammer/voltage-droop. |
| 3 | Bhoumik et al. — FOWLP chiplet-interconnect BIST | arXiv 2503.14784 / IEEE 2025 | chiplet-BIST/test | FEA (Q3D→HSPICE) defect-to-fault mapping for Cu-pillar/RDL + **graph-coloring BIST using only 3 test patterns**, 95.6% diagnosability. |
| 4 | Huang et al. — ARCS inter-die interconnect BIST | IEEE ITC 2024 | chiplet-BIST/test | Alternating Row/Column Stripe test + compression + TX/RX BIST for microbump arrays; **99.9% test-time** and ~53.5% area reduction vs IEEE 1500. |
| 6 | Marinissen et al. — IEEE Std P3405 | IEEE VTS 2024 (Special Session) | standard | Position paper introducing the in-development **P3405** interoperable D2D test-and-repair standard; formal Interconnect-Repair Problem + Protocol-Buffers repair-description language. |
| 7 | Sanchez-Martinez et al. — HSIO post-Si risk ML | IEEE ITC 2020 | post-Si-ML | Supervised SVM/NN/**Boosted-Trees** on 163 eye/calibration features from measured Intel silicon to automate the SATA-link pass/fail PRQ risk decision (94.84% acc). |
| 8 | Miao et al. — CNN eye-diagram impairment classifier | IEEE EPTC 2022 | SI/eye ML | CNN classifies **7 impairment classes** (crosstalk/loss/reflection + composites) from ADS-simulated eye-diagram **images**, localizes them, and regresses a fixing parameter. |
| 11 | HeatSense — NoC thermal-sensor-spoof detector | IEEE TCAD 2026 | thermal AD | **Non-ML** per-router statistical detector (Mean±Kσ with bit-shift σ + approximated WMA) for thermal-Trojan spoofing; up to 82% acc with **~75% less HW** than ML. |
| 12 | Huang et al. — ML defect classification for TSVs | IEEE TCPMT 2018 | interconnect-FD-from-signatures | KNN vs **Random Forest** on HFSS-simulated **S-parameters** (S11/S21) to detect/classify TSV void/short/open and estimate void amount; low-freq band most separable. |
| 13 | Kang et al. — SREL reflection-coefficient FD | arXiv 2304.10207 (2024, Microel. Reliab.) | interconnect-FD-from-signatures | Learns **full S11 frequency pattern** (measured Cu interconnects); novel **Severity-Rating Ensemble Learning** does root-cause + ordinal-severity diagnosis; 99.3% acc, noise-robust. |
| 14 | ChipletQuake — on-die impedance sensing | arXiv 2504.19418 (2025) | impedance/PDN sensing | Fully-digital on-die actuator+TDC mesh sweeps shared interposer **PDN impedance** to detect interposer tampering, dormant HTs, and SLL-count changes on real FPGA SLR chiplets (no extra HW, no signal interface). |

---

## 2. Novelties — what each work claims is new (by theme)

Six distinct novelty themes recur. Tagged with the papers that carry them and whether they're **transferable** to a course D2D-anomaly project.

**(A) Learn representations / discriminate without a comprehensive fault corpus.** The field's central pain is that *labeled* anomalous link data is scarce. #1's signature move is backprop'ing the classifier gradient **only from valid (normal) data** so the latent space stays tight for normal and separates anomalies, without overfitting to a hand-picked anomaly set (its own ablation: 93.1% vs 76.3% accuracy, valid-only vs both-gradients). #13's SREL decomposes "root cause + severity" into a bank of binary classifiers that preserve ordinal severity (beats softmax: 99.3% vs 98.6%). → **Most transferable theme for the course.** Both are direct answers to "we have lots of good links, few labeled bad ones" — the exact D2D data reality. #1's valid-only-gradient trick is a small, principled tweak on a plain AE (course-friendly).

**(B) Anomaly detection from electrical *signatures* rather than images or logic.** #12 and #13 both abandon imaging/logic-test and feed **S-parameters / reflection coefficients** to ML. #13's specific novelty: use the **full frequency-domain S11 *pattern*** (treating discarded outliers as features) instead of a single-frequency scalar — and it claims to be the first electrical-signal method that finds *root cause* non-destructively, not just severity. #12 claims it can regress the **void amount** (0–35%), not just detect. → **Highly transferable**: a D2D link's reflection/insertion signature at bumps/RDL is the same physics; this is a credible feature source when you can't image the link.

**(C) On-chip, resource-constrained detectors that deliberately avoid heavy ML.** #2 (OCTANE) builds fixed-point distance scoring (variance-norm Euclidean `d_E`, cosine-derived `d_C`) with mean/product aggregation, implementable in Kogge-Stone adders + Wallace-tree multipliers at **1.2% die area / ~0.5% power**. #11 (HeatSense) goes further and is **explicitly non-ML** — Mean±Kσ with **σ approximated by bit-shift** (σ_n = Mean/2ⁿ) and an approximated weighted-moving-average, saving up to 75% logic vs ML and eliminating DSP/BUFGMUX entirely, accepting a 10–15% accuracy hit. → **Transferable as the "lightweight on-die" framing**, and a sober counterweight to over-engineering: both show a simple statistical detector is often "good enough" under HW constraints.

**(D) Hierarchical / topological scoring + graded response.** #2 scores per-domain (core/memory/sensor) then aggregates to a system score, mirroring chip topology (vs treating telemetry as one flat vector). #11 uses a 3-level graded anomaly classification (1/2/3 features out-of-bounds → σ5/σ6/σ7 confidence) feeding a **proportional, randomized port-shutdown** countermeasure with staged recovery. → **Transferable**: per-lane/per-channel scores aggregated to a per-link score, with graded lane-throttling/shutdown, is a clean D2D architecture.

**(E) Low-pattern-count structural test + diagnosability theory.** #3 reduces the hexagonal bump-short problem to a **graph-coloring** with only **3 test patterns** and proves 95.6% diagnosability. #4's ARCS exploits the 2D array so pattern count is **logarithmic** (2·(⌈log₂h⌉+⌈log₂w⌉)) and compresses an h×w pattern to h- or w-bit vectors. → **Transferable as the structural-test *baseline*** any learning detector must beat or complement, and as a **synthetic-label generator** (their defect→fault thresholds are free ground truth). Not ML.

**(F) Physical-electrical sensing of the shared substrate.** #14 sweeps the shared **PDN impedance** with an on-die actuator+TDC mesh — no signal interface, no extra HW — and detects dormant/static anomalies (interposer SLL-count changes 129→133, Trust-Hub AES-T1100 HT) that activity-based methods miss; uses Welch's t-test (|t|>4.5) + Wasserstein distance as the decision rule. → **Transferable** as a side-channel way to monitor the *interposer/link fabric* itself, and its golden-vs-measured distance-test is a reusable anomaly rule.

**Standards/infrastructure context (#6, P3405):** not a method, but supplies the **formal vocabulary** (Interconnect-Repair Problem, repair chains, spare lanes, Tx/Rx repair MUXes) and a ready **feature/fault-mode list** for D2D links: contact resistance, capacitive loading, crosstalk, insertion/return loss, eye width/height, jitter, swing, lane skew, thermal gradients, stuck-at, shorts-to-neighbor, bridge-to-power. It also cites the result that **16 placement-aware patterns suffice** for all static+transition interconnect faults.

**Bottom line on transferability:** themes **(A)** and **(B)** are the intellectual core the course should build on (representation-learning under label scarcity; electrical-signature features). Theme **(C)/(D)** define the *deployment* framing. **(E)/(F)** are the baselines and the synthetic-data engines.

---

## 3. Methods — a taxonomy

Seven method families. Each: papers, concrete technique, what's reusable.

### Autoencoder / latent-representation (#1)
- **Technique:** Encoder R¹⁰⁰→R¹¹, Decoder R¹¹→R¹⁰⁰, Classifier R¹¹→[0,1]; joint loss `L = ‖x−x̂‖² − y·log(ŷ)` with **classifier gradient flowing only from valid (y=1) data**. Frozen encoder then feeds LOF / LSAnomaly / NN detectors. SI enhancement = nudge latent toward the **Fermat-Weber (geometric-median) anchor** and decode.
- **Reusable:** the valid-only-gradient tweak (tiny code change on a vanilla AE, big generalization gain); geometric-median anchor as a robust "normal centroid"; latent-space remediation idea (maps to adaptive EQ/de-embedding).

### Classical ML classifiers (#7, #12, #13)
- **Technique:** #7 — cubic-kernel SVM, shallow NN (163-2048-2, tanh), **Boosted Trees** on a 163-dim eye/calibration vector. #12 — KNN (k=5) vs **Random Forest** on S-parameter features. #13 — Random Forest / K-means as ML baselines against its DL.
- **Reusable:** Boosted Trees and Random Forest are the **repeatedly-winning tabular baselines** (#7 BT 94.84%; #12 RF ≫ KNN; #2's XGBoost diagnosis 98–99.9%). For a course project these are the cheap, strong baselines to include; RF also gives free feature-importance (used by #11 to pick features).

### CNN-on-images (#8)
- **Technique:** 3×(Conv+Pool) → Dense(2048)→Dense(1024)→7-way softmax on **eye-diagram images** (grayscale + resize 775×543×3 → 100×70, ~60× data reduction). Also localizes (which line) and links to a linear-regression fixer.
- **Reusable:** treat a D2D eye as an image and classify impairment *type*; the simulator-sweep-then-label data pipeline; the 80%-of-data-needed-for-100%-acc ablation as a data-budget guide. Caveat: 100% on a few-hundred clean synthetic images is an overfitting red flag.

### Transformer / time-series — **ABSENT (a gap, and a relief)**
- **No paper uses transformers or LSTMs.** #1 treats waveforms as 100-vectors via an MLP, not a sequence model. The recommended course methods (Autoencoder/LSTM/statistical AD) therefore have an **uncontested lane**: an LSTM/temporal-AE over per-lane telemetry streams (eye margin, BER, retrain counts, temperature over time) is novel relative to all 11 and is *not* over-engineering.

### On-chip lightweight detectors (#2, #11)
- **Technique:** #2 — fixed-point distance scores `d_E(X)=Σ(1/σ_f²)(X_f−E[X_f])²` and `d_C(X)=‖X‖²−(X·E[X])²/‖E[X]‖²`, per-domain, aggregated by mean `a_M` or product `a_J`; entropy/normalized-mutual-information feature ranking. #11 — Mean±Kσ thresholds with **σ via bit-shift** and approximated WMA, 3-tier graded levels.
- **Reusable:** both are ASIC-friendly templates for an in-line per-link monitor; #2's NMI-based **workload-independent feature selection** is directly applicable to choosing robust link telemetry.

### BIST / DfT structural (#3, #4)
- **Technique:** #3 — graph-coloring → 3 patterns {011,110,101}, wired-AND/wired-OR detectors, block-partitioned FSM. #4 — ARCS stripe patterns, homogeneity compression, TX(MUX+NOR)/RX(NOR+XNOR+tri-state) wrapper cells, OR-tree pass/fail, per-row address-decoder localization.
- **Reusable:** the **deterministic structural baseline** to contrast learning against; their **defect→fault thresholds** (#3 Table III: e.g., A-to-B short with R<200Ω → wired-AND; ~3 nm bump short causes failure) are free labels for a synthetic D2D fault corpus; ARCS RX-side XNOR-vs-golden + OR-tree is a reusable HW anomaly-flagging mechanism.

### Physical / electrical sensing + ML (#12, #13, #14)
- **Technique:** #12/#13 — S-parameter / reflection-coefficient signatures (HFSS-sim for #12; measured VNA 0–14 GHz for #13) + ML. #14 — on-die actuator+TDC PDN-impedance sweep + Welch's t-test / Wasserstein distance vs golden trace.
- **Reusable:** **electrical signatures as the feature** when you can't image or fully test the link; #14's golden-vs-measured statistical distance is a clean unsupervised anomaly rule; #13's **noise-injection robustness protocol** (5/10/15 dB Gaussian) is directly adoptable.

### Compact method table

| Paper | Input / feature | Model | Output |
|---|---|---|---|
| 1 | DRAM-channel waveform, 100-dim vectors (simulated) | AE + classifier (valid-only gradient) → LOF/LSAnomaly/NN; geom-median latent nudge | Normal/anomaly label; SI-enhanced (reconstructed) signal |
| 2 | CPU telemetry: 181/460 MSR + sensor features (measured) | Fixed-point distance scoring (d_E, d_C), per-domain; XGBoost for diagnosis | Per-domain + system anomaly score (AUCROC); incident class (benign/security/safety) |
| 3 | Cu-pillar/RDL geometry → Q3D RLC → HSPICE (sim) | Graph-coloring BIST, 3 patterns; wired-AND/OR detectors | Stuck-at / bridging detect + locate (95.6% diagnosability) |
| 4 | Microbump 2D array h×w (analytical + 40nm synth) | ARCS stripe test + TX/RX BIST | Stuck-at / wired-OR/AND detect + fault location |
| 6 | — (no data; standards position paper) | Formal IRP model + Protocol-Buffers repair language | Standardized test/repair description (no metric) |
| 7 | 163 eye-width/height + Rx calibration codes (measured Intel) | Cubic SVM / shallow NN / **Boosted Trees** | Pass/fail PRQ risk decision (binary) |
| 8 | Eye-diagram **image** 100×70 (ADS sim) | CNN (3 conv blocks) + linear regression | 7-class impairment type + location + fixing parameter |
| 11 | 19 NoC features (router temp/congestion), top-5 (sim) | **Statistical** Mean±Kσ (bit-shift σ) + approx WMA | 3-level anomaly + graded port-shutdown |
| 12 | TSV S11/S21/phase, 200 MHz–20 GHz (HFSS sim) | KNN vs **Random Forest** | Void/short/open class + void amount |
| 13 | Full S11 magnitude pattern 0–14 GHz (measured Cu) | **SREL** (ensemble of binary nets) vs multiclass-CNN/RF | Root cause (mech/corrosion) + ordinal severity |
| 14 | On-die PDN impedance traces, ~100–900 MHz sweep (measured FPGA) | Actuator+TDC sensing + Welch t-test / Wasserstein | Tamper / HT / SLL-change detected (golden-vs-measured) |

---

## 4. Evaluation methods — how these works prove themselves

| Paper | Data source | Baselines | Metrics | Headline result |
|---|---|---|---|---|
| 1 | **Sim** (DRAM-channel SI sim; **synthetic** anomalies) | Contractive-AE; both-gradients variant | Detection acc; Bhattacharyya dist; latent overlap; eye-window-area % | NN detector **95.9%** (+5–9% over baselines); avg **11.3%** eye-area SI gain (max 31.8%) |
| 2 | **Measured** (2 Intel CPUs, PAMPAR; injected attacks) | iForest, Autoencoder, E-SCOUT | **AUCROC** (detection); Accuracy/F1 (diagnosis); area %, power | AUCROC **>0.95** most cases; XGBoost diagnosis **0.96/0.98**+; **1.2% area, ~0.5% power** |
| 3 | **Sim** (Q3D+HSPICE; AES/DES synth for PPA) | Qualitative vs prior pattern-gen work | Diagnosability D; PPA % overhead | 3 patterns detect all SAF+bridging; **95.61%** diagnosability; +1.4–6.6% area |
| 4 | **Analytical + synth** (TSMC 40nm) | IEEE 1500 (wrapper-cell area only) | Area (µm²), test cycles | **99.9%** detection-time cut; **53.5%** area saving (32×64 array) |
| 6 | **None** (position paper) | Prior standards (1838/1687/1500/UCIe/AIB/HBM3) | — (none) | No empirical results; worked UCIe ucie.repair example |
| 7 | **Measured** (Intel CPU+PCH, SATA; 1,275 samples, 3-engineer labels) | SVM vs NN vs BT; full vs PCA-7 | Accuracy / sensitivity / specificity; p-values | **BT 94.84%**; full-163 ≫ PCA-7 (>92% vs <88%, p<1e-8) |
| 8 | **Sim** (ADS eye diagrams; ~100/class) | None (no external model) | Classification accuracy vs epoch | **100%** 7-class acc @10 epochs; ≥80% data needed |
| 11 | **Sim** (CoMeT+AccessNoxim; PARSEC) + FPGA for HW cost | 5 ML models (LR/KNN/NB/DT/**RF**) | Acc/precision/recall/F1; FPGA area/IOB/DSP; recovery/drop | **82%** acc (10–15% < RF); **~75%** logic saving; DSP/BUFGMUX eliminated |
| 12 | **Sim** (HFSS S-params) | KNN vs RF; wide vs low band | Cross-validated accuracy (figures only) | RF ≫ KNN; low-freq (≤5 GHz) most separable; **no single headline %** in text |
| 13 | **Measured** (fabricated Cu vehicles + VNA; 790 samples) + synthetic noise | Multiclass-CNN; RF; K-means | Accuracy / macro-F1; params; inference ms; noise-robustness | **SREL 99.3%**, F1 0.991; most noise-robust |
| 14 | **Measured** (AMD VU37P FPGA, 3 SLRs; Trust-Hub AES-T1100) | Golden-trace self-vs-self reference | Welch t (|t|>4.5); Wasserstein (bootstrap) | Detects HT / interposer-tamper / SLL-change by large margin; **no acc/FPR reported** |

### Evaluation patterns (read these before designing your eval)
- **Simulator-generated or proprietary data dominates.** 6/11 are pure simulation (#1, #3, #8, #11, #12; #4 analytical); the "measured" ones use *proprietary* silicon (#2 Intel CPUs, #7 Intel SATA) or *fabricated lab vehicles* (#13). **There is no shared public D2D-link anomaly benchmark** — the same data-scarcity problem Direction 1 named, but worse (not even a WM-811K equivalent exists here).
- **Anomalies are almost always injected/synthetic.** #1 synthesizes ISI/amplitude/harmonic distortions; #2 injects Spectre/Rowhammer/Plundervolt; #8 sweeps EDA parameters; #13 laser-cuts cracks and chamber-corrodes. Real, naturally-occurring field anomalies are essentially never tested. **This legitimizes a fault-injection / synthetic-anomaly strategy for the course** — it is the field norm, not a shortcut.
- **Metric conventions diverge and are not comparable.** Detection uses AUCROC (#2), accuracy (#1, #7, #8, #11, #12, #13), or statistical-distance thresholds (#14); the BIST papers (#3, #4) report diagnosability/coverage + PPA, not detection accuracy. A few report **no headline number at all** (#12 figures-only, #14 no FPR/ROC). Cross-paper "who's best" claims are therefore unsafe.
- **Hardware cost is reported by exactly the on-chip works** (#2 area/power, #3/#4 PPA, #11 FPGA LUT/DSP) and **ignored by every pure-ML paper** (#1, #7, #8, #12, #13 report zero area/power). If your contribution claims "on-die," you must report PPA; if it's an offline analyzer, the field doesn't expect it.
- **Robustness and reproducibility are thin.** Only #13 does a principled noise sweep; only #1 and #13 give code/data links; suspiciously perfect numbers (#8 100%, #2 diagnosis 0.999) on small/low-diversity sets signal overfitting risk.

### Evaluation bar a course project must clear
1. **Beat a deterministic structural baseline, not just another NN.** #3/#4 detect *hard* stuck-at/bridging cheaply; your ML must justify itself on what they *can't* do — **weak/resistive/parametric defects, drift, aging, in-field online monitoring** (all explicitly out-of-scope in #3, #4).
2. **Include the strong cheap ML baselines** (Random Forest / Boosted Trees / XGBoost — winners in #2, #7, #12) so any deep/temporal model's delta is provable.
3. **Report AUCROC or precision/recall/F1, not bare accuracy**, given the inevitable class imbalance (normal ≫ anomalous).
4. **Do a noise/drift robustness sweep** (#13's 5/10/15 dB protocol is the template) — almost no one else does, so it's cheap differentiation.
5. **If you claim on-die: report PPA** vs a structural baseline (#3/#4 numbers are the comparators). If offline: say so and don't fake area numbers.

---

## 5. Cross-cutting insights for Direction 3

1. **The open gap is precise: ML/statistical anomaly detection on a *standardized D2D PHY link* (UCIe/BoW/AIB), in-field, for *weak/parametric/drift* anomalies.** Every paper sits next to this hole — #3/#4/#6 are D2D-native but **deterministic structural test only** (hard faults); #1/#7/#8/#12/#13 are the right *methods* but on DRAM/SATA/TSV/Cu, not a chiplet link; #2/#11/#14 are on-die anomaly engines but for CPU telemetry / NoC thermal / PDN, not the link signal. Filling the intersection is the contribution.

2. **The baseline you must beat is the structural BIST ladder (#3, #4), framed by their own limitations.** Both explicitly **do not** cover weak opens/shorts, parametric/delay defects, aging, or in-field online monitoring. So the honest pitch is *not* "we detect shorts better" — it's "we detect the **degradation modes BIST leaves on the table**, online, from telemetry." Their defect→fault thresholds (#3 Table III; #4 fault model) are simultaneously your **ground-truth labels**.

3. **The credible data strategy is fault-injection / synthetic anomalies on a simulated or telemetry link — because that is exactly what the field does** (#1 synthetic distortions, #8 EDA sweeps, #2/#11 injected attacks). Best-of-breed: a Q3D/HSPICE-style defect→electrical mapping (#3) to generate *labeled* link anomalies with severity (mirrors #12's void-ratio and #13's discrete severity levels), plus #13's additive-Gaussian-noise augmentation for robustness. State plainly that no public D2D anomaly set exists (the motivation), and **release yours**.

4. **The best starting method given "don't over-engineer" = a plain Autoencoder with #1's valid-only-gradient trick, scored by a simple statistical rule.** This is the lowest-risk, highest-signal choice: it matches the course's recommended Autoencoder/statistical-AD lane, needs only normal data (which is abundant), and #1 *quantifies* the trick's payoff (93.1% vs 76.3%) on an analogous channel. Pair it with cheap detectors on the latent (LOF/LSAnomaly per #1) and a tabular RF/Boosted-Trees baseline (#7/#12) for the delta.

5. **An LSTM / temporal-AE over per-lane telemetry streams is the one genuinely novel-vs-all-11 method and is *not* over-engineering.** No paper models the **time axis** — #1 uses an MLP on static vectors, the rest are per-sample. Eye margin, BER counters, retrain events, lane skew, and link temperature over time (the #6 feature list, the #7 calibration codes) are a natural sequence. An LSTM-AE reconstruction-error detector is squarely in the recommended-methods set and lands in white space.

6. **Use electrical signatures (S-parameters / reflection coefficient / PDN impedance) as features, not just digital telemetry.** #12/#13/#14 show reflection/impedance signatures cleanly separate interconnect anomalies; #12's finding that the **low-frequency band (≤5 GHz) is most separable** (oxide-liner MOS-cap dominates) is a concrete stimulus-design tip. For a D2D link, bump/RDL impedance discontinuities give the same signal — a strong feature source if you can simulate or probe it.

7. **Adopt the per-lane→per-link hierarchical scoring + graded response architecture (#2, #11).** Score each lane, aggregate (mean or product per #2) to a link score, and respond proportionally (graded lane throttle/shutdown + recovery per #11). This is the deployment story that turns a detector into a usable monitor and reuses two papers' designs wholesale.

8. **Be honest about authority limits — detection ≠ verified repair.** #6's IRP and #3/#4's deterministic detectors guarantee correctness; an ML detector cannot. The strongest framing (echoing Direction 1's "verified accelerator") is **ML flags/ranks anomalies online; a deterministic check or BIST confirms before any repair/lane-remap**. This mirrors #2's two-stage edge-detect→cloud-diagnose split.

> **Suggested thesis seed:** an **Autoencoder/LSTM-AE anomaly detector on per-lane D2D link telemetry + reflection signatures**, trained on a **released fault-injection generator** (defect→electrical mapping for weak/parametric link degradation), benchmarked against the **structural-BIST baseline (#3/#4) it complements** and the **RF/Boosted-Trees tabular baseline (#7/#12)**, with a **noise/drift robustness sweep (#13)** and **hierarchical per-lane→per-link graded scoring (#2/#11)** — squarely on-scope, non-over-engineered, and in genuine white space.

---

## 6. New references worth adding to the survey

Deduped from `citations_worth_chasing` across all 11 papers, prioritized. ★ = highest value for the suggested direction.

### Must-cite D2D / chiplet-interconnect test (the native-D2D anchors the survey currently lacks)
- ★ **T.-H. Wang et al., "Test and repair improvements for UCIe," IEEE ETS 2024** (from #3 ref [18]). The closest UCIe-specific D2D test/repair work — directly your modality.
- ★ **P.-Y. Chuang et al., "Generating test patterns for chiplet interconnects…," IEEE TCAD 2024** (#3 [17] / #6 [23]). The 16-pattern placement-aware sufficiency result; the structural-test SOTA to position against.
- **C. Cui et al., "Physical-aware interconnect testing and repairing of chiplets," IEEE ETS 2023** (#3 [16]).
- **S. Chakravarty, "A call to standardize chiplet interconnect testing," IEEE VTS 2022** (#3 [25]) — source of the ~95% shorts-vs-opens statistic; and **"3D interconnect test challenge," ETS 2022** (#4 [18]) — defect taxonomy.
- **IEEE Std 1838-2019** 3D test access standard (#6 [6]); **Marinissen et al., P3405 Part 2, ETS 2024** (#6 [19]).

### Electrical-signature + on-chip sensing for interconnect health (the feature-source anchors)
- ★ **I. Shin, K. Koo, D. Kwon, "Non-invasive on-chip interconnect health sensing based on bit error rates," Sensors 2018** (#13 [20]). On-chip, BER-based, in-situ — the closest thing to an embedded D2D link health monitor.
- ★ **D. Kwon et al., "Early detection of interconnect degradation by continuous monitoring of RF impedance," IEEE TDMR 2009** (#13 [7]). Foundational continuous-impedance interconnect-health monitoring.
- **T. Y. Kang et al., "Early detection & cause analysis of interconnect defects by ranking-CNN of S-parameter patterns," IMAPS 2019** (#13 [21]) — direct predecessor to SREL.
- **T. Mosavirik et al., "ImpedanceVerif: on-chip impedance sensing for tamper detection," IACR TCHES 2023** (#13 [24]); **Mosavirik et al., "Silicon Echoes: frequency-selective impedance Trojan/tamper detection," TCHES 2023** (#14 [5]) — on-die impedance lineage behind #14.
- **C. Okoro et al., "Accelerated stress test of TSV using RF signals," IEEE T-ED 2013** (#12 [28]); **D. H. Jung et al., "TSV defect modeling, measurement and analysis," IEEE TCPMT 2017** (#12 [20]).

### On-chip anomaly engines / SLM (the deployment-architecture anchors)
- **E. Ortega et al., "E-SCOUT: spatial-clustering outlier detection via telemetry," IEEE ITC 2024** (#2 [15]) — the direct prior SLM baseline OCTANE beats.
- **A. Deric, D. Holcomb, "Integrity checking for zero-trust chiplet systems using between-die delay PUFs," IACR TCHES 2022** (#14 [1]); **T. Zhang et al., "SiGuard: run-time SiP security via power-noise variation," IEEE TVLSI 2023** (#14 [3]) — chiplet/SiP runtime integrity.

### ML-for-AD method references (the model-design anchors)
- **L. Ruff et al., "Deep semi-supervised anomaly detection (Deep SAD)," ICLR 2020** (#1 [12]); **D. Gong et al., "Memorizing normality (MemAE)," ICCV 2019** (#1 [8]) — the AE-AD families #1 did *not* compare against; useful baselines/upgrades.
- **R. Medico et al., "Autoencoding density-based anomaly detection for SI," EPEPS 2018** and **"ML-based error detection for SI," IEEE TCPMT 2019** (#1 [4],[5]) — closest SI-AD prior art.
- **S. Chen et al., "Using ranking-CNN for age estimation," CVPR 2017** (#13 [45]) — theory that binary-aggregation beats softmax (underpins SREL; relevant if you do ordinal severity).

### Verify-before-citing
- #1, #13, #14, #3 are **arXiv preprints** (some with IEEE copyright lines but no named venue) — confirm final publication venue before formal citation. #11 is a 2026 TCAD early-access author version — confirm final pagination.
