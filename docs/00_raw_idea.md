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

`T02_paper_outline_contribution_matrix` 已通过 reviewer `PASS`：

- paper outline v0 已细化为论文设计文档。
- `reports/paper/contribution_list.md` 已列出贡献、证据需求和当前状态。
- `reports/paper/claim_evidence_matrix.md` 已把允许措辞和禁止措辞显式化。

下一步唯一任务是 `T03_prompt_corpus_candidate_register`：建立第一批 prompt candidate register v0 和 provenance rules。T03 仍不跑 API，不改 prompt wording，只登记候选、来源边界和可复算资格。

`T03_prompt_corpus_candidate_register` 已通过 reviewer `PASS`：

- candidate register v0 已登记 11 个候选，其中 9 个本地候选具备已验证 hash 和 byte size。
- provenance rules 已写清 direct-recompute、metadata-only、structure-only 和 excluded 的边界。
- corpus manifest 仍诚实标注为 `candidate_register_v0_not_cleaned`，没有把候选登记写成 completed corpus。

下一步唯一任务是 `T04_external_prompt_source_collection`：进入 Phase 1，核验外部 prompt placeholders 的来源、URL、作者/团队和 license/ToS 边界，并决定 `data/*/prompt_corpus` 文件如何进入 git。

`T04_external_prompt_source_collection` 已通过 reviewer `PASS`：

- `.gitignore` 已用窄 allowlist 放开 prompt corpus governance files，没有放开原始私有数据。
- 外部 GitHub 来源已核验 URL、作者和 MIT license，但尚未镜像 prompt 原文。
- Contributor Network 来源仅有 host-level provenance，仍保留为 structure-only。

`T05_normalize_prompt_corpus_v1` 已通过 reviewer `PASS`：

- `corpus_v1.jsonl` 已规范化 11 条记录。
- 其中 9 条 text-ready、10 条 eligible、1 条 metadata-only、1 条 structure-only。
- duplicate report 显示当前无重复；missing metadata report 记录了本地记录的 policy-exempt source_url 缺失和两个外部占位项的 actionable 缺口。
- GitHub MIT source 在 T05 未镜像，仍为 metadata-only；Contributor Network 仍为 structure-only。

`T06_corpus_audit_public_private_boundary` 已通过 reviewer `PASS`：

- `public_private_boundary.md` 已明确 9 条 text-ready、1 条 GitHub metadata-only、1 条 Contributor Network structure-only 的使用边界。
- `corpus_v1.jsonl` 已被正式声明为下游 authoritative snapshot。
- T07/T10 的 direct recompute gate 已写清：只有 text-ready + local path + SHA256 记录可进入 full-text coding 或直接复算。

Milestone 1 已完成一次里程碑审查，结论为 `Conditional`：

- Public corpus 与 provenance cleaning 的目标已完成并有 review 支撑。
- 但 clean-environment reproducibility 仍是部分成立，因为外部镜像导入刻意未做，taxonomy/eval 产物仍未生成。

下一步唯一任务是 `T07_manual_taxonomy_coding_v1`：对 9 条 text-ready records 做人工 taxonomy 编码，补足 `prompt_tokens_est` 和 plan-to-schema mapping，为 T08 extractor skeleton 与 T10 screening 准备结构化输入。
