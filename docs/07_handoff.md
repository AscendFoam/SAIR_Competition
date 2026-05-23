# Handoff

## Captain Override (2026-05-23, T12 Review)

Current Unique Task:
- `T12b_run_screening_on_non_deepseek_provider`

Captain decision on review:
- `docs/review/T12_rerun_screening_with_alternate_low_cost_model_review.md` is accepted as `PASS_WITH_WARNINGS`.
- `T12_rerun_screening_with_alternate_low_cost_model` is complete and does not require another automatic review cycle.

Accepted T12 outcome:
- T12 correctly re-ran the frozen Stage A screening on all 9 text-ready local prompts.
- All 9 second-model run directories completed with required artifacts and matching prompt hashes.
- T11 (`deepseek-chat`) and T12 (`deepseek-v4-flash`, thinking disabled) both produced zero surviving candidates under the same T10 elimination rules.
- Shortlist formation is still not allowed.

Warning handling:
- accepted: `N2`, `N3`, `N4`, `N5`, `N6`
- deferred: `N1`
- rejected: none

Current reviewed screening state:
- reviewed run family 1: `artifacts/research_runs/screening/` on `deepseek-chat`
- reviewed run family 2: `artifacts/research_runs/screening_second_model/` on `deepseek-v4-flash`
- confirmed common pattern:
  - P0 fails E1 through parse collapse on both models
  - the other 8 prompts fail E3 through all-false collapse on both models
  - survivor count remains `0/9`

Next worker task:
- `docs/tasks/phase_3_screening_eval/T12b_run_screening_on_non_deepseek_provider.md`
- Goal: attempt one genuine non-DeepSeek Stage A rerun under frozen non-model settings, or explicitly document that no such usable route exists locally.

## Captain Override (2026-05-23, T12 Worker Execution)

Current Unique Task:
- `T12_rerun_screening_with_alternate_low_cost_model`

Worker execution result:
- Task: `T12_rerun_screening_with_alternate_low_cost_model`
- Status: Worker executed, pending review.
- Provider route: `deepseek` (DeepSeek API), model: `deepseek-v4-flash` (thinking disabled)
- Completed runs: 9/9 (no API failures)
- Artifacts: all 9 directories under `artifacts/research_runs/screening_second_model/` contain run_config.json, summary.json, predictions.jsonl, prompt_hash_manifest.json
- SHA256: all 9 prompt hashes match corpus_v1.jsonl
- Second-model manifest: `reports/research/screening/screening_second_model_manifest_v1.md`
- Model comparison note: `reports/research/screening/screening_model_comparison_note_v1.md`
- Run artifacts: `artifacts/research_runs/screening_second_model/<prompt_id>/`

SCREENING FAILURE (confirmed across two models):
- T11 (deepseek-chat): 0 survivors
- T12 (deepseek-v4-flash): 0 survivors
- P0: parse collapse on both models (parse_success_rate 0.27 vs 0.23)
- 8 strict-format prompts: all-false collapse on both models (true_recall 0.00-0.03, false_recall 0.97-1.00)
- Results are numerically near-identical between the two models
- Surviving candidates: 0 on both models
- Shortlist formation: NOT possible under current T10 elimination rules

Alternate models tested but failed during T12 preparation:
- MiniMax-M2.7: empty output on all 64 problems per prompt (parse_success_rate 0.00-0.016)
- deepseek-reasoner: all max_tokens consumed by reasoning_tokens, content empty
- deepseek-v4-flash (thinking enabled): same as deepseek-reasoner

Captain must decide before any shortlist-facing work:
1. Test a non-DeepSeek provider (e.g., GPT-4o-mini, Gemini Flash)
2. Relax E3 all-false collapse threshold (with documented rationale)
3. Expand screening dataset (add hard_slice_sample)
4. Accept all-false collapse as finding and redesign shortlist strategy
5. Redesign screening protocol entirely

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

## Captain Override (2026-05-18)

Current Unique Task:
- `T11_run_screening_on_selected_prompt_candidates`

Captain decision on review:
- `docs/review/T10_build_screening_evaluation_matrix_review.md` verdict `PASS` is accepted.
- `T10_build_screening_evaluation_matrix` is complete and does not require another automatic review cycle.

Ready-for-worker package:
- `docs/tasks/phase_3_screening_eval/T11_run_screening_on_selected_prompt_candidates.md`

T11 worker execution result:
- Task: `T11_run_screening_on_selected_prompt_candidates`
- Status: Worker executed, review accepted.
- Provider route: `deepseek` (DeepSeek API), model: `deepseek-chat`
- Completed runs: 9/9 (no API failures)
- Artifacts: `artifacts/research_runs/screening/<prompt_id>/`
- Execution manifest: `reports/research/screening/screening_execution_manifest_v1.md`

SCREENING FAILURE:
- P0: eliminated by E1 (parse_success_rate = 0.27)
- 8 strict-format prompts: all eliminated by E3 (all-false collapse; false_recall 0.97-1.00, true_recall 0.00-0.03)
- Surviving candidates: 0

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

