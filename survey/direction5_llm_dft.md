# Direction 5: LLM for DFT/Testing — Literature Survey

> **Course project**: VLSI Test (2026 Spring) — Mini Research Project aiming for conference paper submission.
> **Scope**: Applications of LLMs (GPT-4, Llama, Claude, etc.) in DFT and VLSI testing — testbench generation, fail-log interpretation, DFT/scan/ATPG configuration, RTL bug detection, assertion generation, RAG for hardware, structured reasoning for diagnosis, LLM agents for EDA.
> **Compiled**: May 2026. Covers IEEE/ACM/Springer venues (DAC, ICCAD, DATE, MLCAD, ITC, VTS, ETS, ASP-DAC, TCAD, TODAES, TVLSI) + arXiv preprints (this is a fast-moving area).

---

## Tier 1: Must-Read Papers (Directly Tackle LLM for DFT / Testing / Testbench / Fail Logs)

### 1. DFTAgent / LLM Agents as Catalysts for Resilient DFT: An Orchestration-Based Framework Beyond Brittle Scripts
- **Authors**: (MDPI Applied Sciences authors, 2025)
- **Venue**: Applied Sciences, MDPI (2025), Vol. 15, Iss. 21, p. 11390
- **DOI/Link**: https://www.mdpi.com/2076-3417/15/21/11390
- **Abstract**: Proposes DFTAgent, a framework leveraging LLMs to intelligently orchestrate a complete DFT toolchain. The agent abstracts complex EDA DFT tools behind a natural-language interface and a visual workflow, completing the full ATPG task cycle with fault coverage comparable to manually-scripted baselines while exhibiting flexibility and error-handling advantages over brittle Tcl scripts.
- **Why relevant**: Most directly aligned paper for this project — explicitly couples LLM agents with DFT/ATPG flow. Highly transferable as a baseline.
- **Recommended for download**: YES

### 2. Towards LLM-based Root Cause Analysis of Hardware Design Failures
- **Authors**: arXiv 2507.06512 (2025)
- **Venue**: IEEE LAD 2025 / arXiv:2507.06512
- **DOI/Link**: https://arxiv.org/abs/2507.06512
- **Abstract**: Studies how LLMs assist in explaining root causes of design issues and bugs revealed during synthesis and simulation. OpenAI o3-mini reaches correct determination 100% of the time at pass@5; state-of-the-art models exceed 80% (>90% with RAG augmentation).
- **Why relevant**: Direct match for the "automatic interpretation of fail logs / debug suggestions" project objective.
- **Recommended for download**: YES

### 3. FVDebug: An LLM-Driven Debugging Assistant for Automated Root Cause Analysis of Formal Verification Failures
- **Authors**: NVIDIA Research, arXiv 2510.15906 (2025)
- **Venue**: NVIDIA Research / arXiv:2510.15906
- **DOI/Link**: https://arxiv.org/abs/2510.15906
- **Abstract**: Automates analysis of formal-verification counter-examples spanning multiple cycles. Builds a Causal Graph from waveforms + RTL + spec to transform failure traces into actionable fixes. Achieves 95.6% hypothesis quality for root cause and 71.1%/86.8% Pass@1/@5 fix rates on 38 real hardware failures.
- **Why relevant**: Reference architecture for waveform + log fusion debugging — direct inspiration for project pipeline.
- **Recommended for download**: YES

### 4. LLM-Powered EDA Log Analysis for Effective Design Debugging
- **Authors**: Rohit Kanagal (UC Berkeley EECS Tech Report 2025-48)
- **Venue**: UC Berkeley EECS Technical Report 2025-48 (2025)
- **DOI/Link**: https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-48.pdf
- **Abstract**: LLM-assisted EDA tool log analysis using GPT-4 to interpret compile/synthesis errors and provide natural-language explanations. Combines custom RAG to inject task-specific prior knowledge.
- **Why relevant**: Almost a turnkey reference design for the project's fail-log interpretation goal. Includes RAG which is explicitly recommended in the project specs.
- **Recommended for download**: YES

### 5. ChipNeMo: Domain-Adapted LLMs for Chip Design
- **Authors**: M. Liu, T.-D. Ene, R. Kirby, et al. (NVIDIA)
- **Venue**: ICCAD 2023 / arXiv:2311.00176
- **DOI/Link**: https://arxiv.org/abs/2311.00176
- **Abstract**: Industrial domain-adaptation of LLaMA2 for chip design: domain-adaptive tokenization, continued pretraining, instruction alignment, and domain-adapted retrieval. Evaluated on engineering assistant chatbot, EDA-script generation, and bug summarization. 70B model outperforms GPT-4 on chatbot and EDA-scripts; up to 5x model-size reduction with similar/better performance.
- **Why relevant**: Canonical industry reference. Covers bug analysis + chatbot + EDA scripting — three project-relevant pillars in one paper.
- **Recommended for download**: YES

### 6. VerilogEval: Evaluating Large Language Models for Verilog Code Generation
- **Authors**: M. Liu, N. Pinckney, B. Khailany, H. Ren (NVIDIA)
- **Venue**: ICCAD 2023 / arXiv:2309.07544; v2 in 2024
- **DOI/Link**: https://arxiv.org/abs/2309.07544; https://github.com/NVlabs/verilog-eval
- **Abstract**: Benchmark of 156 HDLBits problems with automated functional testing. Defines the standard for evaluating LLM Verilog code-completion. v2 extends to specification-to-RTL tasks with iverilog error categorization.
- **Why relevant**: Standard benchmark we will use to compare methods.
- **Recommended for download**: YES

### 7. RTLLM: An Open-Source Benchmark for Design RTL Generation with Large Language Model
- **Authors**: Y. Lu, S. Liu, Q. Zhang, Z. Xie (HKUST)
- **Venue**: ASP-DAC 2024 / arXiv:2308.05345
- **DOI/Link**: https://arxiv.org/abs/2308.05345; https://github.com/hkust-zhiyao/RTLLM
- **Abstract**: 30 (v2: 50) hand-crafted designs with natural-language specs, golden testbenches, and reference RTL. Defines syntax / functionality / design-quality goals for systematic LLM RTL evaluation via synthesis, simulation, and PPA.
- **Why relevant**: Second pillar benchmark. Pair with VerilogEval as our evaluation harness.
- **Recommended for download**: YES

### 8. AssertLLM: Generating and Evaluating Hardware Verification Assertions from Design Specifications via Multi-LLMs
- **Authors**: W. Fang, M. Li, M. Lu, et al.
- **Venue**: ASP-DAC 2025 / arXiv:2402.00386
- **DOI/Link**: https://arxiv.org/abs/2402.00386
- **Abstract**: Three customized LLMs for extracting structural specs, mapping signal definitions, and generating assertions. Handles natural language + waveform diagrams. 89% syntactically and functionally correct assertions on full-design eval.
- **Why relevant**: Premier paper for spec-to-assertion — the exact "DFT configuration / property generation" we want to study.
- **Recommended for download**: YES

### 9. RTLFixer: Automatically Fixing RTL Syntax Errors with Large Language Models
- **Authors**: Y.-D. Tsai, M. Liu, H. Ren (NVIDIA)
- **Venue**: DAC 2024 / arXiv:2311.16543
- **DOI/Link**: https://arxiv.org/abs/2311.16543; https://github.com/NVlabs/RTLFixer
- **Abstract**: Combines RAG + ReAct prompting to make the LLM an autonomous debugging agent. Resolves 98.5% of compilation errors on 212-error VerilogEval-derived debug dataset.
- **Why relevant**: Strong baseline for the project's "automatic debug suggestions" objective; demonstrates exactly the RAG+reasoning pattern.
- **Recommended for download**: YES

### 10. LLM4DV: Using Large Language Models for Hardware Test Stimuli Generation
- **Authors**: Z. Zhang, G. Chadwick, H. McNally, Y. Zhao, R. Mullins
- **Venue**: arXiv 2310.04535 (NeurIPS workshop) / IEEE 2024
- **DOI/Link**: https://arxiv.org/abs/2310.04535
- **Abstract**: Framework using LLMs to automate test-stimulus generation. Six prompt enhancements. Reaches 89.74–100% coverage on 8 hardware designs; 98.94% on data prefetcher; outperforms constrained-random testing on a CPU.
- **Why relevant**: Most directly comparable existing system for "LLM generates stimuli for testing" — central to the project objective.
- **Recommended for download**: YES

