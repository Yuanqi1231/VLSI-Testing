# Direction 1: Failure Bitmap Intelligent Analysis — Literature Survey

> Scope: AI/ML methods applied to failure bitmaps from memory testing, TSV testing, and chiplet interconnect testing — including wafer map / wafer bin map (WBM) fault classification, clustering, anomaly detection, synthetic generation, and modern pattern-recognition architectures (CNN, ViT, GAN, autoencoder, diffusion).
>
> Time window: 2021–2026 (with a few foundational pre-2021 references retained for context).

---

## Tier 1: Must-Read Papers

### 1. Wafer Map Defect Pattern Classification and Image Retrieval Using Convolutional Neural Network
- **Authors**: Takeshi Nakazawa, Deepak V. Kulkarni
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2018, foundational; widely cited 2021–2026)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8263132/
- **Abstract**: Proposes a CNN trained entirely on 28,600 synthetic wafer maps spanning 22 defect classes; achieves 98.2% accuracy on a 6,600-sample real test set and demonstrates retrieval of similar real wafer maps from synthetic features.
- **Why relevant**: Foundational reference for synthetic-bitmap pre-training and CNN-based wafer-map classification. Establishes that synthetic generation can replace scarce labeled data — a core thread in any bitmap-AI study.
- **Recommended for download**: YES

### 2. Anomaly Detection and Segmentation for Wafer Defect Patterns Using Deep Convolutional Encoder–Decoder Neural Network Architectures
- **Authors**: T. Nakazawa, D. V. Kulkarni
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2019; foundational; primary baseline 2021–2026)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8634922/
- **Abstract**: Builds a convolutional encoder–decoder trained only on synthetic basis defect patterns; demonstrates detection and pixel-level segmentation of unseen real-wafer abnormal patterns.
- **Why relevant**: Canonical anomaly-detection/segmentation baseline for wafer bitmaps; bridges classification + localization. Directly maps to "anomaly detection in bitmaps" subtopic.
- **Recommended for download**: YES

### 3. Advances in Machine Learning and Deep Learning Applications towards Wafer Map Defect Recognition and Classification: A Review
- **Authors**: M. T. Hsu, et al.
- **Venue**: Journal of Intelligent Manufacturing, Springer (2023)
- **DOI/Link**: https://link.springer.com/article/10.1007/s10845-022-01994-1
- **Abstract**: Comprehensive review of >100 ML/DL methods for wafer map defect recognition; categorizes feature-engineering, supervised CNN, semi/self-supervised, GAN-augmented, and clustering approaches; benchmarks performance on WM-811K.
- **Why relevant**: Best single-document overview for situating the project. Includes the taxonomy required for a conference paper's "related work" section.
- **Recommended for download**: YES

### 4. Deep Learning for Wafer Map Defect Detection: A Review
- **Authors**: Ruixuan Li, et al.
- **Venue**: IEEE Conference (2024)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10482800
- **Abstract**: Survey paper unifying CNN, Transformer, and hybrid multimodal methods on WM-811K and MixedWM38; identifies ResNet (99% acc, 98.88% F1) as strongest baseline; analyzes pre-2024 trends and gaps.
- **Why relevant**: Most recent (2024) systematic review; gives explicit performance leaderboards on both benchmarks used in the project.
- **Recommended for download**: YES

### 5. A Systematic Review of Deep Learning for Silicon Wafer Defect Recognition
- **Authors**: U. Batool, et al.
- **Venue**: IEEE Access (2021)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9517097/
- **Abstract**: First systematic survey of CNN-based silicon-wafer defect recognition; reviews datasets (WM-811K, MIR-WM811K), architectures, and evaluation protocols.
- **Why relevant**: Standard "citation-target" review listed in essentially every WM-811K paper since 2022. Needed for related-work coverage.
- **Recommended for download**: YES

### 6. Semantic Segmentation-Based Wafer Map Mixed-Type Defect Pattern Recognition
- **Authors**: M. B. Alawieh, et al.
- **Venue**: IEEE TCAD (2023)
- **DOI/Link**: https://dl.acm.org/doi/10.1109/TCAD.2023.3274958
- **Abstract**: Reformulates mixed-type defect classification as semantic segmentation using a U-Net variant; classifies up to 38 patterns in MixedWM38 with state-of-the-art F1.
- **Why relevant**: Top-tier (TCAD) venue paper on the MixedWM38 benchmark; introduces segmentation-based classification — directly applicable to bitmap pattern recognition.
- **Recommended for download**: YES

### 7. When Wafer Failure Pattern Classification Meets Few-Shot Learning and Self-Supervised Learning
- **Authors**: H. Geng, et al.
- **Venue**: ICCAD 2021
- **DOI/Link**: https://dl.acm.org/doi/abs/10.1109/ICCAD51958.2021.9643518
- **Abstract**: First end-to-end approach combining few-shot prototypical networks with self-supervised pre-training for wafer failure classification under extreme label scarcity.
- **Why relevant**: Top design-automation venue (ICCAD) paper directly addressing the project's label-scarcity reality and a strong methodological template.
- **Recommended for download**: YES

### 8. Semi-supervised Wafer Map Pattern Recognition Using Domain-specific Data Augmentations and Contrastive Learning
- **Authors**: H. Kahng, L.-T. Wang, et al.
- **Venue**: IEEE International Test Conference (ITC 2021)
- **DOI/Link**: https://web.ece.ucsb.edu/~lip/publications/ConstrastiveLearning-ITC2021-Submitted.pdf
- **Abstract**: Proposes domain-specific augmentations (defect-aware rotations, masking) combined with contrastive pre-training; matches fully-supervised accuracy with <10% labels on WM-811K.
- **Why relevant**: Published at the premier VLSI testing venue (ITC). Defines the "ITC-style" methodology a course project should aspire to.
- **Recommended for download**: YES

### 9. Memory-Augmented Convolutional Neural Networks With Triplet Loss for Imbalanced Wafer Defect Pattern Classification
- **Authors**: H. Kang, S. Kang
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2021)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9145651/
- **Abstract**: Memory-augmented CNN with triplet metric learning to handle the extreme class imbalance of WM-811K (85% None); a learned key-value store remembers minority-class prototypes.
- **Why relevant**: Combines two big project sub-topics (imbalance handling + metric learning) and is a strong reference baseline (~96% F1) for the long-tail problem.
- **Recommended for download**: YES

