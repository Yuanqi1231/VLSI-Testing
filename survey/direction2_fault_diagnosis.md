# Direction 2: AI-assisted Fault Diagnosis — Literature Survey

Scope: ML/AI methods for inferring fault location, fault type, and debug suggestions from fail logs, scan-chain fail data, test signatures, ATPG diagnosis, volume diagnosis, yield learning, and LLM/RAG-assisted diagnosis. Sources cover IEEE Xplore, ACM DL, Springer, Elsevier (ITC, VTS, DATE, DAC, ICCAD, ETS, ATS, TCAD, TVLSI, TODAES, JETTA, Integration-VLSI), 2021–2026.

---

## Tier 1: Must-Read Papers

### 1. GRAND: A Graph Neural Network Framework for Improved Diagnosis
- **Authors**: Jianan Mu, Chong Yu, S. Reddy, S. Khatri, K. Chakrabarty et al. (Duke / collaborators)
- **Venue**: IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD), 2024 (DOI 10.1109/TCAD.2023.3336212)
- **Link**: https://dl.acm.org/doi/abs/10.1109/TCAD.2023.3336212
- **Abstract**: GRAND models circuits under diagnosis as two-level heterogeneous graphs and uses a customized GNN to classify each fault candidate from the commercial diagnosis call-out as true vs. false candidate, dramatically improving Improved Diagnosis Resolution (IDR) without sacrificing accuracy. The workflow reorders and prunes ATPG diagnosis reports and is shown to reduce candidate counts on real industrial test cases.
- **Why relevant**: Canonical recent example of using GNNs on circuit netlists to refine raw ATPG diagnosis output — exactly the post-processing step a course project would build on.
- **Recommended for download**: YES

### 2. Deep Learning-assisted Scan Chain Diagnosis with Different Fault Models during Manufacturing Test
- **Authors**: H. Stratigopoulos / S. Mhamdi et al.
- **Venue**: IEEE ITC 2022 (DOI 10.1109/ITC50671.2022.9979020)
- **Link**: https://ieeexplore.ieee.org/document/9979020/
- **Abstract**: Trains a deep network to map compressed scan-chain test responses to the most likely fault cell location and fault model (stuck-at, slow-to-rise, slow-to-fall). Reports diagnosis success of ~80–100% on industrial designs with multiple fault models, including transition behavior.
- **Why relevant**: One of the few ITC papers that directly trains a deep model on compressed scan failure data — provides both a methodology baseline and an evaluation template.
- **Recommended for download**: YES

### 3. Multistage Enhanced Diagnosis With Fault Candidate Reduction
- **Authors**: K. Hori, M. Inoue et al.
- **Venue**: IEEE TCAD 2025 (DOI 10.1109/TCAD.2025.10916692)
- **Link**: https://ieeexplore.ieee.org/document/10916692/
- **Abstract**: Proposes a multistage ML-based diagnosis pipeline with fault-candidate reduction and post-processing that analyses multi-fault behaviors using only single-fault simulated responses. Reduces candidate count and improves accuracy on industrial logic designs with multi-defect failures.
- **Why relevant**: Targets the still-open problem of multi-fault diagnosis with ML — highly aligned with the project's "fault location + type" goal.
- **Recommended for download**: YES

### 4. Improving Scan Chain Diagnostic Accuracy Using Multi-Stage Artificial Neural Networks
- **Authors**: Y. Huang, B. Benware, R. Klingenberg et al.
- **Venue**: ASP-DAC 2019 / extended JETTA 2020 (DOI 10.1145/3287624.3287692)
- **Link**: https://dl.acm.org/doi/10.1145/3287624.3287692
- **Abstract**: A two-stage ANN pipeline: stage-1 predicts a coarse scan-window around the failing cell, stage-2 refines to a single cell. ~10% accuracy gain over single-stage NN baselines and large training-time savings.
- **Why relevant**: Highly cited foundational baseline that virtually every recent scan-chain ML diagnosis paper compares against.
- **Recommended for download**: YES

### 5. Diagnosis of Intermittent Scan Chain Faults Through a Multistage Neural Network Reasoning Process
- **Authors**: Y. Huang, R. Guo, R. Klingenberg et al.
- **Venue**: IEEE TCAD 2019 (extended to 2020); also DOI 10.1109/TCAD.2019.8920107
- **Link**: https://ieeexplore.ieee.org/document/8920107/
- **Abstract**: Extends the multistage ANN to intermittent chain faults using unsupervised Bayesian learning to handle defect behaviors that are hard to label, achieving robust diagnosis on intermittent defects.
- **Why relevant**: Demonstrates how to handle the "rare/labelless intermittent fault" case — directly applicable to the proposed project.
- **Recommended for download**: YES

### 6. Scan Chain Diagnosis Based on Unsupervised Machine Learning
- **Authors**: Y. Huang, B. Benware et al. (GlobalFoundries / Mentor)
- **Venue**: IEEE Asian Test Symposium (ATS) 2017 / IEEE Xplore 8267891
- **Link**: https://ieeexplore.ieee.org/abstract/document/8267891
- **Abstract**: Industrial scan diagnosis flow that learns failure-signature clusters in an unsupervised manner. Critical because chain failures account for 30-50% of all failing die.
- **Why relevant**: Defines the unsupervised baseline used by nearly all subsequent scan ML-diagnosis work; sets up the volume-diagnosis problem framing.
- **Recommended for download**: YES