### 11. UVM² / From Concept to Practice: an Automated LLM-aided UVM Machine for RTL Verification
- **Authors**: arXiv 2504.19959 (2025)
- **Venue**: arXiv:2504.19959 (2025)
- **DOI/Link**: https://arxiv.org/abs/2504.19959
- **Abstract**: First systematic framework for automated, LLM-driven UVM testbench generation: domain-knowledge-guided prompts + syntactic constraints; iteratively refines stimuli via coverage feedback. Mirrors expert workflows in a closed-loop, coverage-driven manner.
- **Why relevant**: Directly tackles UVM testbench generation (project specs explicitly call this out).
- **Recommended for download**: YES

### 12. HAVEN: Hybrid Automated Verification ENgine for UVM Testbench Synthesis with LLMs
- **Authors**: arXiv 2604.27643 (2026)
- **Venue**: arXiv:2604.27643 (2026)
- **DOI/Link**: https://arxiv.org/abs/2604.27643
- **Abstract**: Prevents LLM from writing HDL directly; instead uses it to plan a structured architectural plan, then template-driven UVM-component generation guarantees protocol-correct bus-handshake timing. 100% compile success, 90.6% code / 87.9% functional coverage on 19 open-source IPs.
- **Why relevant**: Important alternative philosophy (LLM-for-planning, not LLM-for-code) — must-contrast in our paper.
- **Recommended for download**: YES

### 13. AutoBench / CorrectBench: Automatic Testbench Generation with Self-Correction using LLMs for HDL Design
- **Authors**: R. Qiu et al. (CorrectBench arXiv 2411.08510); AutoBench arXiv 2407.03891
- **Venue**: arXiv 2407.03891 (AutoBench), 2411.08510 (CorrectBench) — 2024
- **DOI/Link**: https://arxiv.org/abs/2407.03891; https://arxiv.org/abs/2411.08510
- **Abstract**: AutoBench is the first LLM-automated hybrid testbench framework — 57% improvement in pass@1 testbench ratio. CorrectBench adds functional self-validation and self-correction.
- **Why relevant**: Concrete state-of-the-art systems for the project's automated testbench-generation theme.
- **Recommended for download**: YES

### 14. FIXME: Towards End-to-End Benchmarking of LLM-Aided Design Verification
- **Authors**: arXiv 2507.04276 (2025)
- **Venue**: arXiv:2507.04276 (2025)
- **DOI/Link**: https://arxiv.org/abs/2507.04276
- **Abstract**: First end-to-end, multi-model, open-source evaluation framework for assessing LLM performance in hardware functional verification. Addresses the gap where prior work focused mainly on RTL generation rather than functional verification.
- **Why relevant**: Provides the benchmark we will use to evaluate our verification/debug pipeline against published baselines.
- **Recommended for download**: YES

### 15. Chip-Chat: Challenges and Opportunities in Conversational Hardware Design
- **Authors**: J. Blocklove, S. Garg, R. Karri, H. Pearce (NYU)
- **Venue**: MLCAD 2023 / IEEE; arXiv:2305.13243
- **DOI/Link**: https://arxiv.org/abs/2305.13243
- **Abstract**: Case study of an engineer co-architecting an 8-bit accumulator microprocessor with ChatGPT-4. Resulted in the world's first AI-written HDL taped out at Skywater 130 nm. Discusses LLM-as-design-assistant patterns.
- **Why relevant**: The canonical "what's possible / what's hard" qualitative paper to motivate the project's introduction.
- **Recommended for download**: YES

---

## Tier 2: Important Supporting Papers (LLM for Hardware Design, RAG, Agents, Bug Detection)

### 16. VeriDebug: A Unified LLM for Verilog Debugging via Contrastive Embedding and Guided Correction
- **Authors**: arXiv 2504.19099 (2025)
- **Venue**: arXiv:2504.19099 (2025)
- **DOI/Link**: https://arxiv.org/abs/2504.19099
- **Abstract**: Iterative debugging loop (simulation → error localization → correction). 64.7% accuracy on a buggy-Verilog dataset (open-source baselines 11.3%, GPT-3.5-turbo 36.6%). 91% on VerilogEval bench.
- **Why relevant**: Strong technical baseline for LLM-driven Verilog debug.
- **Recommended for download**: YES

### 17. Location-is-Key (LiK): Leveraging Large Language Model for Functional Bug Localization in Verilog
- **Authors**: arXiv 2409.15186 (2024)
- **Venue**: arXiv:2409.15186 (2024)
- **DOI/Link**: https://arxiv.org/abs/2409.15186
- **Abstract**: Open-source LLM solution focused on bug localization in Verilog. 93.3% pass@1 localization vs. GPT-4 at 77.9%. Combined with GPT-3.5 raises bug-fix pass@1 from 40.4% to 58.9%.
- **Why relevant**: Localization is the natural pairing for fail-log analysis. Open-source.

### 18. MEIC: Re-thinking RTL Debug Automation using LLMs
- **Authors**: arXiv 2405.06840 (2024)
- **Venue**: ICCAD 2024 / arXiv:2405.06840
- **DOI/Link**: https://arxiv.org/abs/2405.06840; https://dl.acm.org/doi/10.1145/3676536.3676801
- **Abstract**: Multi-LLM iterative debugging framework treating LLM uncertainty like human-engineer variability. Multiple agents debug to error-free state or coverage threshold.
- **Why relevant**: Multi-agent design pattern we may adopt; published at ICCAD.

### 19. VeriRAG: A Retrieval-Augmented Framework for Automated RTL Testability Repair
- **Authors**: arXiv 2507.15664 (2025)
- **Venue**: arXiv:2507.15664 (2025)
- **DOI/Link**: https://arxiv.org/abs/2507.15664
- **Abstract**: Autoencoder + contrastive-learning retrieval + iterative error correction guided by compiler diagnostics and DFT error reports for RTL testability repair.
- **Why relevant**: One of the few papers explicitly tackling testability (DFT) repair with LLM+RAG.
- **Recommended for download**: YES

### 20. LLM4SecHW: Leveraging Domain-Specific Large Language Model for Hardware Debugging
- **Authors**: W. Fu et al. (Kansas State + collaborators)
- **Venue**: AsianHOST 2023 / arXiv:2401.16448
- **DOI/Link**: https://arxiv.org/abs/2401.16448
- **Abstract**: Compiles dataset of open-source hardware defects from version-control history. Fine-tunes 7B LLMs (StableLM, Falcon, LLaMA2) with LLaMA-Adapter V2 for hardware bug ID & repair.
- **Why relevant**: Important "dataset-from-Git" methodology — relevant to building a fail-log dataset.

### 21. AutoChip: Automating HDL Generation Using LLM Feedback
- **Authors**: S. Thakur et al.
- **Venue**: arXiv 2311.04887 / LAD 2024
- **DOI/Link**: https://arxiv.org/abs/2311.04887
- **Abstract**: Greedy tree-search using compilation + simulation feedback to iteratively refine LLM-generated Verilog. GPT-3.5/GPT-4 ensemble reaches 89.19% on 120-problem benchmark.
- **Why relevant**: Reference for the iterative feedback architecture our debug pipeline can adopt.

### 22. ChatEDA: A Large Language Model Powered Autonomous Agent for EDA
- **Authors**: H. Wu et al. (CUHK)
- **Venue**: IEEE TCAD 2024 / arXiv:2308.10204
- **DOI/Link**: https://arxiv.org/abs/2308.10204
- **Abstract**: LLM-driven autonomous agent for full RTL-to-GDSII flow via API-driven EDA tools. AutoMage fine-tuned LLM beats GPT-4. 98.3% task-decomposition success.
- **Why relevant**: Most cited "LLM agent for EDA flow" paper; structural reference for project agent.

### 23. AutoEDA: Enabling EDA Flow Automation through Microservice-Based LLM Agents
- **Authors**: arXiv 2508.01012 (2025)
- **Venue**: arXiv:2508.01012 (2025)
- **DOI/Link**: https://arxiv.org/abs/2508.01012
- **Abstract**: MCP-based servers for task decomposition, tool selection, automated error handling. 9.9× higher accuracy, 97% token reduction vs. naïve approach.
- **Why relevant**: Modern microservice/MCP pattern — relevant to scalable agent design.

