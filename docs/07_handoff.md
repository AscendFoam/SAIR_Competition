# Handoff

## Captain Override (2026-05-18)

Current Unique Task:
- `T11_run_screening_on_selected_prompt_candidates`

Captain decision on review:
- `docs/review/T10_build_screening_evaluation_matrix_review.md` verdict `PASS` is accepted.
- `T10_build_screening_evaluation_matrix` is complete and does not require another automatic review cycle.

Ready-for-worker package:
- `docs/tasks/phase_3_screening_eval/T11_run_screening_on_selected_prompt_candidates.md`

Worker scope for T11:
- Execute the frozen Stage A screening on the 9 text-ready local prompts.
- Produce reproducible run artifacts under `artifacts/research_runs/screening/`.
- Write `reports/research/screening/screening_execution_manifest_v1.md`.
- Update this handoff file only with execution facts, artifact paths, provider route, and failed/partial run status.

Deferred follow-ups from T10 review:
- `N1`: wording in `screening_matrix_v1.md` should be aligned with authoritative `prompt_features_v1.jsonl` distributions.
- `N2`: wording in `screening_candidate_registry_v1.md` should be aligned with the same authoritative distributions.
- `N4`: indirect references to self-audit / conflict-resolution evidence should be rewritten more directly for report hygiene.

Accepted non-risk:
- `N3`: `.claude/settings.json` noise is accepted as unrelated workspace noise and should not drive research-state decisions.

日期：2026-05-18

## 1. 当前项目状态

项目当前主线仍是 SAIR Stage1 后赛事实证科研，不是继续刷榜，也不是启动 Stage2 solver。研究基线与工作纪律由以下文件定义：

- `docs/02_experiment_plan.md`
- `docs/reference/AI_coding_workflow.md`
- `AGENTS.md`

治理主文件现况：

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

截至当前，T01-T09 均已通过 review 并被 Captain 接受。当前已完成：

- public prompt corpus v1 与 public/private boundary
- 9 条 text-ready local prompts 的 manual taxonomy v1
- 7 个高价值字段的 extractor skeleton 与 focused tests
- taxonomy self-audit、conflict resolution 与 1 处最小数据校正

## 2. Current Unique Task

`T10_build_screening_evaluation_matrix`

任务包：

- `docs/tasks/phase_3_screening_eval/T10_build_screening_evaluation_matrix.md`

状态：

- Worker 已执行，待 review。

T10 worker 执行结果：

- Task: `T10_build_screening_evaluation_matrix`
- 状态: worker 已执行，待 review。
- Screening matrix: `reports/research/screening/screening_matrix_v1.md`（候选池 9 条、smoke split、单模型、repeats=1、parse/collapse gates）
- Candidate registry: `reports/research/screening/screening_candidate_registry_v1.md`（6 core + 3 contrast、excluded records、structural coverage gaps）
- Shortlist rules: `reports/research/screening/screening_shortlist_rules_v1.md`（elimination E1-E4、inclusion I1-I2、anchor-based assembly、target 3-5）
- Config 收敛: `evaluation_matrix.example.json` 中 screening phase prompt_set 已替换为 9 条实际 prompt_id；`repeats` 已统一为整数；`"1-3"` 字符串已消除
- Changed files: `reports/research/screening/screening_matrix_v1.md` (new), `reports/research/screening/screening_candidate_registry_v1.md` (new), `reports/research/screening/screening_shortlist_rules_v1.md` (new), `configs/research/evaluation_matrix.example.json` (updated), `configs/research/README.md` (updated), `reports/research/screening/README.md` (updated), `docs/07_handoff.md` (updated)
- T11 screening execution 尚未开始。

## 3. 已完成任务摘要

### T01-T06：Corpus / Provenance 基线

- T01-T03：完成 research scaffold、paper claim guardrail、prompt candidate register。
- T04：完成外部 provenance v0 和 `.gitignore` 窄 allowlist。
- T05：完成 `corpus_v1.jsonl`，11 条记录中 9 条 text-ready、1 条 metadata-only、1 条 structure-only。
- T06：完成 `public_private_boundary.md`，明确只有 9 条 text-ready + local path + SHA256 的记录可进入 full-text coding / direct recompute。

### T07：Manual taxonomy coding

- `data/interim/prompt_corpus/prompt_features_v1.jsonl`
- 9 条 text-ready local prompts
- 27 个 taxonomy 字段
- token estimate 采用 `round(bytes/4)` 启发式估算

### T08：Extractor skeleton

- `src/sair_competition/analysis/prompt_features.py`
- CLI 入口已存在
- 7 个 rule-ized fields
- 90 项 focused tests 全部通过

### T09：Self-audit and conflict resolution

- `reports/research/taxonomy/self_audit_v1.md`
- `reports/research/taxonomy/conflict_resolution_v1.md`
- P2.0.2 `counterexample_requirement` 从 `optional` 校正为 `absent`
- extractor/manual agreement 达到 63/63（7 fields x 9 prompts）
- 10 个低方差字段保留在 schema 中，但排除出统计模型，仅作 descriptive labels
- reporting boundary 固定为：manual coding = authoritative taxonomy truth；extractor = supporting cross-check

