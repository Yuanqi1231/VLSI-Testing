# Direction 4: AI-assisted Test Optimization — Literature Survey

This survey covers 2021–2026 publications across IEEE/ACM/Springer/Elsevier venues (ITC, VTS, DATE, DAC, ICCAD, ETS, ATS, MLCAD, GLSVLSI, TCAD, TVLSI, TODAES, JETTA, MicEle). Papers are tiered by relevance to the project goal: applying AI/ML to optimize the IC test process itself (scheduling, pattern selection/compaction, adaptive test, power-aware test, outlier detection, 3D-IC/chiplet TAM, reliability-aware test).

---

## Tier 1: Must-Read Papers (Highest Relevance)

### 1. SmartATPG: Learning-based Automatic Test Pattern Generation with Graph Convolutional Network and Reinforcement Learning
- **Authors**: Junhua Huang, Yu Huang, et al.
- **Venue**: 61st ACM/IEEE Design Automation Conference (DAC), 2024
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3649329.3656526
- **Abstract**: Proposes a learning-based ATPG framework that uses Graph Convolutional Networks (GCN) to extract circuit-feature embeddings and uses Reinforcement Learning (RL) to explore the ATPG search space efficiently. The agent learns decisions that drastically reduce backtracking compared with traditional PODEM/FAN, while outperforming ANN-based heuristics on benchmark circuits.
- **Why relevant**: Flagship modern DAC paper combining GNN + RL for ATPG — the canonical reference for AI-assisted test pattern generation.
- **Recommended for download**: YES

### 2. Deep Reinforcement Learning-Based Automatic Test Pattern Generation
- **Authors**: (IEEE authors team)
- **Venue**: IEEE Conference (Document 10531908), 2024
- **DOI/Link**: https://ieeexplore.ieee.org/document/10531908/
- **Abstract**: Applies Deep Q-Network (DQN) to the PODEM ATPG algorithm with a custom reward function. The DRL agent learns an optimal backtracing policy through circuit interaction, achieving runtime reductions up to 50% on benchmarks while maintaining high fault coverage.
- **Why relevant**: Direct demonstration of DRL replacing classical heuristics in PODEM — strong baseline for any RL-in-test paper.
- **Recommended for download**: YES

### 3. DETECTive: Machine Learning-driven Automatic Test Pattern Prediction for Faults in Digital Circuits
- **Authors**: Petrolo, Medya, et al.
- **Venue**: Great Lakes Symposium on VLSI (GLSVLSI), 2024
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3649476.3658696
- **Abstract**: Introduces "Automatic Test Pattern Prediction" (ATPP) — the first fully ML-based ATPG that uses graph deep learning to predict test patterns instead of generating them. Trained on small circuits, it generalizes to circuits 29× larger and is up to 15× faster than academic and 2× faster than commercial ATPG tools.
- **Why relevant**: Pioneers a backtrack-free paradigm; highly novel and a strong target for benchmarking new ATPG-prediction methods.
- **Recommended for download**: YES

### 4. DeepTPI: Test Point Insertion with Deep Reinforcement Learning
- **Authors**: Z. Shi, H. Pei, et al.
- **Venue**: ICCAD 2022 / IEEE TCAD (ext. 2023)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9983950/ ; arXiv: 2206.06975
- **Abstract**: A DRL-based framework for test point insertion (TPI). Combines a Graph Neural Network with Deep Q-Learning to maximize test coverage improvement. Leverages a pre-trained DeepGate model for node embeddings and proposes a dedicated testability-aware attention mechanism.
- **Why relevant**: Foundational reference for RL applied to a classical DfT problem. Public code at github.com/cure-lab/DeepTPI.
- **Recommended for download**: YES

### 5. Reinforcement-Learning-Based Test Point Insertion for Power-Safe Testing in Monolithic 3-D ICs
- **Authors**: Shao-Chun Hung, Arjun Chaudhuri, Krishnendu Chakrabarty
- **Venue**: IEEE Transactions on Computer-Aided Design (TCAD), Vol. 44, Issue 11, pp. 4419-4432, 2025 (extended from VTS 2023)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10972002/ ; VTS: https://ieeexplore.ieee.org/document/10174135/
- **Abstract**: Monolithic 3D ICs face severe power-supply noise (PSN) during at-speed delay testing. An RL framework inserts test points and generates low-switching patterns that mitigate PSN-induced voltage droop without degrading test coverage. Demonstrates power-safe testing for advanced packaging.
- **Why relevant**: Combines three project foci — 3D-IC, power-aware test, and RL — by a leading test-research group (Chakrabarty).
- **Recommended for download**: YES

### 6. Scan Cell Segmentation Based on Reinforcement Learning for Power-Safe Testing of Monolithic 3D ICs
- **Authors**: Shao-Chun Hung, Arjun Chaudhuri, Sanmitra Banerjee, Krishnendu Chakrabarty
- **Venue**: ITC 2023
- **DOI/Link**: https://ieeexplore.ieee.org/document/10351068/
- **Abstract**: Uses RL to segment scan cells in M3D ICs to minimize switching activity without adverse impact on test coverage. Benchmark M3D designs validate the framework.
- **Why relevant**: Companion to paper #5; demonstrates a second RL formulation for 3D-IC power-safe test. Direct ITC venue.
- **Recommended for download**: YES

### 7. Machine Learning-Based Adaptive Outlier Detection for Underkill Reduction in Analog/RF IC Testing
- **Authors**: A. Niranjan, S. Neethirajan, et al. (Texas Instruments + academic)
- **Venue**: IEEE VLSI Test Symposium (VTS), 2023
- **DOI/Link**: https://ieeexplore.ieee.org/document/10140005/
- **Abstract**: Proposes an adaptive outlier detection method that dynamically computes outlier boundaries based on per-wafer performance distributions, updated as new customer-return ICs are observed. Evaluated on an industrial Texas Instruments dataset, the method significantly reduces "underkill" (defective ICs that escape testing).
- **Why relevant**: Premier example of adaptive, ML-based outlier detection in analog/RF test; strong industrial benchmark.
- **Recommended for download**: YES

