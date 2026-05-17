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

`T09_taxonomy_self_audit_and_conflict_resolution`

任务包：

- `docs/tasks/phase_2_prompt_taxonomy/T09_taxonomy_self_audit_and_conflict_resolution.md`

状态：

- Ready for worker，尚未执行。
- T01、T02、T03、T04、T05、T06、T07、T08 已通过 review 并由 Captain 标记完成。

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

T07 worker 执行结果：

- Task: `T07_manual_taxonomy_coding_v1`
- 状态: worker 已执行，待 review。
- Coding pool: 9 条 text-ready local records，排除了 1 条 metadata-only 和 1 条 structure-only。
- Token estimate: 使用 bytes/4 启发式估算，非 tokenizer 精确计数。
- Changed files: `data/interim/prompt_corpus/prompt_features_v1.jsonl` (new), `data/interim/prompt_corpus/corpus_v1.jsonl` (token estimate backfill), `configs/research/prompt_feature_taxonomy.yaml` (v1 update), `reports/research/taxonomy/taxonomy_v1.md` (new), `reports/research/taxonomy/taxonomy_mapping_note.md` (new), `reports/research/taxonomy/README.md` (updated), `docs/07_handoff.md` (updated)。
- T08 extractor skeleton 尚未执行。
- T10 screening 尚未开始。

T08 worker 执行结果：

- Task: `T08_prompt_feature_extractor_skeleton`
- 状态: worker 已执行，待 review。
- Extractor module: `src/sair_competition/analysis/prompt_features.py`
- Rule-ized fields: 7 (prompt_bytes_bucket, prompt_tokens_est_bucket, verdict_contract, rule_or_heuristic_block, opening_strategy, counterexample_requirement, explicit_final_token)
- Known disagreement: P2.0.2 counterexample_requirement (extractor: absent, manual: optional)
- Token estimate wording: unified to `round(bytes/4)` in taxonomy_v1.md and taxonomy YAML
- Tests: 90 focused tests, all passing (schema, bucket boundaries, field alignment on all 9 prompts, boundary gate, round-trip JSON)
- Changed files: `src/sair_competition/analysis/prompt_features.py` (new), `src/sair_competition/analysis/__init__.py` (updated), `src/sair_competition/cli.py` (updated), `tests/test_prompt_feature_extractor.py` (new), `reports/research/taxonomy/extractor_v1_notes.md` (new), `reports/research/taxonomy/taxonomy_v1.md` (token estimate fix), `reports/research/taxonomy/README.md` (updated), `configs/research/prompt_feature_taxonomy.yaml` (estimation_method fix), `docs/07_handoff.md` (updated)。
- T09 self-audit 尚未开始。
- T10 screening 尚未开始。

T08 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T08_prompt_feature_extractor_skeleton_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T08。
- Extractor result: 7 个高价值字段已规则化；CLI 入口已存在；90 项 focused tests 全部通过；token estimate 文档口径已统一为 `round(bytes/4)`。
- Non-blocking followups:
  - T09 复核 P2.0.2 `counterexample_requirement` 的 manual vs extractor 分歧。
  - T09 明确低方差字段的保留/降权/仅说明性使用策略。
  - T09 区分“extractor 行为稳定性测试”与“manual coding 一致性主张”的边界。