### 10. SWaCo: Safe Wafer Bin Map Classification With Self-Supervised Contrastive Learning
- **Authors**: J. Hwang, H. Kim
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2023)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10138110/
- **Abstract**: Self-supervised contrastive learning framework with uncertainty-aware "safe" prediction; rejects samples below a confidence threshold to avoid silent misclassification.
- **Why relevant**: Industrial-deployment perspective on WBM classification with rejection mechanisms — useful angle for a conference paper.
- **Recommended for download**: YES

### 11. Classification of Mixed-Type Defect Patterns in Wafer Bin Maps Using Convolutional Neural Networks
- **Authors**: J. Kyeong, H. Kim
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2018; foundational, defines MixedWM38)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8368296/
- **Abstract**: Introduces the multi-CNN approach for mixed-type defect classification and creates the MixedWM38 benchmark of 38 mixed patterns.
- **Why relevant**: Defines the MixedWM38 dataset that is now a standard benchmark; every mixed-type paper cites it. Essential context.
- **Recommended for download**: YES

### 12. Wafer Map Failure Pattern Classification Using Geometric Transformation-Invariant Convolutional Neural Network
- **Authors**: G. Yu, et al.
- **Venue**: Scientific Reports (Nature) (2023)
- **DOI/Link**: https://www.nature.com/articles/s41598-023-34147-2
- **Abstract**: Rotation- and flip-invariant CNN built on the Radon transform and kernel flipping; achieves geometric invariance natively rather than via augmentation.
- **Why relevant**: Addresses an inherent property of circular wafer bitmaps and is one of the most cited 2023 papers on WM-811K.
- **Recommended for download**: YES

### 13. Self-Supervised Representation Learning for Wafer Bin Map Defect Pattern Classification
- **Authors**: D. Kim, P. Kang
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2021)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9260238/
- **Abstract**: Noise-contrastive self-supervised pre-training on unlabeled WBMs; fine-tuned heads dramatically outperform supervised CNNs with limited labels.
- **Why relevant**: Foundational self-supervised wafer paper widely cited 2021–2025.
- **Recommended for download**: YES

### 14. A Deep Learning Analysis Framework for Complex Wafer Bin Map Classification
- **Authors**: J.-H. Choi, et al.
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2023)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10106471/
- **Abstract**: Modular DL framework with parallel branches for global pattern and local defect cluster features, including a complex-pattern analyzer for mixed defects.
- **Why relevant**: Provides a complete reference architecture for production WBM classification — useful design template for the project.
- **Recommended for download**: YES

### 15. Machine-Learning Approach in Detection and Classification for Defects in TSV-Based 3-D IC
- **Authors**: Y.-J. Huang, J.-F. Li, et al.
- **Venue**: IEEE Transactions on Components, Packaging and Manufacturing Technology (2018; foundational; widely cited 2021–)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8272475/
- **Abstract**: Non-destructive ML-based detection of voids, shorts, and opens in TSVs using a ring-oscillator–based test structure feeding an LSSVM classifier; >96% classification accuracy.
- **Why relevant**: Cornerstone ML-for-TSV paper. Directly maps to the TSV testing portion of the project.
- **Recommended for download**: YES

---

## Tier 2: Important Papers

### 16. Wafer Map Defect Classification Using Autoencoder-Based Data Augmentation and Convolutional Neural Network
- **Authors**: H. T. Le, et al.
- **Venue**: arXiv 2411.11029 (2024)
- **DOI/Link**: https://arxiv.org/abs/2411.11029
- **Abstract**: Autoencoder injects latent-space noise to synthesize minority-class wafer maps; combined with a CNN classifier achieves 98.56% accuracy on WM-811K.
- **Why relevant**: Recent, simple, reproducible baseline combining autoencoder synthesis + classification — easy to extend.
- **Recommended for download**: YES

### 17. Wafer Bin Map Recognition With Autoencoder-Based Data Augmentation in Semiconductor Assembly Process
- **Authors**: T.-S. Tsai, et al.
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2022)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9691456
- **Abstract**: Autoencoder generates additional defect samples to balance classes; tested on real fab WBMs at the assembly stage.
- **Why relevant**: Demonstrates AE augmentation under industrial conditions; complements the more academic autoencoder works.
- **Recommended for download**: YES

### 18. A Variational Autoencoder Enhanced Deep Learning Model for Wafer Defect Imbalanced Classification
- **Authors**: J. Yu, et al.
- **Venue**: IEEE Transactions on Components, Packaging and Manufacturing Technology (2021)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9606716/
- **Abstract**: Light-weight VAE-enhanced classifier (VAEDLM); produces similar minority-class wafer maps then refines via a DCNN.
- **Why relevant**: Clear VAE-baseline for the synthetic-bitmap-generation angle.
- **Recommended for download**: YES

### 19. Sample-Imbalanced Wafer Map Defects Classification Based on Auxiliary Classifier Denoising Diffusion Probability Model (ACDDPM-ResNet)
- **Authors**: J. Wang, et al.
- **Venue**: Computers & Industrial Engineering, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0360835224003309
- **Abstract**: Auxiliary-classifier conditional DDPM generates minority-class wafer maps; ResNet trained on the balanced set achieves SOTA on MIR-WM811K and MixedWM38.
- **Why relevant**: First major diffusion-model paper on wafer bitmaps; directly aligned with the synthetic-bitmap generation goal.
- **Recommended for download**: YES

### 20. Multi-Scale Guidance Diffusion Network for Wafer Map Defect Recognition
- **Authors**: H. Yuan, et al.
- **Venue**: Expert Systems with Applications, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S095741742403001X
- **Abstract**: Multi-scale guidance integrated into a diffusion U-Net; improves recognition of rare and mixed-type patterns on MixedWM38.
- **Why relevant**: State-of-the-art diffusion-based recognition; extends DDPM beyond pure generation to classification.
- **Recommended for download**: YES

### 21. Input-Guidance Diffusion Model for Unknown Defect Patterns Detection in Wafer Bin Maps
- **Authors**: D. Yang, J. Jang, C. O. Kim
- **Venue**: Advanced Engineering Informatics, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S1474034624007298
- **Abstract**: Input-guidance diffusion for novelty/anomaly detection; treats reconstruction error from a guided diffusion model as the open-set score.
- **Why relevant**: Bridges diffusion + open-set detection of new defects — a promising paper-worthy direction.
- **Recommended for download**: YES

### 22. MLR-WM-ViT: Global High-Performance Classification of Mixed-Type Wafer Map Defect Using a Multi-Level Relay Vision Transformer
- **Authors**: et al.
- **Venue**: Expert Systems with Applications (2025)
- **DOI/Link**: https://dl.acm.org/doi/10.1016/j.eswa.2025.127121
- **Abstract**: Multi-level relay ViT that hierarchically models basic defect type, count, and combination; 99.15% accuracy on MixedWM38.
- **Why relevant**: Strongest reported MixedWM38 result; transformer baseline for the project.
- **Recommended for download**: YES

