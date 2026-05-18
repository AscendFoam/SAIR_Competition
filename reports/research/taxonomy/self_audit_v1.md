# Taxonomy Self-Audit v1

Date: 2026-05-18
Task: T09_taxonomy_self_audit_and_conflict_resolution
Scope: T07 manual coding vs T08 extractor skeleton, 9 text-ready local prompts

## 1. Sample Coverage

- Total corpus records: 11
- Text-ready local records coded: 9
- Metadata-only records excluded: 1 (GitHub, no local text)
- Structure-only records excluded: 1 (Contributor Network, unresolved provenance)
- T06 boundary gate: respected by both T07 coding and T08 extractor; no non-text-ready records entered full-text coding or feature extraction.

The 9 coded prompts span 4 structural families:

| Family | Count | Members |
|---|---|---|
| A: Minimal baseline | 1 | P0 |
| B: Guardrail-heavy lineage | 5 | P1.1.1, P1.2.2, P1.2.3, P1.2.5, P1.2.8 |
| C: Official archetype adaptations | 3 | P2.0.0, P2.0.1, P2.0.2 |
| D: Reserved external | 0 | (future) |

Coverage gap: Family D is empty. The 2 external records cannot fill it until mirrored and coded in a future task. This limits generalizability but is honest.

## 2. Manual Coding Pool vs Extractor Coverage

### 2.1 Rule-ized fields (T08 extractor)

7 fields have keyword/pattern-based extraction rules:

| Field | Extractor match (9 prompts) | Manual agreement |
|---|---|---|
| `prompt_bytes_bucket` | 9/9 | 9/9 (exact) |
| `prompt_tokens_est_bucket` | 9/9 | 9/9 (exact) |
| `verdict_contract` | 9/9 | 9/9 (exact) |
| `rule_or_heuristic_block` | 9/9 | 9/9 (exact) |
| `opening_strategy` | 9/9 | 9/9 (exact) |
| `explicit_final_token` | 9/9 | 9/9 (exact) |
| `counterexample_requirement` | 8/9 | 8/9 (1 known disagreement) |

### 2.2 Placeholder fields (manual only)

19 fields are not rule-ized and remain manual-only:

`cheatsheet_density`, `compression_style`, `system_goal_framing`, `stepwise_reasoning_block`, `examples_block`, `safety_or_guardrail_block`, `verdict_positioning`, `examples_before_rules`, `finite_model_search_hint`, `false_filter_orientation`, `ce_search_depth`, `proof_like_true_support`, `identity_or_invariant_guidance`, `ambiguity_handling`, `parser_friendliness`, `formatting_redundancy`, `provenance_status`, `builds_on_public_work`, `post_release_relation`

### 2.3 Manual vs Extractor Mismatch Table

| Prompt | Field | Manual | Extractor | Documented? | Impact |
|---|---|---|---|---|---|
| P2.0.2 | `counterexample_requirement` | optional | absent | Yes (extractor_v1_notes.md, test comments) | Low: only 1 record, field itself is low-variance |

This is the only mismatch across 63 comparisons (7 fields x 9 prompts). Agreement rate: 98.4%.

## 3. Field Variance Note

### 3.1 High-variance fields (useful for T10/T19)

Fields with >= 3 distinct values across 9 prompts:

| Field | Unique values | Distribution |
|---|---|---|
| `prompt_bytes_bucket` | 3 | short:2, medium:4, long:3 |
| `prompt_tokens_est_bucket` | 3 | short:2, medium:4, long:3 |
| `cheatsheet_density` | 4 | none:1, light:2, medium:2, heavy:4 |
| `rule_or_heuristic_block` | 4 | none:1, compact:4, extended:3, saturated:1 |
| `false_filter_orientation` | 4 | absent:1, low:1, medium:5, high:2 |
| `proof_like_true_support` | 4 | absent:1, weak:3, medium:4, strong:1 |
| `ambiguity_handling` | 3 | unspecified:1, balanced:1, conservative_false:7 |

### 3.2 Moderate-variance fields

| Field | Unique values | Distribution |
|---|---|---|
| `verdict_contract` | 2 | relaxed:1, strict:8 |
| `opening_strategy` | 4 | unknown:1, trivial_first:6, balanced:1, counterexample_first:1 |
| `compression_style` | 2 | natural_language:3, hybrid:6 |
| `stepwise_reasoning_block` | 2 | false:2, true:7 |
| `safety_or_guardrail_block` | 2 | false:1, true:8 |
| `verdict_positioning` | 2 | verdict_first:1, verdict_last:8 |
| `parser_friendliness` | 2 | low:1, high:8 |
| `explicit_final_token` | 2 | false:1, true:8 |
| `formatting_redundancy` | 2 | none:1, light:8 |
| `counterexample_requirement` | 3 | absent:7, encouraged:1, optional:1 |
| `builds_on_public_work` | 2 | none_declared:6, official_only:3 |

### 3.3 Zero-variance fields (single value across all 9 prompts)

| Field | Value |
|---|---|
| `system_goal_framing` | true (all 9) |
| `finite_model_search_hint` | false (all 9) |
| `identity_or_invariant_guidance` | false (all 9) |
| `examples_before_rules` | false (all 9) |
| `examples_block` | none (all 9) |
| `provenance_status` | local_project (all 9) |
| `post_release_relation` | pre_release_design (all 9) |

