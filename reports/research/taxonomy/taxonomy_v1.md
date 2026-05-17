# Taxonomy v1 Manual Coding Report

Date: 2026-05-17
Task: T07_manual_taxonomy_coding_v1
Taxonomy version: TAX_V1_MANUAL_CODING

## 1. Coding Pool

Full-text taxonomy coding was performed on 9 `included_text_ready` local records from `corpus_v1.jsonl`.

Why only 9:

- `corpus_v1.jsonl` contains 11 records total.
- 1 record (`public_placeholder_ce_first_github`) is `included_metadata_only` with no local prompt text, no SHA256, and no file path. It cannot be full-text coded.
- 1 record (`public_placeholder_contributor_prompt`) is `included_structure_only` with only host-level provenance. It cannot be full-text coded.
- Only the 9 text-ready records with local file paths and SHA256 hashes are eligible for full-text coding per the T06 boundary gate.

The 2 non-text-ready records are excluded from `prompt_features_v1.jsonl` entirely. They are not coded as "no features found"; they are not coded at all.

## 2. Token Estimate Method

All 9 text-ready records previously had `prompt_tokens_est = 0`. T07 backfills these estimates using a simple heuristic:

- Method: `prompt_tokens_est = round(prompt_bytes / 4)`
- Rationale: For ASCII-dominant English text with light use of backtick notation and special characters, a bytes-per-token ratio of approximately 4 is a reasonable rough estimate.
- Caveat: This is NOT a tokenizer count. No tokenizer (tiktoken, sentencepiece, or otherwise) was run. These values should only be used for coarse bucketing and relative comparison, never for precise token-level analysis or cost estimation.
- The estimation method is documented in each record's `notes` field as "Token estimate: bytes/4 heuristic (T07)."
- The 2 non-text-ready records remain at `prompt_tokens_est = 0`.

## 3. Length Bucket Boundaries

The following boundaries are used for `prompt_bytes_bucket`:

| Bucket | Range | Count |
|---|---|---|
| short | < 2000 bytes | 2 (P0: 511, P2.0.2: 1723) |
| medium | 2000-3499 bytes | 4 (P2.0.1: 2320, P2.0.0: 2448, P1.1.1: 2227, P1.2.2: 3454) |
| long | 3500-7999 bytes | 3 (P1.2.3: 3501, P1.2.8: 3948, P1.2.5: 4059) |
| near_cap | >= 8000 bytes | 0 |

The same proportional boundaries apply to `prompt_tokens_est_bucket`:

| Bucket | Token Range | Count |
|---|---|---|
| short | < 500 | 2 |
| medium | 500-874 | 4 |
| long | 875-1999 | 3 |
| near_cap | >= 2000 | 0 |

No prompt approaches the typical 10KB context cap. The longest prompt (P1.2.5 at 4059 bytes, ~1015 tokens) is well within safe bounds. The `near_cap` bucket is defined for future corpus expansion but is empty in v1.

## 4. Compression Style

Added in T07 to `prompt_feature_taxonomy.yaml` under `length_features`.

| Style | Description | Count |
|---|---|---|
| natural_language | Rules stated primarily in English prose | 3 (P0, P1.1.1, P2.0.1) |
| hybrid | Mix of prose and formal math notation (e.g., `x = T`, backtick expressions) | 6 (P1.2.2, P1.2.3, P1.2.5, P1.2.8, P2.0.0, P2.0.2) |
| symbolic | Rules primarily in mathematical notation | 0 |

Coding rationale: Prompts that reference specific mathematical forms like `x = T`, `T = x`, `x * x` using backtick notation in their rule descriptions are coded as hybrid. Prompts that describe the same concepts purely in prose (e.g., "a lone variable on one side that does not appear on the other side") are coded as natural_language.

This field was assessed as stably codable because the distinction is unambiguous for all 9 prompts.

## 5. ce_search_depth

Added in T07 to `prompt_feature_taxonomy.yaml` under `counterexample_strategy`.

| Depth | Description | Count |
|---|---|---|
| implicit | No explicit CE search instruction | 8 |
| shallow | Brief falsification guidance | 1 (P2.0.1) |
| explicit_multi_step | Detailed multi-step CE search | 0 |

Coding rationale: Only P2.0.1 has an explicit "Counterexample-first policy" section with falsification cues. All other prompts guide toward false verdicts via structural heuristics rather than counterexample search. None of the 9 prompts contain detailed multi-step counterexample construction instructions.

This field is stably codable but has very low variance in the current corpus (8:1:0). It may become more informative if future corpus expansion adds prompts with explicit finite model search or table lookup instructions.

## 6. Feature Distribution Summary

### Structural modules

| Feature | true/yes | false/no | Notes |
|---|---|---|---|
| system_goal_framing | 9 | 0 | All prompts frame the equational reasoning task |
| verdict_contract: strict | 8 | 1 (P0: relaxed) | P0 allows optional reasoning sections |
| stepwise_reasoning_block | 7 | 2 (P0, P2.0.2) | P2.0.2 uses flat filter lists instead |
| examples_block: none | 9 | 0 | No prompt includes worked examples |
| safety_or_guardrail_block | 8 | 1 (P0) | P0 has no guardrails |
| rule_or_heuristic_block: saturated | 1 | 8 | Only P1.2.5 |

### Opening strategies

| Strategy | Count | Prompts |
|---|---|---|
| trivial_first | 5 | P1.1.1, P1.2.2, P1.2.3, P1.2.5, P1.2.8 |
| balanced | 1 | P2.0.0 |
| counterexample_first | 1 | P2.0.1 |
| unknown | 2 | P0 (no rules), P2.0.2 (flat filters) |

### Verdict positioning