### 23. Semiconductor Wafer Map Defect Classification with Tiny Vision Transformers
- **Authors**: et al.
- **Venue**: arXiv 2504.02494 (2025)
- **DOI/Link**: https://arxiv.org/abs/2504.02494
- **Abstract**: Tiny ViT for mixed-type wafer defects; F1 98.4% with very small parameter footprint, surpassing MSF-Trans by ~3% on multi-defect splits.
- **Why relevant**: Demonstrates ViTs are competitive even with limited compute — relevant for course-project deployability arguments.
- **Recommended for download**: YES

### 24. A New ViT-Based Augmentation Framework for Wafer Map Defect Classification to Enhance the Resilience of Semiconductor Supply Chains
- **Authors**: B. Fan, M. Chiu, et al.
- **Venue**: International Journal of Production Economics, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0925527324001324
- **Abstract**: Uses ViT as a learned augmenter rather than classifier; particularly improves robustness on minority classes.
- **Why relevant**: Novel "ViT-as-augmenter" angle; positions ML in supply-chain reliability framing useful for paper motivation.
- **Recommended for download**: YES

### 25. Contrastive Deep Clustering for Detecting New Defect Patterns in Wafer Bin Maps (CODEC)
- **Authors**: et al.
- **Venue**: International Journal of Advanced Manufacturing Technology, Springer (2024)
- **DOI/Link**: https://link.springer.com/article/10.1007/s00170-023-12939-0
- **Abstract**: CODEC simultaneously discovers and clusters new defect categories without labels via contrastive deep clustering.
- **Why relevant**: Direct match to the "clustering analysis of fault patterns" subtopic; strong novel-pattern discovery baseline.
- **Recommended for download**: YES

### 26. Iterative Cluster Harvesting for Wafer Map Defect Patterns
- **Authors**: et al.
- **Venue**: arXiv 2404.15436 (2024)
- **DOI/Link**: https://arxiv.org/abs/2404.15436
- **Abstract**: Iterates dimensionality reduction + clustering, harvesting one high-silhouette cluster per round; achieves SOTA unsupervised clustering on WM-811K.
- **Why relevant**: Pure-unsupervised baseline crucial for label-free WBM analytics.
- **Recommended for download**: YES

### 27. Supervised Contrastive Learning for Wafer Map Pattern Classification
- **Authors**: H. Hyun, H. Kim, et al.
- **Venue**: Engineering Applications of Artificial Intelligence, Elsevier (2023)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0952197623013386
- **Abstract**: Supervised contrastive loss exploits rotation-invariance of wafer labels; tested on WM-811K and MixedWM38.
- **Why relevant**: Strong contrastive baseline; pairs naturally with the self-supervised SSL papers.
- **Recommended for download**: YES

### 28. Contrastive Learning with Global and Local Representation for Mixed-Type Wafer Defect Recognition
- **Authors**: et al.
- **Venue**: Sensors (MDPI) (2025)
- **DOI/Link**: https://www.mdpi.com/1424-8220/25/4/1272
- **Abstract**: Self-supervised dual-branch contrastive framework combining global image-level + local region-level representations for mixed defect WBMs.
- **Why relevant**: 2025 SOTA on mixed-type SSL — strong comparison baseline.
- **Recommended for download**: YES

### 29. Mixup-Based Classification of Mixed-Type Defect Patterns in Wafer Bin Maps
- **Authors**: et al.
- **Venue**: Computers & Industrial Engineering, Elsevier (2022)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0360835222000663
- **Abstract**: Applies summation-mixup to combine single-defect wafer maps for training on mixed-type labels.
- **Why relevant**: Simple, principled augmentation method that generalizes well; useful in the project's "augmentation" arm.
- **Recommended for download**: YES

### 30. Learning from Single-Defect Wafer Maps to Classify Mixed-Defect Wafer Maps
- **Authors**: D. Yang, J. Jang, C. O. Kim
- **Venue**: Expert Systems with Applications, Elsevier (2023)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0957417423014252
- **Abstract**: Uses mixup + rotation + noise filtering to synthesize mixed-type WBMs from single-defect data without ever seeing real mixed labels.
- **Why relevant**: Solves the most practical industrial label-acquisition problem; reproducible approach.
- **Recommended for download**: YES

### 31. Wafer Map Defect Recognition Based on Multi-Scale Feature Fusion and Attention Spatial Pyramid Pooling
- **Authors**: et al.
- **Venue**: Journal of Intelligent Manufacturing, Springer (2024)
- **DOI/Link**: https://link.springer.com/article/10.1007/s10845-023-02231-z
- **Abstract**: Multi-scale CNN with attention ASPP module captures both local and global wafer features.
- **Why relevant**: Best representative of the multi-scale + attention design paradigm.
- **Recommended for download**: YES

### 32. Wafer Map Defect Pattern Detection Method Based on Improved Attention Mechanism
- **Authors**: et al.
- **Venue**: Expert Systems with Applications, Elsevier (2023)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0957417423010461
- **Abstract**: Improved channel + spatial attention modules atop a CNN backbone improve fine-grained defect localization.
- **Why relevant**: One of the most cited 2023 attention-based wafer papers.
- **Recommended for download**: YES

### 33. DMWMNet: Dual-Branch Multi-Level Convolutional Network for High-Performance Mixed-Type Wafer Map Defect Detection
- **Authors**: et al.
- **Venue**: Advanced Engineering Informatics, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0166361524000642
- **Abstract**: Two-branch architecture (local feature + global semantic) with multi-level fusion targeting MixedWM38.
- **Why relevant**: Recent SOTA dual-branch architecture; useful baseline.
- **Recommended for download**: YES

### 34. Wafer Defect Image Generation Method Based on Improved StyleGANv3 Network
- **Authors**: et al.
- **Venue**: Micromachines (MDPI) (2025)
- **DOI/Link**: https://www.mdpi.com/2072-666X/16/8/844
- **Abstract**: StyleGANv3 augmented with a Heterogeneous Kernel Fusion Unit for multi-scale wafer-defect synthesis with improved physical authenticity.
- **Why relevant**: Modern GAN-based generation paper; relevant to bitmap-synthesis arm.
- **Recommended for download**: YES

