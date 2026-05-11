# Raw Idea

日期：2026-05-12

## 1. 解决什么问题

SAIR Stage1 已完成参赛提交，但已有资产不应停留在比赛归档。新的研究问题是：

> Prompt 作为文本蒸馏载体时，其结构、长度、模块顺序、输出契约、内容来源与模型和分布偏移之间有什么可量化关系？

项目要把 Stage1 公开 prompt 生态转化为一个可复现的 empirical research platform，产出 prompt corpus、feature taxonomy、统一评测协议、统计结论、textual distillation 方法和论文初稿。

## 2. 为什么现在值得做

- Stage1 参赛提交已经收口，最终提交为 `P1.2.5_minimal_rule_missing_hard_composition`。
- 仓库已有可复用工程资产：公开数据标准化、固定切分、baseline runner、complete prompt runner、verdict parser、metrics、family tagger、offline rule assets、canonical axes 和 review set。
- released final evaluation subsets 已公开，适合做后赛事实证分析，但必须明确标注 `post-release analysis`。
- 继续刷 prompt 的边际价值下降，转向 corpus 和 taxonomy 更容易形成论文贡献。

## 3. 最小可验证实验

第一阶段最小实验不是跑分，而是验证研究结构能落地：

1. 建立 `prompt_corpus` schema 和目录。
2. 列出 `8-12` 个可分析 prompt 候选。
3. 对本地 `P1.2.3`、`P1.2.5` 和官方 strict archetypes 做人工 taxonomy v0。
4. 用统一 screening matrix 跑通一个小样本评测。
5. 输出 corpus audit summary 和 taxonomy summary。

## 4. 最相似已有工作

已知最接近方向包括：

- `Less Is More: Cognitive Load and the Single-Prompt Ceiling in LLM Mathematical Reasoning`
- prompt evolution / prompt optimization 相关研究
- chain-of-thought distillation 与 textual distillation 相关研究
- formal math reasoning benchmark 与 LLM judge pipeline 相关工作

本项目的差异化点不应是“又做一批 prompt 变体”，而是：

- provenance-aware public prompt corpus
- prompt feature taxonomy
- prompt 结构和模型、split、family tag 的交叉分析
- released subsets 的后赛事实证鲁棒性分析
- feature-aware textual distillation 方法

## 5. 失败标准

出现以下情况应暂停或缩窄方向：

- 研究退化成 leaderboard 复盘。
- 只比较 prompt 总分，没有 taxonomy 或统计检验。
- 在 released subsets 上调 prompt 后宣称盲测泛化。
- prompt corpus 缺少来源、hash、许可和归因说明。
- API 成本失控，未按 screening 到 shortlist 的阶段化设计推进。
- Stage2 solver 过早占用主线。

## 6. 初筛决策

Go。

理由：已有仓库资产足以支撑 Phase 0 到 Phase 3，研究问题和非目标清晰，最小实验可在不新增大规模模型成本的前提下启动。

## 7. 当前状态

`T01_research_scaffold` 已通过 reviewer `PASS`：

- research config、prompt corpus、research reports 和 paper 目录脚手架已落地。
- corpus manifest 明确仍是 `seed_scaffold_not_collected`，没有伪称已收集语料。
- paper outline v0 已存在，但仍是 planning scaffold，不包含实验结论。

下一步唯一任务是 `T02_paper_outline_contribution_matrix`：把 outline v0 细化为 claim/evidence/contribution 矩阵，再进入真实 corpus candidate register。
