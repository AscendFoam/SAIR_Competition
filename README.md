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

Repository-local pytest cache and temp files are configured to live under `artifacts/`:

- `artifacts/pytest_cache/`
- `artifacts/pytest_tmp/`

These paths are ignored by git to avoid root-level clutter.

## Notes

- `data/raw/` is for untouched official files.
- `prompts/complete/` stores prompt files that can be tested or submitted directly.
- `reports/experiments/` stores experiment-level logs and summaries.
- `artifacts/final/` is reserved for release candidates and frozen submission assets.
