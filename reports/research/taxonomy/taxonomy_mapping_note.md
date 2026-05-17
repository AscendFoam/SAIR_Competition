# Taxonomy Mapping Note: Experiment Plan 6.2 to YAML Fields

Date: 2026-05-17
Task: T07_manual_taxonomy_coding_v1

## Purpose

This document maps each feature field from experiment plan section 6.2 (`docs/02_experiment_plan.md`) to the corresponding field in `configs/research/prompt_feature_taxonomy.yaml` (TAX_V1_MANUAL_CODING) and `prompt_features_v1.jsonl`. It also documents which fields are directly adopted, which are modified, and which are deferred.

## Mapping Table

### Length features

| Experiment plan 6.2 field | YAML field | Mapping status | Notes |
|---|---|---|---|
| `prompt_bytes` | (not in taxonomy YAML; in corpus_v1.jsonl) | direct | Byte count lives in the corpus record, not the taxonomy feature record. |
| `prompt_tokens_est` | (not in taxonomy YAML; in corpus_v1.jsonl) | direct | Token estimate lives in the corpus record. |
| `near_10kb_cap` | (derivable from prompt_bytes_bucket) | derived | Not a separate taxonomy field. Derivable as `prompt_bytes_bucket == "near_cap"`. |
| `length_bucket` | `prompt_bytes_bucket` | renamed | Experiment plan calls it `length_bucket`; YAML uses `prompt_bytes_bucket` for clarity. Same semantics and same allowed values (short/medium/long/near_cap). |
| `compression_style` | `compression_style` | direct | Added in T07. Was deferred from T01 review. Now stably coded. |

### Structural modules

| Experiment plan 6.2 field | YAML field | Mapping status | Notes |
|---|---|---|---|
| `has_task_framing` | `system_goal_framing` | renamed | Same semantics. YAML uses the boolean type. |
| `has_magma_reset` | (not in YAML) | deferred | All 9 prompts implicitly assume standard magma framework. Low differentiating value. Can be added if future prompts differ. |
| `has_no_hidden_axioms_warning` | (not in YAML) | deferred | No prompt includes this. Placeholder for future corpus expansion. |
| `has_verdict_first_contract` | (derivable from `verdict_positioning`) | derived | `verdict_positioning == "verdict_first"` captures this. |
| `has_strict_final_answer_contract` | (derivable from `verdict_contract`) | derived | `verdict_contract == "strict"` captures this. |
| `has_stepwise_checklist` | `stepwise_reasoning_block` | renamed | Same semantics. |
| `has_decision_tree` | (not in YAML) | deferred | Ordered reasoning discipline approximates this but is not a formal decision tree. |
| `has_ce_lookup_or_table` | (derivable from `finite_model_search_hint`) | derived | `finite_model_search_hint == true` would capture explicit finite model construction. |
| `has_trivial_magma_rule` | (derivable from TRUE-check rules in `manual_coding_note`) | partial | The singleton-collapse and symmetric singleton rules in guardrail-heavy prompts serve this purpose. Not a standalone taxonomy field. |
| `has_false_filters` | (derivable from `false_filter_orientation`) | derived | `false_filter_orientation != "absent"` captures this. |
| `has_true_positive_rules` | (derivable from `proof_like_true_support`) | derived | `proof_like_true_support != "absent"` captures this. |
| `has_examples` | `examples_block` | renamed | `examples_block != "none"` captures this. All 9 prompts are `none`. |
| `has_confidence_or_uncertainty_language` | (not in YAML) | deferred | No prompt includes this. |

### Module order

| Experiment plan 6.2 field | YAML field | Mapping status | Notes |
|---|---|---|---|
| `first_substantive_module` | `opening_strategy` | renamed | Same semantics, same allowed values. |
| `ce_before_true_rules` | (derivable from module order) | derived | Can be inferred from `opening_strategy == "counterexample_first"`. |
| `true_rules_before_ce` | (derivable from module order) | derived | Can be inferred from `opening_strategy == "trivial_first"`. |
| `format_contract_position` | `verdict_positioning` | partial | YAML captures output-level verdict position. Prompt-level format contract position is not separately coded. |
| `guardrail_position` | (not in YAML) | deferred | Could be added as a separate field. Currently implicit in `safety_or_guardrail_block = true`. |

### Counterexample strategy

| Experiment plan 6.2 field | YAML field | Mapping status | Notes |
|---|---|---|---|
| `counterexample_mode` | `counterexample_requirement` | renamed | Same semantics: required/encouraged/optional/absent. |
| `ce_search_depth` | `ce_search_depth` | direct | Added in T07. Was deferred from T01 review. Now stably coded but low variance. |
| `false_default_when_uncertain` | (derivable from `ambiguity_handling`) | derived | `ambiguity_handling == "conservative_false"` captures this. |
| `true_default_when_no_ce` | (not in YAML) | deferred | No prompt in the current corpus defaults to true when no counterexample is found. Can be added if needed. |

### TRUE strategy