### 3.4 Near-zero-variance fields (9:1 or 8:1 split)

| Field | Dominant value | Minority |
|---|---|---|
| `ce_search_depth` | implicit (8) | shallow (1: P2.0.1) |

## 4. Field Usage Classification for T10/T19

### 4.1 Fields directly usable for screening and statistical analysis

These fields have sufficient variance and are either extractor-verified or straightforward to validate manually:

- `prompt_bytes_bucket` / `prompt_tokens_est_bucket`: length effect analysis
- `rule_or_heuristic_block`: rule density effect
- `false_filter_orientation`: false-filter tradeoff analysis
- `proof_like_true_support`: true-path strength analysis
- `cheatsheet_density`: density vs performance
- `opening_strategy`: strategy ordering effect (though distribution is skewed toward trivial_first)
- `ambiguity_handling`: conservative bias analysis
- `verdict_contract`: format strictness effect (limited by 1:8 split)

### 4.2 Fields usable as descriptive/illustrative labels only

These fields have moderate variance but too few records for robust statistical testing. Use for grouping, narrative, and hypothesis generation:

- `compression_style`
- `stepwise_reasoning_block`
- `safety_or_guardrail_block`
- `verdict_positioning`
- `parser_friendliness`
- `explicit_final_token`
- `formatting_redundancy`
- `counterexample_requirement` (after T09 adjudication)
- `builds_on_public_work`

### 4.3 Fields requiring manual override (not extractor-trusted)

All 19 placeholder fields remain manual-only. Additionally, for P2.0.2 `counterexample_requirement`, the manual coding value takes precedence over extractor output per the adjudication in `conflict_resolution_v1.md`.

### 4.4 Zero-variance fields: retain but do not model

These fields contribute no discriminative power in the current 9-prompt corpus:

- `system_goal_framing` (all true)
- `finite_model_search_hint` (all false)
- `identity_or_invariant_guidance` (all false)
- `examples_before_rules` (all false)
- `examples_block` (all none)
- `provenance_status` (all local_project)
- `post_release_relation` (all pre_release_design)

Retention rationale: These fields may become informative after corpus expansion (e.g., adding external prompts with different provenance). Removing them now would lose schema continuity. They should be excluded from statistical models but retained in the taxonomy schema and feature records.

## 5. Single-Coder Bias Assessment

### 5.1 Known limitation

T07 was a single-pass manual coding by one worker. No inter-annotator agreement metric exists.

### 5.2 Mitigating factors

1. All coding decisions are documented in `coder_note` and `manual_coding_note` per record.
2. Borderline decisions are explicitly flagged (e.g., P1.2.3 byte boundary, P2.0.2 counterexample_requirement).
3. The taxonomy YAML defines strict allowed_values for each field, constraining the coding space.
4. T08 extractor provides an independent keyword-based cross-check on 7 fields, achieving 98.4% agreement.

### 5.3 Fields most susceptible to single-coder bias

- `false_filter_orientation`: Requires subjective judgment of "high" vs "medium" vs "low" false-filter emphasis. Distribution: absent:1, low:1, medium:5, high:2.
- `proof_like_true_support`: Strength levels (strong/medium/weak/absent) involve judgment about how comprehensive the TRUE-path rules are.
- `cheatsheet_density`: none/light/medium/heavy is inherently subjective.
- `ambiguity_handling`: Requires inferring the prompt's implicit stance on uncertain cases.

### 5.4 Fields least susceptible to bias

- `prompt_bytes_bucket` / `prompt_tokens_est_bucket`: Deterministic from byte count.
- `verdict_contract`: Directly checkable from keyword patterns.
- `explicit_final_token`: Directly checkable from keyword patterns.
- `provenance_status` / `post_release_relation`: Deterministic from corpus metadata.

## 6. Claims Not Supported by Current Data

The following claims cannot be made from the current 9-prompt taxonomy:

1. **"Prompt length has a monotonic relationship with performance."** The corpus has too few prompts and no performance data yet.
2. **"Trivial-first prompts outperform counterexample-first prompts."** Only 1 CE-first prompt exists.
3. **"Strict formatting improves parse stability."** Only 1 relaxed-format prompt (P0), which is also the minimal baseline. Confound: format strictness is inseparable from rule content.
4. **"The taxonomy generalizes to all SAIR Stage1 prompts."** Only 9 local prompts coded; 0 external prompts in the coding pool.
5. **"The extractor can replace manual coding."** Only 7 of 26 feature fields are rule-ized, with 1 known disagreement.
6. **"Compression style affects reasoning quality."** Only 2 values (natural_language: 3, hybrid: 6), and no performance data.

## 7. Recommendations for T09 Adjudication Input

Based on this self-audit, the following issues require adjudication in `conflict_resolution_v1.md`:

1. P2.0.2 `counterexample_requirement`: manual `optional` vs extractor `absent`.
2. `rule_or_heuristic_block` saturated/extended heuristic fragility.
3. Low-variance field policy (retain/deprioritize/descriptive-only).
4. Extractor stability vs manual alignment reporting boundary.
5. Whether any minimal corrections to `prompt_features_v1.jsonl` are warranted.