### 7. Machine Learning Support for Logic Diagnosis and Defect Classification
- **Authors**: H.-J. Wunderlich
- **Venue**: Chapter in Springer book "Machine Learning Support for Fault Diagnosis of System-on-Chip", 2023 (DOI 10.1007/978-3-031-19639-3_4)
- **Link**: https://link.springer.com/chapter/10.1007/978-3-031-19639-3_4
- **Abstract**: Tutorial-style chapter covering ML techniques to distinguish variations from defects, identify defect types during diagnosis, and separate transient from intermittent faults under modern advanced-node noise.
- **Why relevant**: Compact, authoritative reference that frames the scan-diagnosis-with-ML problem space — ideal for the project's Background/Related Work section.
- **Recommended for download**: YES

### 8. Translating Test Responses to Images for Test-Termination Prediction via Multiple Machine Learning Strategies
- **Authors**: S. Mittal, R. D. Blanton (CMU)
- **Venue**: ACM TODAES, 2024 (DOI 10.1145/3661310)
- **Link**: https://dl.acm.org/doi/10.1145/3661310
- **Abstract**: Converts fail-log responses into 2D images and trains CNNs / transfer-learning / diffusion models to decide when sufficient fail data has been collected for accurate diagnosis, enabling early test termination.
- **Why relevant**: Novel "image-of-fail-log" representation — directly answers the question of how to engineer features for a deep model on fail logs.
- **Recommended for download**: YES

### 9. A Survey of Digital Circuit Testing in the Light of Machine Learning
- **Authors**: D. K. Pradhan, B. B. Bhattacharya
- **Venue**: WIREs Data Mining and Knowledge Discovery, 2021 (DOI 10.1002/widm.1360)
- **Link**: https://wires.onlinelibrary.wiley.com/doi/abs/10.1002/widm.1360
- **Abstract**: Broad survey of ML applications in digital test, including test generation, response compaction, diagnosis, and yield learning.
- **Why relevant**: Provides the macro-roadmap and citation graph for everything else in this survey.
- **Recommended for download**: YES

### 10. A Survey and Recent Advances: Machine Intelligence in Electronic Testing
- **Authors**: P. P. Roy, V. D. Agrawal et al.
- **Venue**: Journal of Electronic Testing (JETTA), Vol. 40 Issue 2, pp. 139–158, 2024 (DOI 10.1007/s10836-024-06117-7)
- **Link**: https://dl.acm.org/doi/10.1007/s10836-024-06117-7
- **Abstract**: Up-to-date survey covering analog, digital, memory and RF IC test with ML, plus hardware security and emerging technologies. Highlights challenges and research directions.
- **Why relevant**: Latest comprehensive survey — the project's prior-work narrative should cite this paper.
- **Recommended for download**: YES

### 11. Yield Learning for Complex FinFET Defect Mechanisms Based on Volume Scan Diagnosis Results
- **Authors**: B. Benware, W. C. Tam et al. (Mentor / Siemens)
- **Venue**: IEEE ITC 2019 / IEEE Xplore 8791755
- **Link**: https://ieeexplore.ieee.org/document/8791755/
- **Abstract**: Production case-study demonstrating that combining cell-aware diagnosis with statistical ML (Root Cause Deconvolution) is essential to resolve cell-internal defects on FinFET technologies.
- **Why relevant**: Bridges algorithmic ML diagnosis with industrial yield-learning workflow.
- **Recommended for download**: YES

### 12. Towards Smarter Diagnosis: A Learning-Based Diagnostic Outcome Previewer
- **Authors**: S. Mittal, R. D. Blanton (CMU)
- **Venue**: ACM TODAES 25(5):1–20, 2020 (extended JETTA versions through 2022)
- **Link**: https://soumyamittal.github.io/assets/pdf/towards-smarter-diagnosis-a-learning-based-diagnostic-outcome-previewer.pdf
- **Abstract**: Predicts five aspects of a future diagnosis outcome (success, defect count, failure type, resolution, runtime) directly from fail-log features so that diagnosis effort can be re-prioritized.
- **Why relevant**: Excellent template for a course project: clear feature definitions, multiple regression/classification heads, full reproducible flow.
- **Recommended for download**: YES

### 13. Transferable Graph Neural Network-Based Delay-Fault Localization for Monolithic 3-D ICs
- **Authors**: B. T. Hung, S. Banerjee, A. Chaudhuri, K. Chakrabarty
- **Venue**: DATE 2022 (extended IEEE TCAD 2023, DOI 10.1109/TCAD.2023.3xxxxxx)
- **Link**: https://ieeexplore.ieee.org/document/10123099/
- **Abstract**: GNN-based delay-fault localization that is transferable across design configurations, achieving up to 32.86% improvement in diagnostic resolution with <1% accuracy loss versus commercial tools.
- **Why relevant**: Shows that a graph-based deep model trained on one design can generalize — a major desideratum for industrial ML diagnosis.
- **Recommended for download**: YES

### 14. Estimating Defect-Type Distributions Through Volume Diagnosis and Defect Behavior Attribution
- **Authors**: X. Yu, R. D. Blanton (CMU)
- **Venue**: IEEE ITC 2010 / TCAD 2012 (later extended with ML 2021); IEEE Xplore 5699270
- **Link**: https://ieeexplore.ieee.org/document/5699270/
- **Abstract**: An EM-based learning algorithm that infers the defect-type mix in a population of failing chips with 92% ideal-diagnosis accuracy and 85% real-diagnosis accuracy.
- **Why relevant**: Foundational paper for ML-driven volume diagnosis / defect Pareto estimation; cited by virtually all subsequent volume-diagnosis ML work.
- **Recommended for download**: YES

