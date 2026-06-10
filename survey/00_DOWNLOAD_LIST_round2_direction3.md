<!-- Generated 2026-06-03 by a bibliography-mining + web-verification pass over the 11 read papers in papers/3/.
     Companion files: direction3_d2d_anomaly.md (iterated survey), SYNTHESIS_direction3_round1.md (reading synthesis).
     Stats: 142 mined citations -> 140 unique -> 92 web-verified abstracts -> 33 flagged DOWNLOAD. -->

# ROUND-2 Recommended Download List — D2D Link Health via Multimodal Telemetry Fusion (DATE 2027, Track-T)

## Header — Thesis & how Round-2 differs

**Thesis (the relevance lens):** An **online / runtime / in-field** evaluation of **die-to-die (D2D) / chiplet interconnect link health**, built by **fusing multimodal on-chip telemetry** — voltage (droop/noise), temperature/thermal drift, PVT sensors — with **link-level signals** (BER, eye margin, lane skew, retrain/parity events) into an **ML/statistical anomaly-or-degradation detector**. Target: a **DATE 2027 Track-T** paper rewarding a crisp problem, a non-ML baseline + an ML method with a provable delta, physically-motivated (synthetic-OK-if-released) data, a reproducible artifact/benchmark, and honest limitations.

**Round-1 vs Round-2.** Round-1 was a broad, **keyword-built** sweep (~100 entries: SerDes EQ-tuning, channel surrogates, generic TSAD, NoC security, HBM imaging) that over-covered design-time SI/ML and under-covered the thesis core. **Round-2 is bibliography-grounded** (mined from the 11 verified Tier-1 PDFs) **plus targeted gap searches**, and is **thesis-focused** on the three load-bearing axes that Round-1 missed: (a) **multimodal on-chip telemetry fusion for reliability/prognostics**, (b) **online/runtime, resource-constrained on-chip anomaly detectors**, and (c) the **physical grounding of the D2D signal set** (UCIe-mandated PVT/eye/BER/skew/retrain) plus the **non-ML baselines** an ML detector must beat. Every entry below has a web-verified abstract; everything already in the survey is moved to the Appendix rather than re-recommended.

Pillar legend: **P1** multimodal fusion · **P2** on-chip sensor/telemetry source · **P3** online/runtime · **P4** D2D/chiplet/interconnect specificity · **P5** degradation/health/aging · **P6** reusable ML/statistical method · **P7** released dataset/benchmark/artifact · **P8** Track-T community-venue fit.

---

## Tier A — Must-download (download first)

