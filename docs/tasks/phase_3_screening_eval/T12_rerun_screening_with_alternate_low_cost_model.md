# T12 Rerun Screening With Alternate Low-Cost Model

## Task ID

`T12_rerun_screening_with_alternate_low_cost_model`

## Goal

Re-run the frozen Stage A screening on the same 9 text-ready local prompts with one alternate low-cost provider/model so Captain can determine whether T11's zero-survivor result is a DeepSeek-specific collapse or a protocol-wide failure.

## Why Now

T11 passed review and is Captain-accepted, but it produced a valid screening failure on `deepseek / deepseek-chat`: 0 candidates survived the frozen elimination gates. We must resolve whether that outcome is model-specific before writing any shortlist-facing summary or moving toward recomputed benchmark selection. The cleanest next step is to keep the Stage A protocol frozen and vary only provider/model.

## Allowed Files

Worker may only modify or create files in:

```text
artifacts/research_runs/screening_second_model/
reports/research/screening/README.md
reports/research/screening/screening_second_model_manifest_v1.md
reports/research/screening/screening_model_comparison_note_v1.md
docs/07_handoff.md
```

Worker may read, but must not edit, the frozen design and prior-run inputs:

```text
configs/research/evaluation_matrix.example.json
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
reports/research/screening/screening_execution_manifest_v1.md
artifacts/research_runs/screening/
```

## Forbidden Scope

- Do not edit any T10 design file or `configs/research/evaluation_matrix.example.json`.
- Do not edit `src/`, `tests/`, `prompts/complete/`, `data/`, or any prompt text.
- Do not alter T11 artifacts in `artifacts/research_runs/screening/`.
- Do not change screening `prompt_set`, `dataset_set`, `repeats`, `temperature`, `max_tokens`, `reasoning_mode`, or elimination thresholds.
- Do not use released final evaluation subsets.
- Do not write the old shortlist-facing T12 summary or claim that a shortlist exists unless the rerun actually produces enough surviving candidates.
- Do not update `docs/04_task_board.md`; Captain owns task-completion state.

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
docs/tasks/phase_3_screening_eval/T10_build_screening_evaluation_matrix.md
docs/tasks/phase_3_screening_eval/T11_run_screening_on_selected_prompt_candidates.md
configs/research/evaluation_matrix.example.json
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/corpus_audit/public_private_boundary.md
reports/research/screening/README.md
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
reports/research/screening/screening_execution_manifest_v1.md
artifacts/research_runs/screening/
```

## Required Decisions

T12 may make only execution-level decisions:

1. Which one alternate provider/model route is available locally and is not `deepseek / deepseek-chat`.
2. How the rerun directories are named under `artifacts/research_runs/screening_second_model/`.
3. Whether an identical-config retry is needed for a failed run.

T12 must not make new design decisions about:

- which prompts are screened
- which thresholds define collapse
- whether the shortlist rules should be relaxed
- whether T11 "counts"
- whether Stage A is rewritten

## Expected Output

### 1. Alternate-model screening artifacts

Produce one run directory per prompt under:

```text
artifacts/research_runs/screening_second_model/
```

Each run must contain:

- `run_config.json`
- `summary.json`
- `predictions.jsonl`
- `prompt_hash_manifest.json`

### 2. Second-model execution manifest

Write:

```text
reports/research/screening/screening_second_model_manifest_v1.md
```

For each of the 9 prompts, record:

- prompt id
- run directory
- dataset used
- actual provider route used
- actual model used
- whether the run completed
- whether required artifacts are present
- top-line metrics copied or mapped from `summary.json`
- which elimination rules, if any, were triggered

### 3. Short comparison note for Captain

Write:

```text
reports/research/screening/screening_model_comparison_note_v1.md
```

This note must stay execution-facing and concise. It should report:

- DeepSeek T11 survivor count vs alternate-model survivor count
- whether all-false collapse persists
- whether parse collapse persists for P0
- whether Captain now has enough surviving candidates to reopen shortlist formation

This is not the paper-facing screening summary.

### 4. Handoff update

Update `docs/07_handoff.md` with:

- T12 execution status
- provider/model used
- artifact locations
- survivor count
- whether shortlist formation is now possible
- any failed or partial reruns

## Escalation Rule

If no alternate provider/model route is actually available in the local environment, stop and report that fact clearly in `docs/07_handoff.md`. Do not fall back to `deepseek / deepseek-chat`, and do not invent a fake rerun.

## Verification

Run:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

Also verify:

- all 9 rerun directories contain the 4 required artifacts
- each `predictions.jsonl` contains 64 rows
- prompt hashes match `corpus_v1.jsonl`
- frozen non-model fields match the T10 matrix
- the manifest and comparison note match what is on disk

## Docs To Update

- `reports/research/screening/README.md`
- `reports/research/screening/screening_second_model_manifest_v1.md`
- `reports/research/screening/screening_model_comparison_note_v1.md`
- `docs/07_handoff.md`

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T12_rerun_screening_with_alternate_low_cost_model
Changed files:
- ...

Execution summary:
- provider_route:
- model:
- prompt count executed:
- completed runs:
- surviving candidates:
- failed or retried runs:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
