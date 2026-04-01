# SAIR Competition Workspace

This repository is the engineering workspace for the SAIR equational-theories competition project.

## Current scope

- Convert the competition plan into a runnable repository skeleton
- Manage prompt experiments as versioned artifacts
- Keep data, prompts, configs, reports, and code separated
- Prepare a minimal CLI for prompt composition and local evaluation utilities

## Quick start

1. Create a virtual environment.
2. Install the package in editable mode:

```powershell
python -m pip install -e .[dev]
```

3. Validate the repository layout:

```powershell
sair validate-layout
```

If you want to use the tools before installing the package, you can also run:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

4. Render a complete prompt from a template and cheatsheet:

```powershell
sair build-complete-prompt `
  prompts/templates/baseline_minimal.j2 `
  prompts/cheatsheets/example_cheatsheet.txt `
  prompts/complete/example_complete_prompt.txt
```

## Public data workflow

After placing official public files into `data/raw/`, run:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli prepare-public-data --raw-dir data/raw --interim-dir data/interim
python -m sair_competition.cli make-splits --dataset-path data/interim/public_all.jsonl --output-dir data/interim/splits
python -m sair_competition.cli run-baseline-eval --dataset-path data/interim/splits/holdout.jsonl --output-dir artifacts/candidates/baseline_holdout
```

If you want to start the offline family-labeling line before the next prompt iteration:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli tag-problem-families `
  --dataset-path data/interim/splits/smoke.jsonl `
  --output-path data/interim/splits/smoke_tagged.jsonl `
  --summary-dir reports/experiments/smoke_family_tags
```

This writes a tagged copy of the split with `family_tags` / `family_signals`, which can then be passed to both baseline and complete-prompt evaluators.

The current tagger is especially tuned to carve out finer slices inside three high-value families:

- singleton collapse
- disjoint sides
- constant-operation candidate

That makes it easier to inspect whether a prompt is failing because it misses a specific true-heavy structural subfamily, rather than because it is weak everywhere.

If you already have an older predictions file from before the tagger existed, you can backfill the tags without rerunning the model:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli attach-family-tags-to-predictions `
  --predictions-path artifacts/candidates/P1_2_3_implicit_guardrail_v2/predictions.jsonl `
  --tagged-dataset-path data/interim/splits/smoke_tagged.jsonl `
  --output-path artifacts/candidates/P1_2_3_implicit_guardrail_v2_tagged_slice/predictions.jsonl
```

Then turn the tagged families plus the tagged error slices into an offline rule-asset bundle:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli build-offline-rule-assets `
  --tagged-dataset-path data/interim/splits/smoke_tagged.jsonl `
  --error-summary-path artifacts/candidates/P1_2_3_implicit_guardrail_v2_tagged_slice_analysis/summary.json `
  --output-path configs/prompts/rule_registry.offline_assets_v2.jsonl `
  --report-path reports/experiments/offline_rule_assets_smoke/summary.md
```

This bundle is meant to support offline labeling, analysis, and future programmatic use. It is not a signal to rewrite the `P1_2_3` prompt wording directly.

You can then attach those offline assets back onto tagged rows or tagged predictions:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli attach-offline-rule-assets `
  --input-path artifacts/candidates/P1_2_3_implicit_guardrail_v2_tagged_slice/predictions.jsonl `
  --rule-assets-path configs/prompts/rule_registry.offline_assets_v2.jsonl `
  --output-path artifacts/candidates/P1_2_3_implicit_guardrail_v2_asset_slice/predictions.jsonl
```

And audit which offline assets still map to missed-true slices on the current mainline:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli audit-offline-rule-assets `
  --predictions-path artifacts/candidates/P1_2_3_implicit_guardrail_v2_asset_slice/predictions.jsonl `
  --rule-assets-path configs/prompts/rule_registry.offline_assets_v2.jsonl `
  --output-dir reports/experiments/offline_rule_asset_audit_smoke
```

This gives you a prioritized asset-level backlog, so the next step can target tagging, slicing, or future implicit prompt injection without blindly rewriting wording.

If several top assets keep matching the same rows, deduplicate them into canonical axes first:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli consolidate-offline-rule-axes `
  --predictions-path artifacts/candidates/P1_2_3_implicit_guardrail_v2_asset_slice/predictions.jsonl `
  --audit-summary-path reports/experiments/offline_rule_asset_audit_smoke/summary.json `
  --output-dir reports/experiments/offline_rule_axis_smoke