### 24. Customized Retrieval Augmented Generation and Benchmarking for EDA Tool Documentation QA
- **Authors**: Y. Pu et al.
- **Venue**: ICCAD 2024 / arXiv:2407.15353
- **DOI/Link**: https://arxiv.org/abs/2407.15353
- **Abstract**: Customized RAG with contrastive-trained text embeddings, distilled rerankers, and fine-tuned generative models for EDA documentation QA.
- **Why relevant**: Must-read template for our RAG component over DFT/testing docs.
- **Recommended for download**: YES

### 25. AssertGen: Enhancement of LLM-aided Assertion Generation through Cross-Layer Signal Bridging
- **Authors**: arXiv 2509.23674 (2025)
- **Venue**: IEEE ATS 2025 / arXiv:2509.23674
- **DOI/Link**: https://arxiv.org/abs/2509.23674
- **Abstract**: Chain-of-thought extraction of verification objectives from specs; bridges cross-layer signal chains between spec and RTL; generates SVAs.
- **Why relevant**: Newer ATS 2025 paper directly on the assertion-generation thread.

### 26. SANGAM: SystemVerilog Assertion Generation via Monte Carlo Tree Self-Refine
- **Authors**: arXiv 2506.13983 (2025)
- **Venue**: arXiv:2506.13983 (2025)
- **DOI/Link**: https://arxiv.org/abs/2506.13983
- **Abstract**: LLM-guided MCTS for industry-level spec → SVA generation.
- **Why relevant**: Tree-search-augmented LLM reasoning — a methodological idea to consider.

### 27. UVLLM: An Automated Universal RTL Verification Framework using LLMs
- **Authors**: arXiv 2411.16238 (2024)
- **Venue**: arXiv:2411.16238 (2024)
- **DOI/Link**: https://arxiv.org/abs/2411.16238
- **Abstract**: End-to-end hardware design verification using UVM + LLMs.
- **Why relevant**: One of the broader UVM-integration frameworks.

### 28. UVMarvel: an Automated LLM-aided UVM Machine for Subsystem-level RTL Verification
- **Authors**: arXiv 2605.04704 (2026)
- **Venue**: arXiv:2605.04704 (2026)
- **DOI/Link**: https://arxiv.org/abs/2605.04704
- **Abstract**: Subsystem-level UVM testbench framework. 95.65% code coverage; verification time 4.5h vs. days for manual.
- **Why relevant**: Subsystem-level extension of LLM UVM work.

### 29. VerilogReader: LLM-Aided Hardware Test Generation
- **Authors**: R. Ma, Y. Yang, Z. Liu, J. Zhang, M. Li, J. Huang, G. Luo
- **Venue**: ICCAD 2024 / arXiv:2406.04373
- **DOI/Link**: https://arxiv.org/abs/2406.04373
- **Abstract**: LLM as a Verilog reader for Coverage-Directed Test Generation, with Verilator simulation + coverage feedback to drive new stimulus generation.
- **Why relevant**: Coverage-directed loop pattern — likely to inform our experiment design.

### 30. RTLCoder: Fully Open-Source and Efficient LLM-Assisted RTL Code Generation
- **Authors**: S. Liu, W. Fang, Y. Lu, J. Wang, Q. Zhang, H. Geng, Z. Xie (HKUST)
- **Venue**: IEEE TCAD 2025 / arXiv:2312.08617
- **DOI/Link**: https://arxiv.org/abs/2312.08617; https://github.com/hkust-zhiyao/RTL-Coder
- **Abstract**: 27k instruction-code pairs; quality-feedback training; 7B model trained on 4 GPUs. First open-source LLM beating GPT-3.5 on RTL benchmarks.
- **Why relevant**: We may use this as our base RTL-generation engine when building a closed-loop.
- **Recommended for download**: YES

### 31. VeriGen: A Large Language Model for Verilog Code Generation
- **Authors**: S. Thakur, B. Ahmad, et al.
- **Venue**: ACM TODAES 2024 / arXiv:2308.00708
- **DOI/Link**: https://arxiv.org/abs/2308.00708; https://github.com/shailja-thakur/VGen
- **Abstract**: Fine-tunes CodeGen on Verilog from GitHub + textbooks. Outperforms commercial Codex on functional correctness.
- **Why relevant**: The first widely-used open-source Verilog LLM. Foundational.

### 32. BetterV: Controlled Verilog Generation with Discriminative Guidance
- **Authors**: Z. Pei et al. (CUHK)
- **Venue**: ICML 2024 / arXiv:2402.03375
- **DOI/Link**: https://arxiv.org/abs/2402.03375
- **Abstract**: Generative discriminator guides LLM toward netlist-friendly Verilog. 68.1% / 46.1% pass@1 on VerilogEval-machine/human; beats GPT-4.
- **Why relevant**: Demonstrates discriminator-guided generation for DFT/PPA-friendly RTL.

### 33. CraftRTL: High-quality Synthetic Data Generation for Verilog Code Models with Correct-by-Construction Non-Textual Representations and Targeted Code Repair
- **Authors**: NVIDIA (M. Liu et al.)
- **Venue**: ICLR 2025 / arXiv:2409.12993
- **DOI/Link**: https://arxiv.org/abs/2409.12993
- **Abstract**: Correct-by-construction synthetic data for waveforms / Karnaugh maps / state diagrams; targeted code-repair injection. Starcoder2-15B FT achieves SOTA on VerilogEval & RTLLM.
- **Why relevant**: Methodology blueprint for building synthetic DFT/testing datasets.

### 34. OriGen: Enhancing RTL Code Generation with Code-to-Code Augmentation and Self-Reflection
- **Authors**: arXiv 2407.16237
- **Venue**: ICCAD 2024
- **DOI/Link**: https://arxiv.org/abs/2407.16237
- **Abstract**: Code-to-code augmentation via knowledge distillation + self-reflection from compiler feedback. +9.8% over previous SOTA on VerilogEval-Human; +18.1% over GPT-4 on self-reflection bench.
- **Why relevant**: Self-reflection mechanism is directly transferable to our debug suggestion loop.

### 35. MAGE: A Multi-Agent Engine for Automated RTL Code Generation
- **Authors**: arXiv 2412.07822 (2024)
- **Venue**: arXiv:2412.07822 (2024)
- **DOI/Link**: https://arxiv.org/abs/2412.07822
- **Abstract**: High-Temperature RTL Sampling + Scoring + State-Checkpoint debugging. Multi-agent specialization avoids single-agent context-switching.
- **Why relevant**: Multi-agent design pattern that we can mirror for DFT/testing.

### 36. Spec2RTL-Agent: Automated Hardware Code Generation from Complex Specifications Using LLM Agent Systems
- **Authors**: arXiv 2506.13905 (2025)
- **Venue**: arXiv:2506.13905 (2025)
- **DOI/Link**: https://arxiv.org/abs/2506.13905
- **Abstract**: Multi-agent: reasoning module → progressive coding (pseudocode → Python → C++ → RTL via HLS) → adaptive reflection. 75% fewer human interventions vs. existing approaches.
- **Why relevant**: Spec → testbench pipeline could re-use this layered intermediate-representation approach.

### 37. LASHED: LLMs And Static Hardware Analysis for Early Detection of RTL Bugs
- **Authors**: arXiv 2504.21770 (2025)
- **Venue**: arXiv:2504.21770 (2025)
- **DOI/Link**: https://arxiv.org/abs/2504.21770
- **Abstract**: Combines static analysis + LLMs for RTL security-bug detection via Assets Identification → Static Analysis → Contextualization. 87.5% of flagged instances are plausible CWEs.
- **Why relevant**: Hybrid static+LLM approach is a strong pattern we may use for fault-symptom recognition.

### 38. BugWhisperer: Fine-Tuning LLMs for SoC Hardware Vulnerability Detection
- **Authors**: arXiv 2505.22878 (2025)
- **Venue**: IEEE VTS 2025 / arXiv:2505.22878
- **DOI/Link**: https://arxiv.org/abs/2505.22878
- **Abstract**: Fine-tunes specialized LLMs for SoC hardware security verification, with GPT-4 / GPT-4o serving as replicator models.
- **Why relevant**: VTS 2025 paper — directly the target conference.
- **Recommended for download**: YES

### 39. SecureRAG-RTL: Retrieval-Augmented, Multi-Agent, Zero-Shot LLM-Driven Framework for Hardware Vulnerability Detection
- **Authors**: arXiv 2603.05689 (2026)
- **Venue**: arXiv:2603.05689 (2026)
- **DOI/Link**: https://arxiv.org/abs/2603.05689
- **Abstract**: RAG-empowered hardware vulnerability detection; evaluation across 18 LLMs shows up to 57.14% accuracy increase.
- **Why relevant**: RAG + zero-shot + multi-agent — three patterns we will compare against.

