# 原始波形故障诊断流水线 (waveform-ML)

本文件说明本课程项目新增的**原始 RX 波形**故障诊断流水线（在已有 `d2dsim` ngspice
仿真器之上）。最终报告见仓库根目录 `报告_D2D波形故障诊断.md`。

## 组成
| 文件 | 作用 | 运行环境 |
|---|---|---|
| `d2dsim/wave_campaign.py` | 生成原始波形数据集（10 类故障 × 全温区 × 良性 droop × 噪声种子） | 系统 python3（纯标准库） |
| `inspect_waves.py` | 数据可视化：每类眼图 / 波形 / 遥测覆盖 | `drl_hw2`（numpy/matplotlib） |
| `ml_diagnose.py` | 诊断（逻辑回归基线 + 1-D CNN）+ 三项消融 + 严重度回归 + 出图 | `drl_hw2`（torch/numpy/matplotlib） |

`d2dsim` 本次新增能力（默认关闭，不影响旧的特征数据流水线）：
- `params.noise_on / noise_gain`：受害 lane 电阻瞬态热噪声（`trnoise`，RMS∝√(4kTR·Δf)）。
- `params.vdroop_benign`：良性、可观测的工况 droop（混杂因子，记入遥测）。
- 故障类新增 `r_drift`（分布式串阻 [Ω]）、`c_drift`（并联电容膨胀）。
- `physics.r_on_temp`：温度相关驱动 `Ron(T)=Ron0·(T/T0)^1.5`（温度闭合眼图的主导机制）。

## 一键复现
```bash
cd sim
# 1) 数据集（约 16 min；输出 out/wave/waveforms.csv + meta.json）
python3 -c "from d2dsim.wave_campaign import run_wave_campaign; run_wave_campaign(out_dir='out/wave')"
# 2) 可视化（out/wave/inspect/*.png）
~/miniconda3/envs/drl_hw2/bin/python inspect_waves.py --data out/wave
# 3) 训练 + 消融 + 出图（out/wave/results.json + out/wave/plots/*.png）
~/miniconda3/envs/drl_hw2/bin/python ml_diagnose.py --data out/wave
```
快速冒烟测试：`run_wave_campaign(out_dir='out/wave_quick', quick=True, seeds=2)`。

## 数据格式
- `out/wave/waveforms.csv`：每行 `run_id,label,sev,temp_C,vdroop_frac,noise_seed,s0..s1023`
  （波形 = 128 UI × 8 样/UI；UI=62.5 ps @16 GT/s）。
- `out/wave/meta.json`：固定 TX 比特序列、samples_per_ui、RX 延迟、类别、遥测列等。

## 实验与产物
- 诊断：`results.json` 的 `cnn_waveform_acc / baseline_logistic_acc`；混淆矩阵 `plots/confusion_cnn.png`。
- 遥测消融（混杂去除）：`telemetry_ablation`（完整波形）+ `lossy_ablation`（有损标量眼裕度）；
  关键图 `plots/lossy_confounder.png`、`plots/telemetry_ablation.png`。
- 区域消融（沿区/平台区，3 次重初始化均值±std）：`region_ablation_acc`、`plots/region_ablation.png`。
- 严重度回归：`severity`（r_drift / c_drift 的 MAE、R²）、`plots/severity_*.png`。

## 主要结果（786 样本，测试 198）
- CNN 诊断 0.803 vs 逻辑回归 0.702。
- 严重度回归 R²：c_drift 0.998 / r_drift 0.867。
- **核心洞见**：完整波形下遥测近乎冗余（0.803→0.864，误报不变）；有损标量眼裕度下遥测把
  高应力健康链路**误报 37.5%→0%**——多模态融合的价值取决于观测的有损性。
- 区域：全 0.806 ≈ 沿区 0.785 ≫ 平台区 0.660；阻抗不连续仅在沿区可检（0.94 / 0.00）。

