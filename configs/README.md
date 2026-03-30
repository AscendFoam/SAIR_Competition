# Configs

This directory stores machine-readable configuration files for:

- model endpoints or aliases
- evaluation runs
- prompt build defaults
- local rule registries and offline rule-asset bundles

Use example files as templates and create local copies as needed.

For the current offline-rule-asset workflow:

- `configs/prompts/rule_registry.example.jsonl` documents the lightweight prompt-facing registry shape.
- `configs/prompts/offline_rule_assets.example.jsonl` documents the richer offline-first asset shape used for tagging, slicing, and audit workflows.
- local generated bundles such as `rule_registry.offline_assets_v2.jsonl` are meant to stay local unless you explicitly want to publish a sanitized example.