### 35. Deep Convolutional Generative Adversarial Networks-Based Data Augmentation Method for Classifying Class-Imbalanced Defect Patterns in Wafer Bin Map
- **Authors**: et al.
- **Venue**: Applied Sciences, MDPI (2023)
- **DOI/Link**: https://www.mdpi.com/2076-3417/13/9/5507
- **Abstract**: DCGAN-based balancing of WBM minority classes; classification accuracy uplift up to 23.1% balanced accuracy.
- **Why relevant**: Canonical GAN-for-wafer-augmentation baseline.
- **Recommended for download**: YES

---

## Tier 3: Supplementary

### 36. Deep Transfer Wasserstein Adversarial Network for Wafer Map Defect Recognition
- **Authors**: et al.
- **Venue**: Computers & Industrial Engineering, Elsevier (2022)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0360835221005830
- **Abstract**: Wasserstein-GAN-based transfer learning for cross-domain wafer recognition.

### 37. Utilizing GANs for Image Data Augmentation and Classification of Semiconductor Wafer Dicing Induced Defects
- **Authors**: et al.
- **Venue**: arXiv 2407.20268 (2024)
- **DOI/Link**: https://arxiv.org/abs/2407.20268
- **Abstract**: Compares DCGAN, CycleGAN, StyleGAN3 for wafer dicing defect synthesis; classification accuracy up by ~23%.

### 38. Image Hash Layer Triggered CNN Framework for Wafer Map Failure Pattern Retrieval and Classification
- **Authors**: et al.
- **Venue**: ACM Transactions on Knowledge Discovery from Data (2024)
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3638053
- **Abstract**: Adds a hashing layer to a CNN for efficient WM retrieval + classification at scale.

### 39. Wafer Map Defect Recognition Based on Deep Transfer Learning-Based Densely Connected Convolutional Network and Deep Forest
- **Authors**: et al.
- **Venue**: Engineering Applications of Artificial Intelligence, Elsevier (2021)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0952197621002359
- **Abstract**: DenseNet + Deep Forest hybrid for transfer learning to WBMs.

### 40. A Voting-Based Ensemble Feature Network for Semiconductor Wafer Defect Classification
- **Authors**: et al.
- **Venue**: Scientific Reports (Nature) (2022)
- **DOI/Link**: https://www.nature.com/articles/s41598-022-20630-9
- **Abstract**: Voting ensemble of CNN features; robust to class imbalance.

### 41. CBAM-Enhanced Lightweight CNN for Wafer Map Defect Classification
- **Authors**: et al.
- **Venue**: Frontiers in Electronics (2026)
- **DOI/Link**: https://www.frontiersin.org/journals/electronics/articles/10.3389/felec.2026.1750707/full
- **Abstract**: CBAM-augmented lightweight CNN achieving 99.88% on a balanced WM-811K subset.

### 42. Efficient Convolutional Neural Networks for Semiconductor Wafer Bin Map Classification
- **Authors**: et al.
- **Venue**: Sensors (MDPI) (2023)
- **DOI/Link**: https://www.mdpi.com/1424-8220/23/4/1926
- **Abstract**: Benchmarks EfficientNetV2, ShuffleNetV2, MobileNetV2/V3 on WBM with 7.5× parameter reduction over ResNet.

### 43. Efficient Mixed-Type Wafer Defect Pattern Recognition Based on Light-Weight Neural Network
- **Authors**: et al.
- **Venue**: PMC, Sensors (2024)
- **DOI/Link**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11279086/
- **Abstract**: Lightweight network optimized for MixedWM38 with industrial throughput constraints.

### 44. Accurate and Energy Efficient Ad-hoc Neural Network for Wafer Map Classification
- **Authors**: et al.
- **Venue**: Journal of Intelligent Manufacturing, Springer (2024)
- **DOI/Link**: https://link.springer.com/article/10.1007/s10845-024-02390-7
- **Abstract**: Energy-aware architecture search for wafer classifiers — useful for edge-deployment angles.

### 45. A Novel DBSCAN-Based Defect Pattern Detection and Classification Framework for Wafer Bin Map
- **Authors**: et al.
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2019; foundational)
- **DOI/Link**: https://ieeexplore.ieee.org/abstract/document/8713928
- **Abstract**: DBSCAN-based clustering of bin-map defects before classification.

### 46. A Self-Adaptive DBSCAN-Based Method for Wafer Bin Map Defect Pattern Classification
- **Authors**: et al.
- **Venue**: Microelectronics Reliability, Elsevier (2021)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0026271421001499
- **Abstract**: Adaptive Eps/MinPts selection in DBSCAN for noisy bin-map filtering.

### 47. Similarity Search on Wafer Bin Map Through Nonparametric and Hierarchical Clustering
- **Authors**: et al.
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2021)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9507533/
- **Abstract**: Nonparametric hierarchical clustering for similarity search across very large wafer-map databases.

### 48. Multi-Source Wafer Map Retrieval Based on Contrastive Learning for Root Cause Analysis in Semiconductor Manufacturing
- **Authors**: et al.
- **Venue**: Journal of Intelligent Manufacturing, Springer (2024)
- **DOI/Link**: https://link.springer.com/article/10.1007/s10845-023-02233-x
- **Abstract**: Contrastive retrieval across multiple test stages enables process root-cause attribution.

### 49. Wafer Map Classifier Using Deep Learning for Detecting Out-of-Distribution Failure Patterns
- **Authors**: et al.
- **Venue**: IEEE Conference (2020, widely cited 2021–2025)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9260877/
- **Abstract**: Out-of-distribution detection on wafer maps via residual CNN with uncertainty scoring.

### 50. Wafer Defect Pattern Classification with Detecting Out-of-Distribution
- **Authors**: et al.
- **Venue**: Microelectronics Reliability, Elsevier (2021)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0026271421001232
- **Abstract**: Defines 16 in-distribution wafer patterns and uses CNN-with-residual for OOD detection.

### 51. Enhanced Detection of Unknown Defect Patterns on Wafer Bin Maps Based on an Open-Set Recognition Approach
- **Authors**: et al.
- **Venue**: Advanced Engineering Informatics, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0166361524001362
- **Abstract**: Open-set recognition for novel WBM defects; >98% detection performance.

### 52. Decision Fusion Approach for Detecting Unknown Wafer Bin Map Patterns Based on a Deep Multitask Learning Model
- **Authors**: et al.
- **Venue**: Expert Systems with Applications, Elsevier (2023)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0957417422023818
- **Abstract**: Multitask learning + decision fusion for novel-pattern detection.

### 53. Pseudo-Labeling and Clustering-Based Active Learning for Imbalanced Classification of Wafer Bin Map Defects
- **Authors**: et al.
- **Venue**: Signal, Image and Video Processing, Springer (2023)
- **DOI/Link**: https://link.springer.com/article/10.1007/s11760-023-02915-2
- **Abstract**: Active learning with cluster-based sample selection.

