# T11 Run Screening on Selected Prompt Candidates

## Task ID

`T11_run_screening_on_selected_prompt_candidates`

## Goal

Execute the Stage A screening runs defined by T10 for the 9 text-ready local prompts, using the frozen screening matrix and producing reproducible run artifacts for T12.

## Why Now

T10 has passed review and is now Captain-accepted. The candidate pool, field-usage rules, required artifacts, and shortlist rules are frozen enough to support execution. T12 depends on the artifacts from this task, so T11 is now the single critical-path task.

## Allowed Files

Worker may only modify or create files in:

```text
artifacts/research_runs/screening/
reports/research/screening/README.md
reports/research/screening/screening_execution_manifest_v1.md
docs/07_handoff.md
```

Worker may read, but must not edit, the frozen design inputs:

```text
configs/research/evaluation_matrix.example.json
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
```

## Forbidden Scope

- Do not edit `configs/research/evaluation_matrix.example.json` or any T10 design file.
- Do not edit `src/`, `tests/`, `prompts/complete/`, or any prompt text.
- Do not run released-subset analysis or any Stage B / Stage C evaluation.
- Do not write the T12 screening summary early.
- Do not change the candidate pool away from the 9 text-ready local prompts.
- Do not change screening `prompt_set`, `dataset_set`, `repeats`, `temperature`, `max_tokens`, or `reasoning_mode`.
- Do not update `docs/04_task_board.md`; Captain owns task completion state.

## Inputs to Read

```text
README.md
AGENTS.md
docs/02_experiment_plan.md
docs/04_task_board.md
docs/06_eval_protocol.md
docs/07_handoff.md
docs/08_risks_and_open_questions.md
docs/review/T10_build_screening_evaluation_matrix_review.md
docs/tasks/phase_3_screening_eval/T10_build_screening_evaluation_matrix.md
configs/research/evaluation_matrix.example.json
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/corpus_audit/public_private_boundary.md
reports/research/screening/README.md
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
```

## Expected Output

### 1. Screening run artifacts

Produce one run directory per prompt under:

```text
artifacts/research_runs/screening/
```

Each run must contain the T10-required artifacts:

- `run_config.json`
- `summary.json`
- `predictions.jsonl`
- `prompt_hash_manifest.json`

### 2. Screening execution manifest

Write:

```text
reports/research/screening/screening_execution_manifest_v1.md
```

This file should record, for each of the 9 prompts:

- prompt id
- run directory
- dataset used
- actual provider route used
- whether the run completed
- whether the required artifacts are present
- top-line metrics copied from `summary.json`

This is an execution manifest only, not the T12 interpretation report.

### 3. Handoff update

Update `docs/07_handoff.md` with:

- T11 execution status
- artifact locations
- actual provider route used
- any failed or partial runs
- any execution facts that T12 must know

## Required Decisions

T11 must make only execution-level decisions:

1. What concrete `provider_route` is used for the frozen screening config.
2. How run directories are named under `artifacts/research_runs/screening/`.
3. Whether an identical-config retry is needed for a failed run.

T11 must not make new design decisions about:

- which prompts are in the pool
- which fields are descriptive-only
- shortlist logic
- protocol wording

## Verification

Run:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

Also verify that all 9 run directories contain the 4 required artifacts and that the manifest matches what is on disk.

## Docs to Update

- `reports/research/screening/README.md`
- `reports/research/screening/screening_execution_manifest_v1.md`
- `docs/07_handoff.md`

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T11_run_screening_on_selected_prompt_candidates
Changed files:
- ...

Execution summary:
- provider_route:
- prompt count executed:
- completed runs:
- failed or retried runs:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