### 40. HardSecBench: Benchmarking the Security Awareness of LLMs for Hardware Code Generation
- **Authors**: arXiv 2601.13864 (2026)
- **Venue**: arXiv:2601.13864 (2026)
- **DOI/Link**: https://arxiv.org/abs/2601.13864
- **Abstract**: 924 Verilog and firmware-C tasks spanning 76 CWE entries.
- **Why relevant**: Benchmark we can adapt for evaluating a DFT/security-aware LLM.

### 41. LASP / LASA / LASSO: LLM-Aided Security Property Generation
- **Authors**: Multiple papers — LASP (MLCAD 2024), LASA (arXiv 2506.17865, 2025), LASSO (MLCAD 2025)
- **Venue**: MLCAD 2024–2025
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3670474.3685967; https://arxiv.org/abs/2506.17865; https://faculty.eng.ufl.edu/sandip/wp-content/uploads/sites/681/2026/02/mlcad25.pdf
- **Abstract**: Series of LLM + RAG frameworks producing non-vacuous security properties / SVAs for bus-based SoC verification.
- **Why relevant**: Reference series for security-property generation; covers the assertion-generation alternative direction.

### 42. VERT: A SystemVerilog Assertion Dataset to Improve Hardware Verification with LLMs
- **Authors**: A. Menon et al.
- **Venue**: ACM TODAES 2025 / arXiv:2503.08923
- **DOI/Link**: https://arxiv.org/abs/2503.08923; https://github.com/anandmenon12/vert
- **Abstract**: SVA dataset for fine-tuning OSS LLMs. Deepseek Coder 6.7B / Llama 3.1 8B reach 96.88% correctness on OpenTitan/CVA6, beating GPT-4.
- **Why relevant**: Dataset + benchmark we can use directly.

### 43. ChipGPT: How far are we from natural language hardware design
- **Authors**: K. Chang et al.
- **Venue**: arXiv:2305.14019 (2023)
- **DOI/Link**: https://arxiv.org/abs/2305.14019
- **Abstract**: Zero-code 4-stage natural-language → logic-design framework over LLMs.
- **Why relevant**: Early influential framework; cited by most subsequent work.

### 44. GPT4AIGChip: Towards Next-Generation AI Accelerator Design Automation via Large Language Models
- **Authors**: arXiv 2309.10730 (2023)
- **Venue**: ICCAD 2023 / arXiv:2309.10730
- **DOI/Link**: https://arxiv.org/abs/2309.10730
- **Abstract**: LLM-driven AI-accelerator design framework using natural language; demos democratization of accelerator design.
- **Why relevant**: Illustrates broader LLM-for-EDA application class.

### 45. AssertLLM (Multi-LLM Pipeline) — Pre-RTL Assertion Generation paper
- **Authors**: arXiv 2505.07995 (Spec2Assertion)
- **Venue**: arXiv:2505.07995 (2025)
- **DOI/Link**: https://arxiv.org/abs/2505.07995
- **Abstract**: Pre-RTL automatic assertion generation from specs.
- **Why relevant**: Spec-driven assertion — pairs with our DFT-aware property work.

---

## Tier 3: Supplementary (Surveys, Code LLM Foundations, Software Bug Detection, Adjacent Topics)

### 46. Large Language Models (LLMs) for Electronic Design Automation (EDA) — Special Session Paper
- **Authors**: arXiv 2508.20030 (2025)
- **Venue**: ICCAD 2025 special session / arXiv:2508.20030
- **DOI/Link**: https://arxiv.org/abs/2508.20030
- **Abstract**: Broad survey of LLM applications across EDA workflow.
- **Why relevant**: Reference survey for the related-work section.
- **Recommended for download**: YES

### 47. A Survey of Research in Large Language Models for Electronic Design Automation
- **Authors**: ACM TODAES 2025
- **Venue**: ACM TODAES Vol. 30, Iss. 3, 2025
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3715324
- **Abstract**: Comprehensive survey of LLM use across EDA stages.
- **Why relevant**: Backbone reference for related-work.

### 48. LLM-Assisted Circuit Verification: A Comprehensive Survey
- **Authors**: H. Liu et al.
- **Venue**: ASP-DAC 2026 / IEEE TCAD 2024 ref
- **DOI/Link**: https://yuntaolu.github.io/files/Liu-2026-ASPDAC-LLMDVSurvey.pdf
- **Abstract**: Survey focused on LLM-assisted circuit verification (most aligned with this project).
- **Why relevant**: Directly maps to the project verification scope.
- **Recommended for download**: YES

### 49. LLM4EDA: Emerging Progress in Large Language Models for Electronic Design Automation
- **Authors**: arXiv 2401.12224
- **Venue**: arXiv:2401.12224 (2024)
- **DOI/Link**: https://arxiv.org/abs/2401.12224
- **Abstract**: Early but widely-cited LLM-for-EDA survey.
- **Why relevant**: Common citation; sets the historical narrative.

### 50. A Survey of Circuit Foundation Model: Foundation AI Models for VLSI Circuit Design and EDA
- **Authors**: Z. Xie et al.
- **Venue**: arXiv:2504.03711 (2025)
- **DOI/Link**: https://arxiv.org/abs/2504.03711
- **Abstract**: Surveys 130+ circuit foundation models / decoder-based LLM EDA methods.
- **Why relevant**: Big-picture survey that contextualizes our project within foundation-model trends.

### 51. The Dawn of Agentic EDA: A Survey of Autonomous Digital Chip Design
- **Authors**: arXiv:2512.23189 (2026)
- **Venue**: arXiv:2512.23189 (2026)
- **DOI/Link**: https://arxiv.org/abs/2512.23189
- **Abstract**: Most recent survey on agentic-LLM EDA approaches.
- **Why relevant**: Current-state snapshot of agent paradigms.

### 52. Evaluating Large Language Models Trained on Code (Codex / HumanEval)
- **Authors**: M. Chen et al. (OpenAI)
- **Venue**: arXiv:2107.03374 (2021)
- **DOI/Link**: https://arxiv.org/abs/2107.03374
- **Abstract**: Introduces HumanEval benchmark and Codex. Foundational LLM-for-code paper.
- **Why relevant**: Citation backbone for code-LLM evaluation methodology.

### 53. DAVE: Deriving Automatically Verilog from English
- **Authors**: H. Pearce, B. Tan, R. Karri
- **Venue**: ACM/IEEE MLCAD Workshop 2020 / arXiv:2009.01026
- **DOI/Link**: https://arxiv.org/abs/2009.01026
- **Abstract**: First fine-tuned GPT-2 for Verilog generation. 94.8% correctness on undergraduate-level tasks.
- **Why relevant**: Origin paper — must cite for historical context.

### 54. Benchmarking Large Language Models for Automated Verilog RTL Code Generation
- **Authors**: S. Thakur et al.
- **Venue**: DATE 2023 / arXiv:2212.11140
- **DOI/Link**: https://arxiv.org/abs/2212.11140
- **Abstract**: Early systematic benchmark of LLMs on Verilog.
- **Why relevant**: Predecessor to VerilogEval; cited everywhere.

### 55. CodeV: Empowering LLMs for Verilog Generation through Multi-Level Summarization
- **Authors**: arXiv:2407.10424 (2024)
- **Venue**: arXiv:2407.10424 (2024)
- **DOI/Link**: https://arxiv.org/abs/2407.10424
- **Abstract**: Multi-level summarization instruction tuning for Verilog.
- **Why relevant**: Alt training strategy; relevant baseline.

### 56. HaVen: Hallucination-Mitigated LLM for Verilog Code Generation Aligned with HDL Engineers
- **Authors**: arXiv:2501.04908 (2025)
- **Venue**: DATE 2025 / arXiv:2501.04908
- **DOI/Link**: https://arxiv.org/abs/2501.04908
- **Abstract**: Addresses logical, symbolic, and knowledge hallucinations in Verilog LLMs.
- **Why relevant**: Hallucination is the central LLM reliability issue our project must address.