```

This collapses exact-overlap assets into one main axis and records child-axis subset relations, so the same missed-true slice is not counted three times under different family names.

Then build a deduplicated review set that assigns each actionable row to its most specific canonical axis:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli build-offline-rule-review-set `
  --predictions-path artifacts/candidates/P1_2_3_implicit_guardrail_v2_asset_slice/predictions.jsonl `
  --consolidation-summary-path reports/experiments/offline_rule_axis_smoke/summary.json `
  --output-dir reports/experiments/offline_rule_review_set_smoke
```

The resulting review set is meant to support two next steps:

- expand the family tagger with narrower child buckets
- prepare future implicit or programmatic positive signals without copying wording back into the prompt

Alongside `review_set.jsonl`, the tool also writes:

- `annotation_checklist.md` for a flat manual checklist
- `p0_p1_review_template.md` for higher-priority structured review and conclusion backfill

If you are using conda:

```powershell
conda run -n DLEnv cmd /c "set PYTHONPATH=src&& python -m sair_competition.cli prepare-public-data --raw-dir data/raw --interim-dir data/interim"
conda run -n DLEnv cmd /c "set PYTHONPATH=src&& python -m sair_competition.cli make-splits --dataset-path data/interim/public_all.jsonl --output-dir data/interim/splits"
conda run -n DLEnv cmd /c "set PYTHONPATH=src&& python -m sair_competition.cli run-baseline-eval --dataset-path data/interim/splits/holdout.jsonl --output-dir artifacts/candidates/baseline_holdout"
```

## Complete prompt experiments

Run a complete prompt against a local split with an OpenAI-compatible API:

```powershell
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' -m sair_competition.cli run-complete-prompt-eval `
  --dataset-path data/interim/splits/smoke.jsonl `
  --prompt-path prompts/complete/example_complete_prompt.txt `
  --output-dir artifacts/candidates/complete_prompt_smoke `
  --dotenv-path .env `
  --model deepseek-chat `
  --limit 8
```

Then analyze the resulting predictions:

```powershell
& 'C:\ProgramData\anaconda3\envs\DLEnv\python.exe' -m sair_competition.cli analyze-errors `
  --predictions-path artifacts/candidates/complete_prompt_smoke/predictions.jsonl `
  --output-dir artifacts/candidates/complete_prompt_smoke_analysis
```

The current workspace also has a dedicated `official_archetype_distillation` prompt track for three strict-adapted branches:

- `balanced`
- `counterexample-first`
- `fast-filters`

These are meant to be smoke-tested as side branches, not merged into the `P1_2_3` mainline until they show better parse stability or cleaner error movement.

Compare several candidate runs and write a compact experiment report:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli compare-candidates `
  --candidate-dir artifacts/candidates/P1_1_1_strict_first_draft_smoke `
  --candidate-dir artifacts/candidates/P1_2_0_smoke_iter1 `
  --candidate-dir artifacts/candidates/P1_3_0_smoke_iter2 `
  --baseline-dir artifacts/candidates/P1_1_1_strict_first_draft_smoke `
  --output-dir reports/experiments/smoke_prompt_compare
```

## Cache behavior

This repository no longer pins pytest to a fixed workspace temp directory, because stale Windows temp folders under `artifacts/pytest_tmp*` can become permission-broken.

The supported local entrypoint is:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_pytest.ps1 tests/test_offline_rule_review.py -q
```

This wrapper:

- picks the `DLEnv` Python automatically when available
- disables external plugin autoload
- creates a fresh per-run temp directory under `artifacts/manual_checks/pytest_runs/`
- points `TMP` / `TEMP` at that run-local directory as well
- keeps `cacheprovider` disabled so pytest does not leave extra cache clutter behind

Bare `pytest` may still inherit unrelated plugins from the broader conda environment, so the wrapper is the recommended path for stable local runs.

## Notes

- `data/raw/` is for untouched official files.
- `prompts/complete/` stores prompt files that can be tested or submitted directly.
- `reports/experiments/` stores experiment-level logs and summaries.
- `artifacts/final/` is reserved for release candidates and frozen submission assets.
