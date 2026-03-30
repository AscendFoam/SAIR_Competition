# Prompt Assets

Prompt work is split into:

- `templates/`: reusable prompt templates
- `cheatsheets/`: rule-focused text blocks
- `complete/`: fully rendered prompts ready to test
- `archive/`: older prompt versions kept for reference

The current prompt strategy keeps two lines alive at the same time:

- the stable local mainline around `P1_2_3`
- a separate `official archetype distillation` track that reinterprets the official `balanced`, `counterexample-first`, and `fast-filters` prompt styles as strict local smoke-test branches