### 57. DeepRTL: Bridging Verilog Understanding and Generation with a Unified Representation Model
- **Authors**: arXiv:2502.15832 (2025)
- **Venue**: arXiv:2502.15832 (2025)
- **DOI/Link**: https://arxiv.org/abs/2502.15832
- **Abstract**: CodeT5+ FT for unified understanding+generation. Beats GPT-4 on understanding tasks.
- **Why relevant**: Encoder-decoder alternative architecture.

### 58. Revisiting VerilogEval: A Year of Improvements in Large-Language Models for Hardware Code Generation
- **Authors**: arXiv:2408.11053 (2024)
- **Venue**: LAD 2024 / arXiv:2408.11053
- **DOI/Link**: https://arxiv.org/abs/2408.11053
- **Abstract**: Re-evaluates Llama 3.1 405B (58% pass), GPT-4 Turbo, RTL-Coder. Includes spec-to-RTL tasks.
- **Why relevant**: Tracks the benchmark landscape evolution.

### 59. OpenLLM-RTL: Open Dataset and Benchmark for LLM-Aided Design RTL Generation
- **Authors**: arXiv (2024)
- **Venue**: ICCAD 2024
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3676536.3697118
- **Abstract**: Open-source dataset + benchmark for RTL generation.
- **Why relevant**: Possible dataset source.

### 60. ICCAD LLM4HWDesign Contest 2024
- **Authors**: GA Tech EIC + NVIDIA
- **Venue**: ICCAD 2024 contest
- **DOI/Link**: https://nvlabs.github.io/LLM4HWDesign/
- **Abstract**: Community-driven dataset construction for LLM hardware code generation.
- **Why relevant**: Live community dataset; can sample our test cases from here.

### 61. ProtocolLLM: RTL Benchmark for SystemVerilog Generation of Communication Protocols
- **Authors**: arXiv:2506.07945 (2025)
- **Venue**: arXiv:2506.07945 (2025)
- **DOI/Link**: https://arxiv.org/abs/2506.07945
- **Abstract**: Protocol-focused benchmark targeting timing correctness.
- **Why relevant**: Protocols are common DUT for our project's testbench task.

### 62. CodeT5+: Open Code Large Language Models for Code Understanding and Generation
- **Authors**: Y. Wang et al. (Salesforce)
- **Venue**: arXiv:2305.07922 (2023)
- **DOI/Link**: https://arxiv.org/abs/2305.07922
- **Abstract**: Family of encoder-decoder code LLMs used by DeepRTL etc.
- **Why relevant**: Base model citation.

### 63. CodeBERT: A Pre-Trained Model for Programming and Natural Languages
- **Authors**: Z. Feng et al. (Microsoft)
- **Venue**: EMNLP 2020
- **DOI/Link**: https://arxiv.org/abs/2002.08155
- **Abstract**: Foundational code-NL bimodal pretraining.
- **Why relevant**: Background citation for code-LLM lineage.

### 64. PyHDL-Eval: An LLM Evaluation Framework for Hardware
- **Authors**: C. Batten et al. (Cornell)
- **Venue**: MLCAD 2024
- **DOI/Link**: https://www.csl.cornell.edu/~cbatten/pdfs/batten-pyhdl-eval-mlcad2024.pdf
- **Abstract**: Eval framework for hardware code (Python-based HDLs).
- **Why relevant**: Alternative evaluation benchmark.

### 65. PromptV: Leveraging LLM-powered Multi-Agent Prompting for High-quality Verilog Generation
- **Authors**: arXiv (2024)
- **Venue**: 2024 / arXiv
- **DOI/Link**: https://www.promptlayer.com/research-papers/revolutionizing-chip-design-with-ai-powered-verilog
- **Abstract**: Multi-agent prompting (generator, testbench, teacher, learner).
- **Why relevant**: Inspirational multi-agent pattern.

### 66. SPICEPilot: Navigating SPICE Code Generation and Simulation with AI Guidance
- **Authors**: arXiv:2410.20553 (2024)
- **Venue**: arXiv:2410.20553 (2024)
- **DOI/Link**: https://arxiv.org/abs/2410.20553
- **Abstract**: Python-based SPICE generation via LLMs for analog design.
- **Why relevant**: Analog-side parallel — shows generalizability.

### 67. TPU-Gen: LLM-Driven Custom Tensor Processing Unit Generator
- **Authors**: arXiv:2503.05951 (2025)
- **Venue**: arXiv:2503.05951 (2025)
- **DOI/Link**: https://arxiv.org/abs/2503.05951
- **Abstract**: LLM-driven custom TPU generation; TCL/Python scripts for PPA.
- **Why relevant**: End-to-end accelerator-generation system; agent reference.

### 68. iScript: A Domain-Adapted Large Language Model and Benchmark for Physical Design Tcl Script Generation
- **Authors**: arXiv:2603.04476 (2026)
- **Venue**: arXiv:2603.04476 (2026)
- **DOI/Link**: https://arxiv.org/abs/2603.04476
- **Abstract**: Domain-adapted Qwen3-8B for Innovus Tcl + benchmark.
- **Why relevant**: Closest analog for an LLM that writes DFT/ATPG tool scripts.

### 69. ORAssistant: A Custom RAG-based Conversational Assistant for OpenROAD
- **Authors**: arXiv:2410.03845 (2024)
- **Venue**: arXiv:2410.03845 (2024)
- **DOI/Link**: https://arxiv.org/abs/2410.03845
- **Abstract**: RAG-based assistant for OpenROAD usage (GSoC 2024).
- **Why relevant**: Practical RAG implementation reference.

### 70. Using LLMs to Facilitate Formal Verification of RTL
- **Authors**: arXiv:2309.09437 (2023)
- **Venue**: arXiv:2309.09437 (2023)
- **DOI/Link**: https://arxiv.org/abs/2309.09437
- **Abstract**: GPT-4 generates SVAs from buggy RTL; up to 6× coverage improvement vs. prior automated methods.
- **Why relevant**: Important early demonstration of LLM ↔ formal verification synergy.

### 71. AutoVCoder: A Systematic Framework for Automated Verilog Code Generation using LLMs
- **Authors**: arXiv:2407.18333 (2024)
- **Venue**: arXiv:2407.18333 (2024)
- **DOI/Link**: https://arxiv.org/abs/2407.18333
- **Abstract**: Systematic framework integrating multiple optimizations.
- **Why relevant**: Adjacent integrated framework.

### 72. CodeS / Towards LLM-Powered Verilog RTL Assistant: Self-Verification and Self-Correction
- **Authors**: arXiv:2406.00115 (2024)
- **Venue**: arXiv:2406.00115 (2024)
- **DOI/Link**: https://arxiv.org/abs/2406.00115
- **Abstract**: Verilog RTL assistant with self-verification and self-correction.
- **Why relevant**: Self-verification loop is core to fail-log interpretation.

### 73. TrojanWhisper: Evaluating Pre-trained LLMs to Detect and Localize Hardware Trojans
- **Authors**: arXiv:2412.07636 (2024)
- **Venue**: arXiv:2412.07636 (2024)
- **DOI/Link**: https://arxiv.org/abs/2412.07636
- **Abstract**: GPT-4o / Gemini 1.5 Pro evaluation on Trojan detection.
- **Why relevant**: Detection task pattern reusable for fault detection.

### 74. Unleashing GHOST: An LLM-Powered Framework for Automated Hardware Trojan Design
- **Authors**: arXiv:2412.02816 (2024)
- **Venue**: arXiv:2412.02816 (2024)
- **DOI/Link**: https://arxiv.org/abs/2412.02816
- **Abstract**: LLM Trojan-generation framework; 83.33% evasion of GNN detectors.
- **Why relevant**: Adversarial side — limitations discussion.

### 75. LLM-Aided Testbench Generation and Bug Detection for Finite-State Machines
- **Authors**: arXiv:2406.17132 (2024)
- **Venue**: arXiv:2406.17132 (2024)
- **DOI/Link**: https://arxiv.org/abs/2406.17132
- **Abstract**: FSM-targeted LLM testbench + bug detection.
- **Why relevant**: Narrow but directly relevant DUT class (FSM is common in DFT tests).

### 76. L4: Diagnosing Large-scale LLM Training Failures via Automated Log Analysis
- **Authors**: arXiv:2503.20263 (2025)
- **Venue**: FSE 2025 / arXiv:2503.20263
- **DOI/Link**: https://arxiv.org/abs/2503.20263
- **Abstract**: 53.9% of LLM-training failures diagnosable from logs alone. Empirical study of 428 production failures.
- **Why relevant**: Methodology for empirical log-analysis study — transferable to our test log corpus.