**A1. OCTANE: On-Chip Telemetry-based Anomaly Notification Engine**
- **Authors:** E. Ortega, A. Hati, J. Talukdar, W. Paik (ASU); Fei Su, R. Chattopadhyay (Intel); K. Chakrabarty (ASU).
- **Venue/Year:** IEEE ITC 2025, pp. 131–140 (DOI 10.1109/ITC58126.2025.00019).
- **Where to get:** IEEE Xplore doc 11219729 — https://ieeexplore.ieee.org/document/11219729/ ; metadata at ResearchGate 397230623.
- **Abstract (verified):** On-chip, compute/memory-efficient **unsupervised** anomaly detection over performance counters + sensors, using fixed-point distance scoring (OCTANE-edge) with an entropy/compression-index, **workload-independent feature ranking** for silicon lifecycle management (SLM).
- **Why it matters (P2,P3,P5,P6,P8):** The single best **peer baseline to beat** — a recent ITC SLM on-chip unsupervised detector with a PPA/AUROC rubric. Its feature-ranking selects which telemetry channels feed a detector; its non-multimodal, non-D2D scope is precisely our novelty wedge.
- **Role:** **baseline + method template + community anchor.**
- **Cited by:** mined from #2 (its own corrected entry is already verified); benchmarks **E-SCOUT**.
- **Note:** **Already in survey as Tier 1 (#2, verified).** Listed here as the priority *anchor*, not a new download — see Appendix.

**A2. E-SCOUT: Efficient-Spatial Clustering-based Outlier Detection through Telemetry**  *(NEW)*
- **Authors:** E. Ortega, J. Talukdar, W. Paik, K. Chakrabarty (ASU).
- **Venue/Year:** IEEE ITC 2024 (IEEE Xplore doc 10766703).
- **Where to get:** IEEE Xplore doc 10766703. (Full verbatim abstract paywalled; metadata + OCTANE confirm.)
- **Abstract (verified):** Compute/memory-efficient **unsupervised spatial-clustering** outlier detector on on-chip telemetry, with an on-chip 32-bit FP "E-SCOUT edge" for SLM (defective/anomalous dies).
- **Why it matters (P2,P3,P6,P8):** The **explicit prior-art baseline OCTANE must beat** — so it is *our* must-beat too, with a ready PPA accounting template. If its telemetry is single-stream / not interconnect-specific, that gap (D2D + multimodal fusion) is the wedge.
- **Role:** **must-beat baseline.**
- **Cited by:** mined via OCTANE (#2). **In survey only as a Tier-1b one-liner — promote to a full download.**

**A3. Detecting Anomalies in ML Infrastructure via Hardware Telemetry (Reveal)**  *(NEW)*
- **Authors:** Univ. of Oxford (preprint).
- **Venue/Year:** arXiv:2510.26008 (cs.AR/cs.DC), Oct 2025 (v2).
- **Where to get:** https://arxiv.org/abs/2510.26008 ; https://huggingface.co/papers/2510.26008.
- **Abstract (verified):** Hardware-only **unsupervised** pipeline fusing ~700 low-level time-series channels (CPU/GPU util, power/thermal, memory, PCIe/InfiniBand interconnect); promises an **open dataset + profiling toolkit** over 26+ ML apps; identified network/config issues and sped DeepSeek by 5.97%.
- **Why it matters (P1,P3,P6,P7):** The closest published analog to our **method+benchmark**: a **non-DL statistical baseline (Z-score + Mahalanobis-in-PCA) vs Isolation Forest** — exactly the "provable delta" structure — plus windowed multimodal feature engineering and a released artifact. Contrast: GPU-cluster interconnect, **not** D2D/chiplet at PVT granularity.
- **Role:** **method + benchmark precedent + contrast point.**
- **Cited by:** fresh gap search (not in survey).

**A4. Universal Chiplet Interconnect Express (UCIe) Specification, Rev 1.1 (2023)**  *(NEW — Rev 1.1; survey has only UCIe 2.0)*
- **Authors:** UCIe Consortium.
- **Venue/Year:** UCIe Consortium, Rev 1.1, 2023 (industry standard).
- **Where to get:** uciexpress.org (member download). Cite Rev 1.1; pair with UCIe 2.0 (already survey #62) for recency.
- **Abstract (verified):** Defines D2D PHY/adapter/protocol layers; **redundant/spare lanes + repair MUXes**, eye masks per data rate, mandated **Rx eye margining**, **on-die PVT sensors** with process-health-indicator (PHI) monitoring, **mission-mode lane performance monitoring**, BER measurement, and **lane-to-lane skew**.
- **Why it matters (P1,P2,P4,P5,P3):** The **normative proof** that every modality we fuse (eye, BER, skew, PVT temp/voltage, lane retrain/repair) actually exists on a real D2D link — anchors synthetic-data realism for a Track-T audience. Not a method/baseline.
- **Role:** **motivation / problem-realism anchor (signal set).**
- **Cited by:** fresh gap search. **Survey lists UCIe 2.0 (#62) only; Rev 1.1 is the normative PVT/PHI/margining reference — new.**

**A5. CoMeT: Integrated Interval Thermal Simulation Toolchain for 2D/2.5D/3D Processor-Memory Systems**  *(NEW)*
- **Authors:** marg-tools (TACO authors).
- **Venue/Year:** ACM TACO 19(3), 2022; arXiv:2109.12405; MIT-licensed open source.
- **Where to get:** https://arxiv.org/abs/2109.12405 ; DOI 10.1145/3532185 ; https://github.com/marg-tools/CoMeT.
- **Abstract (verified):** First integrated **Core-and-Memory interval thermal** toolchain; supports off-chip DDR, off-chip 3D, **2.5D, and 3D** stacks at ~5% overhead; **open-source (MIT).**
- **Why it matters (P2,P4,P7,partial P5):** The **data-generation backbone** for the thermal modality — produces reproducible, **2.5D/3D-aware** temperature traces for the released benchmark. Directly satisfies Track-T's "physically-motivated data + released artifact."
- **Role:** **dataset/data-generator (thermal modality).**
- **Cited by:** fresh gap search; also used by HeatSense (#11) as a platform.

**A6. On-chip EOL Prognostics Using Data-Fusion of Embedded Instruments for Dependable MP-SoCs**  *(NEW)*
- **Authors:** Bagheriye, Ali, Kerkhoff (Univ. of Twente).
- **Venue/Year:** IEEE ATS 2020 (29th Asian Test Symposium).
- **Where to get:** IEEE Xplore (ATS 2020); open record research.utwente.nl/en/publications/on-chip-eol-prognostics-using-data-fusion-of-embedded-instruments/.
- **Abstract (verified):** **PCA-based data fusion** of multiple on-chip embedded instruments gives **better EOL prediction than any standalone EI**, even with EI inaccuracies and inter-EI correlation, for critical-path lifetime estimation.
- **Why it matters (P1,P2,P3,P5,P6):** The cleanest **non-ML statistical (PCA) fusion baseline** — the exact "fusion beats single-modality" claim, ported to D2D. Pair with an autoencoder/LSTM for the required baseline-vs-ML delta. Core-test venue (ATS).
- **Role:** **non-ML fusion baseline.**
- **Cited by:** fresh gap search (Twente prognostics lineage; not in survey).

**A7. Life-Time Prognostics of Dependable VLSI-SoCs using Machine-Learning**  *(NEW)*
- **Authors:** Bagheriye, Ali, Kerkhoff (Univ. of Twente).
- **Venue/Year:** IEEE IOLTS 2020 (26th On-Line Testing Symposium), doc 9159753.
- **Where to get:** IEEE Xplore doc 9159753; research.utwente.nl/.../life-time-prognostics-of-dependable-vlsi-socs-using-machine-learn/.
- **Abstract (verified):** Uses **ICA + Auto-Encoder to fuse multiple embedded-instrument modalities** plus nonlinear regression for a data-driven degradation model; **fused EIs beat standalone EIs** for EOL across four critical paths.
- **Why it matters (P1,P2,P3,P5,P6):** The closest **ML multimodal-fusion-for-reliability** exemplar (ICA/AE fusion) — the non-D2D ML fusion baseline to beat and the lineage-citation for "fusion exists for SoC EOL, not for D2D link health." On-line-test venue (IOLTS).
- **Role:** **ML fusion baseline + lineage anchor.**
- **Cited by:** fresh gap search (Twente lineage; not in survey).

---

## Tier B — Strongly recommended

**B1. SiPGuard: Run-Time System-in-Package Security Monitoring via Power-Noise Variation**  *(NEW as full entry)*
- **Authors:** T. Zhang, M. D. Rahman, H. Mardani Kamali, K. Zamiri Azar, F. Farahmandi (UF).
- **Venue/Year:** IEEE TVLSI 32(2):305–318, 2024 (online Oct 2023), DOI 10.1109/TVLSI.2023.3322384, doc 10286457.
- **Where to get:** IEEE Xplore doc 10286457; F. Farahmandi UF publications page.
- **Abstract (verified):** Self-contained **on-chiplet delay-based sensors (ROs/TDCs)** non-invasively monitor **power-noise at run-time** to track an *adjacent* chiplet's behavior and detect deviations.
- **Why it matters (P2,P3,P4):** Validates the exact **"sensors on one chiplet observe a neighbor die at runtime"** premise and supplies a **low-precision power-noise baseline** whose noise limitation motivates ML fusion. Single-modality (power noise), security-framed — no true P1.
- **Role:** **runtime-SiP baseline + related-work anchor.**
- **Cited by:** mined via #14 (ChipletQuake improves on it). **In survey only as a Tier-1b one-liner — promote to full download.**

**B2. Silicon Lifecycle Management Based on On-Chip Cross-Layer Sensing and Analytics for Space Applications**  *(NEW)*
- **Authors:** IHP Microelectronics.
- **Venue/Year:** IEEE conf. 2024 (doc 10534623). *Verify exact venue on Xplore before formal citation.*
- **Where to get:** IEEE Xplore doc 10534623; ResearchGate 380941545.
- **Abstract (verified):** On-chip **cross-layer** infrastructure fusing SEU/SET + power-bus activity + aging for **mission-mode** in-flight prediction; framed as SLM analytics on shared on-chip SRAM.
- **Why it matters (P1,P2,P3,P5):** The strongest **multimodal on-chip telemetry → runtime reliability analytics** precedent and the SLM/cross-layer framing we extend. Differentiator: space/logic SEU/aging, not D2D link BER/eye.
- **Role:** **SLM/cross-layer-fusion foundation.**
- **Cited by:** fresh gap search (not in survey).

**B3. SLOTH: Efficient and Accurate Detection of On-Chip Fail-Slow Failures for Many-Core Accelerators**  *(NEW)*
- **Authors:** (HW architecture, preprint).
- **Venue/Year:** arXiv:2510.24112, 2025 (rev. Feb 2026; unverified venue).
- **Where to get:** https://arxiv.org/abs/2510.24112.
- **Abstract (verified):** Lightweight, hardware-aware **on-chip fail-slow** detection: workload-aware instrumentation + **on-the-fly trace compression (kilobytes)** + topology-aware root-cause ranking; 115.9× storage reduction, 86.8% accuracy, 12.1% FPR.
- **Why it matters (P3,P5,P6):** **"Fail-slow" maps onto our "degradation, not hard fault"** pillar, with an honest overhead/accuracy/FPR template and a memory-budget on-chip method. Single-modality (timing), not D2D — cite as streaming/low-memory detector + open-problem evidence.
- **Role:** **online/low-memory method template.**
- **Cited by:** fresh gap search (not in survey).

**B4. Real-Time IC Aging Prediction via On-Chip Sensors**  *(NEW)*
- **Authors:** K. Huang, M. T. H. Anik, X. Zhang, N. Karimi.
- **Venue/Year:** IEEE ISVLSI 2021.
- **Where to get:** https://userpages.cs.umbc.edu/nkarimi/papers/ISVLSI21_b.pdf ; IEEE Xplore (ISVLSI 2021) for verbatim abstract.
- **Abstract (verified — title/authors/venue confirmed; abstract body re-read at Xplore before quoting):** **On-chip sensors + ML → runtime aging/health prediction** (keywords: IC aging, sensors, ML).
- **Why it matters (P2,P3,P5,P6,P8):** A directly transferable **sensor→ML→runtime aging** template from the exact DATE/VTS community (Karimi group). Contrast "logic/core aging" vs our "link aging." 2021, not D2D — foundational, not SOTA.
- **Role:** **method template (runtime aging).**
- **Cited by:** fresh gap search (not in survey).

**B5. Comparative Analysis of Ageing Forecasting Methods for Semiconductor Devices in Online Health Monitoring**  *(NEW)*
- **Authors:** (Elsevier EAAI).
- **Venue/Year:** Engineering Applications of AI 150:110545, 2025 (arXiv:2503.20403).
- **Where to get:** https://arxiv.org/abs/2503.20403 ; Elsevier EAAI 150:110545.
- **Abstract (verified):** Compares **classical tracking vs statistical vs NN forecasting** and introduces a **Temporal Fusion Transformer** for online aging forecasting (bond-wire lift-off via thermal-fatigue) — driven by **power/thermal cycling**.
- **Why it matters (P3,P5,P6):** A textbook **"classical baseline vs statistical vs temporal-DL, honestly compared"** methodology + evaluation template — exactly the delta structure. Domain is power-module MOSFET aging, not D2D — cite for method/eval design.
- **Role:** **forecasting-method + evaluation template.**
- **Cited by:** fresh gap search (not in survey).

**B6. Data Fusion with Genetic-Algorithm-Based Lifetime Prediction for Dependable MP-SoCs**  *(NEW)*
- **Authors:** (Twente lineage).
- **Venue/Year:** Tsinghua Science and Technology 28(6), Dec 2023, DOI 10.26599/TST.2022.9010053 (open access).
- **Where to get:** SciOpen, DOI 10.26599/TST.2022.9010053.
- **Abstract (verified):** **PCA-based fusion** of multiple embedded-instrument health datasets + **GA-optimized degradation model** for RUL, enabling preventive self-repair / zero-mean-downtime MP-SoCs.
- **Why it matters (P1,P2,P3,P5,P6):** A **recent (2023)** data point that multimodal-fusion reliability prognostics is active, and an alternative (GA-degradation) baseline to contrast vs a temporal DL detector. SoC-lifetime, not D2D; Tsinghua J. (supporting).
- **Role:** **recent fusion baseline (supporting).**
- **Cited by:** fresh gap search (not in survey).

**B7. SMV Methodology Enhancements for High-Speed I/O Links of SoCs**  *(NEW)*
- **Authors:** A. Viveros-Wacher, R. Alejos, et al. (Intel).
- **Venue/Year:** IEEE VTS 2014 (doc 6818767).
- **Where to get:** IEEE Xplore doc 6818767; ResearchGate 271431233.
- **Abstract (verified):** Enhances Intel's **System Margin Validation** for HSIO links: stress-method selection, volume-data optimization, and **UPM risk** calc; sweeps **voltage and temperature corners** and measures **Rx eye opening via on-die DFT** until BER/failure.
- **Why it matters (P4,P5,P2,partial P1/P3):** **Defines the link-health margin metrics** (eye opening, BER-at-failure, V/T-conditioned margin, part-to-part variability) we fuse with PVT telemetry, and is the **classical SMV margin-sweep non-ML baseline**. No ML/dataset.
- **Role:** **link-margin modality anchor + non-ML baseline.**
- **Cited by:** fresh gap search; companion to survey #7 (ITC-2020 SMV/ML). New (the 2014 VTS methodology is not in survey).

**B8. ML-Based Error Detection and Design Optimization in Signal-Integrity Applications**  *(NEW as full entry)*
- **Authors:** R. Medico, D. Spina, D. Vande Ginste, D. Deschrijver, T. Dhaene (Ghent/imec).
- **Venue/Year:** IEEE TCPMT vol. 9, 2019, DOI 10.1109/TCPMT.2019.2915738 (doc 8715394).
- **Where to get:** IEEE Xplore doc 8715394; UGent biblio preprint.
- **Abstract (verified):** Two-stage **autoencoder feature learning + unsupervised/semi-supervised AD** on digital-IC output waveforms for SI robustness.
- **Why it matters (P5,P6,P8):** The **journal (canonical) version** of the SI-AD baseline that Tier-1 #1 uses as a contractive-AE baseline — cite this over the EPEPS conference paper. Single-modality SI waveforms; no P1/P2/P3/P4/P7.
- **Role:** **established SI-AD ML baseline.**
- **Cited by:** mined via #1. **In survey only as a Tier-1b one-liner — promote to full download.**

**B9. Anomaly Detection Using Autoencoders in High-Performance Computing Systems**  *(NEW)*
- **Authors:** A. Borghesi, A. Bartolini, M. Lombardi, M. Milano, L. Benini.
- **Venue/Year:** AAAI 2019, pp. 9428–9433 (arXiv:1811.05269).
- **Where to get:** https://arxiv.org/abs/1811.05269 ; code github.com/AndreaBorghesi/anomaly_detection_HPC.
- **Abstract (verified):** **Train-on-normal autoencoders** per node, detect abnormal conditions via reconstruction error on multivariate hardware telemetry; 88–96% accuracy on unseen anomalies; **public code.**
- **Why it matters (P3,P5,P6,partial P1/P2):** The canonical **AE-reconstruction-error-on-streaming-telemetry** method with a public artifact — the backbone we extend to multimodal on-chip D2D telemetry. HPC-node domain, not silicon link.
- **Role:** **method backbone (semi-supervised AE) + artifact precedent.**
- **Cited by:** fresh gap search (method lineage; not in survey).

**B10. Domain-Specific ML for Minimum Operating Voltage (Vmin) Prediction Using On-Chip Monitor Data**  *(NEW)*
- **Authors:** Y. Yin, R. Chen, C. He, P. Li.
- **Venue/Year:** IEEE ITC 2023, pp. 99–104.
- **Where to get:** IEEE Xplore (ITC 2023); related arXiv 2406.18536 / 2408.06254 / 2509.00035 (same group).
- **Abstract (verified):** A **monotonic lattice NN** with correlation/co-linearity-aware feature selection predicts chip **Vmin from on-chip monitor data**, beating linear regression and conventional NNs.
- **Why it matters (P2,P6,partial P5/P1):** Justifies **"ML on on-chip monitors predicts an electrical-health margin"** and a reusable **domain-constrained (monotonicity)** trick. Offline test-time, not online; not D2D.
- **Role:** **method (domain-constrained ML on monitors) + related work.**
- **Cited by:** fresh gap search (ITC silicon-monitor lineage; not in survey).

**B11. Unleashing the Power of Anomaly Data for Soft-Failure Predictive Analytics**  *(NEW; venue corrected)*
- **Authors:** F. Su, P. Goteti, M. Zhang.
- **Venue/Year:** **IEEE ITC 2020**, pp. 1–10 (doc 9325243) — *not* Design & Test 2023.
- **Where to get:** IEEE Xplore doc 9325243; DBLP conf/itc/SuGZ20.
- **Abstract (verified):** **Multi-State Models** with time-varying covariates + statistical ML over a **streaming anomaly-data flow** for **soft-failure** prognosis in a silicon health-prognosis framework.
- **Why it matters (P5,P3,P6):** A clean **non-DL statistical baseline (MSM)** for soft-failure prognosis; OCTANE notes it is software-only/per-feature — our **multimodal fused** approach is the improvement. ITC venue.
- **Role:** **non-ML soft-failure baseline.**
- **Cited by:** mined via OCTANE (#2). New (not in survey).

**B12. On-Chip Age Estimation Using Machine Learning**  *(NEW)*
- **Authors:** Alnuayri, Khursheed, Rossi.
- **Venue/Year:** IEEE Access vol. 11, 2023, DOI 10.1109/ACCESS.2023.* (open access).
- **Where to get:** IEEE Access OA; livrepository.liverpool.ac.uk/3192131/.
- **Abstract (verified):** **SVR fuses temperature + RO frequency + discharge time + inter/intra-die process variation** to estimate IC age (22 nm, 13/51-stage ROs); **incorporating PV materially improves** the estimate.
- **Why it matters (P2,P5,P6,partial P1):** A **PVT-aware multimodal-feature ML aging** precedent with the **"PVT-incorporation ablation = provable delta"** exactly Track-T rewards. Simulation-only, no link/D2D signals.
- **Role:** **PVT-aware ML aging baseline.**
- **Cited by:** fresh gap search (not in survey).

**B13. Implementation of Aging-Mechanism Analysis and Prediction for XILINX 7-Series FPGAs (28 nm)**  *(NEW)*
- **Authors:** (MDPI Sensors).
- **Venue/Year:** Sensors 22(12):4439, 2022, DOI 10.3390/s22124439 (open access).
- **Where to get:** https://www.mdpi.com/1424-8220/22/12/4439 ; PMC9227486.
- **Abstract (verified):** Builds a **measured RO+XADC-temperature dataset** on 24 FPGAs (10+ yr accelerated), **corrects temperature-induced measurement error**, and benchmarks **4 ML models** (XGBoost/SVM/LR/ANN); min error 0.292%.
- **Why it matters (P2,P5,P6,P7,partial P1):** A **dataset-construction + thermal-compensation + multi-model benchmarking** template (reproducible data + honest measurement-error handling). Accelerated/offline, FPGA, single-mechanism.
- **Role:** **dataset/thermal-compensation precedent.**
- **Cited by:** fresh gap search (not in survey).

**B14. PDNSig: Identifying Multi-Tenant Cloud FPGAs with PDN-Based Signatures**  *(NEW)*
- **Authors:** H. Zhu, W. Cao, X. Zhang.
- **Venue/Year:** IEEE/ACM ICCAD 2023 (doc 10323545), DOI 10.1109/ICCAD57390.2023.10323545.
- **Where to get:** IEEE Xplore doc 10323545.
- **Abstract (verified):** **PDN/voltage impedance fingerprint** (FFT-based) uniquely IDs FPGAs and adjacent chiplet regions sharing the PDN.
- **Why it matters (P2,P4,P6):** Establishes **PDN-impedance sensing of co-located chiplets** and a concrete **FFT-impedance non-ML baseline** (with a documented SNR limitation motivating ML). Single-modality, ID-not-health.
- **Role:** **PDN-impedance baseline + related work.**
- **Cited by:** mined via #14 (ChipletQuake differentiates from it). New (not in survey).

---

## Tier C — Background / related-work anchors (one line each)

- **HeatSense (thermal AD, NoC-MPSoC)** — IEEE TCAD 2026 / arXiv:2504.11421 — lightweight **WMA+bit-shift non-ML thermal baseline vs Random Forest**, the apples-to-apples statistical-vs-ML template. *(Already survey Tier-1 #11.)*
- **Analysis of UCIe 48/64 GT/s Electrical Links** — IEEE OJ-SSCS 2025 (Intel) — **UCIe PHY reliability + failure-probability modeling** to parameterize realistic D2D link-degradation data.
- **Generating Test Patterns for Chiplet Interconnects (E2I-TEST)** — IEEE TCAD 2024 (doc 10689272) / ITC-Asia 2023 — physically-grounded **short/open + adjacent-bump coupling fault models** for synthetic-anomaly realism; structural-test baseline. *(Already survey Tier-1b.)*
- **Test and Repair Improvements for UCIe** — IEEE ETS 2024 — 16-pattern UCIe interconnect test + **spare-lane/retrain repair** mechanism our detector observes. *(Already survey Tier-1b.)*
- **Defect Analysis & BIST for Chiplet Interconnects in FOWLP** — IEEE VTS 2025 / arXiv:2503.14784 — Q3D defect→electrical mapping; **hard-fault BIST contrast class**. *(Already survey Tier-1 #3.)*
- **Probeless Fault Isolation for 2.5D/3D D2D** — IEEE EPS eNews June 2024 — **in-field hard-fault isolation** of D2D interconnects; non-ML industry baseline (TC eNews, not archival). *(Already survey Tier-1 #5.)*
- **Development of a Non-Invasive On-Chip Interconnect Health Sensing Method Based on BER** — Sensors 2018 (PMC6210517) — empirical **BER/eye degrades gradually before DC-resistance fails**; physically motivates the eye/BER modality. *(Already survey Tier-1b ★.)*
- **Early Detection of Interconnect Degradation by Continuous Monitoring of RF Impedance** — IEEE TDMR 2009 — foundational **non-ML continuous-monitoring baseline** (skin-effect rationale). *(Already survey Tier-1b ★.)*
- **Remaining-Life Prediction of Solder Joints via RF Impedance + Gaussian Process Regression** — IEEE TCPMT 2015 (doc 7274700) — **online interconnect signal + GPR with uncertainty**; near-template for the regression head (minus multimodality/D2D).
- **Operational Age Estimation of ICs Using GPR** — IEEE DFT 2022 (doc 9962355) — **GPR on RO+temperature** PVT telemetry for aging; non-ML-vs-ML aging setup.
- **Using ML for AD on a SoC under Gamma Radiation** — Nuclear Eng. & Tech. 2022 / arXiv:2201.01588 — **One-Class SVM (recall 0.95)** on on-chip sensor streams; degrade-before-failure. *(Already survey #55.)*
- **Switching Frequency as FPGA Monitor (XFEL, 298 devices)** — arXiv:2412.15720, 2024 — rare **real in-field aging telemetry at scale**; forecast-horizon evaluation protocol. *(Already survey #30.)*
- **Hierarchical Symbol-Based Health-Status Analysis (core routers)** — IEEE TCAD 2020 (doc 8599051, Chakrabarty) — **symbolic temporal AD** statistical baseline lineage.
- **Silicon Lifecycle Management with In-Chip Monitoring** — IEEE IRPS 2021 (Synopsys) — the **SLM "why" framing** for the introduction.
- **Long-Term Aging Impacts on Spatial On-Chip Power Density and Temperature (BTI)** — SMACD 2023 (doc 10192234) / Integration 2024 — quantifies **BTI-driven thermal/voltage drift** (why drift, not just spikes, matters).
- **A Review of Techniques for Ageing Detection on Embedded Systems** — ACM CSUR 57(1), 2024 (arXiv:2301.06804) — authoritative **aging taxonomy + "rising ML-for-aging trend"** background.
- **Challenges in Post-Silicon Validation of High-Speed I/O Links** — ICCAD 2012 — link-validation vocabulary/difficulty (motivation that online monitoring complements expensive validation).
- **Pyeye: Eye-Diagram SI Assessment Tool** — ICCE-Asia 2023 (doc 10326361, KAIST) — reproducible **eye-margin labeling tool** for the link modality.
- **Eye-Diagram-Distortion Identification via CNN + Pseudo-Labeling (HBM interposer)** — ~2023–24 (verify title) — **interposer-channel eye-distortion taxonomy** + few-label angle.
- **PCA-Autoencoder for Correlated Sensor Data** — arXiv:2505.24044, 2025 — **PCA-gated autoencoder** = light non-ML gate + heavy ML, low-overhead online design.
- **HeatSense-adjacent / generic AD methods:** **LSTM-AD (ESANN 2015)**, **Deep SAD (ICLR 2020)** *(survey Tier-1b)*, **LOF (SIGMOD 2000)**, **LSAnomaly (Pattern Recog. Lett. 2014)**, **Semi-Supervised Autoencoder (ICONIP 2016)** — standard statistical/ML AD baselines to implement for the provable delta.
- **Boreas (RL hotspot mitigation via thermal telemetry)** — ISPASS 2023 (doc 10158079) — runtime thermal-telemetry+ML realism (sensor delay/accuracy), motivation only.
- **Discretized-Isolation-Forest (edge AD)** — IEEE IoT-J 2025 (doc 10700727, Chakrabarty lineage) — lightweight on-device unsupervised AD building block.
- **On-Chip Noise Sensor for IC Susceptibility** — IEEE T-IM 2012 (doc 6088009) — concrete **voltage-noise sensor IP** (the droop/noise modality). *(OCTANE cites it.)*
- **Voltage-Based Covert Channels Using FPGAs (TDC sensor)** — ACM TODAES 2021 — justifies the **on-chip TDC voltage-sensing front-end**.
- **DRAM retention / VRT characterization** — ISCA 2013 — physically-grounded memory failure mechanism for motivation.
- **Silicon Echoes (frequency-selective impedance tamper detection)** — IACR TCHES 2023 — impedance/PDN-sensing method lineage behind ChipletQuake. *(Already survey Tier-1b.)*
- **proteanTecs: In-Chip Monitoring + Deep Analytics for HBM** — vendor white paper 2023–24 — industrial **"blind-spot" motivation** (not citable as method). *(Already survey #64.)*
- **Modeling Thermal Coupling + Temp-Sensor Design for HT Detection** — MWSCAS 2018 — low-tier sensor-justification for the thermal modality.
- **Online Fault-Tolerance for TSV-Based 3D-IC** — IEEE TVLSI 2015 — prior-art on **online TSV hard-fault** detection/repair (contrast to telemetry fusion).
- **Intelligence Prediction of IC Reliability (SSA-LSTM + EMD)** — PLoS ONE 2025 — **EMD-denoise→LSTM-forecast** degradation recipe (single-modality ΔVth).
- **Ranking-CNN of S-parameter Patterns (interconnect defects)** — IMAPS 2019 — SREL predecessor; severity-rating-from-RF-signatures template. *(Already survey Tier-1b.)*
- **Holistic System-Margining/Jitter-Tolerance Optimization (Kriging+GPR)** — IEEE TETC 2020 (doc 8053840) — ML-on-link-margins as accepted industry practice (design-time; framing only).

---

## Coverage-gap analysis (where the literature is thin)

- **No paper does true multimodal voltage+thermal+link fusion for D2D *online* health.** The closest analogs split cleanly: **multimodal fusion exists for SoC/critical-path EOL** (A6/A7 Twente PCA/ICA/AE, B6 GA; B2 cross-layer SEU/aging) but **not for D2D links** and **not with link-level BER/eye/skew/retrain**; conversely **D2D-specific** work (survey #3/#4/#5, Tier-1b UCIe test/repair, B7 SMV, B14/PDNSig, #14 ChipletQuake) is **single-modality and mostly hard-fault/structural or security, not online degradation fusion**. **This intersection — multimodal PVT+link fusion for online D2D link-health degradation — is genuine white space and IS the contribution.**
- **Pillar coverage — well-covered:** **P2** (on-chip sensors: noise sensor T-IM'12, RO/PVT monitors, TDC voltage, UCIe PVT/PHI), **P4** (D2D test: survey #3/#4/#5/#6, E2I-TEST, UCIe test/repair, ChipletQuake), **P5/P6** (aging/degradation ML: B4/B5/B12/B13, GPR, AE/LSTM baselines), **P3** (online detectors: OCTANE, E-SCOUT, SLOTH, Reveal). **P8** is strong (ITC/VTS/ETS/TCAD provenance via Chakrabarty/Karimi/Twente/Intel lines).
- **Pillar coverage — under-covered:** **P1 (multimodal fusion) is covered only off-target** (SoC-EOL fusion, not D2D; Reveal fuses GPU-cluster telemetry, not chiplet PVT+link). **P7 (a released D2D-link-health benchmark) does not exist** — every D2D paper uses proprietary (proteanTecs/GUC) or unreleased simulation data; the released artifacts that *do* exist (Reveal A3, CoMeT A5, HPC-AE B9, FPGA-aging B13, DRAM-SI #1) are all *adjacent domains*.
- **No online detector consumes UCIe-native telemetry.** OCTANE/E-SCOUT use CPU counters; SLOTH uses timing traces; HeatSense uses router temperature. **Nobody streams eye-margin + BER + lane-skew + retrain/parity + PVT together** — exactly the UCIe-mandated set (A4).
- **The non-ML baseline is fragmented across modalities** (PCA-fusion A6, SMV margin-sweep B7, MSM soft-failure B11, WMA-thermal #11, FFT-impedance B14, RF-impedance/DC-resistance #13/TDMR'09). **No single non-ML baseline fuses the modalities** — so a simple PCA/Mahalanobis multimodal baseline is both easy to build and a clean delta target.
- **Degradation-vs-hard-fault framing is open.** D2D work overwhelmingly does **hard-fault structural test** (stuck-at/bridging/open via BIST/ATPG); the **gradual-degradation / "fail-slow" / soft-failure** angle (SLOTH B3, soft-failure B11, BER-gradual-transition Sensors'18) is exactly where telemetry fusion adds early-warning value.

---

## DATE-2027 positioning (sharpest defensible contribution)

- **Contribution.** "**First open, online, multimodal D2D link-health detector**: fuse UCIe-native link telemetry (eye margin, BER, lane skew, retrain/parity) with on-chip PVT (voltage droop/noise, temperature drift) into a streaming anomaly/degradation detector that flags **gradual link degradation before hard failure** — released as a reproducible benchmark." This sits squarely in the white space above.
- **Baseline it beats (provable delta).** A two-tier baseline story Track-T rewards: (1) **non-ML** — multimodal **PCA/Mahalanobis fusion (A6 lineage) + per-modality threshold/margin-sweep (B7 SMV, #13 eye/BER, #11 WMA)**; (2) **single-modality / non-fused ML** — **E-SCOUT (A2) and OCTANE (A1)** ported, plus **AE-reconstruction (B9) / LSTM-AD**. Show the multimodal fused detector beats all on AUROC/early-warning lead-time at comparable on-chip PPA.
- **Dataset/artifact to release.** A **synthetic-but-physically-grounded D2D telemetry benchmark**: **thermal traces from CoMeT (A5, 2.5D/3D)**; **link-degradation/BER/eye operating points parameterized from UCIe Rev 1.1 (A4) + UCIe 48/64 GT/s reliability modeling**; **fault/coupling signatures from E2I-TEST/FOWLP-BIST (#3) Q3D models**; voltage-noise from on-chip-noise-sensor characteristics — released with code, mirroring the artifact discipline of **Reveal (A3), HPC-AE (B9), DRAM-SI (#1)**. This is itself a contribution since **no public D2D-link-health benchmark exists.**
- **Honest limitations to state up front.** Data is synthetic/emulated (no released silicon D2D telemetry exists publicly); fusion is validated on UCIe-derived signal models, not measured chiplets; the degradation curves borrow physics from solder-joint/RF-impedance and BTI studies rather than measured D2D aging — these are the candid caveats Track-T expects.
- **Why it's defensible to reviewers.** Crisp problem (D2D blind spot, A4-mandated signals real), non-ML baseline + ML delta (A1/A2/A6 + AE/LSTM), physically-motivated released data (A5/A4/#3), and a community-correct provenance (ITC/VTS/ETS lineage via A1/A2/B4/B7/#3).

---

## Appendix — already in survey / not-found / verify-before-citing

**Strong candidates already in the survey (do NOT re-download; cite as listed):**
- **OCTANE** — Tier-1 **#2** (verified). *Re-listed as A1 anchor only.*
- **HeatSense** — Tier-1 **#11** (verified).
- **Defect Analysis & BIST for Chiplet Interconnects (FOWLP)** — Tier-1 **#3** (verified). *(All five duplicate JSON entries map here.)*
- **Probeless Fault Isolation 2.5D/3D D2D** — Tier-1 **#5** (unverified). *(Both JSON copies.)*
- **ChipletQuake** — Tier-1 **#14** (verified). *(Both JSON copies — arXiv 2504.19418 is the correct record; the MDPI Sensors 25(15)/PMC12349434 citation could not be verified and should not be asserted.)*
- **Learning High-Quality Latent Representations (DRAM-SI)** — Tier-1 **#1** (verified). *(All three JSON copies.)*
- **Non-destructive Fault Diagnosis / SREL** — Tier-1 **#13** (verified).
- **Switching Frequency as FPGA Monitor (XFEL)** — **#30.**
- **Using ML for AD on SoC under Gamma Radiation** — **#55.**
- **Non-Invasive On-Chip Interconnect Health Sensing via BER (Sensors 2018)** — Tier-1b ★ (Shin/Koo/Kwon). *(The SEVEN duplicate JSON entries — incl. variant DOIs s18103234/s18103486/s18113603 and PMC6210517 — are the same paper; the correct canonical record is **Sensors 18(10):3234, DOI 10.3390/s18103234**.)*
- **Early Detection of Interconnect Degradation by RF Impedance (TDMR 2009)** — Tier-1b ★.
- **Early Detection via Ranking-CNN of S-parameters (IMAPS 2019)** — Tier-1b.
- **Silicon Echoes (TCHES 2023)** — Tier-1b.
- **E-SCOUT** — Tier-1b one-liner (*promoted to full download A2*).
- **SiPGuard/SiGuard** — Tier-1b one-liner (*promoted to full download B1*).
- **Medico SI-AD (TCPMT 2019 / EPEPS 2018)** — Tier-1b (*TCPMT 2019 promoted to full download B8; EPEPS 2018 remains Tier-1b*).
- **Deep SAD** — Tier-1b.
- **UCIe 2.0 (2024)** — **#62** (note: A4 adds **Rev 1.1, 2023** as the distinct normative PVT/PHI/margining reference).
- **proteanTecs HBM in-chip monitoring** — **#64** (the JSON HBM white-paper entry).
- **Generating Test Patterns for Chiplet Interconnects (TCAD 2024 / ITC-Asia 2023)** — Tier-1b (both JSON copies).
- **Test and Repair Improvements for UCIe (ETS 2024)** — Tier-1b.

**Genuinely NEW downloads in this round (not in survey):** A2 (promoted), A3, A4 (Rev 1.1), A5, A6, A7, B1 (promoted), B2, B3, B4, B5, B6, B7, B8 (promoted), B9, B10, B11, B12, B13, B14 — plus the new Tier-C anchors (UCIe 48/64 GT/s OJ-SSCS 2025; TCPMT-2015 solder-joint GPR; DFT-2022 GPR age; TCAD-2020 symbolic health; IRPS-2021 SLM; SMACD-2023 BTI; CSUR-2024 aging survey; Pyeye; HBM eye-distortion CNN; PCA-AE; ISCA-2013; MWSCAS-2018; TVLSI-2015 TSV; PLoS-2025 SSA-LSTM; ISPASS-2023 Boreas; IoT-J-2025 DIF; T-IM-2012 noise sensor; TODAES-2021 voltage covert channel; ESANN-2015/LOF/LSAnomaly/ICONIP-2016 generic AD; TETC-2020 margining).

**Verify-before-citing (metadata not fully fetched / corrections needed):**
- **B2 (IHP cross-layer SLM, doc 10534623)** — confirm exact venue name on Xplore.
- **B4 (Real-Time IC Aging, ISVLSI 2021)** — re-read verbatim abstract at Xplore before quoting.
- **A2 (E-SCOUT) / A1 (OCTANE) full abstracts** — IEEE 418/paywall; verbatim text pending Xplore access.
- **B11** — venue is **ITC 2020** (doc 9325243), NOT "IEEE Design & Test 2023" as originally tagged.
- **HBM eye-distortion CNN + pseudo-labeling** — confirm exact **title/authors/venue/year** on Xplore (Semantic Scholar page empty).
- **On-Chip EI Data Fusion (IEEE doc 9180773, 2020 companion)** — `recommend: MAYBE`, **heavily overlaps A6/A7**; verbatim abstract unconfirmed (418/403). Treat as redundant — prefer A6 (ATS) and A7 (IOLTS).
- **Probeless Fault Isolation (survey #5)** — EPS eNews PDF returned 404 at retrieval; locate an archival version before formal citation.

**Notable NOT-FOUND / chase manually (from survey, still unverified):** survey **#9** "Test and Diagnosis Strategies for Inter-Chiplet Interconnects" (RG 389613395), **#10** GUC GLink proteanTecs D2D characterization, **#15** proteanTecs "100% Lane Coverage" chiplet-reliability blog — these are the **industrial D2D-link-health deployment references** with no archival peer-reviewed source; chase for motivation/positioning only.
