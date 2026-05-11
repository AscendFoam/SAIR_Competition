# Research Reports

本目录用于存放 Stage1 后赛事实证科研的可读报告骨架。

当前脚手架对应的子目录职责：

- `corpus_audit/`: 语料规模、来源、hash 覆盖、缺失元数据、license 或 ToS 风险。
- `taxonomy/`: prompt feature taxonomy 的定义、自审和冲突处理说明。
- `screening/`: 小样本筛选、shortlist 和塌缩排查。
- `full_eval/`: 统一配置下的完整复算结果摘要。
- `statistical_analysis/`: 描述统计、配对分析与假设检验说明。
- `figures/`: 论文图表备注、绘图依赖和 figure narrative。

约束：

- 这里是研究报告层，不是原始运行产物层。
- 任何涉及 released final evaluation subsets 的部分都要显式写 `post-release analysis`。
- 没有完成的实验只能写计划、模板或待填状态，不能写成既成事实。