### 8. (Invited) Redefining Outliers for On-Wafer Electrical Testing
- **Authors**: (Invited MLCAD authors)
- **Venue**: ACM/IEEE Int'l Symp. on Machine Learning for CAD (MLCAD), 2024
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3670474.3689186
- **Abstract**: Invited paper that re-examines wafer-level outlier-detection methodology. Uses Gaussian Process Regression (GPR) for electrical test outlier detection and demonstrates that even simple GPR outperforms DPAT for detecting spatially-anomalous die.
- **Why relevant**: Definitive recent survey of the GP/ML outlier-detection landscape; cites and contextualizes all PAT/GDBN work.
- **Recommended for download**: YES

### 9. Improving Efficiency and Robustness of Gaussian Process-Based Outlier Detection via Ensemble Learning
- **Authors**: (IEEE authors, 2023)
- **Venue**: IEEE Conference, 2023
- **DOI/Link**: https://ieeexplore.ieee.org/document/10351109/
- **Abstract**: Applies ensemble learning to Gaussian Process regression for IC outlier detection. On industrial production-test data, improves latent-fault detection robustness by 15.6% while cutting computation time by 98.6% versus conventional GP-based methods.
- **Why relevant**: Critical efficiency improvement that makes GP outlier detection production-ready.
- **Recommended for download**: YES

### 10. CNN-Based Stochastic Regression for IDDQ Outlier Identification
- **Authors**: Y. Yamato, et al.
- **Venue**: IEEE Transactions on Computer-Aided Design (TCAD), Vol. 42, 2023
- **DOI/Link**: https://ieeexplore.ieee.org/document/10059120/
- **Abstract**: A CNN-based stochastic regression model predicts IDDQ value mean and standard deviation for each DUT, enabling detection of defective parts missed by simple 6σ rules. Improves DPPM reduction beyond conventional IDDQ paradigms.
- **Why relevant**: Showcases deep learning replacing rule-based IDDQ outlier methods at TCAD-level rigor.
- **Recommended for download**: YES

### 11. Frequency-scaled Thermal-aware Test Scheduling for 3D ICs Using Machine Learning-based Temperature Estimation
- **Authors**: (Elsevier authors)
- **Venue**: Microelectronics Journal (Elsevier), 2022
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0026269222001653
- **Abstract**: Heuristic, session-based 3D-IC test scheduler that uses an ML-based predictive thermal model in place of an expensive simulator. Co-optimizes frequency scaling, thermal awareness, and test time for stacked 3D ICs.
- **Why relevant**: First clear demonstration that ML surrogates can drive thermal-aware 3D-IC test scheduling — central topic for our project.
- **Recommended for download**: YES

### 12. ML-Assisted IC Test Binning with Real-Time Prediction at the Edge
- **Authors**: (IEEE authors)
- **Venue**: IEEE Conference, 2023
- **DOI/Link**: https://ieeexplore.ieee.org/document/10102972/
- **Abstract**: An edge-deployed ML model performs real-time binning of fail parts during testing. Achieves 20–40× improvement over conventional statistical screening; cost-aware model tunes for maximum failure capture with minimal overkill.
- **Why relevant**: Edge ML inference inside the test cell — operational, deployable adaptive test architecture.
- **Recommended for download**: YES

### 13. Deep Learning-Based Performance Testing for Analog Integrated Circuits
- **Authors**: (IEEE TVLSI authors)
- **Venue**: IEEE Transactions on VLSI Systems (TVLSI), 2024
- **DOI/Link**: https://dl.acm.org/doi/10.1109/TVLSI.2024.3496777 ; arXiv: 2406.00516
- **Abstract**: A DNN-based framework maps responses of analog circuit-under-test modules to specifications. Test modules are selected by a 0-1 integer program, and a DNN aggregates predictions to estimate specs. Minimizes required test modules while guaranteeing accuracy.
- **Why relevant**: Quintessential test-time/cost reduction via DL for analog ICs — strong adaptive-test reference.
- **Recommended for download**: YES

### 14. A Survey and Recent Advances: Machine Intelligence in Electronic Testing
- **Authors**: (Springer JETTA authors)
- **Venue**: Journal of Electronic Testing (JETTA), 2024
- **DOI/Link**: https://link.springer.com/article/10.1007/s10836-024-06117-7
- **Abstract**: Comprehensive survey of ML/AI applications in electronic testing, including ATPG, fault diagnosis, adaptive test, outlier detection, and test optimization. Highlights recent advances in ANN, PCA, GNN-based techniques.
- **Why relevant**: Essential survey to cite for related-work positioning.
- **Recommended for download**: YES

### 15. A Novel Approach to Reducing Testing Costs and Minimizing Defect Escapes Using Dynamic Neighborhood Range and Shapley Values
- **Authors**: (ACM TODAES authors)
- **Venue**: ACM Transactions on Design Automation of Electronic Systems (TODAES), 2025
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3716826
- **Abstract**: For wafer acceptance test (WAT), proposes a dynamic-neighborhood method that retains outliers and uses Shapley values to weight feature importance in a multi-objective cost-vs-escape formulation. Reduces test cost while minimizing defective dice that escape detection.
- **Why relevant**: Combines explainable ML (Shapley) with test cost optimization — a publishable methodological angle to extend.
- **Recommended for download**: YES

---

## Tier 2: Important Papers

### 16. InF-ATPG: Intelligent FFR-Driven ATPG with Advanced Circuit Representation Guided Reinforcement Learning
- **Authors**: (arXiv preprint, 2025)
- **Venue**: arXiv 2512.00079
- **DOI/Link**: https://arxiv.org/abs/2512.00079
- **Abstract**: Partitions circuits into fanout-free regions (FFRs); a novel QGNN circuit-representation guides an RL agent. Reduces backtracks by 55.06% (vs. traditional) and 38.31% (vs. ML baselines) while improving fault coverage.
- **Why relevant**: Strongest recent RL ATPG numbers; extends SmartATPG with circuit-aware features.

