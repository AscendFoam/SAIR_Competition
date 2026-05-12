# Task Board

日期：2026-05-12

## Current Unique Task

`T03_prompt_corpus_candidate_register`: 建立第一批 prompt candidate register v0、provenance rules 和 corpus source hygiene。

任务包：

- `docs/tasks/phase_0_research_setup/T03_prompt_corpus_candidate_register.md`

状态：Ready for worker，尚未执行。

为什么现在做它：

- `T01` 已完成研究脚手架，`T02` 已完成 paper claim/evidence guardrail。
- Phase 0 还缺第一批 prompt candidate register 和 provenance rules。
- 先登记本地与可公开候选，再进入 Phase 1 的正式 corpus 清洗，可避免混入不可公开 prompt 或把结构级记录误写成可复算记录。

## Milestone 0: Research Repositioning and Repository Setup

- [x] `C00`: Captain 初始化治理文档。
- [x] `T01`: Research scaffold and seed configs。
- [x] `T02`: Paper outline v0 and contribution list extraction。
- [ ] `T03`: Prompt corpus candidate register v0 and provenance rules。

Exit criteria:

- `configs/research/`、`data/*/prompt_corpus/`、`reports/research/`、`reports/paper/` 已创建。
- `prompt_corpus_manifest.json` 存在并能解释当前 corpus 状态。
- paper outline v0 写清 RQ、contributions 和 section skeleton。
- paper claim/evidence/status 矩阵写清哪些 claim 已有证据、哪些只是计划。
- 后续任务不再以“继续 Stage2”或“继续冲榜”为默认主线。

T01 review result:

- Verdict: `PASS`
- Review file: `docs/review/T01_research_scaffold_review.md`
- Non-blocking followups: taxonomy mapping、`ce_search_depth` / `compression_style` 字段、正式 eval config 中 `repeats` 类型，将分别进入 T02/T07/T10 后续任务。

T02 review result:

- Verdict: `PASS`
- Review file: `docs/review/T02_paper_outline_contribution_matrix_review.md`
- Non-blocking followups: `outline.md` 绝对路径链接、`unsupported_do_not_claim` 示例缺失、C7 内部 justification 边界，分别进入 T03/T21 后续约束。

## Milestone 1: Public Corpus and Provenance Cleaning

- [ ] `T04`: Collect official, local, GitHub, paper and contributor prompt candidates into raw index。
- [ ] `T05`: Normalize corpus schema, hash prompt files, and generate duplicate/missing metadata report。
- [ ] `T06`: Write corpus audit summary and public/private asset boundary note。

Exit criteria:

- 至少 `8-12` 个 prompt 候选进入可分析 corpus。
- 每个候选有 source type、source ref、hash 或结构级编码原因。
- 不可公开或不可合法存储的 prompt 只做结构级记录。

## Milestone 2: Prompt Taxonomy v1

- [ ] `T07`: Manual taxonomy coding for representative prompts。
- [ ] `T08`: Implement prompt feature extractor skeleton and tests。
- [ ] `T09`: Taxonomy self-audit and conflict resolution report。

Exit criteria:

- `prompt_features_v1.jsonl` 覆盖第一批候选。
- taxonomy report 能解释字段、边界案例和复核结果。

## Milestone 3: Screening Evaluation

- [ ] `T10`: Build screening evaluation matrix。
- [ ] `T11`: Run screening on selected prompt candidates。
- [ ] `T12`: Write screening summary and shortlist report。

Exit criteria:

- shortlist 包含 `3-5` 个 prompt。
- 每个 shortlist prompt 说明代表的结构类型和进入理由。
- parse collapse、all-true/all-false collapse 被显式检查。

## Milestone 4: Full Evaluation and Recomputed Benchmark

- [ ] `T13`: Build official or near-official model eval configs。
- [ ] `T14`: Run or import full eval outputs with complete run configs。
- [ ] `T15`: Summarize model transfer gap and robustness gap。

Exit criteria:

- 主表包含 accuracy、strict F1、parse success、true/false recall、cost/time 或等价字段。
- released final evaluation subsets 明确标注为 `post-release analysis`。

## Milestone 5: Textual Distillation and Ablations

- [ ] `T16`: Human distilled prompt `D1.0` design and rationale。
- [ ] `T17`: Feature-aware prompt variants for controlled ablations。
- [ ] `T18`: Ablation summary and method decision。

Exit criteria:

- 至少一个 distillation 方法有明确正结果或负结果。
- 方法选择没有使用 released subsets 作为 reward。

## Milestone 6: Statistical Analysis and Figures

- [ ] `T19`: Descriptive and paired statistical analysis。
- [ ] `T20`: Generate paper figures and figure notes。

Exit criteria:

- 每张图都支持一个明确论文论点。
- 混杂因素和限制写入 analysis note。

## Milestone 7: Paper Draft and Reproducibility Package

- [ ] `T21`: Paper draft v0。
- [ ] `T22`: Reproducibility statement and release manifest。
- [ ] `T23`: Milestone review for publication readiness。

Exit criteria:

- 论文主贡献、实验表、图、limitations 和 attribution 完整。
- release manifest 明确哪些资产可公开，哪些仅本地保留。

## Status Rules

- Worker 完成后不直接勾选任务。
- Reviewer 给出 `PASS` 后，Captain 才把任务标记为完成。
- `PASS_WITH_WARNINGS` 的 warning 必须分类为 accepted、deferred 或 rejected。
- `BLOCK` 时只派修 blocking issue 的小任务。
