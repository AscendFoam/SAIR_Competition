# Handoff

日期：2026-05-17

## 1. 当前项目状态

项目已从 Stage1 参赛收口切换到 Stage1 后赛事实证科研。核心基准文档是：

- `docs/02_experiment_plan.md`
- `docs/reference/AI_coding_workflow.md`

当前治理文档已初始化：

- `AGENTS.md`
- `CLAUDE.md`
- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## 2. Current Unique Task

`T07_manual_taxonomy_coding_v1`

任务包：

- `docs/tasks/phase_2_prompt_taxonomy/T07_manual_taxonomy_coding_v1.md`

状态：

- Ready for worker，尚未执行。
- T01、T02、T03、T04、T05、T06 已通过 review 并由 Captain 标记完成。

T01 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T01_research_scaffold_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T01。
- Non-blocking followups: T03 清理 `storage_policy` typo；T07 前补 taxonomy mapping、`compression_style` 和 `ce_search_depth` 决策；T10 前收敛 `repeats` schema。

T02 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T02_paper_outline_contribution_matrix_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T02。
- Non-blocking followups: T03 修正 `outline.md` 绝对路径链接；T03/T21 前补 rejected/unsupported claim；C7 只保留为 setup/motivation。

T03 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T03_prompt_corpus_candidate_register_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T03。
- Candidate register: 11 candidates total; 9 direct-recompute local candidates; 1 metadata-only placeholder; 1 structure-only placeholder.
- Non-blocking followups: T04 处理 `data/*/prompt_corpus` git tracking strategy；T04 补 external placeholder URL/author/license；T05/T07 后续处理 token estimates。

T04 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T04_external_prompt_source_collection_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T04。
- Git tracking: `.gitignore` narrow allowlist for prompt corpus governance files。
- External provenance: GitHub MIT source verified but not mirrored; Contributor Network remains host-level / structure-only。
- Non-blocking followups: T05 split eligible/text-ready counts；T05/T06 seek stable contributor URL and more external candidates；T05 align raw_index example schema。

T05 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T05_normalize_prompt_corpus_v1_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T05。
- Corpus v1: 11 records; 9 text-ready; 10 eligible; 1 metadata-only; 1 structure-only; 0 mirrored external; 0 duplicates.
- Non-blocking followups: `corpus_v1.jsonl` 作为 authoritative corpus snapshot；token estimate deferred to T07；GitHub MIT mirror decision and Contributor Network stable URL deferred to T06 or later provenance task；missing metadata grouping cosmetic and not required now。

T06 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T06_corpus_audit_public_private_boundary_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T06。
- Boundary note summary: 9 text-ready local records; 1 GitHub metadata-only record; 1 Contributor Network structure-only record; 0 excluded; direct-recompute gate explicitly limited to the 9 text-ready records.
- Non-blocking followups: handoff wording should keep `eval-ready now = 9` distinct from manifest `eligible_count = 10`; manifest `records_present` includes one report path; `prompt_tokens_est`、GitHub MIT mirror decision、Contributor Network stable URL 继续 deferred。

Milestone 1 review 判断：

- Verdict: `Conditional`
- Review file: `docs/review/M1_review.md`
- Captain action: accepted as milestone gate; Milestone 1 closes and Milestone 2 may start。
- Gate condition: T07/T10 must continue to use `corpus_v1.jsonl` plus T06 boundary gates as the only eligibility source; metadata-only / structure-only records stay out of full-text coding and eval until a later reviewed task changes status。

## 3. 下一位 Worker 需要先读

```text
README.md
AGENTS.md
docs/02_experiment_plan.md
docs/03_architecture.md
docs/04_task_board.md
docs/06_eval_protocol.md
docs/07_handoff.md
docs/08_risks_and_open_questions.md
docs/tasks/phase_2_prompt_taxonomy/T07_manual_taxonomy_coding_v1.md
docs/review/T06_corpus_audit_public_private_boundary_review.md
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/research/corpus_audit/summary.md
reports/research/corpus_audit/public_private_boundary.md
configs/research/prompt_feature_taxonomy.yaml
```