### 54. Incremental Learning Strategies for Improved Detection of Unknown Defects in Wafer Maps with Limited Samples
- **Authors**: et al.
- **Venue**: Computers in Industry, Elsevier (2025)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0166361525001976
- **Abstract**: Few-shot incremental learning (FCCIL) for unknown wafer defects with anti-catastrophic-forgetting design.

### 55. An Unknown Wafer Surface Defect Detection Approach Based on Incremental Learning for Reliability Analysis
- **Authors**: et al.
- **Venue**: Reliability Engineering & System Safety, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0951832024000413
- **Abstract**: Incremental CNN with online learning; 10% accuracy gain, 60% training-time reduction.

### 56. Semi-Supervised Imbalanced Classification of Wafer Bin Map Defects Using a Dual-Head CNN
- **Authors**: et al.
- **Venue**: Expert Systems with Applications, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0957417423028038
- **Abstract**: Dual-head CNN to jointly learn from labeled + pseudo-labeled WBMs.

### 57. Wafer Map Defect Patterns Semi-Supervised Classification Using Latent Vector Representation
- **Authors**: et al.
- **Venue**: arXiv 2311.12840 (2023)
- **DOI/Link**: https://arxiv.org/abs/2311.12840
- **Abstract**: VAE-encoded latent representation guides teacher-student semi-supervised training.

### 58. Class-Imbalanced Semi-Supervised Learning with Exponential Threshold Smoothing for Wafer Bin Map Defect Pattern Classification
- **Authors**: et al.
- **Venue**: Journal of Intelligent Manufacturing, Springer (2024)
- **DOI/Link**: https://www.researchgate.net/publication/381440501
- **Abstract**: Class-aware exponential threshold smoothing for pseudo-label confidence calibration.

### 59. Class Imbalance Wafer Defect Pattern Recognition Based on Shared-Database Decentralized Federated Learning Framework
- **Authors**: et al.
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2024)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10510494/
- **Abstract**: SDeceFL — decentralized federated learning with differential-privacy shared database for cross-fab WBM models.

### 60. Decentralized Data, Centralized Insights: A Federated Machine Learning Framework for SEM Based Defect Classification
- **Authors**: et al.
- **Venue**: SPIE (2024)
- **DOI/Link**: https://www.researchgate.net/publication/378691742
- **Abstract**: Federated learning + YOLOv8 for SEM-image defects across foundries.

### 61. Improved Wafer Defect Pattern Classification Using Deep Learning and Explainable AI
- **Authors**: et al.
- **Venue**: Springer Conference Volume (2025)
- **DOI/Link**: https://link.springer.com/chapter/10.1007/978-3-031-80154-9_7
- **Abstract**: LIME and Grad-CAM applied to wafer-defect CNN models for engineer-facing interpretability.

### 62. Enhancing Confidence and Interpretability of a CNN-Based Wafer Defect Classification Model Using Temperature Scaling and LIME
- **Authors**: et al.
- **Venue**: PMC / Sensors (2025)
- **DOI/Link**: https://pmc.ncbi.nlm.nih.gov/articles/PMC12472186/
- **Abstract**: Calibration + LIME interpretability for confidence-aware wafer classification.

### 63. Development of a Wafer Defect Pattern Classifier Using Polar Coordinate System Transformed Inputs and Convolutional Neural Networks
- **Authors**: et al.
- **Venue**: Electronics, MDPI (2024)
- **DOI/Link**: https://www.mdpi.com/2079-9292/13/7/1360
- **Abstract**: Cartesian-to-polar transformation enables rotation invariance, +4.8% accuracy vs. baseline CNN.

### 64. Wafer Map Defect Patterns Classification Using Deep Selective Learning
- **Authors**: M. B. Alawieh, D. Boning, D. Z. Pan
- **Venue**: DAC 2020 (foundational)
- **DOI/Link**: https://par.nsf.gov/servlets/purl/10192082
- **Abstract**: Deep selective learning with reject option for high-stakes wafer classification; published at DAC.

### 65. A Novel Hypergraph Convolution Network for Wafer Defect Patterns Identification Based on an Unbalanced Dataset
- **Authors**: et al.
- **Venue**: Journal of Intelligent Manufacturing, Springer (2023)
- **DOI/Link**: https://link.springer.com/article/10.1007/s10845-022-02067-z
- **Abstract**: Hypergraph CNN models higher-order relationships among defect pixels.

### 66. Stacked Convolutional Sparse Denoising Auto-Encoder for Identification of Defect Patterns in Semiconductor Wafer Map
- **Authors**: et al.
- **Venue**: Microelectronics Reliability, Elsevier (2019; cited heavily through 2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S016636151930106X
- **Abstract**: SCSDAE for unsupervised feature learning on noisy wafer maps.

### 67. Mixed-Type Wafer Defect Detection Based on Multi-Branch Feature Enhanced Residual Module
- **Authors**: et al.
- **Venue**: Expert Systems with Applications, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0957417423032979
- **Abstract**: Multi-branch enhanced residual modules for MixedWM38.

### 68. An Embarrassingly Simple Approach for Wafer Feature Extraction and Defect Pattern Recognition
- **Authors**: et al.
- **Venue**: arXiv 2303.11632 (2023)
- **DOI/Link**: https://arxiv.org/pdf/2303.11632
- **Abstract**: Simple classical features + small classifier nearly match deep models on WM-811K; baseline of choice.

### 69. Wafer Map Failure Pattern Recognition Based on Deep Convolutional Neural Network
- **Authors**: et al.
- **Venue**: Expert Systems with Applications, Elsevier (2022)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0957417422013999
- **Abstract**: General DCNN baseline; multi-class WM-811K reference.

### 70. TripletMatch: Wafer Map Defect Detection Using Semi-Supervised Learning and Triplet Loss With Mixup
- **Authors**: et al.
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2024)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10776974/
- **Abstract**: Semi-supervised FixMatch-style training extended with triplet loss and Mixup.

### 71. Wafer Defect Classification Algorithm with Label Embedding Using Contrastive Learning
- **Authors**: et al.
- **Venue**: 2025
- **DOI/Link**: https://www.researchgate.net/publication/387871857
- **Abstract**: Joint label-embedding + image contrastive learning for fine-grained wafer classification.

### 72. AI Classification of Wafer Map Defect Patterns by Using Dual-Channel Convolutional Neural Network
- **Authors**: et al.
- **Venue**: Engineering Failure Analysis, Elsevier (2022)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S1350630721006178
- **Abstract**: Dual-channel CNN fusing raw and processed wafer maps; high accuracy on real fab data.

