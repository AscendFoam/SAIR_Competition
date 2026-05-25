# Handoff

## Captain Override (2026-05-25, T12b Review)

Current Unique Task:
- `T12c_write_screening_summary_and_shortlist_report`

Captain decision on review:
- `docs/review/T12b_run_screening_on_non_deepseek_provider_review.md` is accepted as `PASS_WITH_WARNINGS`.
- `T12b_run_screening_on_non_deepseek_provider` is complete and does not require another automatic review cycle.

Accepted T12b outcome:
- T12b correctly executed the frozen Stage A screening on a genuinely non-DeepSeek route: `ZhipuAI / glm-4.7-flash` with thinking disabled.
- All 9 third-route run directories completed with required artifacts and matching prompt hashes.
- The reviewed cross-provider evidence now shows that the earlier all-false and parse collapse was DeepSeek-specific.
- Shortlist formation is now allowed.

Warning handling:
- accepted: `N1`, `N3`, `N4`, `N5`, `N6`, `N7`
- deferred: `N8`
- rejected: `N2`

Current reviewed screening state:
- reviewed run family 1: `artifacts/research_runs/screening/` on `deepseek-chat` -> `0/9` survivors
- reviewed run family 2: `artifacts/research_runs/screening_second_model/` on `deepseek-v4-flash` -> `0/9` survivors
- reviewed run family 3: `artifacts/research_runs/screening_third_route/` on `glm-4.7-flash` -> `8/9` survivors
- cross-provider conclusion:
  - all-false collapse is DeepSeek-specific
  - P0 parse collapse is DeepSeek-specific
  - P1.1.1 is the only candidate eliminated on both provider families

Next worker task:
- `docs/tasks/phase_3_screening_eval/T12c_write_screening_summary_and_shortlist_report.md`
- Goal: write the screening summary, mechanically apply shortlist rules to the reviewed survivor pool, and recommend `3-5` prompts for Stage B without running any new API evaluations.

## Captain Override (2026-05-23, T12b Worker Execution)

Current Unique Task:
- `T12b_run_screening_on_non_deepseek_provider`

Worker execution result:
- Task: `T12b_run_screening_on_non_deepseek_provider`
- Status: Worker executed, pending review.
- **Non-DeepSeek provider route found and successfully used: ZhipuAI (glm-4.7-flash, thinking disabled).**
- Provider availability note: `reports/research/screening/screening_provider_route_availability_v1.md`
- T12b executed a full 9-prompt screening rerun on ZhipuAI glm-4.7-flash with thinking disabled.
- **8/9 candidates survive elimination.** Cross-provider evidence gap (R27) is now resolved.
- All-false collapse is confirmed as **DeepSeek-specific, not protocol-wide.**

Execution summary:
- Provider: ZhipuAI, model: glm-4.7-flash (thinking disabled)
- Completed runs: 9/9 (0 API failures)
- Survivors: **8** (only P1.1.1 eliminated by E3; P0 no longer parse-collapsed)
- Artifacts: all 9 directories under `artifacts/research_runs/screening_third_route/` contain all 4 required artifacts
- Third-route manifest: `reports/research/screening/screening_third_route_manifest_v1.md`
- Cross-provider note: `reports/research/screening/screening_cross_provider_note_v1.md`
- Shortlist formation: **now possible** with 8 surviving candidates

Route assessment summary:
- MiniMax (MiniMax-M2.7): credentials present, but model returns empty output at max_tokens=256 (tested in T12 prep; user confirmed "minimax不可用")
- ZhipuAI (glm-4.7-flash): tested and works with thinking disabled (zai-sdk installed in gemini_api conda env)
- Google (gemini-3-flash-preview): no API key configured; not tested due to VPN constraints

Current reviewed screening state (three providers):
- reviewed run family 1: `artifacts/research_runs/screening/` on `deepseek-chat` — 0 survivors
- reviewed run family 2: `artifacts/research_runs/screening_second_model/` on `deepseek-v4-flash` — 0 survivors
- reviewed run family 3: `artifacts/research_runs/screening_third_route/` on `glm-4.7-flash` — **8 survivors**
- confirmed: all-false collapse is DeepSeek-specific; screening protocol works correctly on ZhipuAI

Next step:
- Captain should proceed with shortlist formation using the 8 ZhipuAI survivors, or decide whether to run additional screening rounds on other providers.

## Captain Override (2026-05-23, T12 Review)

Current Unique Task:
- ~~`T12b_run_screening_on_non_deepseek_provider`~~ (worker executed, pending review)

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
- reviewed run family 1: `artifacts/research_runs/screening/` on `deepseek-chat` — 0 survivors
- reviewed run family 2: `artifacts/research_runs/screening_second_model/` on `deepseek-v4-flash` — 0 survivors
- reviewed run family 3: `artifacts/research_runs/screening_third_route/` on `glm-4.7-flash` — **8 survivors** (T12b)
- confirmed: all-false and parse collapse are **DeepSeek-specific**; screening protocol produces 8/9 survivors on ZhipuAI

