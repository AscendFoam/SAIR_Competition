# Prompt Templates

- `evaluation.jinja2`: repository-formalized reconstruction of the official `evaluation` template referenced by `data/raw/prompt_templates.jsonl`. It is kept for provenance and comparison against public run traces.
- `evaluation_strict_v1.jinja2`: engineering-oriented strict template for local experiments. It is tuned to maximize parse compliance on OpenAI-compatible chat models such as DeepSeek.
- `baseline_minimal.j2`: minimal baseline prompt used for early pipeline shakedown.