| Position | Count | Prompts |
|---|---|---|
| verdict_last | 8 | All except P0 |
| verdict_first | 1 | P0 |

### False filter orientation

| Orientation | Count | Prompts |
|---|---|---|
| high | 2 | P1.1.1, P2.0.1 |
| medium | 4 | P1.2.2, P1.2.3, P1.2.5, P1.2.8 |
| low | 1 | P2.0.0 |
| absent | 2 | P0, P2.0.2 |

### Proof-like TRUE support

| Level | Count | Prompts |
|---|---|---|
| strong | 1 | P1.2.5 |
| medium | 4 | P1.2.2, P1.2.3, P1.2.8, P2.0.0 |
| weak | 2 | P1.1.1, P2.0.1 |
| absent | 2 | P0, P2.0.2 |

### Ambiguity handling

| Handling | Count | Prompts |
|---|---|---|
| conservative_false | 6 | P1.1.1, P1.2.2, P1.2.3, P1.2.5, P1.2.8, P2.0.2 |
| balanced | 1 | P2.0.0 |
| unspecified | 2 | P0, P2.0.1 |

### Parser friendliness

| Level | Count | Prompts |
|---|---|---|
| high | 8 | All strict-format prompts |
| low | 1 | P0 (VERDICT: prefix format) |

## 7. Features Now Supported vs Planning Placeholder

### Now supported (stable coding, all 9 records)

All fields in `prompt_features_v1.jsonl` are stably coded for all 9 text-ready records:

- Length features: prompt_bytes_bucket, prompt_tokens_est_bucket, cheatsheet_density, compression_style
- Structural modules: system_goal_framing, verdict_contract, stepwise_reasoning_block, examples_block, rule_or_heuristic_block, safety_or_guardrail_block
- Module order: opening_strategy, verdict_positioning, examples_before_rules
- Counterexample strategy: counterexample_requirement, finite_model_search_hint, false_filter_orientation, ce_search_depth
- True strategy: proof_like_true_support, identity_or_invariant_guidance, ambiguity_handling
- Output stability: parser_friendliness, explicit_final_token, formatting_redundancy
- Provenance: provenance_status, builds_on_public_work, post_release_relation

### Planning placeholder (not yet coded, deferred to future tasks)

The following fields from experiment plan section 6.2 are NOT represented in the current taxonomy YAML because they require either extractor-level implementation or finer-grained coding that cannot be stably applied to all 9 prompts:

- `has_magma_reset`: Whether the prompt explicitly resets the magma definition. Could be added if needed, but all 9 prompts implicitly assume the standard magma framework.
- `has_no_hidden_axioms_warning`: Whether the prompt warns against assuming hidden axioms. None of the 9 prompts include this.
- `has_decision_tree`: Whether the prompt provides an explicit decision tree. The ordered reasoning discipline in some prompts approximates this but is not a formal decision tree.
- `has_confidence_or_uncertainty_language`: Whether the prompt discusses uncertainty or confidence. None of the 9 prompts include this.
- `has_law_family_rules`, `has_shared_lhs_rules`, `has_new_vars_rules`, `has_target_amplification_rules`, `has_singleton_collapse_rules`: These problem-family-specific rule fields would require a different coding granularity. The current taxonomy captures the aggregate effect through `proof_like_true_support` and the named TRUE-check rules in `manual_coding_note`.
- `true_mode` subcategories (rewrite, substitution, structural_family, trivial_magma, positive_signal, weak_heuristic): The current `proof_like_true_support` field captures the aggregate strength. Subcategorization would add complexity without clear benefit at the 9-prompt scale.

### Fields with low variance (codable but not yet informative)

- `ce_search_depth`: 8 implicit, 1 shallow. Will become more informative with corpus expansion.
- `finite_model_search_hint`: All 9 are false. No prompt currently includes finite model search guidance.
- `identity_or_invariant_guidance`: All 9 are false. No prompt includes explicit algebraic identity or invariant guidance.
- `examples_before_rules`: All 9 are false. No prompt has examples.
- `examples_block`: All 9 are none.
- `builds_on_public_work`: 6 none_declared, 3 official_only.

These fields are retained because they may differentiate prompts in future corpus expansion.

## 8. Prompt Family Groupings

Based on the taxonomy coding, the 9 prompts cluster into four structural families:

### Family A: Minimal baseline (1 prompt)
- P0: Empty cheatsheet, relaxed format, no rules.

### Family B: Guardrail-heavy local lineage (5 prompts)
- P1.1.1 → P1.2.2 → P1.2.3 → P1.2.5 (progressive rule expansion)
- P1.2.8 (branch from P1.2.2 with modified anti-bias)

Shared features: trivial_first, conservative_false, strict format, heavy cheatsheet density, hybrid compression, all local_contrast role.

Distinguishing axis: proof_like_true_support (weak → medium → strong) and rule_or_heuristic_block (compact → extended → saturated).

### Family C: Official archetype adaptations (3 prompts)
- P2.0.0: balanced
- P2.0.1: counterexample_first
- P2.0.2: fast-filters (trivial_first)

Shared features: strict format, official_only provenance, official_archetype role.

Distinguishing axis: opening_strategy, false_filter_orientation, cheatsheet_density.

### Family D: (Reserved for future external prompts)
Currently empty. The 2 non-text-ready external records would potentially belong here if mirrored and coded in a future task.

## 9. Coding Integrity Notes

- Coder: single-pass manual coding by T07 worker.
- No inter-annotator agreement metric is available for v1 (single coder).
- All borderline decisions are documented in `coder_note` per record.
- The taxonomy v1 should be treated as a coding reference for T08 extractor skeleton design, not as a final annotation gold standard.
- A self-audit (T09) should review coding consistency before the taxonomy is used for statistical analysis.
