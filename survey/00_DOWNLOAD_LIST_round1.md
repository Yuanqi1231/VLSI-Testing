# Round 1 Download Priority List — VLSI Testing Survey

**Target venue: DATE 2027, Track T (Test, Reliability and Security)**
Likely abstract deadline ~early Sept 2026, full deadline ~mid-Sept 2026. Course demo 2026-06-11 → ~3 months runway to extend into a DATE submission.

Total surveyed: **527 papers** across 5 directions (2021–2026, IEEE/ACM/Springer/Elsevier + key arXiv). Per-direction details in `direction[1-5]_*.md`.

This file consolidates the **top recommendations to download first** so I can refine relevance after you've read abstracts in context. Mark each as `[x]` once downloaded.

## DATE-T-specific lens

DATE Track T past acceptances reward: (a) a crisp problem statement, (b) a strong **non-ML baseline** AND an ML method (so the delta is provable), (c) realistic data (synthetic is OK if physically motivated and released), (d) a reproducible artifact (code + dataset), (e) honest limitations.

Of the 5 candidate directions, ranked by fit for DATE 2027 Track T:

| Rank | Direction | DATE fit | Reason |
|------|-----------|----------|--------|
| 1 | **D3: D2D Link Anomaly Detection** | ★★★★★ | Chiplet test is the hottest DATE-T topic 2025–26; IEEE P3405 is freshly opening a benchmark void you can fill. Synthetic-OK aligns. |
| 2 | **D2: AI-assisted Fault Diagnosis** | ★★★★★ | Has consistent DATE-T history (scan diagnosis, ML for ATPG). LLM+scan-fail-log is genuinely novel and reproducible on ISCAS/ITC benchmarks. |
| 3 | **D1: Failure Bitmap Analysis** | ★★★★ | DATE-T accepts wafer-map ML occasionally; would need a *bitmap-for-chiplet/TSV* angle to stand out from the saturated wafer-map literature. |
| 4 | **D4: AI-assisted Test Optimization** | ★★★★ | DATE-T regularly publishes test scheduling/TPI papers. RL+chiplet+thermal angle is timely. |
| 5 | **D5: LLM for DFT** | ★★★ | LLM-for-EDA is hot but the venue is currently dominated by DAC/ICCAD/MLCAD. Doable, but needs a strong test-specific angle to be clearly DATE-T. |

**Strongest combined angle**: D2 + D5 — LLM/RAG agent that ingests scan fail logs + ATPG diagnostic reports → ranked fault candidates + natural-language debug steps, evaluated on ISCAS-89 / ITC'99. This is reproducible, has a clear non-ML baseline (existing diagnosis tools), and no published end-to-end system exists.

**Alternate strong angle**: D3 — first public multi-modal D2D anomaly-detection benchmark (synthetic BER + eye + jitter + thermal + PDN streams, parameterized by physical model), with an Autoencoder+LSTM baseline. The dataset itself is a contribution worth a DATE paper.

---

## A. Cross-Direction Top 10 (download these first if time is tight)

These appear in multiple directions or are foundational across the whole VLSI-ML space.