| Experiment plan 6.2 field | YAML field | Mapping status | Notes |
|---|---|---|---|
| `true_mode` | (partial: `proof_like_true_support`) | partial | YAML captures strength (strong/medium/weak/absent) but not subcategory (rewrite/substitution/structural_family/etc.). Subcategorization deferred due to small corpus size. |
| `has_law_family_rules` | (not in YAML) | deferred | Problem-family-specific. Would require finer-grained coding. |
| `has_shared_lhs_rules` | (not in YAML) | deferred | Same as above. |
| `has_new_vars_rules` | (not in YAML) | deferred | Same as above. |
| `has_target_amplification_rules` | (not in YAML) | deferred | Same as above. |
| `has_singleton_collapse_rules` | (not in YAML; noted in `manual_coding_note`) | partial | Captured in per-record notes, not as a standalone boolean. The guardrail-heavy prompts (P1.2.2+) all include singleton collapse rules. |

### Output stability

| Experiment plan 6.2 field | YAML field | Mapping status | Notes |
|---|---|---|---|
| `allows_reasoning_text` | (derivable from `verdict_contract`) | derived | `verdict_contract == "relaxed"` (only P0). |
| `requires_single_word_output` | `explicit_final_token` | renamed | Same semantics. |
| `requires_final_line` | (derivable from `verdict_positioning`) | derived | `verdict_positioning == "verdict_last"` implies a final-line answer. |
| `case_contract` | (not in YAML) | deferred | All strict prompts use lowercase `true`/`false`. P0 uses uppercase `TRUE`/`FALSE`. Not separately coded. |
| `parse_risk` | `parser_friendliness` | inverse | `parser_friendliness` is the inverse of `parse_risk` (high friendliness = low risk). |

## Seed scaffold fields adopted without change

The following fields from the original TAX_V1_SEED scaffold are used directly in TAX_V1_MANUAL_CODING without modification:

- `prompt_bytes_bucket` (categorical: short/medium/long/near_cap)
- `prompt_tokens_est_bucket` (categorical: short/medium/long/near_cap)
- `cheatsheet_density` (categorical: none/light/medium/heavy)
- `system_goal_framing` (boolean)
- `verdict_contract` (categorical: strict/semi_strict/relaxed/unknown)
- `stepwise_reasoning_block` (boolean)
- `examples_block` (categorical: none/positive_only/negative_only/mixed)
- `rule_or_heuristic_block` (categorical: none/compact/extended/saturated)
- `safety_or_guardrail_block` (boolean)
- `opening_strategy` (categorical: trivial_first/counterexample_first/balanced/rules_first/unknown)
- `verdict_positioning` (categorical: verdict_last/verdict_with_justification/verdict_first/unknown)
- `counterexample_requirement` (categorical: required/encouraged/optional/absent)
- `finite_model_search_hint` (boolean)
- `false_filter_orientation` (categorical: high/medium/low/absent)
- `proof_like_true_support` (categorical: strong/medium/weak/absent)
- `identity_or_invariant_guidance` (boolean)
- `ambiguity_handling` (categorical: conservative_false/balanced/conservative_true/unspecified)
- `parser_friendliness` (categorical: high/medium/low/unknown)
- `explicit_final_token` (boolean)
- `formatting_redundancy` (categorical: none/light/medium/heavy)
- `provenance_status` (categorical: official_public/public_reproducible/local_project/social_or_partial/unknown)
- `builds_on_public_work` (categorical: none_declared/official_only/public_prompt_adaptation/mixed_public_sources/unknown)
- `post_release_relation` (categorical: pre_release_design/post_release_analysis_only/unknown)

## Fields added in T07

- `compression_style` (categorical: natural_language/symbolic/hybrid) — under length_features
- `ce_search_depth` (categorical: implicit/shallow/explicit_multi_step) — under counterexample_strategy
- `bucket_boundary_notes` (documentation section) — documents bucket thresholds

## Fields tightened in T07

- `rule_or_heuristic_block` allowed_values: the `saturated` value is now exercised (P1.2.5), whereas in the seed scaffold it was defined but never used.
- `verdict_contract` allowed_values: the `relaxed` value is now exercised (P0), providing a concrete example.

## Fields not yet exercised in the 9-record corpus

- `verdict_contract: semi_strict` — no prompt uses this intermediate form
- `examples_block: positive_only, negative_only, mixed` — no prompt has examples
- `opening_strategy: rules_first` — no prompt leads with rules as the first dominant strategy
- `counterexample_requirement: required` — no prompt requires counterexample construction
- `proof_like_true_support: absent` (in non-empty prompts) — P0 is the only prompt with absent support, but it has no rules at all
- `formatting_redundancy: medium, heavy` — all prompts are none or light
- `provenance_status: official_public, public_reproducible, social_or_partial` — all 9 are local_project
- `builds_on_public_work: public_prompt_adaptation, mixed_public_sources` — all are none_declared or official_only
- `compression_style: symbolic` — all prompts use prose or hybrid
- `ce_search_depth: explicit_multi_step` — no prompt has detailed CE search instructions

These unused values are retained for future corpus expansion and should not be removed.
