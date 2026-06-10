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