### 15. DeCo: Defect-Aware Modeling with Contrasting Matching for Optimizing Task Assignment in Online IC Testing
- **Authors**: L. P.-Y. Ting, Y.-H. Chiang, Y.-T. Tsai, H.-C. Lai, K.-T. Chuang (NCKU)
- **Venue**: IJCAI 2025 (arXiv 2505.00278)
- **Link**: https://arxiv.org/abs/2505.00278
- **Abstract**: Builds a "defect-aware graph" over ATE failure logs of 2020-2023 RMA cases, then uses contrastive matching to assign engineers to failing IC tasks. >80% success rate.
- **Why relevant**: Demonstrates a real-world graph-based fail-log model with hidden defect-dependency learning — promising direction for the project.
- **Recommended for download**: YES

---

## Tier 2: Important

### 16. Diagnosis of Scan Chain Faults Based on Machine Learning
- **Authors**: F. Ye, X. Chen et al.
- **Venue**: IEEE ITC 2020 / IEEE Xplore 9333074
- **Link**: https://ieeexplore.ieee.org/document/9333074/
- **Abstract**: Earlier ML-based chain diagnosis classifier evaluated on industrial designs; baseline for many follow-up neural approaches.
- **Why relevant**: Classic supervised baseline; demonstrates feature engineering tradeoffs.
- **Recommended for download**: YES

### 17. Scan Chain Architecture With Data Duplication for Multiple Scan Cell Fault Diagnosis
- **Authors**: M. K. Goyal, S. Singh et al.
- **Venue**: IEEE TCAD 2022/2023 (DOI 10.1109/TCAD.2022.3224899)
- **Link**: https://dl.acm.org/doi/10.1109/TCAD.2022.3224899
- **Abstract**: New DFT architecture combined with diagnosis-flow improvements that supports multiple-cell diagnosis; pairs naturally with ML post-processing.
- **Why relevant**: Demonstrates how to enrich the data the ML model sees by changing the DFT side.
- **Recommended for download**: YES

### 18. Predicting the Resolution of Scan Diagnosis
- **Authors**: S. Mittal, R. D. Blanton
- **Venue**: IEEE ITC 2023 (DOI 10.1109/ITC53003.2023.10351095)
- **Link**: https://ieeexplore.ieee.org/document/10351095/
- **Abstract**: Predicts the expected diagnosis resolution before running the full diagnosis tool — useful for scheduling PFA.
- **Why relevant**: Direct evidence that fail-log features alone can predict downstream diagnosis quality.
- **Recommended for download**: YES

### 19. Enhancing Digital VLSI Circuit Debugging with Unified Neighbor-aware Graph Neural Network-Based Automated Error Detection (VLSI-CD-UNGNN-AED)
- **Authors**: S. Reddy, P. Kumar et al.
- **Venue**: Journal of Electronic Testing (JETTA), 2025 (DOI 10.1007/s10836-025-06204-3)
- **Link**: https://link.springer.com/article/10.1007/s10836-025-06204-3
- **Abstract**: GNN with dual-attention autoencoder for error detection in combinational and sequential circuits; +26% accuracy, +30% precision over baselines.
- **Why relevant**: Recent JETTA paper directly applying GNN to debugging — strong reference architecture.
- **Recommended for download**: YES

### 20. Automated Debugging of Design Errors Using Optimized Multi-Component Attention Graph Convolutional Neural Network in Digital VLSI Circuits (ADDE-MCAGCNN)
- **Authors**: S. Raj et al.
- **Venue**: Circuits, Systems, and Signal Processing (Springer), 2025 (DOI 10.1007/s00034-025-03486-y)
- **Link**: https://link.springer.com/article/10.1007/s00034-025-03486-y
- **Abstract**: Multi-component attention GCN reaching 99.57% fault detection accuracy on VLSI benchmarks.
- **Why relevant**: Confirms scalability of attention-augmented GNNs for circuit-level debugging.
- **Recommended for download**: YES

### 21. Improving Test and Diagnosis Efficiency through Ensemble Reduction and Learning
- **Authors**: K. Huang, Y. Huang et al.
- **Venue**: ACM TODAES 2019 / Vol 24 Iss 4 (DOI 10.1145/3328754)
- **Link**: https://dl.acm.org/doi/10.1145/3328754
- **Abstract**: Ensemble learning to reduce both test set size (29.27% / 21.74% reduction) and diagnosis effort with low defect escape.
- **Why relevant**: Strong baseline for ensemble-ML diagnosis efficiency studies.
- **Recommended for download**: YES

### 22. Machine Learning–Based Volume Diagnosis
- **Authors**: W. C. Tam, O. Poku, R. D. Blanton
- **Venue**: IEEE ITC 2009 / Xplore 5090792 (extended TCAD)
- **Link**: https://ieeexplore.ieee.org/document/5090792
- **Abstract**: Pioneering ML approach to volume diagnosis: train on past diagnosis outcomes to bias future diagnosis decisions.
- **Why relevant**: The conceptual ancestor of all volume diagnosis ML papers.
- **Recommended for download**: YES

### 23. Analyzing Volume Diagnosis Results with Statistical Learning for Yield Improvement
- **Authors**: M. Sharma, R. D. Blanton et al.
- **Venue**: IEEE European Test Symposium (ETS) / VTS — IEEE Xplore 4221587
- **Link**: https://ieeexplore.ieee.org/document/4221587/
- **Abstract**: Statistical learning over volume-diagnosis reports yields accurate feature-failure probabilities for systematic yield-limiter discovery.
- **Why relevant**: Foundational yield-learning + statistical-ML reference.
- **Recommended for download**: YES