| # | Paper | Venue | Why download first |
|---|-------|-------|---------------------|
| A1 | **A Survey and Recent Advances: Machine Intelligence in Electronic Testing** — Huang et al. | JETTA 2024 | Single best related-work source; cited by D2 and D4 Tier 1. [link](https://link.springer.com/article/10.1007/s10836-024-06117-7) |
| A2 | **GRAND: A GNN Framework for Improved Diagnosis** | IEEE TCAD 2024 | Canonical modern ML diagnosis paper, appears in both D2 and D4. [link](https://ieeexplore.ieee.org/document/10336212/) |
| A3 | **Machine-Learning Approach in Detection and Classification for Defects in TSV-Based 3-D IC** | IEEE TCPMT 2018 | Bridges D1 (TSV bitmap) and D3 (interconnect), widely cited. [link](https://ieeexplore.ieee.org/document/8272475/) |
| A4 | **ChipNeMo: Domain-Adapted LLMs for Chip Design** — NVIDIA | ICCAD 2023 / arXiv:2311.00176 | The canonical LLM-for-EDA paper, must-cite for D5. [link](https://arxiv.org/abs/2311.00176) |
| A5 | **DFTAgent — LLM Agents as Catalysts for Resilient DFT** | Applied Sciences (MDPI) 2025 | Only paper explicitly orchestrating DFT/ATPG toolchain with LLM agents. [link](https://www.mdpi.com/2076-3417/15/21/11390) |
| A6 | **Towards LLM-based Root Cause Analysis of Hardware Design Failures** | IEEE LAD 2025 / arXiv:2507.06512 | Direct template for fail-log RCA. [link](https://arxiv.org/abs/2507.06512) |
| A7 | **SmartATPG: GCN + RL ATPG** | DAC 2024 | Flagship modern ATPG paper. [link](https://dl.acm.org/doi/10.1145/3649329.3656526) |
| A8 | **When Wafer Failure Pattern Classification Meets Few-Shot Learning and Self-Supervised Learning** — Geng et al. | ICCAD 2021 | Best D1 methodology template. [link](https://dl.acm.org/doi/abs/10.1109/ICCAD51958.2021.9643518) |
| A9 | **Learning High-Quality Latent Representations for Anomaly Detection and SI Enhancement in High-Speed Signals** | arXiv 2506.18288 (2025) | Closest analog of the D3 target problem. [link](https://arxiv.org/abs/2506.18288) |
| A10 | **OCTANE: On-Chip Telemetry-based Anomaly Notification Engine** | IEEE 2025 (Xplore 11219729) | Reference on-chip unsupervised AD engine for D3. [link](https://ieeexplore.ieee.org/document/11219729/) |

---

## B. Top 5 per Direction (after A-list)

### Direction 1 — Failure Bitmap Intelligent Analysis (`direction1_failure_bitmap.md`)
- [ ] **D1-1.** Nakazawa & Kulkarni, *Wafer Map Defect Pattern Classification* — IEEE TSM 2018 — foundational CNN-on-synthetic-bitmap. [doc/8263132](https://ieeexplore.ieee.org/document/8263132/)
- [ ] **D1-2.** Nakazawa & Kulkarni, *Anomaly Detection and Segmentation for Wafer Defect Patterns* — IEEE TSM 2019 — canonical AE baseline. [doc/8634922](https://ieeexplore.ieee.org/document/8634922/)
- [ ] **D1-7.** Geng et al., *Few-Shot + Self-Supervised Wafer Classification* — ICCAD 2021. (also A8)
- [ ] **D1-8.** Kahng et al., *Contrastive Wafer Bin Map* — ITC 2021. [PDF](https://web.ece.ucsb.edu/~lip/publications/ConstrastiveLearning-ITC2021-Submitted.pdf)
- [ ] **Wang et al., ACDDPM-ResNet** — Computers & Industrial Engineering 2024 — diffusion model for wafer bitmap synth (in Tier 2 but flagged in summary).

### Direction 2 — AI-assisted Fault Diagnosis (`direction2_fault_diagnosis.md`)
- [ ] **D2-1.** GRAND — TCAD 2024 (also A2)
- [ ] **D2-2.** *Deep Learning-assisted Scan Chain Diagnosis with Different Fault Models* — ITC 2022. [doc/9979020](https://ieeexplore.ieee.org/document/9979020/)
- [ ] **D2-3.** *Multistage Enhanced Diagnosis With Fault Candidate Reduction* — TCAD 2025. [doc/10916692](https://ieeexplore.ieee.org/document/10916692/)
- [ ] **D2-8.** *Translating Test Responses to Images for Test-Termination Prediction* — ACM TODAES 2024. [10.1145/3661310](https://dl.acm.org/doi/10.1145/3661310)
- [ ] **D2-15.** **DeCo** — Defect-Aware Contrast for Online IC Testing — IJCAI 2025 / arXiv:2505.00278.

### Direction 3 — D2D Link Anomaly Detection (`direction3_d2d_anomaly.md`)
- [ ] **D3-1.** *Latent Representations for AD + SI in High-Speed Signals* — arXiv 2506.18288 (also A9)
- [ ] **D3-2.** OCTANE (also A10)
- [ ] **D3-3.** *Defect Analysis and BIST for Chiplet Interconnects in FOWLP* — arXiv 2503.14784 (2025). [link](https://arxiv.org/abs/2503.14784)
- [ ] **D3-6.** **IEEE Std P3405** — Chiplet Interconnect Test and Repair — VTS/ETS 2024. [doc/10538776](https://ieeexplore.ieee.org/document/10538776/)
- [ ] **D3-11.** **HeatSense** — Thermal Anomaly Detection for NoC-Enabled MPSoCs — arXiv 2504.11421 (IEEE 2025). [link](https://arxiv.org/abs/2504.11421)

### Direction 4 — AI-assisted Test Optimization (`direction4_test_optimization.md`)
- [ ] **D4-1.** SmartATPG — DAC 2024 (also A7)
- [ ] **D4-3.** *DETECTive: ML-driven Test Pattern Prediction* — GLSVLSI 2024. [10.1145/3649476.3658696](https://dl.acm.org/doi/10.1145/3649476.3658696)
- [ ] **D4-4.** **DeepTPI: Test Point Insertion with DRL** — ICCAD 2022 / TCAD 2023. [doc/9983950](https://ieeexplore.ieee.org/document/9983950/)
- [ ] **D4-5.** *RL-Based TPI for Power-Safe M3D Testing* — TCAD 2025. [doc/10972002](https://ieeexplore.ieee.org/document/10972002/)
- [ ] **D4-7.** *ML-Based Adaptive Outlier Detection for Analog/RF IC Testing* — VTS 2023 (TI data). [doc/10140005](https://ieeexplore.ieee.org/document/10140005/)

### Direction 5 — LLM for DFT / Testing (`direction5_llm_dft.md`)
- [ ] **D5-1.** DFTAgent (also A5)
- [ ] **D5-2.** LLM-based RCA of HW Design Failures (also A6)
- [ ] **D5-3.** **FVDebug** — NVIDIA arXiv:2510.15906. [link](https://arxiv.org/abs/2510.15906)
- [ ] **D5-6.** **VerilogEval** — ICCAD 2023 / arXiv:2309.07544. [link](https://arxiv.org/abs/2309.07544)
- [ ] **D5-10.** **LLM4DV** — Test Stimuli Generation — arXiv 2310.04535. [link](https://arxiv.org/abs/2310.04535)

---

## C. Most Promising Research Gaps (from agent reports)

These are the angles I'd target if turning this into a conference paper. Each is a candidate project scope:

1. **D1 — Cross-modal foundation model for bitmaps**: pretrain on WM-811K + synthetic memory fail bitmaps + synthetic TSV/chiplet maps; fine-tune per modality. Builds the missing memory/chiplet bitmap benchmark as a side contribution.
2. **D2 — LLM/RAG diagnosis agent over scan fail logs**: combines LLM + RAG + scan fail-log → fault location + type + natural-language debug suggestion. No published end-to-end system.
3. **D3 — Multi-modal D2D anomaly benchmark + model**: fuse BER + eye-margin + jitter + thermal + PDN-noise streams in a single time-series AD model on chiplet PHY data. No public benchmark exists.
4. **D4 — RL test scheduling for heterogeneous chiplets under UCIe 2.0 + IEEE P3405**: with a learned thermal surrogate inside the RL training loop. Releasable benchmark possible.
5. **D5 — Closed-loop LLM-driven scan/ATPG fail-log diagnosis with structured RAG + CoT**: end-to-end manufacturing-test scan-fail + ATPG report → fault candidates + repair, with public benchmark. Cross-cuts D1+D2.

**Note**: D2-#2, D5-#5, and D1-#1 are highly aligned — pursuing the LLM-scan-diagnosis angle could anchor a conference paper that hits 3 directions at once.

---

## How to proceed

1. **Glance at the A-list (10 papers)** first — they ground the related work across all directions.
2. **Pick 1-2 directions** of interest based on which research-gap angle excites you.
3. **Download that direction's Top 5** from section B.
4. Tell me which ones you got — I'll deepen the survey on that direction (find the next 10-20 with closer relevance, identify code repos, datasets, etc.) and start identifying the concrete project scope.

Update this file with `[x]` as you download. I'll iterate from there.