## 4. Worker 执行边界

下一位 worker 只执行 T07：

- 基于 `corpus_v1.jsonl` 和 T06 boundary gate，对 9 条 text-ready local prompts 做人工 taxonomy coding。
- 生成第一版 `prompt_features_v1.jsonl`、taxonomy report 和 experiment-plan 到 taxonomy seed 的 mapping note。
- 为 9 条 text-ready records 回填 reviewable 的 `prompt_tokens_est` 与 length bucket，供后续 T08/T10 使用。
- 保持 GitHub metadata-only 和 Contributor Network structure-only 记录不进入 full-text coding。

不要做：

- 不改 `src/`。
- 不跑 API eval。
- 不改 prompt wording。
- 不下载或镜像外部 prompt 原文。
- 不删除或重命名历史文档。
- 不改 `docs/04_task_board.md` 完成状态。

允许修改文件：

- `data/interim/prompt_corpus/corpus_v1.jsonl`
- `data/interim/prompt_corpus/prompt_features_v1.jsonl`
- `configs/research/prompt_feature_taxonomy.yaml`
- `reports/research/taxonomy/README.md`
- `reports/research/taxonomy/taxonomy_v1.md`
- `reports/research/taxonomy/taxonomy_mapping_note.md`
- `docs/07_handoff.md`

Current corpus boundary summary：

- text-ready records: `9`
- metadata-only records: `1`
- structure-only records: `1`
- eval-eligible now: `9` (`eligible_count = 10` in manifest still includes the metadata-only GitHub record as provenance-eligible, not eval-ready-now)
- external prompt text mirrored: no
- T07/T10 gating rule: only text-ready records with local path and SHA256 may enter direct recompute

T05 corpus summary：

- `corpus_v1_record_count = 11`
- `eligible_count = 10`
- `text_ready_count = 9`
- `mirrored_external_count = 0`
- `metadata_only_count = 1`
- `structure_only_count = 1`
- `excluded_count = 0`
- duplicate report: no duplicates found in T05
- mirrored GitHub prompt text: no

## 5. Reviewer 重点

T07 reviewer 类型：normal。

重点检查：

- 是否只对 9 条 text-ready local records 做 full-text taxonomy coding。
- `prompt_features_v1.jsonl` 是否与 taxonomy seed 和 mapping note 一致，且没有把 extractor 或 eval 写成已完成。
- `prompt_tokens_est` 与 length bucket 口径是否诚实、可复核、不过度宣称。
- 是否没有把 metadata-only / structure-only 记录提升为 full-text coded 或 eval-ready。
- 是否为 T08 extractor skeleton 和 T10 screening 留下清晰、可解析的输入。

## 6. 完成 T07 后 Captain 要做

如果 review 为 `PASS`：

1. 在 `docs/04_task_board.md` 勾选 `T07`。
2. 更新本文件的当前状态。
3. 可以推荐进入 `T08`，但不直接执行。
4. 若 taxonomy coding 越过 T06 boundary gate、把 metadata-only 或 structure-only 记录做成 full-text features、或把 token estimate 写成未经支持的精确 claim，则阻止进入 T08。

如果 `PASS_WITH_WARNINGS`：

1. 把 warning 分类为 accepted、deferred、rejected。
2. deferred 写入 `docs/08_risks_and_open_questions.md`。
3. 再决定是否进入下一任务。

如果 `BLOCK`：

1. 只派修 blocking issue 的小任务。
2. 同一任务最多自动复审一次。
3. 第二次仍 BLOCK 则停止交给用户裁决。

## 7. 当前未验证事项

- T07 manual taxonomy coding 尚未执行。
- GitHub MIT external source 仍未镜像，本地 external text-ready record 仍为 `0`。
- contributor-network 占位项仍只有 host-level official provenance，尚未解析到稳定的具体 prompt 页面。
- `prompt_tokens_est` 在 `corpus_v1` 中仍全部为 `0`。
- screening / recomputed benchmark / post-release analysis 仍未开始执行。
- T08/T10 仍依赖 T07 先给出稳定的 manual taxonomy 与 length-bucket 口径。