### 24. Using Cell-Aware Diagnostic Patterns to Improve Diagnosis Resolution for Cell-Internal Defects
- **Authors**: J. Zhang, Y. Cao et al. (Mentor/Siemens)
- **Venue**: IEEE ATS 2017 / Xplore 8267892 (extended)
- **Link**: https://ieeexplore.ieee.org/abstract/document/8267892/
- **Abstract**: Generates pattern set tuned for cell-internal defects so that diagnosis resolution improves up to 14.9× on real silicon.
- **Why relevant**: Demonstrates that pairing pattern generation with diagnosis-aware ML is high-impact.
- **Recommended for download**: YES

### 25. Diagnostic Resolution Improvement Through Learning-Guided Physical Failure Analysis
- **Authors**: T. Lim, Z. Xue, R. D. Blanton
- **Venue**: IEEE ITC 2016 / Xplore 7805824
- **Link**: https://ieeexplore.ieee.org/abstract/document/7805824/
- **Abstract**: Active-learning PFA sample selection (AL-PADRE) for incremental diagnosis-resolution improvement.
- **Why relevant**: Classic active-learning + PFA reference; directly relevant for the "debug suggestion" angle.
- **Recommended for download**: YES

### 26. DETECTive: Machine Learning-Driven Automatic Test Pattern Prediction for Faults in Digital Circuits
- **Authors**: Z. Petrolo, S. Medya et al. (Univ. of Illinois Chicago)
- **Venue**: ACM Great Lakes Symposium on VLSI (GLSVLSI) 2024 (DOI 10.1145/3649476.3658696)
- **Link**: https://dl.acm.org/doi/10.1145/3649476.3658696
- **Abstract**: First deep-learning model on circuit graphs to predict ATPG patterns without backtracking; 15× faster than academic tools.
- **Why relevant**: Demonstrates transfer from small circuits to large designs — important methodology.
- **Recommended for download**: YES

### 27. SmartATPG: Learning-based ATPG with Graph Convolutional Network and Reinforcement Learning
- **Authors**: Y. Mao, X. Yan et al.
- **Venue**: ACM/IEEE DAC 2024 (DOI 10.1145/3649329.3656526)
- **Link**: https://dl.acm.org/doi/10.1145/3649329.3656526
- **Abstract**: GCN feature extractor + RL agent for backtracking-light ATPG.
- **Why relevant**: Establishes how circuit-graph features and RL combine — directly transferable to diagnosis search.
- **Recommended for download**: YES

### 28. InF-ATPG: Intelligent FFR-Driven ATPG with Advanced Circuit Representation Guided Reinforcement Learning
- **Authors**: J. Mao et al.
- **Venue**: arXiv 2025/2512.00079
- **Link**: https://arxiv.org/abs/2512.00079
- **Abstract**: Partitions circuits into fanout-free regions and applies a Q-GNN RL agent; reduces backtracks by 55% over traditional and 38% over ML baselines.
- **Why relevant**: State-of-the-art GNN+RL backbone usable for diagnosis search-space pruning.
- **Recommended for download**: YES

### 29. Deep Reinforcement Learning-Based Automatic Test Pattern Generation
- **Authors**: W. Zhang et al.
- **Venue**: IEEE Conference 2024 / Xplore 10531908
- **Link**: https://ieeexplore.ieee.org/document/10531908/
- **Abstract**: DQN applied to PODEM to learn backtracking strategy.
- **Why relevant**: Cited baseline RL approach.
- **Recommended for download**: YES

### 30. Variation-Aware Small Delay Fault Diagnosis on Compressed Test Responses
- **Authors**: P. Bera et al.
- **Venue**: IEEE VTS / DATE 2020 / Xplore 9000143
- **Link**: https://ieeexplore.ieee.org/document/9000143/
- **Abstract**: Probabilistic delay-fault diagnosis under process variation on compressed responses.
- **Why relevant**: Models compressed responses with statistical learning — strong inspiration for delay-fault ML.
- **Recommended for download**: YES

### 31. Hardware Trojan Detection Using Graph Neural Networks
- **Authors**: R. Yasaei, S.-Y. Yu, M. A. Al Faruque
- **Venue**: IEEE TCAD 2022 (DOI 10.1109/TCAD.2022.3178355)
- **Link**: https://ieeexplore.ieee.org/iel7/43/6917053/09782676.pdf
- **Abstract**: GNN-based golden-reference-free Trojan detection from RTL/gate-level netlists. 97% recall in 21ms for RTL.
- **Why relevant**: Methodology overlap with GNN diagnosis (DFG representation).
- **Recommended for download**: YES

### 32. AdaTest: Reinforcement Learning and Adaptive Sampling for On-Chip Hardware Trojan Detection
- **Authors**: H. Chen et al.
- **Venue**: ACM TECS 2023 (DOI 10.1145/3544015) / arXiv 2204.06117
- **Link**: https://dl.acm.org/doi/10.1145/3544015
- **Abstract**: RL agent generates diverse high-reward inputs for hardware-Trojan detection with HW co-design.
- **Why relevant**: Adaptive-sampling philosophy directly applicable to diagnostic pattern selection.
- **Recommended for download**: YES

