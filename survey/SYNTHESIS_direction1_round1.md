# Direction 1 — Reading Synthesis & DATE 2027 Plan (Round 1)

Based on the 7 papers downloaded to `papers/1/`. All 7 are **wafer-map / wafer-bin-map (WBM)** works — this matters: it is the saturated sub-area, and the course's real Direction-1 scope (memory / TSV / chiplet-interconnect bitmaps) is wide open. See Part 4 for how to exploit that for DATE.

The 7 papers:
| # | Short name | Venue/Year | Type |
|---|-----------|-----------|------|
| P1 | Nakazawa & Kulkarni — CNN classification + retrieval | IEEE TSM 2018 | primary |
| P2 | Nakazawa & Kulkarni — encoder–decoder anomaly detection + segmentation | IEEE TSM 2019 | primary |
| P3 | SWaCo — self-supervised contrastive WBM classification | IEEE TSM 2023 | primary |
| P4 | Wang & Ni — DL framework for **complex (multi-bin, multi-GFA)** WBM | IEEE TSM 2023 | primary |
| P5 | Batool et al. — Systematic Review of DL for wafer defect recognition | IEEE Access 2021 | review |
| P6 | Li & Kang — DL for Wafer Map Defect Detection: A Review | PHM-Hangzhou 2023 | review |
| P7 | Kim & Behdinan — Advances in ML/DL for WMDD: a review | J. Intelligent Manufacturing 2023 | review |

---

## Part 1 — Source of Data (across the 7 papers)

**Headline finding: real fab data is almost always private/confidential; the field runs on a couple of public benchmarks + synthetic data.**

### Public benchmarks (reusable)
- **WM-811K** (Wu et al., TSM 2015) — *the* de-facto benchmark. **811,457** real wafer-bin-maps from 46,393 lots. **9 single-type classes** (Center, Donut, Edge-Loc, Edge-Ring, Loc, Near-full, Scratch, Random, None). **~78–79% are UNLABELED**; of the labeled portion, *None* dominates (~85%) and the rarest defects are <0.02–0.15%. Maps are binary (fail die = 1) and variable-sized → papers resize, commonly to 64×64 (SWaCo) via nearest-neighbor. Used by P3, and cited as the standard by P4–P7. Mirrored on Kaggle / MIR-Lab.
- **Mixed-WM38** (Wang et al., 2020) — **38,015** maps, **38 classes** = 8 single + 29 mixed (2/3/4 co-occurring) + 1 normal, at **52×52**. The go-to benchmark for *mixed-type* defects (P7). Public on Kaggle.
- **Pleschberger et al. 2019** simulated analog wafer-test set — on **Zenodo** (doi 10.5281/zenodo.2542504). 1,000 maps, 5 patterns + Gaussian noise, ~17,000 dies each with (x,y) + electrical test result. A ready-made *synthetic* set (noted by P7).

### Private/in-house data
- P1/P2: Intel fab wafers (P1: 1,191 real wafers, 9 of 22 classes present; P2: 1,191 wafers, used only for evaluation). Confidential — only per-class % reported, sometimes from as few as 3 wafers.
- P4: in-house MBWBM (465 wafers: 265 with GFA / 200 without) from chip-probe test; per-die GFA masks hand-labeled by engineers.