## 4. 下一位 Worker 必读

```text
README.md
AGENTS.md
docs/02_experiment_plan.md
docs/03_architecture.md
docs/04_task_board.md
docs/06_eval_protocol.md
docs/07_handoff.md
docs/08_risks_and_open_questions.md
docs/review/T10_build_screening_evaluation_matrix_review.md
docs/review/M1_review.md
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/research/corpus_audit/summary.md
reports/research/corpus_audit/public_private_boundary.md
configs/research/prompt_feature_taxonomy.yaml
configs/research/evaluation_matrix.example.json
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
reports/research/taxonomy/extractor_v1_notes.md
reports/research/taxonomy/self_audit_v1.md
reports/research/taxonomy/conflict_resolution_v1.md
reports/research/screening/README.md
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
src/sair_competition/analysis/prompt_features.py
tests/test_prompt_feature_extractor.py
```

## 5. Worker 执行边界

T10 已执行，待 review。下一位 worker 不应重复执行 T10。

- 如 review 为 PASS，可进入 T11 (run screening on selected prompt candidates)。
- T11 应基于 `screening_matrix_v1.md` 定义的 matrix 执行 screening。
- T11 需填入 `provider_route` 实际值，但不得更改 screening phase 的其他 frozen 字段（temperature, max_tokens, reasoning_mode, repeats, prompt_set, dataset_set）。
- T11 应使用 `screening_shortlist_rules_v1.md` 做 shortlist 决策，T12 写 screening summary。

允许修改文件：

- `docs/04_task_board.md`（仅 Captain，勾选 T10）
- 其他文件由 T11 任务包定义

T11 任务包未创建前，worker 不应提前执行 T11。

## 6. Current corpus / taxonomy facts

Current corpus boundary summary：

- total corpus records: `11`
- text-ready local records: `9`
- metadata-only records: `1`
- structure-only records: `1`
- eval-eligible now: `9`
- mirrored external text-ready records: `0`

Current taxonomy / extractor summary：

- taxonomy fields coded: `27`
- rule-ized fields: `7`
- extractor/manual agreement after T09 adjudication: `63/63`
- low-variance fields excluded from models: `10`
- authoritative corrected mismatch count: `1` historical mismatch, now resolved

## 7. Reviewer 重点（给 T10）

T10 reviewer 类型应为 `normal`。

重点检查：

- screening matrix 是否只使用 T06/T09 允许的候选池（9 条 text-ready）和字段。
- `repeats` 是否从 `"1-3"` 说明性字符串收敛为正式可执行整数。
- 是否清楚区分 T10 matrix 设计 与 T11 screening execution。
- 是否把 10 个低方差字段正确降为 descriptive-only，不作为 shortlist 主决策依据。
- 是否把 manual coding 设为权威特征来源，而不是把 extractor 输出写成 authoritative truth。
- shortlist rules 的 elimination/inclusion 条件是否具体、可执行、不会导致 T12 需要做主观判断。
- candidate registry 是否正确分类 6 core / 3 contrast candidates，以及 excluded records 的排除理由是否充分。
- 是否没有偷跑实验结论或性能预测。

## 8. Captain 在 T10 review 后要做

如果 review 为 `PASS`：

1. 在 `docs/04_task_board.md` 勾选 `T10`。
2. 更新本文件的当前状态。
3. 可以推荐进入 T11，但不直接执行。
4. 若 screening matrix 候选池不含 9 条 text-ready records、repeats 未收敛为整数、或 shortlist rules 留有模糊主观判断空间，则阻止进入 T11。

如果 `PASS_WITH_WARNINGS`：

1. 把 warning 分类为 accepted / deferred / rejected。
2. deferred 写入 `docs/08_risks_and_open_questions.md`。
3. 再判断是否允许进入 T11。

如果 `BLOCK`：

1. 只派修 blocking issue 的小任务。
2. 同一任务最多自动复审一次。
3. 第二次仍 `BLOCK`，停止并交给用户裁决。

## 9. 当前未验证事项

- T10 screening evaluation matrix 已执行，待 review。
- Screening matrix 已定义：9 条候选、smoke split、单模型、repeats=1、parse/collapse gates、structural coverage test。
- Shortlist rules 已定义：elimination E1-E4（parse failure、all-true、all-false、non-reproducible）、inclusion I1-I2（structural uniqueness、no near-duplicate）、anchor-based assembly。
- T11 screening execution 尚未开始。
- external text-ready coverage 仍为 `0`；GitHub MIT source 仍未镜像。
- contributor-network 占位项仍只有 host-level provenance。
- screening / recomputed benchmark / post-release analysis 仍未实际运行。
- `.claude/settings.json` 仍是与研究提交无关的本地工具权限噪音，应避免混入正式提交。