### 77. A Review of Large Language Models for Automated Test Case Generation
- **Authors**: MDPI MLKE 7(3):97, 2025
- **Venue**: MDPI Machine Learning and Knowledge Extraction (2025)
- **DOI/Link**: https://www.mdpi.com/2504-4990/7/3/97
- **Abstract**: Survey of LLMs for software test-case generation.
- **Why relevant**: Software-testing techniques that transfer to hardware testing.

### 78. Bugs in Large Language Models Generated Code: An Empirical Study
- **Authors**: arXiv:2403.08937 (2024)
- **Venue**: arXiv:2403.08937 (2024)
- **DOI/Link**: https://arxiv.org/abs/2403.08937
- **Abstract**: 10 bug patterns in LLM-generated code (Misinterpretations, Syntax, Hallucinated Object, etc.).
- **Why relevant**: Bug taxonomy to motivate why fail-log analysis is needed for LLM outputs themselves.

### 79. Integrating Various Software Artifacts for Better LLM-based Bug Localization and Program Repair (DEVLoRe)
- **Authors**: arXiv:2412.03905 (2024)
- **Venue**: arXiv:2412.03905 (2024)
- **DOI/Link**: https://arxiv.org/abs/2412.03905
- **Abstract**: Issue text + stack trace + debug info → 49.3% single-method-bug localization, 56.0% plausible patches.
- **Why relevant**: Software-side analog for fail-log + symptom fusion.

### 80. Understanding and Mitigating Errors of LLM-Generated RTL Code
- **Authors**: arXiv:2508.05266 (2025)
- **Venue**: arXiv:2508.05266 (2025)
- **DOI/Link**: https://arxiv.org/abs/2508.05266
- **Abstract**: Studies error taxonomy in LLM-generated RTL.
- **Why relevant**: Bug-cause taxonomy specifically for hardware LLM outputs.

### 81. AutoVeriFix: Automatically Correcting Errors and Enhancing Functional Correctness in LLM-Generated Verilog Code
- **Authors**: arXiv:2509.08416 (2025)
- **Venue**: arXiv:2509.08416 (2025)
- **DOI/Link**: https://arxiv.org/abs/2509.08416
- **Abstract**: Auto-corrector for Verilog functional errors.
- **Why relevant**: Likely baseline for any correction-loop comparison.

### 82. R3A: Reliable RTL Repair Framework with Multi-Agent Fault [Localization]
- **Authors**: arXiv:2511.20090 (2025)
- **Venue**: arXiv:2511.20090 (2025)
- **DOI/Link**: https://arxiv.org/abs/2511.20090
- **Abstract**: Multi-agent RTL repair; 90.6% fix rate within time limit; 45% more bugs covered than traditional methods.
- **Why relevant**: Recent state-of-the-art multi-agent debug — strong target to beat.

### 83. ChipBench: A Next-Step Benchmark for Evaluating LLM Performance in AI-Aided Chip Design
- **Authors**: arXiv:2601.21448 (2026)
- **Venue**: arXiv:2601.21448 (2026)
- **DOI/Link**: https://arxiv.org/abs/2601.21448
- **Abstract**: Modern comprehensive bench — Claude-4.5-opus only 30.74% on Verilog gen, 13.33% on Python ref-model gen.
- **Why relevant**: Reveals saturation issue with VerilogEval; we should target ChipBench for our eval.

### 84. Comprehensive Verilog Design Problems: Next-Generation Benchmark Dataset for Evaluating LLMs and Agents on RTL Design and Verification
- **Authors**: arXiv:2506.14074 (2025)
- **Venue**: arXiv:2506.14074 (2025)
- **DOI/Link**: https://arxiv.org/abs/2506.14074
- **Abstract**: Next-gen benchmark covering verification too.
- **Why relevant**: Modern benchmark including verification (matches our scope).

### 85. Self-HWDebug: Automation of LLM Self-Instructing for Hardware Security Verification
- **Authors**: arXiv:2405.12347 (2024)
- **Venue**: arXiv:2405.12347 (2024)
- **DOI/Link**: https://arxiv.org/abs/2405.12347
- **Abstract**: Self-instruct LLM for debug instruction generation; assertion-based validation.
- **Why relevant**: Self-instruct technique applicable to fail-log debug-instruction generation.

### 86. FLAG: Formal and LLM-assisted SVA Generation for Formal Specifications of On-Chip Communication Protocols
- **Authors**: arXiv:2504.17226 (2025)
- **Venue**: arXiv:2504.17226 (2025)
- **DOI/Link**: https://arxiv.org/abs/2504.17226
- **Abstract**: Hybrid formal + LLM SVA generation; SAT-based filtering.
- **Why relevant**: Hybrid pattern that improves LLM robustness for assertions.

### 87. Divergent Thoughts toward One Goal: LLM-based Multi-Agent Collaboration System for EDA
- **Authors**: arXiv:2502.10857 (2025)
- **Venue**: arXiv:2502.10857 (2025)
- **DOI/Link**: https://arxiv.org/abs/2502.10857
- **Abstract**: Multi-agent collaboration system for EDA.
- **Why relevant**: Multi-agent CoT pattern for EDA agents.

### 88. AiEDA: Agentic AI Design Framework for Digital ASIC System Design
- **Authors**: arXiv:2412.09745 (2024)
- **Venue**: arXiv:2412.09745 (2024)
- **DOI/Link**: https://arxiv.org/abs/2412.09745
- **Abstract**: Agentic AI design framework for digital ASIC.
- **Why relevant**: Agent design template.

### 89. ChaTCL: LLM-Based Multi-Agent RAG Framework for TCL Script Generation
- **Authors**: 2025 (researchgate 394636089)
- **Venue**: 2025
- **DOI/Link**: https://www.researchgate.net/publication/394636089
- **Abstract**: Multi-agent RAG for TCL script generation.
- **Why relevant**: Direct candidate for generating ATPG/DFT Tcl scripts.

### 90. EDA Corpus: A Large Language Model Dataset for Enhanced Interaction with OpenROAD
- **Authors**: arXiv:2405.06676 (2024)
- **Venue**: arXiv:2405.06676 (2024)
- **DOI/Link**: https://arxiv.org/abs/2405.06676
- **Abstract**: Dataset for LLM + OpenROAD.
- **Why relevant**: Dataset reference; demonstrates corpus-construction methodology.

### 91. RTLRepoCoder: Repository-Level RTL Code Completion through the Combination of Fine-Tuning and Retrieval Augmentation
- **Authors**: arXiv:2504.08862 (2025)
- **Venue**: arXiv:2504.08862 (2025)
- **DOI/Link**: https://arxiv.org/abs/2504.08862
- **Abstract**: Repo-level RTL completion via FT + RAG.
- **Why relevant**: Modern FT+RAG pattern.

### 92. MAHL: Multi-Agent LLM-Guided Hierarchical Chiplet Design with Adaptive Debugging
- **Authors**: arXiv:2508.14053 (2025)
- **Venue**: arXiv:2508.14053 (2025)
- **DOI/Link**: https://arxiv.org/abs/2508.14053
- **Abstract**: Multi-agent LLM for chiplet design with adaptive debugging.
- **Why relevant**: Adaptive debugging + chiplet (cross-disciplinary with Direction 3).

### 93. Learning to Debug: LLM-Organized Knowledge Trees for Solving RTL Assertion Failures
- **Authors**: arXiv:2511.17833 (2025)
- **Venue**: arXiv:2511.17833 (2025)
- **DOI/Link**: https://arxiv.org/abs/2511.17833
- **Abstract**: Organizes debugging knowledge as trees to solve RTL assertion failures.
- **Why relevant**: Knowledge-structuring approach for systematic debug — highly relevant.
- **Recommended for download**: YES

### 94. Insights from Verification: Training a Verilog Generation LLM with Reinforcement Learning with Testbench Feedback
- **Authors**: arXiv:2504.15804 (2025)
- **Venue**: arXiv:2504.15804 (2025)
- **DOI/Link**: https://arxiv.org/abs/2504.15804
- **Abstract**: RL training of Verilog LLM using testbench feedback as reward.
- **Why relevant**: Closes the verification feedback loop; relevant if we explore RL-style refinement.