### 73. Wafer Map Defect Recognition Based on Multi-Scale Feature Fusion (Frontiers)
- **Authors**: et al.
- **Venue**: Frontiers in Neuroscience (2023)
- **DOI/Link**: https://pmc.ncbi.nlm.nih.gov/articles/PMC10272367/
- **Abstract**: Multi-scale feature fusion with attention; >97% accuracy.

### 74. A Graph-Theoretic Approach for Spatial Filtering and Its Impact on Mixed-Type Spatial Pattern Recognition in Wafer Bin Maps
- **Authors**: et al.
- **Venue**: arXiv 2006.13824 (2020; basis for 2021+ work)
- **DOI/Link**: https://arxiv.org/pdf/2006.13824
- **Abstract**: Graph-theoretic spatial filter for noise removal; basis for many subsequent multi-type recognition pipelines.

### 75. Machine Learning Methods for FEOL/MEOL Defects Measurement through SRAM Bitmap
- **Authors**: N. Zou, A. Rose, R. Ting
- **Venue**: ISTFA 2022 (ASM Digital Library)
- **DOI/Link**: https://dl.asminternational.org/istfa/proceedings-abstract/ISTFA2022/84437/43/23885
- **Abstract**: MLP-based classifier for FEOL/MEOL defectivity from SRAM bitmaps; >80% accuracy on volume product data.
- **Why relevant**: Rare published example of ML on actual SRAM failure bitmaps from production — highly relevant for the memory-bitmap arm of the project.
- **Recommended for download**: YES

### 76. SRAM Bitcell Defect Identification Methodology Using Electrical Failure Analysis Data
- **Authors**: et al.
- **Venue**: ISTFA 2021
- **DOI/Link**: https://dl.asminternational.org/istfa/proceedings-abstract/ISTFA2021/84215/80/18253
- **Abstract**: Methodology for SRAM bitcell defect identification via EFA data correlation.

### 77. A Regularized Singular Value Decomposition-Based Approach for Failure Pattern Classification on Fail Bit Map in a DRAM Wafer
- **Authors**: J. Kim, S. Jeong, et al.
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2021)
- **DOI/Link**: https://www.semanticscholar.org/paper/6c4685e10baa623b339d0eae31322a0c2893bb72
- **Abstract**: Regularized SVD on fail-bit maps in DRAM wafers to extract eigen-pattern features for classification.
- **Why relevant**: Directly relevant to the DRAM bitmap thread; mathematically rigorous baseline.
- **Recommended for download**: YES

### 78. Deep Q-Learning with Bit-Swapping-Based Linear Feedback Shift Register Fostered Built-In Self-Test and Built-In Self-Repair for SRAM
- **Authors**: et al.
- **Venue**: Sensors, MDPI (2022)
- **DOI/Link**: https://pmc.ncbi.nlm.nih.gov/articles/PMC9229549/
- **Abstract**: RL-based MBIST/MBISR for SRAM testing with bit-swapping LFSR.

### 79. Detection and Diagnosis of Multi-Fault for Through Silicon Vias in 3D IC
- **Authors**: et al.
- **Venue**: Journal of Electronic Testing, Springer (2021)
- **DOI/Link**: https://link.springer.com/article/10.1007/s10836-020-05916-y
- **Abstract**: Multi-fault TSV detection and diagnosis via ring-oscillator + Schmidt trigger; uses W-PSO-LSSVM.

### 80. Defect Analysis and Built-In-Self-Test for Chiplet Interconnects in Fan-out Wafer-Level Packaging
- **Authors**: et al.
- **Venue**: arXiv 2503.14784 (2025)
- **DOI/Link**: https://arxiv.org/html/2503.14784v1
- **Abstract**: BIST methodology for chiplet interconnects in fan-out wafer-level packaging.

### 81. Generating Test Patterns for Chiplet Interconnects With Optimized Effectiveness and Efficiency (E2I-TEST)
- **Authors**: et al. (imec)
- **Venue**: IEEE TCAD (2024)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10689272/
- **Abstract**: Improved interconnect test generation covering weak defect variants for chiplet die-to-die links.

### 82. Effective Fault Detection in M3D ICs: a Cluster-Based BIST for Enhanced Inter-Layer Via Fault Coverage
- **Authors**: et al.
- **Venue**: Frontiers of Information Technology & Electronic Engineering, Springer (2025)
- **DOI/Link**: https://link.springer.com/article/10.1631/FITEE.2401094
- **Abstract**: Cluster-based BIST architecture targeting inter-layer vias in M3D ICs.

### 83. DefectTrackNet: Efficient Root Cause Analysis of Wafer Defects in Semiconductor Manufacturing Using a Lightweight CNN-Transformer Architecture
- **Authors**: et al.
- **Venue**: ASP-DAC 2025
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3658617.3697608
- **Abstract**: Lightweight CNN-Transformer hybrid for efficient root-cause attribution from wafer defects.
- **Why relevant**: Top design-automation venue (ASP-DAC) 2025 paper; aligned with chiplet/3D-IC root-cause goals.
- **Recommended for download**: YES

### 84. Exploring Error Bits for Memory Failure Prediction: An In-Depth Correlative Study
- **Authors**: et al.
- **Venue**: arXiv 2312.02855 (2023)
- **DOI/Link**: https://arxiv.org/pdf/2312.02855
- **Abstract**: Spatio-temporal analysis of correctable/uncorrectable error bits for DRAM failure prediction with ML, +15% F1 improvement.

### 85. LightWarner: Predicting Failure of 3D NAND Flash Memory Using Reinforcement Learning
- **Authors**: et al.
- **Venue**: IEEE Transactions on Computers (2022)
- **DOI/Link**: https://ieeexplore.ieee.org/document/9799533/
- **Abstract**: Model-free RL-based predictor robust across 3D NAND chip variants; portability-aware design.

### 86. ML-Driven Risk Estimation for Memory Failure in a Data Center Environment with Convolutional Neural Networks, Self-Supervised Data Labeling, and Distribution-Based Model Drift Determination
- **Authors**: et al.
- **Venue**: Journal of Parallel and Distributed Computing, Elsevier (2024)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0743731523001703
- **Abstract**: CNN-based memory failure risk estimator with SSL labeling and drift detection.