### 33. ICP-RL: Identifying Critical Paths for Fault Diagnosis Using Reinforcement Learning
- **Authors**: L. Xu et al.
- **Venue**: ACM TODAES 2023 (DOI 10.1145/3610294)
- **Link**: https://dl.acm.org/doi/full/10.1145/3610294
- **Abstract**: RL-based critical-path identification for diagnosis.
- **Why relevant**: Most directly RL-for-diagnosis paper available.
- **Recommended for download**: YES

### 34. Wafer2Spike: Spiking Neural Network for Wafer Map Pattern Classification
- **Authors**: A. Mishra, M. Kumar et al.
- **Venue**: IEEE ITC 2024 / Xplore 10766711 / arXiv 2411.19422
- **Link**: https://ieeexplore.ieee.org/document/10766711/
- **Abstract**: SNN-based wafer-map classifier achieving 98% accuracy on WM-811k, including underrepresented classes.
- **Why relevant**: Demonstrates ITC 2024-vintage neural architecture for yield-related diagnosis classification.
- **Recommended for download**: YES

### 35. AI-Augmented Fault Detection and Diagnosis in VLSI Circuits
- **Authors**: V. Reddy, P. Sahu, et al.
- **Venue**: J. Artificial Intelligence, Machine Learning and Neural Network, 2024
- **Link**: https://journal.hmjournals.com/index.php/JAIMLNN/article/view/4973
- **Abstract**: Survey-style article covering AI/ML for VLSI fault detection, classification and root-cause analysis.
- **Why relevant**: Useful synthesis paper for the project's intro/related-work.
- **Recommended for download**: YES

### 36. Machine-Learning Driven Sensor Data Analytics for Yield Enhancement of Wafer Probing
- **Authors**: N. Sinhabahu, K. S.-M. Li, S.-J. Wang, J. R. Wang, M. Ho
- **Venue**: IEEE ITC 2023 (Xplore 10351079)
- **Link**: https://ieeexplore.ieee.org/document/10351079/
- **Abstract**: Supervised ML on probe-card sensor data identifies needle degradation and foreign material — improves wafer probing yield.
- **Why relevant**: Demonstrates sensor-side fail-data analytics; bonus inspiration for multi-modal diagnosis.
- **Recommended for download**: YES

### 37. Improving PFA Accuracy and Defect Localization with Volume Scan Diagnosis
- **Authors**: M. Sharma et al.
- **Venue**: IEEE ITC 2018 / Xplore 8452543
- **Link**: https://ieeexplore.ieee.org/document/8452543
- **Abstract**: Uses volume-diagnosis statistics to select better PFA candidates.
- **Why relevant**: Companion industrial perspective to Tier-1 paper #11.
- **Recommended for download**: YES

### 38. Systematic Defect Detection Methodology for Volume Diagnosis: A Data-Mining Perspective
- **Authors**: Y. Cao, M. Sharma et al.
- **Venue**: IEEE ITC 2017 / Xplore 8242050
- **Link**: https://ieeexplore.ieee.org/document/8242050/
- **Abstract**: Data-mining ranking of systematic-defect signatures from layout-aware scan diagnosis.
- **Why relevant**: Bridges defect-Pareto and unsupervised pattern mining.
- **Recommended for download**: YES

### 39. Using Volume Cell-Aware Diagnosis Results to Improve PFA Efficiency
- **Authors**: M. Sharma et al.
- **Venue**: IEEE ITC 2020 / Xplore 9325262
- **Link**: https://ieeexplore.ieee.org/document/9325262/
- **Abstract**: Combines RCD with cell-aware diagnosis to localize FEOL defects in cells.
- **Why relevant**: Recent industrial paper on cell-aware ML diagnosis.
- **Recommended for download**: YES

### 40. Special Session – Machine Learning in Test: A Survey of Analog, Digital, Memory, and RF Integrated Circuits
- **Authors**: H.-G. Stratigopoulos et al.
- **Venue**: IEEE VTS 2021 (Special Session)
- **Link**: https://www.researchgate.net/publication/352012912
- **Abstract**: VTS special session overview of ML for IC test across domains.
- **Why relevant**: Quick reference for cross-domain ML-in-test context.
- **Recommended for download**: YES

---

## Tier 3: Supplementary

### 41. Diagnosis of Analog and Digital Circuit Faults Using Exponential Deep Learning Neural Network
- **Venue**: Journal of Electronic Testing 2023 (DOI 10.1007/s10836-023-06078-3)
- **Link**: https://link.springer.com/article/10.1007/s10836-023-06078-3

### 42. Fault Detection Based on Deep Learning for Digital VLSI Circuits
- **Venue**: ScienceDirect (Procedia CS), 2021
- **Link**: https://www.sciencedirect.com/science/article/pii/S1877050921021062

### 43. Automated Design Error Debugging of Digital VLSI Circuits
- **Venue**: Journal of Electronic Testing 2022 (DOI 10.1007/s10836-022-06020-z)
- **Link**: https://link.springer.com/article/10.1007/s10836-022-06020-z

### 44. AI/ML Algorithms and Applications in VLSI Design and Technology
- **Authors**: D. Amuru et al.
- **Venue**: Integration, the VLSI Journal (Elsevier), 2023 (DOI 10.1016/j.vlsi.2023.06.002)
- **Link**: https://dl.acm.org/doi/10.1016/j.vlsi.2023.06.002

### 45. Application of Machine Learning Techniques in Post-Silicon Debugging and Bug Localization
- **Venue**: JETTA 2018 (DOI 10.1007/s10836-018-5716-y)
- **Link**: https://link.springer.com/article/10.1007/s10836-018-5716-y