### 95. Automatically Improving LLM-based Verilog Generation using EDA Tool Feedback
- **Authors**: arXiv:2411.11856 (2024)
- **Venue**: ACM TODAES 2025 / arXiv:2411.11856
- **DOI/Link**: https://arxiv.org/abs/2411.11856
- **Abstract**: Studies the question: can EDA tool feedback actually improve LLM Verilog generation? Empirical answer: yes, with limits.
- **Why relevant**: Carefully measures the EDA-feedback design space.

### 96. SystemVerilog Assertion Test Generation paper (Iterative LLM-Based Assertion Generation Using Syntax-Semantic Representations for Functional Coverage-Guided Verification)
- **Authors**: arXiv:2602.15388 (2026)
- **Venue**: arXiv:2602.15388 (2026)
- **DOI/Link**: https://arxiv.org/abs/2602.15388
- **Abstract**: Iterative syntax-semantic representation for coverage-guided assertion generation.
- **Why relevant**: Coverage-guided iterative pattern.

### 97. PRO-V: An Efficient Program Generation Multi-Agent System
- **Authors**: arXiv:2506.12200 (2025)
- **Venue**: arXiv:2506.12200 (2025)
- **DOI/Link**: https://arxiv.org/abs/2506.12200
- **Abstract**: Multi-agent program generation system.
- **Why relevant**: Modern multi-agent pattern relevant to LLM testbench generators.

### 98. ResBench: Benchmarking LLM-Generated FPGA Designs with Resource Awareness
- **Authors**: arXiv:2503.08823 (2025)
- **Venue**: arXiv:2503.08823 (2025)
- **DOI/Link**: https://arxiv.org/abs/2503.08823
- **Abstract**: Resource-aware FPGA design eval.
- **Why relevant**: PPA-aware benchmark; complements our pass/fail evaluation.

### 99. Agentic AI-based Coverage Closure for Formal Verification
- **Authors**: arXiv:2603.03147 (2026)
- **Venue**: arXiv:2603.03147 (2026)
- **DOI/Link**: https://arxiv.org/abs/2603.03147
- **Abstract**: Agentic coverage closure for formal verification.
- **Why relevant**: Highly relevant if we extend project to coverage closure.

### 100. Retrieve, Schedule, Reflect: LLM Agents for Chip QoR Optimization
- **Authors**: arXiv:2603.13767 (2026)
- **Venue**: arXiv:2603.13767 (2026)
- **DOI/Link**: https://arxiv.org/abs/2603.13767
- **Abstract**: Agentic LLM for chip QoR optimization via natural-language expertise + RAG.
- **Why relevant**: Tool-use + RAG agent design.

### 101. MCP4EDA: LLM-Powered Model Context Protocol RTL-to-GDSII Automation
- **Authors**: arXiv:2507.19570 (2025)
- **Venue**: arXiv:2507.19570 (2025)
- **DOI/Link**: https://arxiv.org/abs/2507.19570
- **Abstract**: MCP server for LLM ↔ open-source EDA toolchains.
- **Why relevant**: Modern tool-orchestration protocol; could be useful infra.

### 102. PyraNet: A Multi-Layered Hierarchical Dataset for Verilog
- **Authors**: arXiv:2412.06947 (2024)
- **Venue**: arXiv:2412.06947 (2024)
- **DOI/Link**: https://arxiv.org/abs/2412.06947
- **Abstract**: Hierarchical Verilog dataset.
- **Why relevant**: Dataset source.

### 103. MG-Verilog (Best Paper, IEEE LAD 2024)
- **Authors**: GA Tech EIC Lab
- **Venue**: IEEE LAD 2024 (Workshop on LLM-Aided Design)
- **DOI/Link**: https://responsible.computing.gatech.edu/mg-verilog-won-the-best-paper-award-at-the-first-workshop-on-llm-aided-design/
- **Abstract**: Multi-granularity Verilog dataset paired with NL descriptions.
- **Why relevant**: Quality dataset for instruction tuning.

### 104. VHDL-Eval: A Framework for Evaluating Large Language Models in VHDL Code Generation
- **Authors**: arXiv:2406.04379 (2024)
- **Venue**: arXiv:2406.04379 (2024)
- **DOI/Link**: https://arxiv.org/abs/2406.04379
- **Abstract**: VHDL-side evaluation framework.
- **Why relevant**: VHDL is still common in DFT/legacy environments.

### 105. VeriThoughts: Enabling Automated Verilog Code Generation using Reasoning and Formal Verification
- **Authors**: arXiv:2505.20302 (2025)
- **Venue**: arXiv:2505.20302 (2025)
- **DOI/Link**: https://arxiv.org/abs/2505.20302
- **Abstract**: 20k+ Verilog modules with reasoning traces; formal-verification-based eval.
- **Why relevant**: Reasoning-traces dataset; novel formal-eval methodology.

### 106. A Multi-Expert Large Language Model Architecture for Verilog Code Generation
- **Authors**: arXiv:2404.08029 (2024)
- **Venue**: arXiv:2404.08029 (2024)
- **DOI/Link**: https://arxiv.org/abs/2404.08029
- **Abstract**: Mixture-of-experts for Verilog.
- **Why relevant**: Architectural reference.

### 107. HDLGen-ChatGPT (RISC-V Processor VHDL+Verilog testbench/EDA project generation)
- **Authors**: Logicademy
- **Venue**: ACM Workshop on Rapid System Prototyping (RSP) 2023
- **DOI/Link**: https://dl.acm.org/doi/abs/10.1145/3625223.3649280
- **Abstract**: Open-source tool: ChatGPT in tandem for HDL + testbench + Vivado/Quartus project gen.
- **Why relevant**: Practical reference tool for our pipeline.

### 108. Hardware Trojan Dataset of RISC-V and Web3 Generated with ChatGPT-4
- **Authors**: MDPI Data 9(6):82, 2024
- **Venue**: MDPI Data (2024)
- **DOI/Link**: https://www.mdpi.com/2306-5729/9/6/82
- **Abstract**: LLM-generated Trojan dataset.
- **Why relevant**: Dataset for fault-injection variants.

### 109. From Prompt to Accelerator: LLM-Based Analog In-Memory Accelerator Design Automation
- **Authors**: GLSVLSI 2025
- **Venue**: GLSVLSI 2025
- **DOI/Link**: https://dl.acm.org/doi/10.1145/3716368.3735276
- **Abstract**: Survey/perspective on LLM-based AIMC design automation.
- **Why relevant**: Adjacent perspective paper.

### 110. ChipChat: My journey making the world's first LLM-architected and taped-out silicon design
- **Authors**: H. Pearce (blog)
- **Venue**: 01001000.xyz (2023, paper companion)
- **DOI/Link**: https://01001000.xyz/2023-12-21-ChatGPT-AI-Silicon/
- **Abstract**: Engineer's first-person account of tape-out.
- **Why relevant**: Provides qualitative insight; useful in motivation/discussion.

### 111. Awesome-LLM4EDA (curated literature list)
- **Authors**: Thinklab-SJTU
- **Venue**: GitHub
- **DOI/Link**: https://github.com/Thinklab-SJTU/Awesome-LLM4EDA
- **Abstract**: Living curated list of LLM-for-EDA papers.
- **Why relevant**: Continuously updated reference; consult periodically through project.

### 112. LLMs for Secure Hardware Design and Related Problems: Opportunities and Challenges
- **Authors**: arXiv:2605.10807 (2026)
- **Venue**: arXiv:2605.10807 (2026)
- **DOI/Link**: https://arxiv.org/abs/2605.10807
- **Abstract**: Survey-style opportunities/challenges discussion for hardware security LLMs.
- **Why relevant**: Discussion-section reference.

### 113. Generative AI Assertions in UVM-Based System Verilog Functional Verification
- **Authors**: MDPI Systems 12(10):390, 2024
- **Venue**: MDPI Systems (2024)
- **DOI/Link**: https://www.mdpi.com/2079-8954/12/10/390
- **Abstract**: GenAI assertions in UVM SystemVerilog functional verification.
- **Why relevant**: Practical UVM + LLM combination.

### 114. Stalled, Biased, and Confused: Uncovering Reasoning Failures in LLMs for Cloud-Based Root Cause Analysis
- **Authors**: arXiv:2601.22208 (2026)
- **Venue**: arXiv:2601.22208 (2026)
- **DOI/Link**: https://arxiv.org/abs/2601.22208
- **Abstract**: Studies reasoning failures of LLMs for cloud root-cause analysis.
- **Why relevant**: Empirical failure-mode study — transferable warning for hardware RCA.

