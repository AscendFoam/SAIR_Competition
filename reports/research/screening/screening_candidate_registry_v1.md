# Screening Candidate Registry v1

Date: 2026-05-18
Task: T10_build_screening_evaluation_matrix
Source: `data/interim/prompt_corpus/corpus_v1.jsonl` (authoritative), `data/interim/prompt_corpus/prompt_features_v1.jsonl` (T09 corrected)

## 1. Screening Candidate Pool

All 9 `included_text_ready` local records are eligible for first-round screening.

### Core Candidates (6)

These candidates represent distinct structural types and are expected to survive screening barring parse failure or collapse:

| # | prompt_id | Short name | Family | Length bucket | Rule block | Opening strategy | False-filter | TRUE support | Candidate role |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `local_p0_official_reconstructed_empty` | P0 | A: Minimal baseline | short | none | unknown | absent | absent | Baseline |
| 2 | `local_p1_2_3_implicit_guardrail_v2` | P1.2.3 | B: Guardrail-heavy | long | extended | trivial_first | medium | medium | Guardrail mainline |
| 3 | `local_p1_2_5_minimal_rule_missing_hard_composition` | P1.2.5 | B: Guardrail-heavy | long | saturated | trivial_first | medium | strong | Rule-saturated high-recall |
| 4 | `local_p2_0_0_official_balanced_strict_v0` | P2.0.0 | C: Official archetype | medium | compact | balanced | low | medium | Balanced archetype |
| 5 | `local_p2_0_1_official_counterexample_first_strict_v0` | P2.0.1 | C: Official archetype | medium | compact | counterexample_first | high | weak | CE-first archetype |
| 6 | `local_p2_0_2_official_fast_filters_strict_v0` | P2.0.2 | C: Official archetype | short | compact | trivial_first | medium | weak | Fast-filters archetype |

Structural uniqueness rationale:

- P0: only relaxed `verdict_contract`, only `parser_friendliness = low`, only no rules.
- P1.2.3: guardrail-heavy mainline with `extended` rules, `medium` false-filter, `medium` TRUE support.
- P1.2.5: only `saturated` rule block, only `strong` TRUE support. RC1 submission version.
- P2.0.0: only `balanced` opening strategy, only `balanced` ambiguity handling, lowest false-filter among non-empty prompts.
- P2.0.1: only `counterexample_first` opening strategy, only `shallow` ce_search_depth, only `encouraged` counterexample_requirement.
- P2.0.2: shortest strict-format prompt, only strict prompt with `stepwise_reasoning_block = false`.

### Contrast Candidates (3)

These candidates belong to the same structural family as core candidates and provide within-family variation for discrimination:

| # | prompt_id | Short name | Family | Length bucket | Rule block | Opening strategy | Contrasts with | Contrast purpose |
|---|---|---|---|---|---|---|---|---|
| 7 | `local_p1_1_1_strict_first_draft` | P1.1.1 | B: Guardrail-heavy | medium | compact | trivial_first | P1.2.3, P1.2.5 | Early draft vs mature mainline: rule density progression compact -> extended -> saturated |
| 8 | `local_p1_2_2_implicit_guardrail_v1` | P1.2.2 | B: Guardrail-heavy | medium | extended | trivial_first | P1.2.3 | Pre-mainline vs mainline: guardrail strengthening and anti-bias expansion |
| 9 | `local_p1_2_8_narrow_singleton_families` | P1.2.8 | B: Guardrail-heavy | long | extended | trivial_first | P1.2.2 | Modified anti-bias: tree-depth focus vs shared-variable focus |

### Deferred Candidates (0)

All 9 text-ready records enter screening. No text-ready record is deferred.

## 2. Non-Candidate Records