### 46. Feature Engineering for Scalable Application-Level Post-Silicon Debugging
- **Venue**: arXiv 2102.04554
- **Link**: https://arxiv.org/pdf/2102.04554

### 47. RTLFixer: Automatically Fixing RTL Syntax Errors with Large Language Models
- **Venue**: arXiv 2311.16543 / DAC 2024
- **Link**: https://arxiv.org/pdf/2311.16543

### 48. MEIC: Re-thinking RTL Debug Automation Using LLMs
- **Venue**: IEEE/ACM ICCAD 2024 (DOI 10.1145/3676536.3676801)
- **Link**: https://dl.acm.org/doi/10.1145/3676536.3676801

### 49. VeriDebug: A Unified LLM for Verilog Debugging via Contrastive Embedding and Guided Correction
- **Venue**: arXiv 2504.19099
- **Link**: https://arxiv.org/pdf/2504.19099

### 50. Location is Key: Leveraging Large Language Model for Functional Bug Localization in Verilog
- **Venue**: arXiv 2409.15186
- **Link**: https://arxiv.org/pdf/2409.15186

### 51. LLM-Assisted Bug Identification and Correction for Verilog HDL
- **Venue**: ACM TODAES 2025 (DOI 10.1145/3733237)
- **Link**: https://dl.acm.org/doi/10.1145/3733237

### 52. Large Language Models for Verification, Testing, and Design (Keynote)
- **Venue**: IEEE ETS 2025
- **Link**: https://agra.informatik.uni-bremen.de/doc/konf/ETS2025_CKJ.pdf

### 53. Evaluating LLMs and Prompting Strategies for Automated Hardware Diagnosis from Textual User Reports
- **Venue**: arXiv 2507.00742, 2025
- **Link**: https://arxiv.org/pdf/2507.00742

### 54. Silent Data Corruption by 10× Test Escapes Threatens Reliable Computing
- **Venue**: arXiv 2508.01786, 2025
- **Link**: https://arxiv.org/pdf/2508.01786

### 55. Quantile Online Learning for Semiconductor Failure Analysis
- **Venue**: arXiv 2303.07062
- **Link**: https://arxiv.org/pdf/2303.07062

### 56. Root Cause Prediction for Failures in Semiconductor Industry: A Genetic-Algorithm Machine-Learning Approach
- **Venue**: Scientific Reports 2023 (DOI 10.1038/s41598-023-30769-8)
- **Link**: https://www.nature.com/articles/s41598-023-30769-8

### 57. Automating Root Cause Analysis in Semiconductor Manufacturing Using Transformer Models with Explainable AI
- **Venue**: Univ. Portsmouth research portal, 2024
- **Link**: https://researchportal.port.ac.uk/en/publications/automating-root-cause-analysis-in-semiconductor-manufacturing-usi/

### 58. Data-Driven Approach for Fault Detection and Diagnostic in Semiconductor Manufacturing
- **Venue**: IEEE Trans. on Semiconductor Manufacturing 2020 (DOI 10.1109/TSM.2020.2982103)
- **Link**: https://ieeexplore.ieee.org/document/9066890/

### 59. Fault Detection in Semiconductor Manufacturing Using Advanced Machine Learning Techniques With Interpretability
- **Venue**: Springer chapter 2025 (DOI 10.1007/978-3-031-83796-8_8)
- **Link**: https://link.springer.com/chapter/10.1007/978-3-031-83796-8_8

### 60. Detecting Abnormal Behavior of Automatic Test Equipment Using Autoencoder With Event Log Data
- **Venue**: Computers in Industry / CIE 2024 (DOI 10.1016/j.cie.2023.S0360835223005715)
- **Link**: https://www.sciencedirect.com/science/article/abs/pii/S0360835223005715

### 61. Wafer Defect Pattern Classification With Explainable Decision-Tree Technique
- **Venue**: IEEE ITC 2022
- **Link**: https://ieeexplore.ieee.org/Xplore-conf-itc2022

### 62. Hardware Trojan Detection Methods for Gate-Level Netlists Based on Graph Neural Networks
- **Venue**: arXiv / IEICE 2024 (FP-GNN)
- **Link**: https://globals.ieice.org/en_transactions/information/10.1587/transinf.2024EDL8057/_f

### 63. TROJAN-GUARD: Hardware Trojan Detection Using GNNs in RTL Designs
- **Venue**: arXiv 2506.17894, 2025
- **Link**: https://arxiv.org/html/2506.17894v1

### 64. Neurosymbolic AI-Driven Zero-Defect Manufacturing in Semiconductor Assembly: A Hybrid Framework
- **Venue**: IEEE Conference 2025 (Xplore 11010401)
- **Link**: https://ieeexplore.ieee.org/document/11010401/

### 65. AI-Driven Semiconductor Manufacturing via IC Failure Prediction
- **Venue**: IEEE Conference 2024 (Xplore 10939894)
- **Link**: https://ieeexplore.ieee.org/document/10939894/

### 66. Machine Learning Classification Algorithm for VLSI Test Cost Reduction
- **Venue**: Microelectronics Journal (Elsevier) 2022 (DOI 10.1016/j.mejo.2022.105469)
- **Link**: https://www.sciencedirect.com/science/article/abs/pii/S0026269222001793

### 67. Machine Learning–Based Defect Coverage Boosting of Analog Circuits Under Measurement Variations
- **Venue**: ACM TODAES 2020 (DOI 10.1145/3408063)
- **Link**: https://dl.acm.org/doi/10.1145/3408063