截至当前，T01-T11 均已通过 review 并被 Captain 接受。T12 已执行，待 review。当前已完成：

- public prompt corpus v1 与 public/private boundary
- 9 条 text-ready local prompts 的 manual taxonomy v1
- 7 个高价值字段的 extractor skeleton 与 focused tests
- taxonomy self-audit、conflict resolution 与 1 处最小数据校正
- T10 screening evaluation matrix 设计
- T11 deepseek-chat screening execution（0 survivors）
- T12 deepseek-v4-flash screening rerun（0 survivors，与 T11 结果一致）

## 2. Current Unique Task

`T12_rerun_screening_with_alternate_low_cost_model`

任务包：

- `docs/tasks/phase_3_screening_eval/T12_rerun_screening_with_alternate_low_cost_model.md`

状态：

- Worker 已执行，待 review。

T12 worker 执行结果：

- Task: `T12_rerun_screening_with_alternate_low_cost_model`
- 状态: worker 已执行，待 review。
- Provider route: `deepseek` (DeepSeek API), model: `deepseek-v4-flash` (thinking disabled)
- Completed runs: 9/9 (no API failures)
- Artifacts: all 9 directories under `artifacts/research_runs/screening_second_model/` contain all 4 required artifacts
- SHA256: all 9 prompt hashes match corpus_v1.jsonl
- Second-model manifest: `reports/research/screening/screening_second_model_manifest_v1.md`
- Model comparison note: `reports/research/screening/screening_model_comparison_note_v1.md`
- Changed files: `artifacts/research_runs/screening_second_model/` (9 run dirs + script + results), `reports/research/screening/screening_second_model_manifest_v1.md` (new), `reports/research/screening/screening_model_comparison_note_v1.md` (new), `reports/research/screening/README.md` (updated), `docs/07_handoff.md` (updated)

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

### T10：Screening evaluation matrix

- `reports/research/screening/screening_matrix_v1.md`
- `reports/research/screening/screening_candidate_registry_v1.md`
- `reports/research/screening/screening_shortlist_rules_v1.md`
- 9 条候选、smoke split、单模型、repeats=1、parse/collapse gates

### T11：Screening execution (deepseek-chat)

- `artifacts/research_runs/screening/` — 9 run directories
- `reports/research/screening/screening_execution_manifest_v1.md`
- SCREENING FAILURE: 0 survivors (P0 parse collapse, 8 strict prompts all-false collapse)

### T12：Screening rerun (deepseek-v4-flash)

- `artifacts/research_runs/screening_second_model/` — 9 run directories
- `reports/research/screening/screening_second_model_manifest_v1.md`
- `reports/research/screening/screening_model_comparison_note_v1.md`
- SCREENING FAILURE confirmed: 0 survivors, numerically near-identical to T11

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
docs/review/T11_run_screening_on_selected_prompt_candidates_review.md
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
reports/research/screening/screening_execution_manifest_v1.md
reports/research/screening/screening_second_model_manifest_v1.md
reports/research/screening/screening_model_comparison_note_v1.md
src/sair_competition/analysis/prompt_features.py
tests/test_prompt_feature_extractor.py
```

## 5. Worker 执行边界

T12 已执行，待 review。下一位 worker 不应重复执行 T12。

- T12 执行结果：所有 9 个候选再次被 elimination gates 淘汰（P0 parse collapse，其余 all-false collapse），与 T11 结果一致。
- Shortlist formation 在 Captain 裁决前不应进行。
- Captain 可能的决策方向：
  1. 换一个非 DeepSeek 的 screening provider（如 GPT-4o-mini 或 Gemini Flash）
  2. 放宽 E3 all-false collapse 的阈值（但需要 documented rationale）
  3. 扩大 screening 数据集（加入 hard_slice_sample）
  4. 接受 all-false collapse 为发现并重新设计 shortlist 策略
  5. 重新设计 screening protocol

允许修改文件：

- `docs/04_task_board.md`（仅 Captain，勾选 T12）
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

## 7. 当前未验证事项

- T12 screening rerun 已完成，待 review。
- SCREENING FAILURE 在两个 DeepSeek 模型间完全一致：deepseek-chat 和 deepseek-v4-flash 均产生 0 个幸存者。
- Shortlist 为空（0 个候选通过 elimination gates，两个模型结果一致）。
- Shortlist formation 在 Captain 裁决前不应进行。
- 非 DeepSeek provider 尚未测试；all-false collapse 可能是 provider 级别的行为模式。
- external text-ready coverage 仍为 `0`；GitHub MIT source 仍未镜像。
- contributor-network 占位项仍只有 host-level provenance。
- screening / recomputed benchmark / post-release analysis 仍需 Captain 决策后才能继续。
- `.claude/settings.json` 仍是与研究提交无关的本地工具权限噪音，应避免混入正式提交。