### Data-usage patterns to copy
- **Train-on-synthetic → test-on-real** (P1, P2, and P4's segmentation stage): when real data is scarce/confidential, train the data-hungry model on synthetic and reserve scarce real data for evaluation (and lighter heads). This is the credibility trick for "no real fab data" projects.
- **Leverage the huge unlabeled portion** of WM-811K via self-/semi-supervised pretraining (P3).
- P4 **released** its synthesized MBWBM dataset on **IEEE DataPort** — a model for making a course project citable.

### Field-wide data problems (named repeatedly by the reviews)
Severe **class imbalance**; **scarce + expensive + noisy labels** (manual, error-prone); **restricted access** to current real data; public benchmarks **"likely outdated"** vs current node sizes; almost **no real-environment, expert-verified validation**; poor reproducibility (most papers release no code/data).

---

## Part 2 — Synthetic Data Generation Strategies (across the 7 papers)

Six families appear. Ordered roughly by how reusable/important they are for the project.

### (1) Parametric statistical point-process — the cheap, reproducible baseline (P1, P2)
- **Recipe (Nakazawa):** model background random defects as a **homogeneous Poisson point process** P(k,λ)=λ^k e^(−λ)/k!; generate points in polar coordinates; **superimpose structured points** (rings, edge bands, scratches, quadrant clusters) by tuning the interval of the uniform distribution that places them; then **bin points into dies and normalize by the max die count** → a **density map** (P1) or a **binary map** (P2).
- **Labels are free / by-construction** (the generated pattern IS the label) and the set is **perfectly class-balanced** (e.g., 1,300/class × 22 classes).
- **Anomaly variant (P2):** train an encoder–decoder on **input(noisy map)/target(clean cluster-only map)** pairs — pixel-wise ground truth comes free from the generator. Detects **unseen** patterns.
- Realism is **geometric/statistical**, *not* defect-physics — flagged as a limitation. This is the obvious thing to *upgrade*.

### (2) GAN-based generation (P4, P5, P7)
- **AdaBalGAN** (Adaptive Balancing GAN) — conditional categorical GAN + an **adaptive controller** that allocates *more* synthetic maps to minority classes based on the per-class accuracy gap → produces a balanced synthetic set. The best-documented GAN recipe; directly reusable design.
- **pix2pix cGAN (P4)** — image-to-image translation: trained on real (binary WBM ↔ 20-bin MBWBM) pairs so the generator learns the empirical **bin↔spatial coupling**; then translate WM-811K binary maps into realistic multi-bin maps. Multi-GFA wafers built by **superimposing** two single-GFA maps (keep smaller bin on overlap).
- Also: FAC-GAN, MGGAN (anti mode-collapse), WaferCaps+DCGAN, JFAL (semi-supervised GAN + transfer).

### (3) Autoencoder / VAE generation & oversampling (P5, P6, P7)
- CAE class-oversampling, VAEDLM, **SS-CDGMM** (conditional VAE generating *labeled* maps via per-class latent variables). Labels assigned via the conditioning variable.

### (4) Compositional / superposition for MULTI-defect maps (P4, P5, P7)
- Segment/extract single-pattern templates (seed-filling / U-Net) then **superimpose** them to manufacture mixed-label maps, because real multi-defect wafers are scarce. The field-standard way to build mixed-type training data. Most studies cap at **2** co-occurring defects (called unrealistic).

### (5) Classical augmentation — with a critical single-channel caveat (P3, P5, P7)
- Rotation / flip / translation / shear / zoom. **SWaCo's key lesson:** for single-channel WBMs, **AVOID Cutout, aggressive cropping, color jitter, greyscale** — they can flip one defect class into another (e.g., removing a Center blob makes it "None"). Best policy found: **rotation + (translation+shear)**.

### (6) Diffusion models — ABSENT (the opportunity)
- **None** of the 7 papers use diffusion; the reviews predate its wafer adoption. Our broader survey found **ACDDPM-ResNet (Computers & Industrial Engineering 2024)** as an early diffusion-on-wafer-bitmap work. A modern, physically-conditioned generative model is an open, publishable angle.

---

## Part 3 — Insights for THIS course project

1. **Don't do "another WM-811K classifier."** P5/P6/P7 show the WBM-classification space is saturated; P1–P4 already hit 98–99% on single-type. DATE-T will reject incremental classifier gains. **Novelty must come from a new modality, a released benchmark/generator, a new problem framing (open-set / multi-defect / realism), or a transfer study.**
2. **The synthetic-data engine is the real intellectual asset.** Every strong paper here lives or dies by its data generator. A clean, *physically-motivated*, *released* generator (closing the field-named realism gap) is itself a contribution and de-risks the "no real data" problem the course explicitly permits.
3. **Reusable baselines are well-defined** — implement these as the "AI baseline" tier so the delta is provable: Nakazawa Poisson-process generator + small CNN (P1); SegNet/U-Net encoder–decoder anomaly seg (P2, SegNet≥U-Net≫FCN); MoCo-style self-supervised contrastive for low-label regime (P3); 3D-conv-over-bin-axis + segment-then-classify for multi-bin (P4, 3D ≫ 2D).
4. **Imbalance + scarce labels are the recurring pain** — frame the contribution around them (self/semi-supervision, conditional generation that auto-balances, cost-sensitive losses which P5 notes are under-explored).
5. **Validate on real, release the artifact.** Reviews criticize synthetic-only validation on tiny real sets and poor reproducibility. Even a modest real or held-out validation + a public code/dataset release materially strengthens a DATE submission.
6. **Mixed-type and open-set are the named growth areas.** Single-type is solved; co-occurring defects (>2) and *unknown/novel* patterns are not.

> **Pivot thesis for DATE:** take the *mature* wafer-map toolkit (Poisson/GAN/diffusion generators, encoder–decoder anomaly seg, contrastive low-label learning, 3D-conv-over-bin) and **re-target it to a modality with no public benchmark — memory-array / TSV / chiplet-interconnect failure bitmaps** — releasing the generator + dataset + baselines. This is novel, on-scope for the course (synthetic/fault-injection allowed), and squarely DATE Track-T.

---

## Part 4 — Proposed DATE 2027 Directions

These came from a design workflow: 5 proposals from distinct strategic angles, each scored by 3 adversarial reviewer lenses (novelty-skeptic, DATE-PC reviewer, feasibility-engineer). **All 5 independently converged on the _memory failure-bitmap_ modality** — strong evidence the pivot away from saturated wafer maps is the right move, and that memory bitmaps are the highest-value open target.

> Ranked (avg reviewer score /5): **RepairNet-Bench 3.67** > MemBitBench 3.33 ≈ OpenBitOS 3.33 > PhysBitGen 3.0 ≈ WaferToMem 3.0.

### ★ Recommended: "Learn-the-heuristic, verify-the-answer" BIRA on memory fail-bitmaps (RepairNet-Bench)

**One-liner.** The on-chip MBIST **failure bitmap** is the input to a tiny CNN that (a) predicts **repairability** early (while the bitmap is still streaming, to cut test time) and (b) proposes a **spare row/column allocation** that a cheap deterministic verifier confirms — benchmarked against classical Built-In Redundancy Analysis (BIRA) on a **released, physically-motivated synthetic bitmap generator**.

**Why it's the strongest.**
- **Genuinely different from the 7 papers.** They all do wafer-map *classification/segmentation* ("name the visual defect class"). This is *combinatorial repair decision-making* (spare allocation is NP-complete; Kuo & Fuchs 1987) on a *memory* bitmap — a different modality, a different task, and a non-ML baseline (classical BIRA) that is genuinely competitive and even optimal, so the AI delta is **provable**, not CNN-vs-CNN.
- **DATE Track-T currency.** Speaks directly to **yield** (false-unrepairable scrap) and **test time** (early abort). The released generator + exact-solver labeler is adoptable community infrastructure (the "WM-811K-for-memory-repair" that doesn't yet exist).
- **Honest AI story.** A deterministic verifier means the ML can never return an invalid repair — "AI as a verified accelerator," exactly the insight the course wants (why AI helps + where its authority must stop).
- **Feasible.** B&B labeler is tractable for spare counts ≤8; model is tiny; runs on a single GPU or even CPU.

**Mandatory refinements (from the reviewers — fold these in from week 1):**
1. **Baseline must be PETRA, not Repair-Most.** Classical early-termination RA already exists: **PETRA** (Powerful Early Termination-based RA, IEEE TCAD 2024) and GPU-parallel **GRAP** (TCAD 2024). If you only beat greedy RM/ESP, a reviewer will say "your real baseline is PETRA." Adopt PETRA + one optimal/parallel RA as the **primary** comparators and frame the claim as a **Pareto statement**: *the learned predictor reaches X% of optimal repair rate at fewer analysis cycles than PETRA, and triggers correct early-scrap/early-accept k% earlier on the streaming partial bitmap, with a verifier guaranteeing zero false repairs.*
2. **Upgrade the allocation head from one-shot top-k to a learned-ordering bounded verified search.** The CNN emits a *ranked* candidate list; a small bounded B&B explores the top-N until it finds a valid cover or hits a step budget. This makes "matches optimal repair rate at X-fold fewer steps" a *provable* property and yields the analysis-steps-vs-repair-rate **Pareto curve** the PC wants.
3. **Build a real March-test reveal model** for the early-termination claim. Tag each injected fault with the earliest March element/address at which it becomes observable (stuck-at immediately; transition/coupling only after the relevant up/down pass); define the k% partial bitmap as faults observable by k% of the address sweep. Don't fake it as "randomly reveal k% of final fails" — that's the result a PC will scrutinize hardest. (~1.5–2 days.)
4. **Split early-decision into verifiable early-ACCEPT vs early-SCRAP.** Early-accept is safe (allocation+verify still runs). Early-scrap is *unverifiable* (you stopped testing), so report it as a **calibrated false-scrap-rate vs test-time-saved tradeoff curve**, not a hard abort under the "provably correct" umbrella.
5. **Distinguish from RARecommender (IEEE 2022).** That work only *recommends which RA algorithm to run* from wafer-level features (~33.6% acc); you operate on the **raw streaming bitmap**, emit a **verified allocation**, and add the **early-termination** test-time lever.

**Synthetic generator (the load-bearing artifact).** Negative-binomial / compound-Poisson **clustered** fault process (the standard clustered-defect yield model) + classical memory fault primitives (single-bit SAF/TF, full/partial **row** = word-line fault, full/partial **column** = bit-line fault, 2D **cluster**, **address-decoder** coupling = paired identical lines) superimposed (OR) on an R×C grid + isolated bit-flip noise p_noise. Label by construction **plus** the exact B&B solver → `(bitmap, is_repairable, optimal_spare_set, min_spares)`. **Measure realism** (faulty-line-count and cluster-size distributions; Poisson-vs-clustered ablation) rather than asserting it — and state plainly that no public real memory bitmap exists (that's the motivation). Include a **"hard" split** with faulty lines near (SR+SC), where greedy provably fails and the delta is visible.

**4-week deliverable (course demo, Jun 11):** generator + RM/ESP/PETRA/B&B baselines + tiny CNN with verifier + comparison plots + interactive demo (inject faults → see RM vs AI allocation + early verdict).
**3-month upgrade to DATE (Jun→Sept):** hardware-cost credibility (area/latency vs CRESTA sub-analyzer count); conditional **diffusion** generator for realism (diffusion is absent from memory bitmaps); open-set novel-fault detector; cross-modality transfer to TSV/chiplet bitmaps; robustness sweeps.

### Alternative A — MemBitBench (benchmark-first, score 3.33)
Release the **first public physics-motivated generator + reference dataset + baselines** for embedded-memory fail bitmaps, dual-labeled with a **March-test fault taxonomy** (SAF/TF/CF/AF/DRF) *and* a BIRA-derived **repairability** label. Method = segment-then-classify U-Net/SegNet (reusing P2/P4 findings) + repairability head. **Reviewer caution:** a "we release a benchmark" paper lives or dies on data credibility — don't claim *measured fidelity vs published stats* (the stats barely exist); instead ship a **datasheet** mapping each fault primitive to a standard functional fault model with explicit provenance, and call realism "physically-motivated, parameter-documented, bounded." Good fallback if you'd rather lead with infrastructure than with the repair method.

### Alternative B — OpenBitOS (open-set novelty, score 3.33)
**Excursion monitoring**: flag *never-before-seen* memory fail-bitmap signatures with a reject option instead of force-classifying. Method = self-supervised contrastive embedding (SWaCo/MoCo lineage, single-channel-safe augmentations) + density-based reject. **Reviewer caution:** open-set is *not* untouched — the wafer literature has it (Frittoli PR 2022; WigDM 2024; several Elsevier 2024 works). Don't claim "never covered"; claim "**ported to the memory-bitmap modality**, with a released open-set benchmark." Pick **one** primary scorer and ablate the rest. Naturally combines with the recommended direction as the "3-month open-set upgrade."

### How to choose
- Want the **sharpest provable delta + a real test-cost story** → **RepairNet-Bench** (recommended).
- Want a **lower-risk infrastructure contribution** the community cites → **MemBitBench**.
- Excited by **anomaly/novelty** and excursion monitoring → **OpenBitOS**.
All three share ~80% of the codebase (the same generator + taxonomy), so you can build the generator once and pivot the framing late. **Strongest single paper = RepairNet-Bench core + MemBitBench's released benchmark + OpenBitOS as the open-set upgrade.**

---

## Part 5 — Additional Reading (fresh, beyond the 7 downloaded)

Prioritized. Items marked ★ are the must-reads for the recommended direction.

### Prior art you MUST cite/beat for the BIRA direction (reviewer-surfaced)
- ★ **PETRA — Powerful Early Termination-based Redundancy Analysis**, IEEE TCAD 2024 (doc 10587206). Classical early-repairability verdict + fast allocation, **no ML** — this is your primary baseline; your ML must beat *it*.
- ★ **GRAP — GPU-parallel Redundancy Analysis**, IEEE TCAD 2024. Parallel optimal-rate RA; the "just parallelize exact RA" rebuttal.
- ★ **RARecommender** (IEEE doc 9691578, 2022). ML that *selects which RA algorithm to run* — the closest ML-for-BIRA prior art; differentiate raw-bitmap input + verified allocation + early-termination.
- Foundational: **Kuo & Fuchs 1987** (spare allocation NP-completeness); **CRESTA**, **Essential-Spare-Pivoting (ESP)**, **Repair-Most** — the classical BIRA ladder.

### Memory fail-bitmap + ML
- ★ **DRAM Fault Classification through Large-Scale Field Monitoring for Robust Memory RAS** — MICRO 2025. Freshest high-venue memory-bitmap-ML anchor.
- **Exploring Error Bits for Memory Failure Prediction** — arXiv:2312.02855 (2023/24). Spatio-temporal error-bit features, real DRAM, +15% F1.
- **Deep Q-Learning BIST/BISR for SRAM** — Sensors/PMC 2022 (open access). RL-driven MBIST+BISR; ML-for-memory-repair reference.
- **Improving DRAM Fault Characterization through ML** (DSN-W 2016) + **Automating DRAM Fault Mitigation by Learning from Experience** (DSN 2017). Foundational ML-on-DRAM-bitmaps.
- **A Hybrid Flow for Memory Failure Bitmap Classification** (IEEE doc 6394222). Rule+ANN (SOM) on embedded-memory fail bitmaps — classic, on-point.
- HBM lead: **A Fail-Slow Detection Framework for HBM Devices** — ACM SC-W 2024 (fail-slow, not bitmap; HBM-bitmap+ML is an open gap).

### Diffusion / modern generative for defect maps (the realism upgrade)
- ★ **ACDDPM-ResNet** — Computers & Industrial Engineering 2024. Auxiliary-classifier DDPM for minority-class wafer maps (WM-811K/MixedWM38). The diffusion baseline to adapt to memory bitmaps.
- ★ **WigDM — Input-guidance diffusion for unknown-defect detection** — Adv. Eng. Informatics 2024. Bridges generation + open-set; the natural successor to ACDDPM to cite/beat.
- **Multi-scale guidance diffusion network for wafer map defect recognition** — ESWA 2024.
- **Generative approach (patch DDPM) for SEM defect images** — arXiv:2407.10348 (2024).
- Code: HuggingFace `diffusers` / lucidrains `denoising-diffusion-pytorch` adapt trivially.

### Open-set / novelty / OOD (the excursion-monitoring upgrade)
- ★ **Deep Open-Set Recognition for Silicon Wafer Production Monitoring** — Frittoli/Boracchi, Pattern Recognition 2022 / arXiv:2208.14071. Canonical open-set-for-wafers; PoliMi group often releases code.
- **Enhanced detection of unknown WBM patterns via open-set recognition (EEOC-SVM)** — C&IE 2024.
- **Framework for detecting unknown WBM patterns using active learning** — ESWA 2024.
- **Wafer defect classification with OOD detection** — Microelectronics Reliability 2021.

### TSV / 3D-IC and chiplet (the cross-modal-transfer upgrade)
- **E2E CNN for failure localisation + characterisation of 3D interconnects** — Nature Sci. Reports 2023 (open access, dataset described). >98% classify, ~100% localize.
- **Machine-Learning Approach for Defects in TSV-Based 3-D IC** (HMC-LDNN) — foundational ML-for-TSV (also in our cross-direction A-list).
- ★ **Defect Analysis and BIST for Chiplet Interconnects in FOWLP** — Chakrabarty et al., VTS 2025 / arXiv:2503.14784. Closest chiplet-test work, **uses no ML on the bitmap** → ML-on-chiplet-bitmap is a genuine open gap, same VTS/DATE community as your target.
- **Test and Diagnosis Strategies for Inter-Chiplet Interconnects** — IEEE 2025. NN-based test-grouping + DWR BIST.

### Datasets to grab now
- **WM-811K** (Kaggle / MIR-WM811K) and **MixedWM38** (Kaggle) — the shared public anchors every reviewer expects; use for related-work grounding and the wafer→memory transfer experiment.
- **Pleschberger 2019** simulated wafer-test set — Zenodo doi 10.5281/zenodo.2542504 (spatial-prior sanity stressor only; it's device-map, not cell-level — a weak OOD set, use with that caveat).

### Verify-before-citing
A couple of search hits were USPTO patents (skip) and one Frontiers item dated 2026 (felec.2026.1750707) is likely early-access — confirm the year.