### 17. FPGNN-ATPG: An Efficient Fault Parallel Automatic Test Pattern Generator
- **Authors**: (GLSVLSI 2023 authors)
- **Venue**: Great Lakes Symposium on VLSI (GLSVLSI), 2023
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3583781.3590250
- **Abstract**: Combines GNN-based fault classification with a fault-driven deterministic ATPG; on 10 industrial benchmarks achieves 7.56× average speedup, 14.13% smaller pattern count, and 100% fault coverage.
- **Why relevant**: Concrete pattern-count reduction via GNN classification.

### 18. Conflict-driven Structural Learning Towards Higher Coverage Rate in ATPG
- **Authors**: (arXiv 2303.02290, 2023)
- **Venue**: arXiv 2303.02290
- **DOI/Link**: https://arxiv.org/pdf/2303.02290
- **Abstract**: SAT-style ATPG augmented with structural conflict-driven learning to improve coverage on hard-to-detect faults.
- **Why relevant**: Bridges SAT-based ATPG and ML learning for coverage improvement.

### 19. Observation Point Insertion Using Deep Learning
- **Authors**: (ICCAD authors)
- **Venue**: 41st IEEE/ACM ICCAD, 2022
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3508352.3561122
- **Abstract**: GCN-based prediction of signal probabilities and optimal observation-point locations for test-pattern count reduction. Uses gate-type, logic, SCOAP, and reconvergent-fanout features.
- **Why relevant**: Complementary to DeepTPI; a different DfT objective.

### 20. Machine Learning-Based DFT Recommendation System for ATPG QoR
- **Authors**: Zorian, Shanyour, et al. (Synopsys + academia)
- **Venue**: IEEE Conference / Patent extension
- **DOI/Link**: https://www.semanticscholar.org/paper/a7bc3533ab14af0431c686f2c356abc05d6751be
- **Abstract**: Trained ML model predicts optimal DfT configurations (scan-chain port counts, chain length) from IC design features (flip-flops, clock domains, faults, primitive gates, coverage). Recommends scan architectures to improve ATPG quality.
- **Why relevant**: An entire design-flow ML recommendation system.

### 21. Wafer-level Adaptive Testing Based on Dual-Predictor Collaborative Decision
- **Authors**: Yuqi Pan, Huaguo Liang, Junming Li, et al.
- **Venue**: Journal of Electronic Testing (JETTA), Vol. 40, Issue 3, pp. 405-415, 2024
- **DOI/Link**: https://www.eng.auburn.edu/~vagrawal/JETTA/FULL_ISSUE_40-3/P07_40-3_Pan_p405-415.pdf
- **Abstract**: Uses two quality predictors (trained from a subset of test items + spatial information) for a per-die test-skip decision. Cuts >42% of test items and reduces test escape and yield loss by >90% in circuit-probing (CP) test.
- **Why relevant**: Direct wafer-level adaptive-test contribution; clean evaluation numbers.

### 22. Low Test Cost Adaptive Testing Method for High-Yield IC Products
- **Authors**: (Elsevier authors)
- **Venue**: Microelectronics Journal / Elsevier, 2025
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0167926025000586
- **Abstract**: Ensemble-learning adaptive test for high-yield products. Reduces test cost by 34% while achieving >99% accuracy in identifying failed chips; handles imbalanced test data via undersampling and filtering.
- **Why relevant**: Modern adaptive test directly addressing AI/HPC volume production challenges.

### 23. RLDA: Valid Test Pattern Identification by Machine Learning Classification Method for VLSI Test
- **Authors**: (Microelectronics Journal authors)
- **Venue**: Microelectronics Journal, 2022
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0026269222001793
- **Abstract**: Regularized Linear Discriminant Analysis (RLDA) classifies test patterns into "valid" (failing) and "invalid" (passing), allowing invalid patterns to be dropped. Achieves 1.75× test-time savings vs. traditional methods.
- **Why relevant**: Foundational ML test-pattern-selection paper.

### 24. VLSI Test through an Improved LDA Classification Algorithm for Test Cost Reduction
- **Authors**: (Microelectronics Journal authors)
- **Venue**: Microelectronics Journal, 2022
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0026269222000969
- **Abstract**: Extends RLDA with refinements for VLSI test cost reduction.
- **Why relevant**: Companion of #23; shows LDA effectiveness for test reduction.

### 25. Machine Learning Classification Algorithm for VLSI Test Cost Reduction
- **Authors**: (Microelectronics authors)
- **Venue**: Microelectronics Journal / Elsevier, 2022
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0167926022000724
- **Abstract**: KNN-based ML classification to drop invalid patterns. Achieves 1.75× test-time reduction.
- **Why relevant**: Alternative classifier to RLDA — useful baseline.

### 26. Deep Learning-assisted Scan Chain Diagnosis with Different Fault Models during Manufacturing Test
- **Authors**: (IEEE 2022 authors)
- **Venue**: IEEE Conference, 2022
- **DOI/Link**: https://ieeexplore.ieee.org/document/9979020/
- **Abstract**: Deep learning predicts probable scan-chain defect locations from compressed responses. Diagnostic success rate 80–100% across multiple fault models.
- **Why relevant**: Diagnosis side of the test optimization story.

### 27. GRAND: A Graph Neural Network Framework for Improved Diagnosis
- **Authors**: (Duke authors / Chakrabarty group)
- **Venue**: IEEE TCAD, 2024 (online Apr 2024)
- **DOI/Link**: https://dl.acm.org/doi/abs/10.1109/TCAD.2023.3336212
- **Abstract**: GNN-based diagnosis distinguishes true faults from false candidates by modeling circuits as graphs. Improves diagnostic resolution 4.51× over fault-simulator-based tools and 5.98× over a state-of-the-art commercial tool.
- **Why relevant**: Highest-quality recent diagnosis-via-GNN reference; influential.

### 28. Semiconductor Final Testing Scheduling Using Q-learning Based Hyper-heuristic
- **Authors**: (Elsevier Expert Systems with Applications authors)
- **Venue**: Expert Systems with Applications, 2022
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0957417421013282
- **Abstract**: Q-learning hyper-heuristic selects low-level heuristics for the flexible-job-shop semiconductor final-test scheduling problem with multi-resource constraints and setup times. Efficient encoding/decoding with left-shift scheme for resource utilization.
- **Why relevant**: Real semiconductor final-test scheduling with RL; transferable framing for SoC scheduling.