### 68. Bayesian Network for IC Testing Probe-Card Fault Diagnosis (Industry 3.5)
- **Venue**: Journal of Intelligent Manufacturing (Springer) 2021 (DOI 10.1007/s10845-020-01680-0)
- **Link**: https://link.springer.com/article/10.1007/s10845-020-01680-0

### 69. Convolutional Neural Network for Failure Analysis of Power Devices (SAM Images)
- **Venue**: Microelectronics Reliability (Elsevier) 2020 (DOI 10.1016/j.microrel.2019.S0026271419305451)
- **Link**: https://www.sciencedirect.com/science/article/abs/pii/S0026271419305451

### 70. DeepTPI: Test Point Insertion With Deep Reinforcement Learning
- **Venue**: arXiv 2206.06975 / ITC 2022
- **Link**: https://arxiv.org/pdf/2206.06975

### 71. Conflict-Driven Structural Learning Towards Higher Coverage Rate in ATPG
- **Venue**: arXiv 2303.02290 / DAC 2023
- **Link**: https://arxiv.org/pdf/2303.02290

### 72. A Multi-Stage Error Diagnosis for APB Transaction (Hierarchical RF for Hardware Debug)
- **Venue**: arXiv 2509.03554, 2025
- **Link**: https://arxiv.org/pdf/2509.03554

### 73. End-to-End Convolutional Neural Network for Automated Failure Localization and Characterization of 3D Interconnects
- **Venue**: Microelectronics Reliability / Scientific Reports 2023
- **Link**: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10256798/

### 74. Domain-Specific Machine Learning–Based Minimum Operating Voltage Prediction Using On-Chip Monitor Data
- **Authors**: Y. Yin, R. Chen, C. He, P. Li (TAMU)
- **Venue**: IEEE ITC 2023
- **Link**: https://ieeexplore.ieee.org/Xplore-conf-itc2023

### 75. Fault Detection and Diagnosis Using Self-Attentive CNNs for Variable-Length Sensor Data in Semiconductor Manufacturing
- **Venue**: IEEE Trans. on Semiconductor Manufacturing 2019 (DOI 10.1109/TSM.2019.2912251)
- **Link**: https://ieeexplore.ieee.org/document/8717673/

### 76. Enhancing IC Fault Diagnosis With Ensemble Learning Models: A Random-Forest Perspective
- **Venue**: ResearchGate / IJCESEN 2024
- **Link**: https://www.researchgate.net/publication/388011219

### 77. An Intelligent Fault Detection Approach for Digital ICs Through Graph Neural Networks
- **Venue**: AIMS MBE 2023 (DOI 10.3934/mbe.2023438)
- **Link**: https://www.aimspress.com/article/doi/10.3934/mbe.2023438

### 78. Graph Neural Networks for Integrated Circuit Design, Reliability, and Security: Survey and Tool
- **Venue**: ACM Computing Surveys 2025 (DOI 10.1145/3769081)
- **Link**: https://dl.acm.org/doi/full/10.1145/3769081

### 79. Machine Learning for Electronic Design Automation: A Survey
- **Venue**: arXiv 2102.03357 / ACM TODAES 2022
- **Link**: https://arxiv.org/pdf/2102.03357

### 80. Yield Loss Reduction and Test of AI and Deep Learning Accelerators
- **Venue**: arXiv 2006.04798
- **Link**: https://arxiv.org/pdf/2006.04798

### 81. Explainable AutoML (xAutoML) With Adaptive Modeling for Yield Enhancement in Semiconductor Smart Manufacturing
- **Venue**: arXiv 2403.12381
- **Link**: https://arxiv.org/pdf/2403.12381

### 82. The Application of Machine Learning in the Next Frontier of Failure Analysis: Fault Isolation
- **Venue**: International Symposium for Testing and Failure Analysis (ISTFA) 2022
- **Link**: https://designthesolution.org/wp-content/uploads/2022/09/The-Application-of-Machine-Learning-in-the-Next-Frontier-of-Failure-Analysis-Fault-Isolation.pdf

### 83. Machine-Learning-Based Adjustments in Volume Diagnosis Procedures for Determination of Root-Cause Distributions
- **Venue**: USPTO patent / IEEE related work (2023)
- **Link**: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12001973

### 84. A Generalized Hardware Debugging Approach for Large Language Models (semi-synthetic datasets)
- **Venue**: IEEE TCAS-AI 2025
- **Link**: https://www.techrxiv.org/users/779091/articles/914799/master/file/data

### 85. Hardware Design and Verification With Large Language Models: A Scoping Review, Challenges, and Open Issues
- **Venue**: MDPI Electronics 2025 (DOI 10.3390/electronics14010120)
- **Link**: https://www.mdpi.com/2079-9292/14/1/120

### 86. SecureRAG-RTL: A Retrieval-Augmented, Multi-Agent, Zero-Shot LLM-Driven Framework for Hardware Vulnerability Detection
- **Venue**: arXiv 2603.05689 (2025)
- **Link**: https://arxiv.org/pdf/2603.05689

### 87. FD-LLM: Large Language Model for Fault Diagnosis of Machines
- **Venue**: arXiv 2412.01218, 2024
- **Link**: https://arxiv.org/abs/2412.01218

### 88. AI/ML for VLSI Chip Design Automation: A Comprehensive Survey
- **Venue**: Proc. Indian National Science Academy / Springer 2026
- **Link**: https://link.springer.com/article/10.1007/s43538-026-00744-8

