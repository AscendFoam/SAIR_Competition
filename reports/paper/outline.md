# Paper Outline v0

状态：planning scaffold，非结果定稿。

## Working Title

Prompt-Based Textual Distillation for Formal Equational Reasoning through the Public SAIR Stage1 Ecosystem

中文工作标题：

基于 SAIR Stage1 公开 prompt 生态的形式代数推理文本蒸馏：语料、结构 taxonomy 与鲁棒性分析

## Core Claim

本文拟研究 SAIR Stage1 公开 prompt 生态中可重复出现的结构模式，构建 provenance-aware prompt corpus 与 feature taxonomy，量化 prompt 结构如何与模型迁移、分布偏移和鲁棒性相关，并评估一种 feature-aware textual distillation 方法是否能改善 parse 或 recall 稳定性。

## Research Questions

- `RQ1`: Stage1 公开 prompt 生态中有哪些可重复出现的结构模块？
- `RQ2`: Prompt 长度、模块顺序、输出契约、counterexample 使用方式与性能指标有什么统计关系？
- `RQ3`: 哪些 prompt 结构在模型间迁移稳定，哪些结构具有明显 model-specific bias？
- `RQ4`: public split 到 released final evaluation subsets 的掉点主要来自哪些结构与分布偏移？
- `RQ5`: 基于公开 prompt corpus 和错误模式的 textual distillation，能否降低 robustness gap 或提升 parse/recall 稳定性？
- `RQ6`: Stage1 文本蒸馏的边界在哪里，它与传统 model distillation、CoT distillation、feedback-driven distillation 有什么关系？

## Contribution List

- 一个带 provenance 的公开 prompt corpus schema 与 manifest 机制。
- 一个面向 Stage1 cheatsheet-style prompts 的 feature taxonomy。
- 一个统一的 screening / recomputed benchmark / post-release analysis 评测矩阵。
- 一组关于 prompt 结构、模型迁移和分布偏移的经验结论。
- 一个小而清晰的 feature-aware textual distillation 方法与受控消融。

## Section Skeleton

1. Introduction
2. Background: SAIR Stage1 and Prompt Textual Distillation
3. Public Prompt Corpus and Feature Taxonomy
4. Experimental Setup
5. Structural Findings
6. Feature-aware Textual Distillation
7. Robustness and Failure Analysis
8. Related Work
9. Limitations, Ethics, and Attribution
10. Conclusion

## Planned Figures

- Prompt length vs performance scatter
- Recall tradeoff plot
- Accuracy-cost-latency Pareto view
- Prompt feature by model heatmap
- Public split vs released subset robustness matrix
- Family-conditioned error heatmap
- `P1_2_3` vs `P1_2_5` risk profile comparison

## Current Evidence Status

- corpus scaffold: available
- taxonomy scaffold: available
- evaluation matrix scaffold: available
- prompt corpus collection: not started
- screening results: not started
- full recomputed benchmark: not started
- post-release analysis: not started
- distillation method evidence: not started

## Not-Yet-Supported Claims

- 不能声称 feature-aware textual distillation 已经提升鲁棒性。
- 不能声称某种 module order 在所有模型上稳定更优。
- 不能声称 released final evaluation subsets 上的观察代表赛时未知盲测泛化。
- 不能声称当前 corpus 已覆盖全部 Stage1 参赛生态。