### 29. Reinforcement Learning for Test-time Optimization in the Network-on-Chip-Based Systems
- **Authors**: (IEEE Conference authors)
- **Venue**: IEEE Conference (Document 11014406), 2025
- **DOI/Link**: https://ieeexplore.ieee.org/document/11014406/
- **Abstract**: MAPIC framework uses pointer-network architecture (and ChatGPT-generated NoC benchmarks) to generate optimal NoC test schedules by mapping cores to I/O pairs.
- **Why relevant**: Direct RL approach to NoC test scheduling; aligns with our 3D-IC TAM scope.

### 30. Test Accuracy Improvement of Ensemble Gaussian Process-Based IC Outlier Detection Using Temporal Similarity Among Wafers
- **Authors**: (IEEE 2024)
- **Venue**: IEEE Conference (Document 11068929), 2024
- **DOI/Link**: https://ieeexplore.ieee.org/document/11068929
- **Abstract**: Ensemble GP outlier detection leveraging temporal similarity across wafer lots. Reduces test escapes by 6.40% over prior EGPR baselines.
- **Why relevant**: Modern GP outlier extension with clean evaluation.

### 31. Yield Loss Reduction and Test of AI and Deep Learning Accelerators
- **Authors**: (arXiv 2006.04798 / IEEE follow-ups)
- **Venue**: arXiv (cross-listed conferences)
- **DOI/Link**: https://arxiv.org/pdf/2006.04798
- **Abstract**: Correlates circuit faults with target AI workload accuracy. Accelerators sustain 5% PE-array fault-rate with <1% accuracy loss — enabling fault-tolerant binning.
- **Why relevant**: Yield-aware testing tailored for AI accelerator chips; very topical.

### 32. Chiplet-Gym: Optimizing Chiplet-based AI Accelerator Design with Reinforcement Learning
- **Authors**: Mishty, Sadi, et al.
- **Venue**: IEEE Transactions / arXiv 2406.00858, 2024
- **DOI/Link**: https://ieeexplore.ieee.org/iel8/12/4358213/10677458.pdf
- **Abstract**: RL framework (PPO) exploring chiplet resource allocation, placement, and packaging architecture. Optimizer-suggested design achieves 1.52× throughput, 0.27× energy, 0.01× die cost at 1.62× package cost vs. monolithic baseline.
- **Why relevant**: Although design-focused, the RL chiplet-architecture environment is directly portable to test-architecture optimization.

### 33. A Comprehensive Review of Machine Learning Applications in VLSI Testing
- **Authors**: (ResearchGate 2024 review)
- **Venue**: Journal review, 2024
- **DOI/Link**: https://www.researchgate.net/publication/378121990
- **Abstract**: Reviews ML for VLSI testing covering ATPG, BIST, adaptive test, outlier detection, diagnosis, and pattern selection.
- **Why relevant**: Strong related-work survey for paper introduction/background.

### 34. AI/ML for Yield Learning and Test Optimization in Semiconductor Manufacturing: A Review of Adaptive Testing, Smarter Limits, and Diagnostic Preservation
- **Authors**: (Research Square preprint, 2024)
- **Venue**: Research Square preprint / journal pending
- **DOI/Link**: https://www.researchsquare.com/article/rs-9464431/v1
- **Abstract**: Reviews adaptive testing, ML-augmented outlier detection, smart limit-setting, and diagnostic preservation during test-time reduction. Cites industrial ML-adaptive reporting at ~25% test-time reduction; unsupervised methods reduce customer DPPM escapes vs. DPAT/NNR on automotive MCUs.
- **Why relevant**: Excellent industry-perspective review.

### 35. Power-Aware ATPG Methodology for Complex Low-Power Designs (PrimePower-based)
- **Authors**: Abdel-Hafez, Dsouza, et al.
- **Venue**: Various IEEE conferences, 2023
- **DOI/Link**: https://www.semanticscholar.org/paper/8445effca76501fe2e800027994983b3e0a2a84c
- **Abstract**: Power-aware ATPG leveraging PrimePower-based sign-off data; reduces pattern count by 26% and runtime by 19% vs. traditional low-power ATPG.
- **Why relevant**: Baseline for power-aware ATPG that AI methods must beat.

### 36. Test-Point Insertion for Multi-Cycle Power-On Self-Test
- **Authors**: (ACM TODAES 2023 authors)
- **Venue**: ACM TODAES, 2023
- **DOI/Link**: https://dl.acm.org/doi/fullHtml/10.1145/3563552
- **Abstract**: TPI technique for multi-cycle POST that reduces test application time while preserving test quality.
- **Why relevant**: Power-on self-test optimization context — useful for power-aware test discussion.

### 37. Deep Q-Learning with Bit-Swapping LFSR for SRAM Built-In Self-Test and Self-Repair
- **Authors**: (Sensors / PMC 2022 authors)
- **Venue**: Sensors / PMC 9229549, 2022
- **DOI/Link**: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9229549/
- **Abstract**: Deep Q-learning-based MBIST checks SRAM arrays; faults injected via DQL and repaired with bit-swapping LFSR (BISR).
- **Why relevant**: RL applied to memory BIST — adjacent BIST optimization angle.

### 38. Efficient Built-In Self-Test Strategy for Neuromorphic Hardware Based on Alarm Placement
- **Authors**: (IEEE 2025)
- **Venue**: IEEE Conference (Document 10859069), 2025
- **DOI/Link**: https://ieeexplore.ieee.org/document/10859069/
- **Abstract**: Online BIST for SNN neuromorphic hardware; maximizes fault coverage and reduces test time via alarm placement strategy.
- **Why relevant**: Specialized BIST optimization for ML hardware.

### 39. Built-in Self-Test and Built-in Self-Repair Strategies Without Golden Signature for Computing in Memory
- **Authors**: (IEEE 2023)
- **Venue**: IEEE Conference (Document 10137074), 2023
- **DOI/Link**: https://ieeexplore.ieee.org/document/10137074/
- **Abstract**: BIST/BISR for compute-in-memory CNN accelerators that tolerates inherent CIM inaccuracy without a golden signature.
- **Why relevant**: Reliability/test of AI accelerators (CIM) — emerging topic.

