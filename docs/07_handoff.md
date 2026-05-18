# Handoff

## Captain Override (2026-05-18, T11 Review)

Current Unique Task:
- `T12_rerun_screening_with_alternate_low_cost_model`

Captain decision on review:
- `docs/review/T11_run_screening_on_selected_prompt_candidates_review.md` is accepted as `PASS_WITH_WARNINGS`.
- `T11_run_screening_on_selected_prompt_candidates` is complete and does not require another automatic review cycle.

Accepted T11 outcome:
- T11 correctly executed the frozen Stage A screening on all 9 text-ready local prompts.
- All 9 run directories completed with required artifacts and matching prompt hashes.
- The zero-survivor result on `deepseek / deepseek-chat` is accepted as a real experimental outcome.
- No shortlist should be written from DeepSeek-only evidence.

Warning handling:
- accepted: `N2`, `N4`, `N5`
- deferred: `N1`, `N3`
- rejected: none

Ready-for-worker package:
- `docs/tasks/phase_3_screening_eval/T12_rerun_screening_with_alternate_low_cost_model.md`

Worker scope for T12:
- Re-run the frozen Stage A screening with one alternate low-cost model/provider route that is not `deepseek / deepseek-chat`.
- Keep prompt set, dataset set, repeats, temperature, max tokens, reasoning mode, and elimination rules frozen.
- Produce a second-model screening manifest and a short comparison note sufficient for Captain to decide whether shortlist formation can resume.
- Update this handoff only with execution facts, artifact paths, provider/model used, survivor counts, and any rerun failure/escalation facts.

Captain interpretation to preserve:
- T11 is complete.
- T11 does not prove the screening protocol is wrong.
- T11 does show that the chosen DeepSeek screening model is insufficient for shortlist formation on this task unless another model reproduces the same collapse.

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

T11 worker execution result:
- Task: `T11_run_screening_on_selected_prompt_candidates`
- Status: Worker executed, pending review.
- Provider route: `deepseek` (DeepSeek API), model: `deepseek-chat`
- Completed runs: 9/9 (no API failures)
- Artifacts: all 9 directories contain run_config.json, summary.json, predictions.jsonl, prompt_hash_manifest.json
- SHA256: all 9 prompt hashes match corpus_v1.jsonl
- Execution manifest: `reports/research/screening/screening_execution_manifest_v1.md`
- Run artifacts: `artifacts/research_runs/screening/<prompt_id>/`

SCREENING FAILURE:
- P0: eliminated by E1 (parse_success_rate = 0.27)
- 8 strict-format prompts: all eliminated by E3 (all-false collapse; false_recall 0.97-1.00, true_recall 0.00-0.03)
- Surviving candidates: 0
- Per shortlist rules: "If fewer than 3 candidates survive, flag a screening failure and escalate to Captain."
- Root finding: deepseek-chat produces systematic all-false bias on the equational-theories task regardless of prompt structure. This is a model-level behavior, not a prompt-level distinction.
- Captain must decide: change screening model, relax E3 thresholds, or redesign screening protocol before T12 can proceed.

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

T11 已执行，待 review。下一位 worker 不应重复执行 T11。

- 如 review 为 PASS，但 screening failure 需要 Captain 先处理再决定 T12 方向。
- T11 执行结果：所有 9 个候选被 elimination gates 淘汰（P0 parse collapse，其余 all-false collapse）。
- T12 在 Captain 裁决前不应写 shortlist 结论。
- Captain 可能的决策方向：
  1. 换一个不同的 screening model（如 GPT-4o-mini 或其他模型）
  2. 放宽 E3 all-false collapse 的阈值（但需要 documented rationale）
  3. 扩大 screening 数据集（加入 hard_slice_sample）
  4. 重新设计 screening protocol

允许修改文件：

- `docs/04_task_board.md`（仅 Captain，勾选 T11）
- 其他文件由后续任务包定义

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

- T11 screening execution 已完成，待 review。
- SCREENING FAILURE: deepseek-chat 对 equational-theories 任务产生系统性全假偏差。8 个 strict-format prompt 的 true_recall 为 0.000-0.032，false_recall 为 0.970-1.000。P0 (relaxed format) 的 parse_success_rate 仅 0.266。
- Shortlist 为空（0 个候选通过 elimination gates）。
- T12 在 Captain 裁决前不应写 shortlist 结论。
- external text-ready coverage 仍为 `0`；GitHub MIT source 仍未镜像。
- contributor-network 占位项仍只有 host-level provenance。
- screening / recomputed benchmark / post-release analysis 仍需 Captain 决策后才能继续。
- `.claude/settings.json` 仍是与研究提交无关的本地工具权限噪音，应避免混入正式提交。
