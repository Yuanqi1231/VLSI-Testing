二、项目形式项目
周期
：4周 （5月14号 – 6月11号）
分组形式
：每组 2–4 人
项目类型
：Mini Research Project 即：小问题、小数据、小系统
但需要明确问题定义、合理方法、清晰实验、有技术洞察（insight）
三、项目方向
学生可从以下方向中选择，也可自行提出相关题目（需老师批准）。
方向1：Failure Bitmap 智能分析
项目内容针对memory / TSV / chiplet互连测试产生的failure bitmap：
自动分类 fault type
聚类分析
anomaly detection
数据来源：自行生成 synthetic bitmap generator、sample fault pattern
方向2：AI辅助故障诊断
项目内容根据：fail log、scan fail信息、测试signature
自动推测：fault location、fault type、debug suggestion
可使用方法：ML classifier、LLM、Rule + AI hybrid
方向3：D2D Link异常检测（Chiplet方向）
项目内容模拟：BER、latency、thermal drift、voltage noise
使用AI：检测link degradation、anomaly detection、runtime monitoring
推荐方法：Autoencoder、LSTM、Statistical anomaly detection
方向4：AI辅助测试优化
项目内容研究：test scheduling、pattern selection、adaptive test、power-
aware test
示例：在有限 power budget 下，如何优化测试顺序？
方向5：LLM for DFT / Testing
项目内容：探索LLM在DFT中的应用，例如：自动生成test bench、自动解释fail 
log、自动生成DFT configuration、自动生成debug建议
推荐方式：Prompt engineering、RAG、Structured reasoning
四、项目要求
必须包含：
1. 问题定义：需要清楚说明：测试问题是什么？为什么重要？AI为什么适合解决？
2. 数据来源说明：数据如何获得？如何生成？是否公开数据集？
3. 方法设计说明：baseline方法、AI方法、输入输出定义
4. 实验结果包括：accuracy/detection rate、runtime、visualization、case 
study
5. 技术分析与Insight
重点讨论：AI为什么有效？
以及：AI在测试中的局限性是什么？
五、项目交付内容
1.  项目报告
（必须）建议：6–10页；包括：背景、问题定义、方法、实验结果、insight
2.  代码（必须）需要：可运行、有README
3.  最终展示（必须）6月11号
每组：10–15分钟；展示内容：问题、方法、demo、insight
几点说明：
1. 不鼓励“卷AI模型”
本项目：重点不是复杂深度学习模型，而是AI是否真正解决了测试问题
2. 不要求真实工业数据
允许 synthetic data 、simulation data 、fault injection 、public benchmark 
重点：问题是否合理
3. 不鼓励“大而空”
避免“AI for Chip Testing Platform”这类过大的题目；建议聚焦一个具体问题