### 40. Fine-grained Adaptive Testing Based on Quality Prediction
- **Authors**: (TODAES authors)
- **Venue**: ACM TODAES, 2020 (foundational citation in 2023–2025 work)
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3385261
- **Abstract**: Trains a quality predictor on a subset of chips and uses predictions to dynamically skip tests on remaining chips.
- **Why relevant**: Foundational reference for adaptive-test ML literature.

### 41. Deep Learning-Based Early-Stage IR-Drop Estimation via CNN Surrogate Modeling
- **Authors**: (arXiv 2601.22707, 2024)
- **Venue**: arXiv 2601.22707
- **DOI/Link**: https://arxiv.org/pdf/2601.22707
- **Abstract**: U-Net-based dense pixel-wise regression for early-stage static IR-drop estimation, replacing expensive simulators.
- **Why relevant**: Surrogate for IR-drop matters because test patterns cause peak switching; ties into power-safe testing.

### 42. ICCAD 2023 CAD Contest Problem C: Static IR Drop Estimation Using Machine Learning
- **Authors**: (Invited paper)
- **Venue**: ICCAD 2023
- **DOI/Link**: https://ieeexplore.ieee.org/document/10323767
- **Abstract**: Contest paper providing the framework for ML-based static IR drop estimation; useful benchmark/dataset link for power-aware test research.
- **Why relevant**: Provides ML-IR-drop benchmark useful for power-aware test research.

### 43. Wafer2Spike: Spiking Neural Network for Wafer Map Pattern Classification
- **Authors**: Mishra, Kumar, et al.
- **Venue**: ITC 2024 / arXiv 2411.19422
- **DOI/Link**: https://ieeexplore.ieee.org/document/10766711/
- **Abstract**: Spiking neural network achieves 98% average accuracy on WM-811k wafer-bin-map benchmark, with superior performance on under-represented defect classes and high computational efficiency.
- **Why relevant**: Wafer-map classification is part of the wafer-level adaptive-test pipeline; ITC 2024 venue is directly in scope.

