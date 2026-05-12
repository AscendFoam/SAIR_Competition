# Paper Outline v0

状态：planning document，非结果定稿。

## Working Title

Prompt-Based Textual Distillation for Formal Equational Reasoning through the Public SAIR Stage1 Ecosystem

中文工作标题：

基于 SAIR Stage1 公开 prompt 生态的形式代数推理文本蒸馏：语料、结构 taxonomy 与鲁棒性分析

## Abstract Draft

We plan to study prompt-based textual distillation for formal equational reasoning through the public SAIR Stage1 ecosystem. The paper will construct a provenance-aware prompt corpus, define a feature taxonomy for cheatsheet-style prompts, and use a unified evaluation protocol to analyze how prompt structure interacts with model transfer and distribution shift. We will also evaluate whether a feature-aware distilled prompt family can improve robustness or parse and recall stability relative to strong local baselines. At the current stage, this is a design target rather than a completed empirical result; corpus collection, screening, full recomputation, and post-release analysis are still pending.

中文摘要草稿：

本文拟基于 SAIR Stage1 公开 prompt 生态，构建带来源追踪的 prompt corpus，定义 cheatsheet-style prompt 的结构 taxonomy，并通过统一评测协议分析 prompt 结构与跨模型迁移、跨分布鲁棒性之间的关系。论文还计划验证一组 feature-aware distilled prompt 是否能够相对于当前本地强基线改善鲁棒性或 parse/recall 稳定性。当前该摘要仅代表研究设计目标，不代表相关实验已经完成；corpus 收集、screening、完整复算和 post-release analysis 仍待后续任务执行。

## Core Claim

当前允许的核心主张只能写成研究意图：

> We study the public SAIR Stage1 prompt ecosystem as a provenance-aware textual distillation setting and test whether prompt structure can explain transfer and robustness behavior across models and splits.

目前还不能把方法效果写成既有结果。

## Research Questions

- `RQ1`: Stage1 公开 prompt 生态中有哪些可重复出现的结构模块？
- `RQ2`: Prompt 长度、模块顺序、输出契约、counterexample 使用方式与性能指标有什么统计关系？
- `RQ3`: 哪些 prompt 结构在模型间迁移稳定，哪些结构具有明显 model-specific bias？
- `RQ4`: public split 到 released final evaluation subsets 的掉点主要来自哪些结构与分布偏移？
- `RQ5`: 基于公开 prompt corpus 和错误模式的 textual distillation，能否降低 robustness gap 或提升 parse/recall 稳定性？
- `RQ6`: Stage1 文本蒸馏的边界在哪里，它与传统 model distillation、CoT distillation、feedback-driven distillation 有什么关系？

## Contribution List Summary

- `C1`: 一个带 provenance 的公开 prompt corpus schema、manifest 机制与来源边界说明。
- `C2`: 一个面向 Stage1 cheatsheet-style prompts 的 feature taxonomy 及其与 problem family tags 的分层关系。
- `C3`: 一个统一的 `screening / recomputed benchmark / post-release analysis` 评测协议与结果记录规范。
- `C4`: 一组关于 prompt 结构、模型迁移、分布偏移和风险画像的经验发现。
- `C5`: 一个小而可控的 feature-aware textual distillation 方法家族与受控消融。
- `C6`: 一个带 attribution、release boundary 和复现说明的研究交付包。

详细状态见 [contribution_list.md](D:/Codes/Math/SAIR_Competition/reports/paper/contribution_list.md)。

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

## Planned Tables

- Table 1: Prompt corpus source breakdown, visibility level, and storage policy.
- Table 2: Prompt taxonomy dimensions and field definitions.
- Table 3: Screening shortlist by prompt family, structure type, and parse stability.
- Table 4: Main recomputed benchmark across prompt, model, and split.
- Table 5: Post-release analysis robustness gap and model transfer gap.
- Table 6: Feature-aware distillation ablation summary.

## Planned Figures

- Prompt length vs performance scatter with LOESS.
- True recall vs false recall tradeoff plot.
- Accuracy-cost-latency Pareto view.
- Prompt feature by model heatmap.
- Public split vs released final evaluation subsets robustness matrix.
- Family-conditioned error heatmap.
- `P1_2_3` vs `P1_2_5` risk profile comparison.

## Evidence Status

- research framing: supported by local planning docs
- Stage1 asset inventory: supported by existing local reports and repository structure
- corpus scaffold and manifest: supported by T01 outputs
- prompt corpus collection: not started
- taxonomy scaffold: supported by T01 output
- taxonomy field mapping from experiment plan section 6.2 to YAML: missing and required before T07
- screening protocol framing: supported by local protocol docs
- actual screening evidence: not started
- full recomputed benchmark evidence: not started
- post-release analysis evidence: not started
- feature-aware distillation method evidence: not started
- reproducibility and attribution package: planned, not assembled

## Current Evidence Sources

- `docs/02_experiment_plan.md`
- `docs/06_eval_protocol.md`
- `docs/08_risks_and_open_questions.md`
- `docs/项目工作历程与阶段性成果总结.md`
- `docs/Stage1结果调研报告.md`
- `docs/review/T01_research_scaffold_review.md`
- `reports/paper/contribution_list.md`
- `reports/paper/claim_evidence_matrix.md`

## Explicit Post-Release Analysis Caveat

论文中所有对 `released final evaluation subsets` 的使用都必须写成 `post-release analysis`。这些 subsets 不能作为 prompt selection reward，也不能被描述成赛时未知盲测。

## Not-Yet-Supported Claims

- 不能声称 feature-aware textual distillation 已经提升鲁棒性。
- 不能声称某种 module order 在所有模型上稳定更优。
- 不能声称 released final evaluation subsets 上的观察代表赛时未知盲测泛化。
- 不能声称当前 corpus 已覆盖全部 Stage1 参赛生态。
- 不能声称 taxonomy YAML 已经与实验计划第 6.2 节字段一一对齐。
- 不能声称 `compression_style` 和 `ce_search_depth` 已经在 TAX_V1 中得到最终决策。

## Writing Constraints For Next Tasks

- T03 收集 corpus candidate 时必须服务于 `RQ1-RQ6`，不能退回“继续找更高分 prompt”叙事。
- T07 之前必须明确 experiment plan feature 到 YAML 字段的 mapping。
- T10 之前必须收敛正式评测配置里 `repeats` 的 schema。