### 115. Integrating LLMs for Explainable Fault Diagnosis in Complex Systems
- **Authors**: arXiv:2402.06695 (2024)
- **Venue**: arXiv:2402.06695 (2024)
- **DOI/Link**: https://arxiv.org/abs/2402.06695
- **Abstract**: LLM + physics-based diagnostic model for explainable fault diagnosis.
- **Why relevant**: Hybrid model+LLM explainability — important for trust in DFT fault diagnosis.

### 116. Exploring LLM-based Frameworks for Fault Diagnosis (Industrial)
- **Authors**: arXiv:2509.23113 (2025)
- **Venue**: arXiv:2509.23113 (2025)
- **DOI/Link**: https://arxiv.org/abs/2509.23113
- **Abstract**: Notes LLMs often under-perform simple rule-based baselines in anomaly detection.
- **Why relevant**: Calibrates expectations; useful limitations discussion.

### 117. Speculative Decoding for Verilog: Speed and Quality, All in One
- **Authors**: arXiv:2503.14153 (2025)
- **Venue**: arXiv:2503.14153 (2025)
- **DOI/Link**: https://arxiv.org/abs/2503.14153
- **Abstract**: Speculative decoding for Verilog code-gen efficiency.
- **Why relevant**: Inference-time technique; could speed up our system.

### 118. VeriOpt: PPA-Aware High-Quality Verilog Generation via Multi-Role LLMs
- **Authors**: arXiv:2507.14776 (2025)
- **Venue**: arXiv:2507.14776 (2025)
- **DOI/Link**: https://arxiv.org/abs/2507.14776
- **Abstract**: PPA-aware Verilog gen using multiple LLM roles.
- **Why relevant**: Multi-role agent reference.

### 119. SimCopilot: Evaluating LLMs for Copilot-Style Code Generation
- **Authors**: arXiv:2505.21514 (2025)
- **Venue**: arXiv:2505.21514 (2025)
- **DOI/Link**: https://arxiv.org/abs/2505.21514
- **Abstract**: Evaluation framework for Copilot-style code gen.
- **Why relevant**: Software-eval methodology, transferable.

### 120. ChipStack UVM AI Agent (commercial reference)
- **Authors**: Chipstack.ai
- **Venue**: Product page
- **DOI/Link**: https://www.chipstack.ai/product-pages/uvmaiagent
- **Abstract**: Commercial UVM AI agent that enhances testbenches and coverage closure.
- **Why relevant**: Reference for industry adoption status.

---

## Key Datasets & Benchmarks

| Name | Scope | Link |
|------|-------|------|
| **VerilogEval** (v1/v2) | 156 HDLBits problems; functional tests | https://github.com/NVlabs/verilog-eval |
| **RTLLM** (v1/v2) | 30→50 hand-crafted RTL designs w/ specs + golden TBs | https://github.com/hkust-zhiyao/RTLLM |
| **OpenLLM-RTL** | Open dataset/benchmark for RTL gen (ICCAD '24) | dl.acm.org/doi/10.1145/3676536.3697118 |
| **VERT** | SystemVerilog Assertion dataset | https://github.com/anandmenon12/vert |
| **PyHDL-Eval** | Python-HDL eval (MLCAD '24) | csl.cornell.edu/~cbatten |
| **VHDL-Eval** | VHDL eval | arXiv:2406.04379 |
| **ProtocolLLM** | SV protocols benchmark | arXiv:2506.07945 |
| **HardSecBench** | 924 Verilog/firmware-C tasks, 76 CWEs | arXiv:2601.13864 |
| **FIXME** | End-to-end LLM verification benchmark | arXiv:2507.04276 |
| **ChipBench** | Next-step LLM evaluation (Verilog gen + Python refmodel gen) | arXiv:2601.21448 |
| **CVDP / Comprehensive Verilog Design Problems** | Next-gen RTL design + verification benchmark | arXiv:2506.14074 |
| **MG-Verilog** | Multi-granularity NL+Verilog dataset (LAD '24 Best Paper) | GA Tech EIC |
| **PyraNet** | Multi-layered hierarchical Verilog dataset | arXiv:2412.06947 |
| **VeriThoughts** | 20k+ Verilog modules with reasoning traces | arXiv:2505.20302 |
| **EDA Corpus (OpenROAD)** | LLM dataset for OpenROAD interaction | arXiv:2405.06676 |
| **ResBench** | Resource-aware FPGA-design eval | arXiv:2503.08823 |
| **HDLBits** | Verilog learning platform — source for VerilogEval | hdlbits.01xz.net |

---

## Identified Research Gaps (for our project to target)

### Most promising gap (recommended target):
**Closed-loop LLM-driven DFT/scan fail diagnosis with structured chain-of-thought reasoning over scan-fail logs + bitmaps**. Existing fail-log RCA work (FVDebug, Berkeley EECS-2025-48, arXiv 2507.06512) targets *design/synthesis logs* and *formal verification counter-examples* — none directly target *manufacturing/scan ATPG fail logs* with structured fault-type / fault-location reasoning. There is no published end-to-end "LLM reads scan fail log + ATPG report + design metadata → outputs fault candidate + repair suggestion" with public benchmark and quantitative metrics. This is also the area where the project specs explicitly mention RAG + structured reasoning as recommended methods. This gap directly maps to **Direction 2 (AI-assisted fault diagnosis)** as well, giving the team flexibility for cross-direction work.

### Other notable gaps:
1. **No standardized "LLM for DFT" benchmark.** VerilogEval / RTLLM / RTLLM-v2 cover RTL gen; FIXME covers verification — but nothing covers DFT configuration / scan chain setup / ATPG script generation. **Opportunity**: a small benchmark of "spec → DFT Tcl + scan config" tasks could be a contribution.
2. **Hallucination quantification in DFT contexts.** HaVen and others address Verilog code hallucination, but DFT/test commands have stricter tool-specific semantics where hallucinated arguments silently produce wrong test patterns. Empirical study would be a clear contribution.
3. **Failure-pattern classification from synthetic scan-fail bitmaps + LLM-generated natural-language summaries.** Cross-cuts Direction 1 (Failure Bitmap intelligent analysis). No published work uses an LLM for human-readable bitmap explanations.
4. **RAG over EDA tool manuals for testing flows specifically.** ORAssistant covers OpenROAD; ChipNeMo covers internal NVIDIA flows. A focused RAG over open-source DFT tool docs (e.g., OpenROAD STA, fault-sim tools, public ATPG materials) is wide open.
5. **Structured reasoning for fault candidate enumeration.** Current LLM debug papers (LiK, VeriDebug, R3A) localize *RTL functional bugs*. Mapping the technique to *fault candidates after scan diagnosis* would be a clear novel application.
6. **Reliability + limitations**: Fault-diagnosis study (arXiv 2509.23113) shows LLMs may underperform rule-based baselines. A rigorous comparison + hybrid (LLM + rule) system for DFT failure interpretation directly answers the project's required "AI limitations" discussion.

### Suggested project framing:
> *"LLM-Assisted Scan-Fail Log Interpretation and DFT Configuration Suggestion via RAG-Augmented Chain-of-Thought Reasoning"* — small, focused, novel, includes synthetic data generation, runs on modest hardware, evaluates against rule-based and prompt-only baselines, addresses both effectiveness AND limitations as the project requires.

---

## Notes for the team

- **Bulk of papers (90+)** are from 2023–2026 — this is a brand-new field. Most concrete work is post-DAVE (2020) and post-ChipGPT/Chip-Chat/VerilogEval (mid-2023). Foundation papers (Codex/HumanEval, CodeBERT, CodeT5+) are 2020–2023.
- **arXiv is heavily represented** because of how recent this is. Conference versions exist for many (ICCAD 2024, ASP-DAC 2024/2025, DAC 2024, VTS 2025, ATS 2025, MLCAD 2024/2025, IEEE LAD 2024).
- **Direct DFT/scan/ATPG LLM papers are still rare** — DFTAgent (paper #1) is the most direct hit. Most "LLM for testing" work today targets functional verification / testbench generation rather than manufacturing-test-flow DFT. **This is where the project can make its novel contribution.**
- **Open implementations to leverage**: NVlabs/verilog-eval, hkust-zhiyao/RTLLM, hkust-zhiyao/RTL-Coder, NVlabs/RTLFixer, shailja-thakur/VGen, anandmenon12/VERT, ZixiBenZhang/ml4dv (LLM4DV).