### 44. Unsupervised Learning Provides Intelligence for Testing Hard-to-Detect Faults
- **Authors**: Soham Roy, Vishwani Agrawal
- **Venue**: ITC 2024 (AI Track Session A1)
- **DOI/Link**: ITC 2024 proceedings (Index in https://www.proceedings.com/content/077/077497webtoc.pdf)
- **Abstract**: Unsupervised ML method targeting hard-to-detect faults for which ATPG often struggles.
- **Why relevant**: Direct ITC 2024 paper on ML for ATPG/test; cite as state-of-the-art.

### 45. Identifying Undetectable Defects Using Equivalence Checking
- **Authors**: Lars Hedrich, et al.
- **Venue**: ITC 2024 (AI Track Session A1)
- **DOI/Link**: ITC 2024 proceedings
- **Abstract**: Equivalence-checking framework to identify undetectable defects, complementary to ML-based ATPG.
- **Why relevant**: Reduces wasted effort on undetectable faults — directly relevant to test optimization.

---

## Tier 3: Supplementary Papers (Context, Foundations, Surveys)

### 46. Test Scheduling Using Ant Colony Optimization for 3D Integrated Circuits
- **Venue**: IEEE (Document 6863973)
- **DOI/Link**: https://ieeexplore.ieee.org/document/6863973/
- **Why relevant**: Foundational metaheuristic 3D-IC scheduler that AI/RL papers compare against.

### 47. An Efficient Test Scheduling to Co-Optimize Test Time and Peak Power for 3D ICs
- **Venue**: IEEE 2020 (Document 9263015)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9263015
- **Why relevant**: Co-optimization formulation directly applicable to RL reward design.

### 48. 3D IC Test Scheduling Using Simulated Annealing
- **Venue**: IEEE (Document 6212659)
- **DOI/Link**: https://ieeexplore.ieee.org/document/6212659/
- **Why relevant**: Standard SA baseline for 3D-IC scheduling experiments.

### 49. A Genetic Algorithm-Based Metaheuristic Approach for Test Cost Optimization of 3D SIC
- **Venue**: IEEE 2021 (Document 9628009)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9628009/
- **Why relevant**: Modern GA for 3D-SIC test cost optimization.

### 50. Thermal-Aware Test Scheduling with Floorplanning for Three-Dimensional Stacked Integrated Circuit
- **Venue**: IEEE 2024 (Document 10681395)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10681395/
- **Why relevant**: 2024 thermal-aware scheduling with floorplanning — direct baseline.

### 51. Approach of Genetic Algorithm for Power-Aware Testing of 3D IC
- **Venue**: IET Computers & Digital Techniques, 2019
- **DOI/Link**: https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-cdt.2018.5079
- **Why relevant**: GA baseline for power-aware 3D-IC test.

### 52. Window-Based Peak Power Model and PSO-Guided 3D Bin Packing for SoC Test Scheduling
- **Venue**: Microelectronics Journal, Elsevier
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0167926015000073
- **Why relevant**: PSO baseline for power-constrained SoC scheduling.

### 53. Multicast-Based Testing and Thermal-Aware Test Scheduling for 3D ICs with a Stacked NoC
- **Venue**: IEEE TCAD (Document 7303920)
- **DOI/Link**: https://ieeexplore.ieee.org/document/7303920/similar
- **Why relevant**: TCAD-grade NoC + thermal scheduling reference.

### 54. Test-Cost Optimization and Test-Flow Selection for 3D-Stacked ICs
- **Authors**: Duke / Chakrabarty group
- **Venue**: IEEE (Document 6548941)
- **DOI/Link**: https://ieeexplore.ieee.org/document/6548941/
- **Why relevant**: Foundational test-cost optimization framework for 3D SICs.

### 55. Test Wrapper and Test Access Mechanism Co-Optimization for System-on-Chip
- **Venue**: IEEE TCAD (cited as classical)
- **DOI/Link**: https://ieeexplore.ieee.org/document/1252857/
- **Why relevant**: Defines the TAM/wrapper co-optimization problem that newer ML papers extend.

### 56. Designing Balanced Wrapper Chains in 3D SoC Under Constrained TSVs
- **Venue**: Innovations in Systems and Software Engineering, Springer, 2021
- **DOI/Link**: https://link.springer.com/article/10.1007/s11334-021-00402-w
- **Why relevant**: SA-based wrapper-chain design; useful baseline.

### 57. A New Die-Level Flexible Design-for-Test Architecture for 3D Stacked ICs
- **Venue**: Microelectronics Journal, Elsevier, 2024
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0167926024000531
- **Why relevant**: 2024 DfT architecture for parallel test in 3D SICs.

### 58. CATCH: A Cost Analysis Tool for Co-optimization of Chiplet-Based Heterogeneous Systems
- **Venue**: arXiv 2503.15753, 2025
- **DOI/Link**: https://arxiv.org/abs/2503.15753
- **Why relevant**: Cost-modeling tool for chiplet test/assembly/silicon; useful for chiplet test cost framing.

### 59. Machine Learning-Based Prediction of Test Power
- **Venue**: IEEE Conference (Document 8791548)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8791548
- **Why relevant**: Early but core paper on ML prediction of test power.

### 60. Machine Learning-Based Test Pattern Analysis for Localizing Critical Power Activity Areas
- **Venue**: IEEE Conference (Document 8244464)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8244464/
- **Why relevant**: Identifies high-risk power patterns via ML.

### 61. SoCRATES: System-on-Chip Resource Adaptive Scheduling Using Deep Reinforcement Learning
- **Venue**: arXiv 2104.14354, 2021
- **DOI/Link**: https://arxiv.org/abs/2104.14354
- **Why relevant**: Adaptive DRL scheduler for SoC; methodology transfers to SoC test scheduling.

### 62. DeepSoCS: A Neural Scheduler for Heterogeneous System-on-Chip (SoC) Resource Scheduling
- **Venue**: arXiv 2005.07666, 2020
- **DOI/Link**: https://arxiv.org/pdf/2005.07666
- **Why relevant**: Companion to SoCRATES; basis for DRL scheduler comparisons.

### 63. NoC Application Mapping Optimization Using Reinforcement Learning
- **Venue**: ACM TODAES, 2022
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3510381
- **Why relevant**: RL-based NoC mapping — transferable methodology for test mapping.

### 64. Robust Deep Learning for IC Test Problems
- **Venue**: IEEE (Document 9336061)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9336061/
- **Why relevant**: Survey of state-of-the-art DL for IC test problems.

### 65. Advanced Outlier Detection Using Unsupervised Learning for Screening Potential Customer Returns
- **Venue**: IEEE 2021 (Document 9325225)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9325225/
- **Why relevant**: Unsupervised outlier detection for customer-return screening.

### 66. Adaptive-Learning-Based Importance Sampling for Analog Circuit DPPM Estimation
- **Venue**: IEEE TCAD (Document 6917044)
- **DOI/Link**: https://ieeexplore.ieee.org/document/6917044/
- **Why relevant**: DPPM estimation methodology for analog ICs.

### 67. Adaptive Outlier Detection for Power MOSFETs Based on Gaussian Process Regression
- **Venue**: arXiv 2201.10126, 2022
- **DOI/Link**: https://arxiv.org/pdf/2201.10126
- **Why relevant**: GP outlier detection for power-device testing.

### 68. Wafer-Level Variation Modeling for Multi-site RF IC Testing via Hierarchical Gaussian Process
- **Venue**: arXiv 2111.01369, 2022
- **DOI/Link**: https://ar5iv.labs.arxiv.org/html/2111.01369
- **Why relevant**: Hierarchical GP for multi-site RF wafer test.

### 69. AI/ML Algorithms and Applications in VLSI Design and Technology
- **Venue**: Integration, the VLSI Journal (Elsevier), 2023
- **DOI/Link**: https://dl.acm.org/doi/10.1016/j.vlsi.2023.06.002
- **Why relevant**: Broad VLSI design/test ML survey.

### 70. A Survey on Machine and Deep Learning in Semiconductor Industry: Methods, Opportunities, and Challenges
- **Venue**: Cluster Computing, Springer, 2023
- **DOI/Link**: https://link.springer.com/article/10.1007/s10586-023-04115-6
- **Why relevant**: Industry-perspective ML survey for semiconductor manufacturing/test.

### 71. Silicon Lifecycle Management (SLM): Requirements, Trends, and Opportunities
- **Venue**: ResearchGate / SLM survey, 2024
- **DOI/Link**: https://www.researchgate.net/publication/383684615
- **Why relevant**: SLM frames in-field test/monitoring as part of the optimization story.

### 72. Convolutional Neural Network for Semiconductor Wafer Defect Detection
- **Venue**: IEEE (Document 8944584)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8944584/
- **Why relevant**: CNN baseline for wafer defect detection.

### 73. Efficient Convolutional Neural Networks for Semiconductor Wafer Bin Map Classification
- **Venue**: Sensors (MDPI), 2023
- **DOI/Link**: https://www.mdpi.com/1424-8220/23/4/1926
- **Why relevant**: Lightweight CNN baselines (MobileNet, ShuffleNet) for WBM classification.

### 74. Predicting Early Failure of Quantum Cascade Lasers During Accelerated Burn-In Testing Using Machine Learning
- **Venue**: Nature Scientific Reports, 2022
- **DOI/Link**: https://www.nature.com/articles/s41598-022-13303-0
- **Why relevant**: Burn-in failure prediction with ML — cross-domain analogy for IC burn-in.

### 75. An Artificial Intelligence-Based Framework for Burn-in Reduction in the Semiconductor Manufacturing Industry
- **Authors**: Ahmed, Hosseinpour, Baraldi, Zio, Lewitschnig
- **Venue**: Springer microelectronics reliability series, 2024
- **DOI/Link**: https://link.springer.com/chapter/10.1007/978-3-031-59361-1_5
- **Why relevant**: Direct AI framework for burn-in reduction.

### 76. A Data-Driven Modelling Framework for Predicting the Quality of Semiconductor Devices to Support Burn-In Decisions
- **Venue**: International Journal of Production Research (Elsevier), 2025
- **DOI/Link**: https://www.sciencedirect.com/science/article/pii/S036083522500261X
- **Why relevant**: ML-based burn-in quality prediction; relevant for adaptive-test/burn-in skip.

### 77. A Machine Learning Approach for Improving Wafer Acceptance Testing Based on Analysis of Station and Equipment Combinations
- **Venue**: Mathematics (MDPI), 2023
- **DOI/Link**: https://www.mdpi.com/2227-7390/11/7/1569
- **Why relevant**: Equipment-aware WAT improvement.

### 78. A Machine Learning-based Approach for Failure Prediction at Cell Level based on Wafer Acceptance Test Parameters
- **Venue**: IEEE Conference (Document 9476151)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9476151/
- **Why relevant**: Cell-level failure prediction from WAT data.

### 79. Wafer-Level Die Re-Test Success Prediction Using Machine Learning
- **Venue**: IEEE Conference (Document 9093672)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9093672/
- **Why relevant**: Predicts whether retesting a die is worthwhile — direct adaptive-test decision.

### 80. Graph Neural Networks for Integrated Circuit Design, Reliability, and Security: Survey and Tool
- **Venue**: ACM Computing Surveys, 2025
- **DOI/Link**: https://dl.acm.org/doi/full/10.1145/3769081
- **Why relevant**: Comprehensive GNN-for-IC survey; cite for GNN background and tool GNN4CIRCUITS.

### 81. Why are Graph Neural Networks Effective for EDA Problems?
- **Venue**: ICCAD 2022
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3508352.3561093
- **Why relevant**: Theoretical motivation for GNNs in EDA/test.

### 82. Efficient and Effective Neural Networks for Automatic Test Pattern Generation
- **Venue**: MLCAD 2024 (Salt Lake City)
- **DOI/Link**: https://dblp.org/db/conf/mlcad/mlcad2024.html
- **Why relevant**: Recent MLCAD paper on NN-based ATPG.

### 83. IR-Aware ECO Timing Optimization Using Reinforcement Learning
- **Venue**: MLCAD 2024
- **DOI/Link**: https://dblp.org/db/conf/mlcad/mlcad2024.html
- **Why relevant**: RL for IR-aware timing closure; transferable framing to power-safe test.

### 84. Boosting CPU Turbo Yield Utilizing Explainable AI
- **Venue**: ITC 2024
- **DOI/Link**: https://dblp.org/db/conf/itc/itc2024.html
- **Why relevant**: XAI for yield improvement at ITC 2024.

### 85. Large Language Models to Generate System-Level Test Programs Targeting Non-functional Properties
- **Venue**: arXiv 2403.10086, 2024
- **DOI/Link**: https://arxiv.org/abs/2403.10086
- **Why relevant**: LLMs in SLT — emerging direction.

### 86. A Wafer Map Yield Prediction Based on Machine Learning for Productivity Enhancement
- **Venue**: ResearchGate / IEEE, 2019
- **DOI/Link**: https://www.researchgate.net/publication/336244772
- **Why relevant**: ML yield prediction baseline.

### 87. Test-data Volume Optimization for Diagnosis
- **Venue**: DAC 2012
- **DOI/Link**: https://dl.acm.org/doi/10.1145/2228360.2228462
- **Why relevant**: Foundational test-data-volume optimization.

### 88. A Genetic Algorithm Based Heuristic Technique for Power Constrained Test Scheduling in Core-Based SoCs
- **Venue**: IEEE (Document 4402522)
- **DOI/Link**: https://ieeexplore.ieee.org/document/4402522/
- **Why relevant**: Classical GA baseline for power-constrained scheduling.

### 89. Power-Aware SoC Test Optimization Through Dynamic Voltage and Frequency Scaling
- **Venue**: IEEE (Document 6673258)
- **DOI/Link**: https://ieeexplore.ieee.org/document/6673258/
- **Why relevant**: DVFS-based power-aware SoC test optimization.

### 90. 3D IC Test Scheduling with Test Pads Considered
- **Venue**: IEEE (Document 7543363)
- **DOI/Link**: https://ieeexplore.ieee.org/abstract/document/7543363/
- **Why relevant**: ILP formulation for 3D test scheduling with test-pad constraints.

### 91. RT-Level ITC'99 Benchmarks and First ATPG Results
- **Venue**: IEEE Design & Test
- **DOI/Link**: https://dl.acm.org/doi/10.1109/54.867894
- **Why relevant**: ITC'99 benchmarks — standard ATPG evaluation suite.

### 92. ITC'99 Benchmark Documentation
- **Venue**: CERC, UT Austin
- **DOI/Link**: https://www.cerc.utexas.edu/itc99-benchmarks/bendoc1.html
- **Why relevant**: Direct ITC'99 benchmark reference.

### 93. ISCAS / ITC / TAU Benchmark Circuits Collection
- **Venue**: GitHub repository
- **DOI/Link**: https://github.com/santoshsmalagi/Benchmarks
- **Why relevant**: ISCAS85/89 + ITC99 benchmarks for ATPG and DfT experiments.

### 94. DEFT: Differentiable Automatic Test Pattern Generation
- **Venue**: arXiv 2512.23746, 2025 (DAC submission)
- **DOI/Link**: https://arxiv.org/html/2512.23746v1
- **Why relevant**: Differentiable ATPG — gradient-based search; novel and recent.

### 95. Test-Architecture Optimization and Test Scheduling for SoCs with Core-Level Expansion of Compressed Test Patterns
- **Venue**: DATE 2008
- **DOI/Link**: https://dl.acm.org/doi/10.1145/1403375.1403422
- **Why relevant**: Compressed-pattern test scheduling foundation.

### 96. Power Reduction Through X-filling of Transition Fault Test Vectors for LOS Testing
- **Venue**: LIRMM / IEEE, 2011
- **DOI/Link**: https://hal-lirmm.ccsd.cnrs.fr/lirmm-00553930
- **Why relevant**: X-fill baseline for power-aware ATPG.

### 97. Testability-Aware Low Power Controller Design with Evolutionary Learning
- **Venue**: arXiv 2111.13332, 2021
- **DOI/Link**: https://arxiv.org/pdf/2111.13332
- **Why relevant**: Evolutionary learning for low-power test controller design.

### 98. Survey on Power-Aware Test Scheduling
- **Venue**: IJARCS, 2025
- **DOI/Link**: https://www.ijarcs.info/index.php/Ijarcs/article/view/7318/5918
- **Why relevant**: Concise survey of power-aware test scheduling literature.

### 99. Comprehensive Power-Aware ATPG Methodology for Complex Low-Power Designs
- **Venue**: Synopsys-affiliated, 2022
- **DOI/Link**: https://www.researchgate.net/publication/366610811
- **Why relevant**: Industrial low-power ATPG methodology.

### 100. AI/ML for VLSI Chip Design Automation: A Comprehensive Survey
- **Venue**: Proceedings of the Indian National Science Academy, Springer, 2026
- **DOI/Link**: https://link.springer.com/article/10.1007/s43538-026-00744-8
- **Why relevant**: Recent comprehensive AI/ML-for-VLSI survey.

### 101. Multi-stage Machine Learning-Based Chain Diagnosis (US Patent)
- **Venue**: US Patent 11361248
- **DOI/Link**: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11361248
- **Why relevant**: Documents Siemens/Mentor ML chain-diagnosis approach.

### 102. Input Data Compression for Machine Learning-Based Chain Diagnosis
- **Venue**: US Patent 11681843
- **DOI/Link**: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11681843
- **Why relevant**: ML chain diagnosis preprocessing — efficient inference.

### 103. Reinforcement Learning Approach for Scheduling Problems
- **Venue**: ResearchGate / various
- **DOI/Link**: https://www.researchgate.net/publication/282375695
- **Why relevant**: General RL-for-scheduling foundation for our SoC test scheduling work.

---

## Key Datasets & Benchmarks

| Resource | Use | Link |
|---|---|---|
| **ISCAS85 / ISCAS89** | Combinational + sequential ATPG/test benchmarks | https://github.com/santoshsmalagi/Benchmarks |
| **ITC'99** | RT-level sequential benchmarks (45 gates → 98k gates, 6.6k FFs) | https://www.cerc.utexas.edu/itc99-benchmarks/bendoc1.html |
| **WM-811k** | Wafer-bin-map defect-pattern classification dataset | Common ML benchmark (used by Wafer2Spike, MobileNetV3 work) |
| **CircuitNet** | Large-scale EDA dataset (10k+ designs) for GNN training | NVIDIA-affiliated open dataset |
| **DeepGate** | Pre-trained GNN gate embeddings (used by DeepTPI) | github.com/cure-lab/DeepGate |
| **DeepTPI code** | Open-source RL TPI implementation | github.com/cure-lab/DeepTPI |
| **SoCRATES code** | Open-source SoC DRL scheduler | github.com/EpiSci/SoCRATES |
| **Texas Instruments analog/RF dataset** | Used in Niranjan et al. VTS 2023 | Industrial (request) |
| **WAT (Wafer Acceptance Test) datasets** | Used by Shapley/dynamic-neighborhood TODAES work | Industrial (typically NDA) |
| **ICCAD 2023 CAD Contest Problem C** | Static IR-drop estimation ML benchmark | https://2023.iccad.com/ |
| **ICCAD 2024 CAD Contest Problem A** | Reinforcement Logic Optimization general cost function | https://dl.acm.org/doi/10.1145/3676536.3689910 |

---

## Identified Research Gaps

1. **RL for chiplet-era TAM/wrapper co-optimization.** Existing RL test-work (DeepTPI, SmartATPG, Chakrabarty's M3D work) covers monolithic 3D ICs and ATPG, but no published work applies modern RL to heterogeneous chiplet TAM optimization that respects UCIe 2.0 DFx constraints and IEEE P3405. **High-impact target**: an RL agent that schedules tests across chiplets with UDA management fabric, balancing test time, peak power, and thermal hotspots.

2. **Joint ATPG + power-aware test scheduling via multi-objective RL.** Most RL ATPG work optimizes pattern count and runtime; most scheduling work uses GA/SA. A unified multi-objective RL that simultaneously generates power-safe patterns AND schedules them under TAM/thermal constraints is unexplored.

3. **Transferable ML for adaptive test across product families.** Niranjan et al. and Pan et al. retrain per-wafer/per-product. A transfer-learning / federated-learning adaptive-test framework that generalizes across product families (e.g., automotive MCU → AI accelerator) is a clear gap.

4. **Reliability-aware test optimization for AI accelerator dies under SDC.** Recent SDC papers (Meta, Google) show silent data corruption escapes current tests. ML-driven test-pattern generation specifically targeting SDC-prone aging-correlated paths under in-system test is open.

5. **Explainable ML for test cost / yield-aware testing.** Only one TODAES paper uses Shapley values; broader XAI (LIME, integrated gradients, SHAP) for test-skip decision auditing under automotive AEC-Q100 traceability is unexplored — a publishable methodological angle.

6. **Joint thermal-aware + power-aware 3D-IC test scheduling with surrogate ML and RL.** Existing ML thermal estimators (Microelectronics J. 2022) only inform a heuristic scheduler. End-to-end RL with ML thermal surrogate as differentiable simulator inside the training loop is a clean, publishable contribution.

7. **LLM-assisted test program synthesis for SLT.** LLM-for-SLT work is nascent (one arXiv 2024 paper). LLM-generated test programs with retrieval-augmented coverage closure for chiplet SLT is wide open.

8. **Benchmarking gap.** There is no standardized "AI4Test" benchmark suite that includes 3D-IC/chiplet test scheduling instances, ATPG-with-power-constraints instances, and adaptive-test wafer datasets. Releasing such a benchmark alongside the paper would maximize impact.

---

*Survey compiled May 2026; covers IEEE/ACM/Springer/Elsevier venues 2021–2026 (with a small number of essential pre-2021 foundational works in Tier 3). Direct paper-PDF download links provided where openly accessible.*