Next worker task (superseded):
- `docs/tasks/phase_3_screening_eval/T12b_run_screening_on_non_deepseek_provider.md`
- Goal: attempt one genuine non-DeepSeek Stage A rerun under frozen non-model settings, or explicitly document that no such usable route exists locally.
- Outcome: non-DeepSeek route found (ZhipuAI glm-4.7-flash). Full screening rerun executed. 8/9 candidates survive. Shortlist formation is now possible.

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

Captain decisions after T12b:
- ✅ **Option 1 done**: ZhipuAI glm-4.7-flash tested and works (8 survivors).
- ❌ **Option 2 not needed**: E3 passes correctly on ZhipuAI.
- ❓ Option 3 (expand dataset): optional, not required for shortlist.
- ✅ **Option 4 partially**: all-false collapse confirmed as DeepSeek-specific finding.
- ❌ **Option 5 not needed**: screening protocol is not broken; collapse was provider-specific.
- **→ Proceed to shortlist formation** with the 8 ZhipuAI survivors.

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
- **T12b ZhipuAI glm-4.7-flash screening rerun（8 survivors — 确认 all-false collapse 是 DeepSeek 特有）**

## 2. Current Unique Task

`T12b_run_screening_on_non_deepseek_provider`

任务包：

- `docs/tasks/phase_3_screening_eval/T12b_run_screening_on_non_deepseek_provider.md`

状态：

- Worker 已执行，待 review。

T12b worker 执行结果：

- Task: `T12b_run_screening_on_non_deepseek_provider`
- 状态: worker 已执行，待 review。
- **结论: 非 DeepSeek provider 路由已找到并成功执行。**
- Provider route: `zhipuai` (ZhipuAI API), model: `glm-4.7-flash` (thinking disabled)
- Completed runs: 9/9 (0 API failures)
- **幸存者: 8/9**（仅 P1.1.1 被 E3 淘汰；P0 在 glm-4.7-flash 上解析率 100%）
- Cross-provider 证据缺口 (R27) **已解决**：all-false collapse 是 DeepSeek 特有，非 protocol 问题。
- 输出目录: `artifacts/research_runs/screening_third_route/`
- 执行 manifest: `reports/research/screening/screening_third_route_manifest_v1.md`
- Cross-provider note: `reports/research/screening/screening_cross_provider_note_v1.md`

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

### T12b：Non-DeepSeek screening rerun (ZhipuAI glm-4.7-flash)

- `artifacts/research_runs/screening_third_route/` — 9 run directories
- `reports/research/screening/screening_third_route_manifest_v1.md`
- `reports/research/screening/screening_cross_provider_note_v1.md`
- `reports/research/screening/screening_provider_route_availability_v1.md`（updated）
- **SCREENING SUCCESS: 8 survivors** — all-false collapse confirmed as DeepSeek-specific
- Shortlist formation is now possible

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
reports/research/screening/screening_provider_route_availability_v1.md
reports/research/screening/screening_third_route_manifest_v1.md
reports/research/screening/screening_cross_provider_note_v1.md
src/sair_competition/analysis/prompt_features.py
tests/test_prompt_feature_extractor.py
```

## 5. Worker 执行边界

T12b 已执行，待 review。下一位 worker 不应重复执行 T12b。

- T12b 执行结果：**非 DeepSeek provider 路由找到并成功执行。**
  - Provider: ZhipuAI (glm-4.7-flash, thinking disabled)
  - 9/9 runs completed, 0 API failures
  - **8/9 候选通过 elimination gates**
  - Shortlist formation: **现在可行**
- 关键发现：all-false collapse 和 parse collapse 是 DeepSeek 特有现象。在 ZhipuAI 上，screening protocol 正常工作。
- R27 (cross-provider 证据缺口) 已解决。
- Shortlist formation 是合理的下一步，但需 Captain 裁决 shortlist 策略。
- 注意：ZhipuAI API 延迟显著高于 DeepSeek（~53 min vs ~9 min），大量 rerun 需考虑时间成本。

允许修改文件：

- `docs/04_task_board.md`（仅 Captain，勾选 T12b）
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

- T12b 已完成（ZhipuAI glm-4.7-flash，8 survivors），待 review。
- SCREENING FAILURE 在两个 DeepSeek 模型间完全一致（0 survivors），但在 ZhipuAI 上不存在（8 survivors）。
- ✅ Cross-provider 证据缺口 (R27) **已解决**：all-false collapse 是 DeepSeek 特有，非 protocol 问题。
- ✅ Shortlist formation **现在可行**（8 个候选通过 elimination gates）。
- ZhipuAI screening 结果仅基于单次运行（repeats=1），正式 shortlist 前是否需要重复运行以评估稳定性，由 Captain 决定。
- Shortlist formation 策略仍需 Captain 裁决（例如：基于 ZhipuAI 结果形成 shortlist，还是仅视为备选信号）。
- external text-ready coverage 仍为 `0`；GitHub MIT source 仍未镜像。
- contributor-network 占位项仍只有 host-level provenance。
- recomputed benchmark / post-release analysis 仍需 Captain 决策后才能继续。
- `.claude/settings.json` 仍是与研究提交无关的本地工具权限噪音，应避免混入正式提交。
