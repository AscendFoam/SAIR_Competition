# T12c Write Screening Summary And Shortlist Report

## Task ID

`T12c_write_screening_summary_and_shortlist_report`

## Goal

Write the Stage A screening summary and mechanically form the `3-5` prompt shortlist for Stage B using the reviewed T11, T12, and T12b evidence, with ZhipuAI `glm-4.7-flash` as the reviewed non-collapsing route that determines shortlist eligibility.

## Why Now

T12b passed review and resolves the cross-provider evidence gap. The earlier zero-survivor outcome is now understood as DeepSeek-specific rather than protocol-wide. Milestone 3 can therefore return to its intended exit path: summarize screening, apply the frozen shortlist rules, and recommend `3-5` prompts for the recomputed benchmark.

## Allowed Files

Worker may only modify or create files in:

```text
reports/research/screening/summary.md
reports/research/screening/shortlist.md
reports/research/screening/README.md
docs/07_handoff.md
```

Worker may read, but must not edit, the reviewed inputs and prior manifests:

```text
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
reports/research/screening/screening_execution_manifest_v1.md
reports/research/screening/screening_second_model_manifest_v1.md
reports/research/screening/screening_model_comparison_note_v1.md
reports/research/screening/screening_provider_route_availability_v1.md
reports/research/screening/screening_third_route_manifest_v1.md
reports/research/screening/screening_cross_provider_note_v1.md
artifacts/research_runs/screening/
artifacts/research_runs/screening_second_model/
artifacts/research_runs/screening_third_route/
data/interim/prompt_corpus/prompt_features_v1.jsonl
data/interim/prompt_corpus/corpus_v1.jsonl
```

## Forbidden Scope

- Do not run any new API evaluations.
- Do not change T10 elimination thresholds or shortlist rules.
- Do not modify any artifact under `artifacts/research_runs/`.
- Do not edit `src/`, `tests/`, `prompts/complete/`, `data/`, or `configs/`.
- Do not redesign the protocol or add a new provider-comparison task.
- Do not update `docs/04_task_board.md`; Captain owns task state.
- Do not promote any claim beyond the reviewed evidence.

## Inputs To Read

```text
README.md
AGENTS.md
docs/02_experiment_plan.md
docs/04_task_board.md
docs/06_eval_protocol.md
docs/07_handoff.md
docs/08_risks_and_open_questions.md
docs/review/T10_build_screening_evaluation_matrix_review.md
docs/review/T11_run_screening_on_selected_prompt_candidates_review.md
docs/review/T12_rerun_screening_with_alternate_low_cost_model_review.md
docs/review/T12b_run_screening_on_non_deepseek_provider_review.md
docs/tasks/phase_3_screening_eval/T10_build_screening_evaluation_matrix.md
docs/tasks/phase_3_screening_eval/T11_run_screening_on_selected_prompt_candidates.md
docs/tasks/phase_3_screening_eval/T12_rerun_screening_with_alternate_low_cost_model.md
docs/tasks/phase_3_screening_eval/T12b_run_screening_on_non_deepseek_provider.md
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
reports/research/screening/screening_execution_manifest_v1.md
reports/research/screening/screening_second_model_manifest_v1.md
reports/research/screening/screening_model_comparison_note_v1.md
reports/research/screening/screening_provider_route_availability_v1.md
reports/research/screening/screening_third_route_manifest_v1.md
reports/research/screening/screening_cross_provider_note_v1.md
data/interim/prompt_corpus/prompt_features_v1.jsonl
data/interim/prompt_corpus/corpus_v1.jsonl
```

## Required Decisions

T12c may make only reporting-level decisions:

1. How to explain the three reviewed screening runs compactly and accurately.
2. How to apply the frozen shortlist rules mechanically to the ZhipuAI survivor pool.
3. Which `3-5` prompts are recommended for Stage B after applying the existing shortlist rules and structural coverage test.
4. Which coverage gaps or warnings must be noted in the shortlist report.

T12c must not make new design decisions about:

- changing E1-E4
- changing the shortlist rules
- adding repeat runs
- running Stage B
- changing the prompt pool

## Expected Output

### 1. Screening summary

Write:

```text
reports/research/screening/summary.md
```

This report must:

- summarize T11, T12, and T12b at a high level
- state clearly that DeepSeek collapse is provider-specific
- identify the reviewed survivor pool on ZhipuAI
- note any remaining caution about latency, metric naming drift, or provider dependence

### 2. Shortlist report

Write:

```text
reports/research/screening/shortlist.md
```

This report must:

- apply `screening_shortlist_rules_v1.md` mechanically
- list eliminated candidates and why
- list eligible candidates
- recommend a final shortlist of `3-5` prompts for Stage B
- explain how each shortlisted prompt contributes structural coverage
- state any warnings or coverage gaps required by the rules

### 3. README update

Update:

```text
reports/research/screening/README.md
```

to reflect that Stage A has completed and shortlist formation is now based on the reviewed cross-provider evidence.

### 4. Handoff update

Update `docs/07_handoff.md` with:

- T12c execution status
- shortlist size and prompt IDs
- the reason those prompts advance
- the fact that Stage B is the next decision point but has not started

## Selection Rule To Apply

For T12c, shortlist eligibility must be based on the reviewed ZhipuAI Stage A run because it is the only reviewed non-collapsing provider route. T11 and T12 must be cited as provider-specific failure-analysis evidence, not as the shortlist decision basis.

## Verification

Verify that:

- every shortlist claim is traceable to the reviewed manifests and notes
- the shortlisted prompts all pass E1-E4 on the reviewed ZhipuAI run
- the final shortlist contains `3-5` prompts
- the shortlist report explicitly references structural coverage, not just raw accuracy
- `docs/07_handoff.md` matches the shortlist report

## Docs To Update

- `reports/research/screening/summary.md`
- `reports/research/screening/shortlist.md`
- `reports/research/screening/README.md`
- `docs/07_handoff.md`

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T12c_write_screening_summary_and_shortlist_report
Changed files:
- ...

Summary decisions:
- eliminated_candidates:
- eligible_candidates:
- shortlisted_candidates:
- coverage_notes:

Verification:
- checked_traceability: pass/fail
- checked_shortlist_size: pass/fail
- checked_handoff_alignment: pass/fail

Risks / follow-up:
- ...
```
