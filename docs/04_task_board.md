# Task Board

## Captain Override (2026-05-23, T12 Review)

- Captain decision: accept `docs/review/T12_rerun_screening_with_alternate_low_cost_model_review.md` as `PASS_WITH_WARNINGS`.
- `T12_rerun_screening_with_alternate_low_cost_model` is complete at the Captain level.
- T12 confirmed the T11 zero-survivor screening failure on a second DeepSeek model, but it did not yet resolve the cross-provider question because both reviewed runs used the DeepSeek provider.
- Current Unique Task: `T12b_run_screening_on_non_deepseek_provider`.
- Active worker package: `docs/tasks/phase_3_screening_eval/T12b_run_screening_on_non_deepseek_provider.md`
- Warning classification for T12 review:
- accepted: `N2` (`thinking_disabled: true` is a documented execution-level compatibility setting), `N3` (JSON numeric serialization only), `N4` (temporary execution script retained as reproducibility aid), `N5` (`.claude/settings.json` noise), `N6` (handoff length is a hygiene concern but the newest Captain section remains authoritative)
- deferred: `N1` (the alternate route was a different model but not a different provider, so provider-specificity remains unresolved)
- rejected: none
- No blocking issue remains for T12. The next worker task is to attempt one genuine non-DeepSeek Stage A rerun without changing frozen non-model settings.

## Captain Override (2026-05-18, T11 Review)

- Captain decision: accept `docs/review/T11_run_screening_on_selected_prompt_candidates_review.md` as `PASS_WITH_WARNINGS`.
- `T11_run_screening_on_selected_prompt_candidates` is complete at the Captain level.
- T11 produced a legitimate screening failure on `deepseek-chat`: 0 survivors after frozen E1/E3 gates. This is treated as a model-behavior finding, not a worker defect.
- Current Unique Task: `T12_rerun_screening_with_alternate_low_cost_model`.
- Active worker package: `docs/tasks/phase_3_screening_eval/T12_rerun_screening_with_alternate_low_cost_model.md`
- Warning classification for T11 review:
- accepted: `N2` (temporary `_run_screening.py` retained as reproducibility aid), `N4` (`.claude/settings.json` noise), `N5` (P0 latency anomaly is explained by relaxed-format long outputs)
- deferred: `N1`, `N3` (metric naming drift between raw `summary.json` and screening-facing recall terminology)
- rejected: none
- T12 supersedes the earlier plan to write a shortlist-facing T12 summary immediately. We need one alternate-model rerun before any shortlist summary is trustworthy.
- This override supersedes stale "T11 is current" language below.

## Captain Override (2026-05-18)

- Captain review decision: accept `docs/review/T10_build_screening_evaluation_matrix_review.md` with verdict `PASS`.
- `T10_build_screening_evaluation_matrix` is complete at the Captain level.
- Current Unique Task: `T11_run_screening_on_selected_prompt_candidates`.
- Active worker package: `docs/tasks/phase_3_screening_eval/T11_run_screening_on_selected_prompt_candidates.md`
- Warning classification for T10 review:
- accepted: `N3` (`.claude/settings.json` noise; not part of research deliverable state)
- deferred: `N1`, `N2`, `N4` (distribution wording consistency and indirect self-audit references)
- rejected: none
- Deferred warnings must be tracked in `docs/08_risks_and_open_questions.md` and cleaned up in a later reporting/doc-hygiene task.
- No blocking issue remains for T10. The only worker task now is to execute frozen Stage A screening under T11.

日期：2026-05-17

## Current Unique Task

`T10_build_screening_evaluation_matrix`: 基于 T06 corpus gate 与 T09 taxonomy adjudication，建立可执行的 screening evaluation matrix，明确候选池、字段使用规则、run config 约束和 shortlist 准入标准。

任务包：

- `docs/tasks/phase_3_screening_eval/T10_build_screening_evaluation_matrix.md`

状态：Ready for worker，尚未执行。

为什么现在做它：

- `T09` 已通过 normal review，manual taxonomy 与 extractor skeleton 的唯一已知分歧已裁决，字段使用边界已写清。
- T10 是进入 screening execution 前的最后一个设计关口；先把候选池、矩阵 schema、字段准入和 run artifact 约束固定，能避免 T11 边跑边改 protocol。
- T09 已明确哪些字段可直接用于 screening、哪些只能 descriptive-only，T10 现在有足够稳定的输入可写成正式矩阵。

## Milestone 0: Research Repositioning and Repository Setup

- [x] `C00`: Captain 初始化治理文档。
- [x] `T01`: Research scaffold and seed configs。
- [x] `T02`: Paper outline v0 and contribution list extraction。
- [x] `T03`: Prompt corpus candidate register v0 and provenance rules。

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

T03 review result:

- Verdict: `PASS`
- Review file: `docs/review/T03_prompt_corpus_candidate_register_review.md`
- Candidate register summary: 11 candidates; 9 direct-recompute local candidates; 1 metadata-only placeholder; 1 structure-only placeholder.
- Non-blocking followups: `data/` gitignore tracking strategy、token estimate、external placeholder provenance、config typo cleanup。

T04 review result:

- Verdict: `PASS`
- Review file: `docs/review/T04_external_prompt_source_collection_review.md`
- External provenance: GitHub source verified with MIT license; Contributor Network remains host-level / structure-only.
- Git tracking: `.gitignore` narrow allowlist now covers prompt corpus governance files.
- Non-blocking followups: direct-recompute vs text-ready counts、fragile LinkedIn provenance、additional external candidates、raw index example schema alignment。

## Milestone 1: Public Corpus and Provenance Cleaning

- [x] `T04`: Collect official, local, GitHub, paper and contributor prompt candidates into raw index。
- [x] `T05`: Normalize corpus schema, hash prompt files, and generate duplicate/missing metadata report。
- [x] `T06`: Write corpus audit summary and public/private asset boundary note。

T05 review result:

- Verdict: `PASS`
- Review file: `docs/review/T05_normalize_prompt_corpus_v1_review.md`
- Corpus v1 summary: 11 records; 9 text-ready; 10 eligible; 1 metadata-only; 1 structure-only; 0 mirrored external; 0 duplicates.
- Captain action: accepted; `T05` marked complete.
- Non-blocking followups: treat `corpus_v1.jsonl` as authoritative over `candidate_register_v0.jsonl`; token estimates deferred to T07; GitHub MIT source mirror decision and Contributor Network stable URL deferred to T06 or later dedicated provenance task; missing metadata report grouping is cosmetic and not required now.

T06 review result:

- Verdict: `PASS`
- Review file: `docs/review/T06_corpus_audit_public_private_boundary_review.md`
- Boundary summary: 9 text-ready local records; 1 GitHub metadata-only record; 1 Contributor Network structure-only record; direct-recompute gate explicitly limited to the 9 text-ready records.
- Captain action: accepted; `T06` marked complete.
- Non-blocking followups: handoff wording should keep `eval-ready now = 9` distinct from manifest `eligible_count = 10`; manifest `records_present` includes a report path; `prompt_tokens_est` and external mirror/provenance issues continue into T07+.

Exit criteria:

- 至少 `8-12` 个 prompt 候选进入可分析 corpus。
- 每个候选有 source type、source ref、hash 或结构级编码原因。
- 不可公开或不可合法存储的 prompt 只做结构级记录。

Milestone 1 review status:

- Milestone review file: `docs/review/M1_review.md`
- Gate: `Conditional`
- Reason: corpus/provenance cleaning goals are complete and review-backed, but clean-environment reproducibility is only partial because external mirror/import is intentionally unresolved and taxonomy/eval inputs are not yet generated.

## Milestone 2: Prompt Taxonomy v1

- [x] `T07`: Manual taxonomy coding for representative prompts。
- [x] `T08`: Implement prompt feature extractor skeleton and tests。
- [x] `T09`: Taxonomy self-audit and conflict resolution report。

T07 review result:

- Verdict: `PASS`
- Review file: `docs/review/T07_manual_taxonomy_coding_v1_review.md`
- Deliverables: `prompt_features_v1.jsonl` with 9 records and 27 taxonomy fields; `corpus_v1.jsonl` token estimate backfill; taxonomy YAML v1 update; taxonomy report and mapping note.
- Captain action: accepted; `T07` marked complete.
- Non-blocking followups: harmonize token estimate formula wording in T08; keep low-variance fields from dominating extractor/statistical use; preserve P1.2.3 bucket-boundary sensitivity note.

T08 review result:

- Verdict: `PASS`
- Review file: `docs/review/T08_prompt_feature_extractor_skeleton_review.md`
- Deliverables: extractor skeleton for 7 high-value fields; CLI entrypoint; 90 focused tests; token estimate wording unified to `round(bytes/4)`.
- Captain action: accepted; `T08` marked complete.
- Non-blocking followups: T09 should adjudicate the P2.0.2 `counterexample_requirement` mismatch, review low-variance fields, and distinguish extractor stability tests from manual-alignment claims.

T09 review result:

- Verdict: `PASS`
- Review file: `docs/review/T09_taxonomy_self_audit_and_conflict_resolution_review.md`
- Deliverables: `self_audit_v1.md` and `conflict_resolution_v1.md`; P2.0.2 `counterexample_requirement` corrected from `optional` to `absent`; extractor/manual agreement reaches 63/63 across 7 rule-ized fields after adjudication.
- Captain action: accepted; `T09` marked complete.
- Warning handling:
  - accepted: `.claude/settings.json` tool-permission noise is unrelated and should stay out of the research commit.
  - deferred: unify low-variance field grouping wording across T09 documents; tighten the final section title/wording in `self_audit_v1.md` if later doc hygiene work is opened.
  - rejected: none.

Exit criteria:

- `prompt_features_v1.jsonl` 覆盖第一批候选。
- taxonomy report 能解释字段、边界案例和复核结果。

Milestone 2 review status:

- Gate: `Pass`
- Reason: T07 manual coding、T08 extractor skeleton 和 T09 self-audit/conflict resolution 已共同满足“taxonomy report 能解释字段、边界案例和复核结果”的退出条件；但 T10 之后仍需继续遵守 low-variance 与 manual-authoritative 的使用边界。

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
