# T12b Run Screening On Non-DeepSeek Provider

## Task ID

`T12b_run_screening_on_non_deepseek_provider`

## Goal

Attempt one genuinely non-DeepSeek rerun of the frozen Stage A screening on the same 9 text-ready local prompts, so Captain can distinguish "DeepSeek-specific collapse" from "protocol-wide collapse."

## Why Now

T11 and T12 are both review-backed and both produced zero survivors, but both completed reviewed runs still used the DeepSeek provider. That means the shortlist problem is confirmed across two DeepSeek models, yet cross-provider generality is still unresolved. The next task is not to relax thresholds or redesign Stage A. The next task is to obtain one true non-DeepSeek contrast if the local environment allows it.

## Allowed Files

Worker may only modify or create files in:

```text
artifacts/research_runs/screening_third_route/
reports/research/screening/README.md
reports/research/screening/screening_third_route_manifest_v1.md
reports/research/screening/screening_cross_provider_note_v1.md
reports/research/screening/screening_provider_route_availability_v1.md
docs/07_handoff.md
```

Worker may read, but must not edit, the frozen design and prior reviewed run inputs:

```text
configs/research/evaluation_matrix.example.json
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
reports/research/screening/screening_execution_manifest_v1.md
reports/research/screening/screening_second_model_manifest_v1.md
reports/research/screening/screening_model_comparison_note_v1.md
artifacts/research_runs/screening/
artifacts/research_runs/screening_second_model/
```

## Forbidden Scope

- Do not edit any T10 design file or `configs/research/evaluation_matrix.example.json`.
- Do not edit `src/`, `tests/`, `prompts/complete/`, `data/`, or any prompt text.
- Do not alter T11 or T12 artifacts.
- Do not change screening `prompt_set`, `dataset_set`, `repeats`, `temperature`, `max_tokens`, `reasoning_mode`, or elimination thresholds.
- Do not write a shortlist-facing summary.
- Do not relax E1-E4 or invent a new shortlist rule.
- Do not fall back to another DeepSeek route and present it as a non-DeepSeek contrast.
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
docs/review/T11_run_screening_on_selected_prompt_candidates_review.md
docs/review/T12_rerun_screening_with_alternate_low_cost_model_review.md
docs/tasks/phase_3_screening_eval/T10_build_screening_evaluation_matrix.md
docs/tasks/phase_3_screening_eval/T11_run_screening_on_selected_prompt_candidates.md
docs/tasks/phase_3_screening_eval/T12_rerun_screening_with_alternate_low_cost_model.md
configs/research/evaluation_matrix.example.json
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/corpus_audit/public_private_boundary.md
reports/research/screening/README.md
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
reports/research/screening/screening_execution_manifest_v1.md
reports/research/screening/screening_second_model_manifest_v1.md
reports/research/screening/screening_model_comparison_note_v1.md
artifacts/research_runs/screening/
artifacts/research_runs/screening_second_model/
```

## Required Decisions

T12b may make only execution-level decisions:

1. Which locally available route qualifies as genuinely non-DeepSeek.
2. Whether that route is usable at the frozen `max_tokens=256` budget.
3. How the run directories are named under `artifacts/research_runs/screening_third_route/`.
4. Whether an identical-config retry is needed for an API failure.

T12b must not make design decisions about:

- whether a same-provider route is "good enough"
- whether to relax E3
- whether to add a harder slice
- whether to redesign Stage A
- whether to form a shortlist despite zero survivors

## Expected Output

### 1. Provider availability note

Write:

```text
reports/research/screening/screening_provider_route_availability_v1.md
```

This note must record:

- which non-DeepSeek routes were actually available locally
- which were attempted
- which failed before producing usable content
- whether a valid non-DeepSeek reviewed rerun was achieved

### 2. If a usable non-DeepSeek route exists: screening artifacts

Produce one run directory per prompt under:

```text
artifacts/research_runs/screening_third_route/
```

Each run must contain:

- `run_config.json`
- `summary.json`
- `predictions.jsonl`
- `prompt_hash_manifest.json`

### 3. If a usable non-DeepSeek route exists: execution manifest

Write:

```text
reports/research/screening/screening_third_route_manifest_v1.md
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

### 4. If a usable non-DeepSeek route exists: cross-provider note

Write:

```text
reports/research/screening/screening_cross_provider_note_v1.md
```

This note must stay execution-facing and concise. It should report:

- DeepSeek survivor count vs non-DeepSeek survivor count
- whether all-false collapse persists
- whether parse collapse persists for P0
- whether Captain now has enough evidence to decide between protocol redesign and shortlist recovery

This is not the paper-facing screening summary.

### 5. Handoff update

Update `docs/07_handoff.md` with:

- T12b execution status
- whether a genuine non-DeepSeek route was available
- provider/model used if a rerun happened
- artifact locations
- survivor count
- whether shortlist formation is now possible
- any failed route attempts that matter for Captain judgment

## Stop Rule

If no genuinely non-DeepSeek route is locally usable, stop after writing:

- `reports/research/screening/screening_provider_route_availability_v1.md`
- `docs/07_handoff.md`

Do not invent a fake rerun, and do not substitute another DeepSeek route.

## Verification

Run:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

If a non-DeepSeek rerun is achieved, also verify:

- all 9 rerun directories contain the 4 required artifacts
- each `predictions.jsonl` contains 64 rows
- prompt hashes match `corpus_v1.jsonl`
- frozen non-model fields match the T10 matrix
- the manifest and cross-provider note match what is on disk

If no rerun is achieved, verify:

- the provider availability note accurately explains why no reviewed non-DeepSeek rerun exists
- `docs/07_handoff.md` matches that note

## Docs To Update

- `reports/research/screening/README.md`
- `reports/research/screening/screening_provider_route_availability_v1.md`
- `reports/research/screening/screening_third_route_manifest_v1.md` if a rerun happens
- `reports/research/screening/screening_cross_provider_note_v1.md` if a rerun happens
- `docs/07_handoff.md`

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T12b_run_screening_on_non_deepseek_provider
Changed files:
- ...

Execution summary:
- attempted_non_deepseek_routes:
- successful_provider_route:
- successful_model:
- prompt count executed:
- completed runs:
- surviving candidates:
- no_route_available:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