T07 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T07_manual_taxonomy_coding_v1_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T07。
- Coding result: `prompt_features_v1.jsonl` 9 条记录、27 个 taxonomy 字段；`corpus_v1.jsonl` 已回填 token estimate；taxonomy YAML 新增 `compression_style`、`ce_search_depth`、`bucket_boundary_notes`。
- Non-blocking followups:
  - T08 修正文档中 token estimate `floor` vs `round` 口径不一致。
  - T08/T09 注意低方差字段不应主导 extractor 或统计解释。
  - 保留 P1.2.3 bucket boundary sensitivity note，不在当前阶段强行重分桶。

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
docs/review/T08_prompt_feature_extractor_skeleton_review.md
docs/review/M1_review.md
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/research/corpus_audit/summary.md
reports/research/corpus_audit/public_private_boundary.md
configs/research/prompt_feature_taxonomy.yaml
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
reports/research/taxonomy/extractor_v1_notes.md
src/sair_competition/analysis/prompt_features.py
tests/test_prompt_feature_extractor.py
```

## 4. Worker 执行边界

下一位 worker 只执行 T09。

- 基于 `prompt_features_v1.jsonl`、`extractor_v1_notes.md`、T08 tests 和 extractor 输出做 taxonomy self-audit。
- 重点处理 P2.0.2 `counterexample_requirement` 分歧、低方差字段处理策略、以及 extractor-stability vs manual-alignment 的叙事边界。
- T10 screening 仍不应先于 T09 启动。

允许修改文件：

- `data/interim/prompt_corpus/prompt_features_v1.jsonl`
- `reports/research/taxonomy/README.md`
- `reports/research/taxonomy/taxonomy_v1.md`
- `reports/research/taxonomy/taxonomy_mapping_note.md`
- `reports/research/taxonomy/extractor_v1_notes.md`
- `reports/research/taxonomy/self_audit_v1.md`
- `reports/research/taxonomy/conflict_resolution_v1.md`
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

T07 taxonomy coding summary：

- coded records: `9` (all text-ready local)
- excluded non-text-ready records: `2` (1 metadata-only, 1 structure-only)
- token estimate method: bytes/4 heuristic, not tokenizer
- taxonomy fields coded: `27` (4 length + 6 structural + 3 module order + 4 counterexample + 3 true strategy + 3 output stability + 3 provenance + 1 compression_style)
- prompt families identified: `4` (minimal baseline, guardrail-heavy lineage, official archetype adaptations, reserved external)

## 5. Reviewer 重点

T09 reviewer 类型：normal。

重点检查：

- 是否真实复核了 manual taxonomy 与 extractor 结果之间的已知分歧，而不是只复述已有文档。
- 是否对低方差字段给出了清晰、可执行的保留/降权/仅说明性使用策略。
- 若修改 `prompt_features_v1.jsonl`，是否逐条说明理由，没有静默改动。
- 是否没有越过 T06 boundary gate 把 non-text-ready records 拉入 full-text coding。
- 是否为 T10 screening 留下清晰、可信的 taxonomy 输入与限制说明。

## 6. 完成 T09 后 Captain 要做

如果 review 为 `PASS`：

1. 在 `docs/04_task_board.md` 勾选 `T09`。
2. 更新本文件的当前状态。
3. 可以推荐进入 `T10`，但不直接执行。
4. 若自审未真正处理已知分歧、低方差字段策略空泛、或静默改动人工标注，则阻止进入 T10。

如果 `PASS_WITH_WARNINGS`：

1. 把 warning 分类为 accepted、deferred、rejected。
2. deferred 写入 `docs/08_risks_and_open_questions.md`。
3. 再决定是否进入下一任务。

如果 `BLOCK`：

1. 只派修 blocking issue 的小任务。
2. 同一任务最多自动复审一次。
3. 第二次仍 BLOCK 则停止交给用户裁决。

## 7. 当前未验证事项

- T09 taxonomy self-audit 尚未执行。
- T08 extractor 有 1 个已知分歧：P2.0.2 counterexample_requirement (extractor: absent, manual: optional)。
- T07 无 inter-annotator agreement（单编码者），T09 self-audit 应复核编码一致性。
- GitHub MIT external source 仍未镜像，本地 external text-ready record 仍为 `0`。
- contributor-network 占位项仍只有 host-level official provenance，尚未解析到稳定的具体 prompt 页面。
- screening / recomputed benchmark / post-release analysis 仍未开始执行。
- T10 screening 仍不应先于 T09 启动主线执行。