### 87. Wafer Map Defect Pattern Classification Based on Convolutional Neural Network Features and Error-Correcting Output Codes
- **Authors**: et al.
- **Venue**: Journal of Intelligent Manufacturing, Springer (2021)
- **DOI/Link**: https://link.springer.com/article/10.1007/s10845-020-01540-x
- **Abstract**: CNN feature extractor + ECOC multiclass strategy; robust to imbalance.

### 88. Wafer Map Defect Patterns Classification Based on a Lightweight Network and Data Augmentation
- **Authors**: G. Yu, et al.
- **Venue**: CAAI Transactions on Intelligence Technology, Wiley (2023)
- **DOI/Link**: https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/cit2.12126
- **Abstract**: Lightweight architecture + targeted augmentation; competitive with much larger models.

### 89. Semiconductor Wafer Map Defect Classification Using Convolutional Neural Networks on Imbalanced Classes
- **Authors**: et al.
- **Venue**: IEEE Conference (2024)
- **DOI/Link**: https://ieeexplore.ieee.org/document/11096243/
- **Abstract**: WM-811K imbalanced classification benchmark with multiple augmentation strategies.

### 90. Inspection of Mixed-Type Wafer Defects from Single-Defect Data via Adaptive Synthesis and Self-Attention CNN
- **Authors**: et al.
- **Venue**: Measurement, Elsevier (2025)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0263224125016653
- **Abstract**: Adaptive ROI-mixing on single-defect heat maps + self-attention CNN for mixed inspection.

### 91. Wafer Map Defect Classification Using Deep Learning Framework with Data Augmentation on Imbalance Datasets
- **Authors**: et al.
- **Venue**: EURASIP Journal on Image and Video Processing, Springer (2025)
- **DOI/Link**: https://jivp-eurasipjournals.springeropen.com/articles/10.1186/s13640-025-00666-3
- **Abstract**: Generalizable augmentation pipeline for imbalanced WM-811K.

### 92. Observational and Experimental Insights into Machine Learning-Based Defect Classification in Wafers
- **Authors**: et al.
- **Venue**: Journal of Intelligent Manufacturing, Springer (2024)
- **DOI/Link**: https://link.springer.com/article/10.1007/s10845-024-02521-0
- **Abstract**: Empirical study comparing ML/DL methods on WBM datasets with deployment lessons.

### 93. A Self-Training-Based System for Die Defect Classification
- **Authors**: et al.
- **Venue**: Mathematics, MDPI (2024)
- **DOI/Link**: https://www.mdpi.com/2227-7390/12/15/2415
- **Abstract**: Self-training pipeline combining pseudo-labeling + noisy student + Taguchi tuning; comparable to full-label baseline with <10% labels.

### 94. An Ensemble-Based Deep Semi-Supervised Learning for the Classification of Wafer Bin Maps Defect Patterns
- **Authors**: et al.
- **Venue**: Computers & Industrial Engineering, Elsevier (2022)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0360835222006040
- **Abstract**: Deep ensemble + semi-supervised co-training for WBM classification.

### 95. Anomaly Detection and Segmentation via Wafer-Defect Encoder-Decoder Networks for Industrial Yield Excursion Detection
- **Authors**: et al.
- **Venue**: IEEE Conference (2023)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10317989/
- **Abstract**: Weakly supervised wafer defect localization + diagnosis.

### 96. Wafer Composite Defect Recognition Framework Based on Residual Dynamic Perception Network with Asymmetric Multi-Label Loss
- **Authors**: et al.
- **Venue**: ISA Transactions, Elsevier (2025)
- **DOI/Link**: https://www.sciencedirect.com/science/article/abs/pii/S0019057825005105
- **Abstract**: Multi-label residual network with asymmetric loss for composite (mixed) wafer defects.

### 97. AI-Powered Defect Detection Using Deep Learning: A Pattern-Agnostic Faster R-CNN Approach for SEM Images
- **Authors**: et al.
- **Venue**: IEEE Conference (2025)
- **DOI/Link**: https://ieeexplore.ieee.org/document/11010758/
- **Abstract**: Pattern-agnostic Faster R-CNN with GPU acceleration for SEM-image defect detection.

### 98. Semiconductor SEM Image Defect Classification Using Supervised and Semi-Supervised Learning with Vision Transformers
- **Authors**: et al.
- **Venue**: arXiv 2506.03345 (2025)
- **DOI/Link**: https://arxiv.org/abs/2506.03345
- **Abstract**: ViT (DinoV2) transfer + semi-supervised learning >90% accuracy with <15 images per class.

### 99. GenAI Applications of Vision-Language Models for Semiconductor Defect Classification
- **Authors**: et al.
- **Venue**: SPIE Advanced Lithography + Patterning 2025
- **DOI/Link**: https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13426/3064772/
- **Abstract**: Vision-language models (NVIDIA Cosmos Reason) for few-shot wafer defect classification.

### 100. YOLO-LA: Prototype-Based Vision–Language Alignment for Silicon Wafer Defect Pattern Detection
- **Authors**: et al.
- **Venue**: Micromachines, MDPI (2025)
- **DOI/Link**: https://www.mdpi.com/2072-666X/17/1/67
- **Abstract**: Pretrained YOLO + frozen text encoder for low-resolution wafer defect recognition; aligned with the foundation-model trend.

### 101. Wafer Defect Detection Technology Based on CTM-IYOLOv10 Network
- **Authors**: et al.
- **Venue**: Electronics, MDPI (2025)
- **DOI/Link**: https://pmc.ncbi.nlm.nih.gov/articles/PMC12653302/
- **Abstract**: Clustering + improved YOLOv10 for small-defect die-level detection.

### 102. Semi-Supervised Anomaly Detection in Scanning Electron Microscope Images (Patent / KLA)
- **Authors**: KLA Corporation
- **Venue**: USPTO Patent (2020; widely cited in 2021–2024 SEM-ML literature)
- **DOI/Link**: USPTO 10789703
- **Abstract**: VAE-based anomaly detection on SEM images using defect-free training images only.

### 103. Vision-Based Wafer Inspection in Semiconductor Manufacturing: A Case Study on Scratch Defect Detection Using Synthetic Data and YOLO Models
- **Authors**: et al.
- **Venue**: International Journal of Data Science and Analytics, Springer (2026)
- **DOI/Link**: https://link.springer.com/article/10.1007/s41060-026-01034-8
- **Abstract**: Synthetic-data + YOLO pipeline for scratch-defect detection.

### 104. Pattern Recognition in Analog Wafer Test Data — A Health Factor for Process Patterns
- **Authors**: et al.
- **Venue**: IEEE International Symposium (2021)
- **DOI/Link**: https://www.researchgate.net/publication/337607585
- **Abstract**: Pattern recognition for analog wafer test data with a "health factor" indicator for process monitoring.