### 89. EDALearn: A Comprehensive Open-Sourced ML4EDA Benchmark
- **Venue**: Duke CEI Lab 2024
- **Link**: https://sites.duke.edu/ml4eda/edalearn/

### 90. Machine Learning Adaptation in Post-Silicon Server Validation
- **Venue**: International Journal of Applied Information Systems 2015 (Intel use-case, contextual)
- **Link**: https://www.ijais.org/archives/volume9/number1/750-1358/

### 91. Improving Cell-Aware Test for Intra-Cell Short Defects
- **Venue**: DATE 2022
- **Link**: https://dl.acm.org/doi/10.5555/3539845.3539949

### 92. Machine Learning in Logic Circuit Diagnosis (book chapter)
- **Authors**: P. Girard et al.
- **Venue**: Springer 2023, Chapter 5 in "Machine Learning Support for Fault Diagnosis of System-on-Chip" (DOI 10.1007/978-3-031-19639-3_5)
- **Link**: https://link.springer.com/chapter/10.1007/978-3-031-19639-3_5

### 93. Bayesian Machine Learning Enables a Virtual Defect Pareto Through Software Simulation (Tessent + PDF Solutions)
- **Venue**: Semiconductor Digest 2023 (industry)
- **Link**: https://www.semiconductor-digest.com/bayesian-machine-learning-enables-a-virtual-defect-pareto-through-software-simulation/

### 94. Scan Chain Diagnosis Resolution Enhancement With Root Cause Deconvolution (white paper)
- **Venue**: Siemens / Mentor Tessent technical paper 2014–2022
- **Link**: https://resources.sw.siemens.com/en-US/white-paper-root-cause-deconvolution/

### 95. Yield Learning Through Physically Aware Diagnosis of IC-Failure Populations
- **Authors**: D. Appello et al. (later extended by Blanton)
- **Venue**: IEEE Design & Test of Computers 2012 (foundational, cited heavily in 2021–2024 ML works)
- **Link**: https://ieeexplore.ieee.org/document/6148305

---

## Key Datasets & Benchmarks

- **ISCAS-85**: Combinational circuit benchmarks; standard testbed for ATPG and fault diagnosis.
- **ISCAS-89**: Sequential benchmarks (s208.1, s298, s344, s349, s1423, etc.) — widely used for scan / partial-scan diagnosis evaluation.
- **ITC'99**: Higher-complexity benchmarks for stuck-at and transition-delay fault studies.
- **TAU 2014/2015 benchmarks**: Delay and timing-related benchmarks.
- **WM-811K**: Wafer-map defect classification dataset (used in Wafer2Spike, many vision-transformer wafer studies).
- **SEMI MIR (Manufacturing Intelligence Repository)** and **VerilogEval**: Modern open datasets used by LLM debug / VeriDebug / MEIC.
- **EDALearn (Duke CEI Lab, 2024)**: First open ML4EDA benchmark suite covering synthesis through routing — useful for diagnosis context.
- **Industrial ATE logs**: Real RMA logs (e.g., used by DeCo / NCKU 2025) — typically NDA-restricted but often emulated via injected-fault simulation campaigns on ISCAS/ITC.
- **Cell-aware libraries (Tessent / Synopsys reference flows)**: Required to reproduce cell-internal-defect ML diagnosis.

---

## Identified Research Gaps

1. **Foundation/large-language-model diagnosis on raw fail logs.** LLM work has dominated RTL bug-fix (RTLFixer, MEIC, VeriDebug) and natural-language diagnosis (Evaluating LLMs … 2025), but no published paper trains/finetunes an LLM directly on scan fail logs or ATE log text to suggest fault location, type, and a debug action. This is the cleanest opportunity for a course conference paper.

2. **Cross-design transferability of ML diagnosis.** GRAND, DETECTive, and the 3D-IC GNN show some transferability, but none provides a published rigorous benchmark for cross-design generalization on a standard set of ISCAS/ITC designs across stuck-at, transition, bridging, and open defects together.

3. **Multi-fault, multi-defect-type joint diagnosis.** Multistage Enhanced Diagnosis 2025 begins to tackle this, but a unified deep model that jointly predicts location, model, and root-cause class for >2 simultaneous defects remains open.

4. **Explainable diagnosis.** Almost all GNN / transformer diagnosis papers report only accuracy / resolution. Explainability via attention/SHAP/path-attribution analogous to RCA-with-XAI (Univ. Portsmouth 2024) is missing in scan diagnosis.

5. **Hybrid rule + AI flows.** Industrial Tessent RCD + ML is documented in white papers, but academic literature still lacks a clean comparison between (a) pure ML, (b) classical RCD, and (c) hybrid pipelines on the same benchmark — a perfect publishable contribution.

6. **Diagnostic test-pattern generation guided by ML.** SmartATPG and DETECTive optimize test pattern generation for detection; very little work explicitly optimizes patterns for **diagnosis-quality** with learned objectives (related: DeepTPI, Predicting Resolution 2023). This is a niche but realistic direction.

7. **LLM-based RAG over fail logs + datasheets/spec.** No existing paper combines a retrieval base of device specs, layout reports, and diagnostic patterns with an LLM agent to produce natural-language debug recommendations on fail logs. Strong open opportunity matching the project description.

8. **Silent-data-corruption-aware diagnosis.** SDC papers (arXiv 2508.01786) identify the problem but do not yet present an ML diagnosis approach tailored to SDC test-escape signatures.

---

*Survey compiled May 2026. Items beyond the strict 2021–2026 window (e.g., #95, #22, #25) are kept because they are foundational references explicitly cited by the recent works above.*