| Record | corpus_inclusion_status | Reason for exclusion |
|---|---|---|
| `public_placeholder_ce_first_github` | `included_metadata_only` | No local prompt text (`prompt_text_path` empty), no SHA256, no file path. T06 boundary gate: text_ready = false. GitHub MIT source verified but not mirrored. |
| `public_placeholder_contributor_prompt` | `included_structure_only` | Host-level provenance only. No stable prompt-level URL, no resolved attribution terms. T06 boundary gate: text_ready = false. |

A later reviewed task may change these records' status if:
1. The GitHub MIT prompt file is mirrored with file-level path, SHA256, byte size, license, and attribution.
2. The Contributor Network record gains a stable prompt-level URL and resolved storage terms.

Until then, these records may appear in the registry as descriptive entries but must not enter screening execution.

## 3. Prompt Family Distribution

| Family | Count | Members | Screening role |
|---|---|---|---|
| A: Minimal baseline | 1 | P0 | Floor baseline for parse/format contrast |
| B: Guardrail-heavy local lineage | 5 | P1.1.1, P1.2.2, P1.2.3, P1.2.5, P1.2.8 | Main body; within-family rule density and anti-bias variation |
| C: Official archetype adaptations | 3 | P2.0.0, P2.0.1, P2.0.2 | Cross-provenance strategy comparison |
| D: Reserved external | 0 | (none) | Not represented; gap acknowledged |

## 4. Structural Coverage Summary

### Length buckets

| Bucket | Count | Prompts |
|---|---|---|
| short (< 2000 bytes) | 2 | P0 (511), P2.0.2 (1723) |
| medium (2000-3499 bytes) | 4 | P1.1.1 (2227), P2.0.1 (2320), P2.0.0 (2448), P1.2.2 (3454) |
| long (3500-7999 bytes) | 3 | P1.2.3 (3501), P1.2.8 (3948), P1.2.5 (4059) |
| near_cap (>= 8000 bytes) | 0 | (none) |

### Opening strategy

| Strategy | Count | Prompts |
|---|---|---|
| trivial_first | 5 | P1.1.1, P1.2.2, P1.2.3, P1.2.5, P1.2.8 |
| balanced | 1 | P2.0.0 |
| counterexample_first | 1 | P2.0.1 |
| unknown | 2 | P0, P2.0.2 |

### Rule density

| Level | Count | Prompts |
|---|---|---|
| none | 1 | P0 |
| compact | 4 | P1.1.1, P2.0.0, P2.0.1, P2.0.2 |
| extended | 3 | P1.2.2, P1.2.3, P1.2.8 |
| saturated | 1 | P1.2.5 |

### Verdict contract

| Contract | Count | Prompts |
|---|---|---|
| relaxed | 1 | P0 |
| strict | 8 | All others |

### False-filter orientation

| Orientation | Count | Prompts |
|---|---|---|
| absent | 1 | P0 |
| low | 1 | P2.0.0 |
| medium | 5 | P1.2.2, P1.2.3, P1.2.5, P1.2.8, P2.0.2 |
| high | 2 | P1.1.1, P2.0.1 |

## 5. Known Coverage Gaps

1. **No external prompts in the screening pool.** Family D is empty. The 2 non-text-ready external records cannot fill it. Screening conclusions apply only to local-project and official-archetype prompts.
2. **No near_cap prompts.** The longest prompt (P1.2.5 at 4059 bytes) is well below the 10KB context cap. Length-effect conclusions cannot extend to near-cap prompts.
3. **Only 1 counterexample_first prompt.** P2.0.1 is the sole representative of this strategy. Within-strategy variation cannot be assessed.
4. **Only 1 balanced prompt.** P2.0.0 is the sole representative.
5. **Only 1 relaxed-format prompt.** P0 is the only non-strict prompt, and it is also the minimal baseline. Format strictness effects are confounded with rule content.
6. **No examples in any prompt.** All 9 prompts have `examples_block = none`. The effect of examples on performance cannot be assessed.

These gaps must be acknowledged in any screening report and should not be claimed as general conclusions.