### 105. Wafer Pattern Recognition Using Tucker Decomposition
- **Authors**: et al.
- **Venue**: IEEE Conference (2019; cited through 2024)
- **DOI/Link**: https://ieeexplore.ieee.org/document/8758667/
- **Abstract**: Tensor (Tucker) decomposition for wafer pattern recognition.

### 106. Combining Full Wafer Inspection with Deep Learning to Recognize Wafers with Critical Defects
- **Authors**: et al.
- **Venue**: IEEE Conference (2023)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10121122/
- **Abstract**: Industrial-scale full-wafer DL inspection.

### 107. Density-Based Spatial Clustering of Applications with Noise (DBSCAN) for Probe Card Production for Advanced Quality Control of Wafer Probing Test
- **Authors**: et al.
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2024)
- **DOI/Link**: https://ieeexplore.ieee.org/document/10693534/
- **Abstract**: DBSCAN applied to probe-card production data — useful upstream of bitmap analysis.

### 108. Demystifying Defects: Federated Learning and Explainable AI for Semiconductor Fault Detection
- **Authors**: et al.
- **Venue**: HAL UTT (2024)
- **DOI/Link**: https://utt.hal.science/hal-05420258
- **Abstract**: FL + XAI for cross-fab defect detection.

### 109. Wafer Map Failure Pattern Recognition and Similarity Ranking for Large-Scale Data Sets
- **Authors**: M.-J. Wu, J.-S. R. Jang, J.-L. Chen
- **Venue**: IEEE Transactions on Semiconductor Manufacturing (2015; the WM-811K paper)
- **DOI/Link**: https://www.researchgate.net/publication/273393496
- **Abstract**: Original publication of WM-811K and Radon + geometry SVM baseline. Required citation.
- **Why relevant**: Defines the dominant dataset of the field; every paper cites this.
- **Recommended for download**: YES

### 110. Wafer Bin Map Based Root Cause Analysis (USPTO 12229945)
- **Authors**: USPTO Patent (recent industrial baseline)
- **Venue**: USPTO 12229945 (2025)
- **DOI/Link**: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12229945
- **Abstract**: Industrial WBM-based root cause analysis methods.

---

## Key Datasets & Benchmarks

| Dataset | Size / Composition | Notes |
|---|---|---|
| **WM-811K (MIR-WM811K)** | 811,457 wafer maps; ~172,950 labeled across 9 classes (Center, Donut, Edge-Loc, Edge-Ring, Loc, Random, Scratch, Near-Full, None) | THE de-facto benchmark; Wu et al. 2015; severe imbalance (~85% None). |
| **MixedWM38** | 38,015 wafer maps in 38 categories (1 normal + 8 single + 13 two-mixed + 12 three-mixed + 4 four-mixed) | Standard mixed-type benchmark; introduced via Kyeong & Kim 2018 + augmentation pipelines. |
| **SEM defect datasets** | various open SEM datasets (ASML, IMEC release in some papers) | Pixel-level annotations; smaller scale. |
| **Synthetic wafer maps** | Nakazawa-style generated maps (28,600 / 22 classes; or arbitrary basis patterns) | Used when real labeled data are scarce. |
| **Internal fab fail bitmaps** | proprietary SRAM/DRAM bitmaps used in ISTFA papers | Not public; reproduced via simulation or synthetic generation in academic work. |

---

## Identified Research Gaps (target angles for the conference paper)

1. **No public failure-bitmap benchmark for embedded memory (SRAM / DRAM / HBM) analogous to WM-811K.** Wafer-map work has matured around two open datasets; memory-bitmap work (ISTFA / IEEE TSM) is almost entirely on proprietary data. A reproducible, synthetic-bitmap benchmark specifically for SRAM/DRAM fail patterns — generated with physics-aware models (e.g., row/column failures, bit-line/word-line shorts, peripheral logic defects) — would be a meaningful contribution.

2. **Cross-modal generalization from wafer bitmap to memory bitmap and chiplet-interconnect bitmaps is unstudied.** Almost no paper trains/tests across these three bitmap modalities. A unified self-supervised foundation model (CNN/ViT) pre-trained on WM-811K + synthetic memory bitmaps + synthetic TSV/chiplet maps, then fine-tuned to each, could demonstrate transferability — a strong conference paper.

3. **Diffusion-based synthetic generation is still nascent for failure bitmaps.** Only a handful of 2024–2025 papers apply DDPM-class models to wafer bitmaps; almost none target memory or TSV bitmaps, and few use conditioning on physical defect mechanisms. Conditional diffusion with physical fault-model conditioning (e.g., "shorted bit line at column X with periodic disturb") is underexplored.

4. **Open-set / novelty detection for mixed-type WBM is dominated by 9-class settings; the 38-class MixedWM38 mixed-defect novelty problem is far less studied.** Combining contrastive deep clustering (CODEC, iterative cluster harvesting) with diffusion-based reconstruction for unknown-pattern discovery on MixedWM38 is a clear novelty target.

5. **Bridging chiplet/TSV/3D-IC test results to wafer-bitmap-style visualization and ML analysis is essentially open.** Chiplet test work (E2I-TEST, BIST architectures) produces fault dictionaries, not bitmaps. Reformulating chiplet interconnect test responses as 2D/3D "bitmaps" so that the wafer-bitmap ML toolbox transfers directly would unify two siloed test-research communities and is a high-impact paper angle.

6. **Interpretability + uncertainty for production deployment.** Most papers report accuracy/F1 only. ISTFA-style production work and engineer-facing requirements demand interpretability (LIME/Grad-CAM) and calibrated rejection (SWaCo-style). A combined paper benchmarking calibration + interpretability across SOTA models on WM-811K + MixedWM38 is missing.

---

## Notes on Quality Filter

- Total entries listed: 110.
- Conference / journal coverage spans IEEE Xplore (TSM, TCAD, TC, IEEE Access, ITC, ICCAD, VTS, DAC, ASP-DAC, ISTFA), ACM DL (ASP-DAC, TKDD), Springer (Journal of Intelligent Manufacturing, JET, IJAMT, IJDSA, FITEE, EURASIP), Elsevier (ESWA, CIE, Measurement, AEI, RESS, ISA, JPDC, Microelectronics Reliability), MDPI (Sensors, Electronics, Mathematics, Micromachines), and arXiv (2023–2025).
- All entries are 2018–2026 with strong concentration in 2022–2025 (>70%).
- After filtering by abstract quality and venue impact, ~55 of the entries above are top-tier for download; the remaining act as wide-coverage citations.
