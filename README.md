# SAIR Competition Workspace

This repository is the engineering workspace for the SAIR equational-theories competition project.

## Current scope

- Convert the competition plan into a runnable repository skeleton
- Manage prompt experiments as versioned artifacts
- Keep data, prompts, configs, reports, and code separated
- Prepare a minimal CLI for prompt composition and local evaluation utilities

## Repository layout

```text
.
├─ artifacts/
├─ configs/
├─ data/
├─ docs/
├─ prompts/
├─ reports/
├─ src/
├─ tests/
└─ webpages/
```

See the plan document for the project strategy:

- `docs/SAIR代数推理竞赛工程化实验计划.md`

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

## Notes

- `data/raw/` is for untouched official files.
- `prompts/complete/` stores prompt files that can be tested or submitted directly.
- `reports/experiments/` stores experiment-level logs and summaries.
- `artifacts/final/` is reserved for release candidates and frozen submission assets.