## 设计要点（便于答辩问答）
- **固定 TX 序列**：所有样本同一 PRBS，使故障+噪声为唯一变量，且沿/平台掩膜对所有样本一致。
- **故障跨全温区**：避免“高温⇒健康”的标签捷径，保证混杂结论非伪。
- **观测真实性**：原始波形属诊断/后硅态；运行时真实可得的是有损标量——故区分两种观测体制。

---

# v2 数据集（采样式操作空间，2026-06-10）

针对 v1 的三处批评（固定码型、healthy 独占 45/65/100 °C 的温度支撑泄漏、串行生成慢）重建：

```bash
# 1) 并行生成（8 worker，~290 runs/min；6000 行约 21 分钟）
~/miniconda3/envs/drl_hw2/bin/python run_wave2.py --out out/wave2 --n-rows 6000 --n-bits 160 --workers 8
# 2) 训练 + 全部 v2 实验
~/miniconda3/envs/drl_hw2/bin/python ml_diagnose_v2.py --data out/wave2
```

## 与 v1 的差异
- **温度**：全部类别 `T ~ U(27,110)`，消除温度支撑泄漏；严重度连续（R 类对数均匀）、位置随机。
- **工作负载变化**：victim/aggressor PRBS 种子逐行随机（`seed_v` 存于 CSV，可重建 TX 比特并作为
  模型的条件输入通道）；benign droop `~U(0,0.12)` 与噪声种子去相关。
- **滋扰（nuisance，非标签）**：逐行通道制造偏差（RLGC/凸点/Ron/Crx 乘性 ±5–15%）+
  TX 发送抖动（RJ 0.2–1.2 ps、DCD ±1 ps、SJ 0–1.2 ps @50–300 MHz）。
- **并发故障**：15% 故障行注入两个不同故障，标签 `a+b` → 多标签目标（healthy=全零）。
- **原始波形保真**：每行完整 1 ps 网格波形存 `out/wave2/raw/w#####.f32`（小端 float32，
  t0/dt/n 见 `scenarios.jsonl`）；CSV 仍为 8 样/UI 重采样网格。
- **眼度量列**：CSV 含 `eye_height_V / eye_width_ps / ber_log10`（与 v1 特征定义一致）。

## v2 实验（ml_diagnose_v2.py → results_v2.json）
1. 多标签诊断：logistic vs CNN(RX) vs CNN(RX+TX 条件) vs +遥测。
2. 码型泛化：测试集 = 未见过的 PRBS 种子（按 seed_v 划分）。
3. 无泄漏遥测消融：单故障 10 类 CNN A/B + 有损标量 A/B（v1 头条结论的复检）。
4. 开集检测：留一故障类，max-softmax 未知类 AUROC。
5. 严重度回归（单故障 r_drift / c_drift）。

## v2 主要结果（6000 样本；results_v2.json）
- **无泄漏遥测消融（核心结论复检通过）**：完整波形 0.789→0.803（遥测收益小）；有损标量体制
  高应力健康误报 **0.49→0.09**（检出率不变 ~0.72）。v1 的 37.5%→0% 含泄漏放大；v2 数值更可信。
- **多标签（阈值经验证集校准）**：CNN exact 0.54–0.59 / macro-F1 0.72；逻辑回归 exact 0.001
  （并发故障的非线性叠加，线性模型完全失效）。健康 FA 偏高（9 个检测位的并集）→ 部署应分层：
  先二分类健康门（FA 0.094），再做根因归属。
- **码型泛化**：未见 PRBS 种子上 exact 0.581 ≈ 随机划分 0.542 —— 跨随机码型训练已足够，
  TX 条件输入无一致增益（不必要）。
- **开集（负结果）**：max-softmax 留一类 AUROC 0.62/0.56/0.30 —— 未知故障被自信误判为相近
  已知类；需显式 OOD（后续工作）。
- **严重度回归稳健**：r_drift R²=0.894、c_drift R²=0.908（全部滋扰下；v1 c_drift 0.998 部分
  来自离散网格可插值性）。
