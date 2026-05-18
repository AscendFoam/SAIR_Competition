# Screening Evaluation Matrix v1

Date: 2026-05-18
Task: T10_build_screening_evaluation_matrix
Status: Matrix defined; execution not started.

## 1. Scope

This document defines the screening evaluation matrix for Stage A of the research experiment pipeline. Screening is a small-sample candidate filtering step that runs all eligible prompts on a single split with a single low-cost model to:

- Check parse stability.
- Observe true/false recall patterns.
- Exclude candidates with collapse, parse failure, or non-reproducible behavior.
- Produce a shortlist of 3-5 prompts for the recomputed benchmark (Stage B).

### Non-scope

- Screening does not produce model predictions for publication.
- Screening does not determine final ranking or relative performance claims.
- Screening does not use released final evaluation subsets.
- Screening does not run ablations or cross-model comparisons.
- Screening does not modify prompt text, taxonomy, or corpus data.

## 2. Candidate Pool Definition

### Eligible candidates (9)

All 9 `included_text_ready` local records from `corpus_v1.jsonl`:

| # | prompt_id | Short name | Family | Length bucket |
|---|---|---|---|---|
| 1 | `local_p0_official_reconstructed_empty` | P0 | A: Minimal baseline | short |
| 2 | `local_p1_1_1_strict_first_draft` | P1.1.1 | B: Guardrail-heavy | medium |
| 3 | `local_p1_2_2_implicit_guardrail_v1` | P1.2.2 | B: Guardrail-heavy | medium |
| 4 | `local_p1_2_3_implicit_guardrail_v2` | P1.2.3 | B: Guardrail-heavy | long |
| 5 | `local_p1_2_5_minimal_rule_missing_hard_composition` | P1.2.5 | B: Guardrail-heavy | long |
| 6 | `local_p1_2_8_narrow_singleton_families` | P1.2.8 | B: Guardrail-heavy | long |
| 7 | `local_p2_0_0_official_balanced_strict_v0` | P2.0.0 | C: Official archetype | medium |
| 8 | `local_p2_0_1_official_counterexample_first_strict_v0` | P2.0.1 | C: Official archetype | medium |
| 9 | `local_p2_0_2_official_fast_filters_strict_v0` | P2.0.2 | C: Official archetype | short |

### Excluded from screening

| Record | Reason |
|---|---|
| `public_placeholder_ce_first_github` | `included_metadata_only`: no local text, no SHA256, no file path. Not text-ready per T06 boundary gate. |
| `public_placeholder_contributor_prompt` | `included_structure_only`: host-level provenance only, unresolved prompt-level attribution. Not text-ready per T06 boundary gate. |

## 3. Allowed Dataset Splits

### Primary screening split

`data/interim/splits/smoke.jsonl` (64 problems)

- Composition: 50 normal + 4 hard1 + 10 hard2
- Labels: 31 true, 33 false
- Rationale: small enough for rapid iteration; mixed difficulty; balanced label distribution; already exists as a fixed local split.

### Optional expansion

If smoke results do not discriminate between candidates (e.g., all candidates score within a narrow band), T11 may additionally screen on a `hard_slice_sample` drawn from `data/interim/splits/dev.jsonl` (174 hard problems: 44 hard1 + 130 hard2). This is optional and must be documented in the T11 execution report if used.

Screening must NOT use `holdout`, `audit`, or any released final evaluation subset.

## 4. Model/Provider Config

### Screening config (single model)

```json
{
  "model_alias": "proxy_low_cost_model",
  "provider_route": "to_fill",
  "temperature": 0,
  "max_tokens": 256,
  "reasoning_mode": "default"
}
```

- `provider_route` is set to `to_fill` until T11 execution confirms the actual API endpoint.
- All other fields are frozen for screening. T11 must not change `temperature`, `max_tokens`, or `reasoning_mode` without a documented rationale.
- The screening model should be a single low-cost model. Using multiple models or provider routes is forbidden in screening.

## 5. Run Configuration

### Prompt set (all 9)

```
local_p0_official_reconstructed_empty
local_p1_1_1_strict_first_draft
local_p1_2_2_implicit_guardrail_v1
local_p1_2_3_implicit_guardrail_v2
local_p1_2_5_minimal_rule_missing_hard_composition
local_p1_2_8_narrow_singleton_families
local_p2_0_0_official_balanced_strict_v0
local_p2_0_1_official_counterexample_first_strict_v0
local_p2_0_2_official_fast_filters_strict_v0
```

### Dataset set

```
smoke
```

### Repeats

`1` (single pass, no repeat consistency check in screening)

### Total screening runs

9 prompts x 1 split x 1 model x 1 repeat = 9 runs

## 6. Required Run Artifacts

Each screening run must produce:

1. `run_config.json`: model/provider config, prompt path, prompt hash, dataset path, dataset version, timestamp
2. `summary.json`: accuracy, strict_f1, parse_success_rate, true_recall, false_recall, problem_count, parse_fail_count
3. `predictions.jsonl`: one row per problem with prompt_id, problem_id, predicted, actual, parsed_ok
4. `prompt_hash_manifest.json`: SHA256 of the prompt file used

T11 must verify that all 9 runs produce all 4 artifacts before proceeding to analysis.

## 7. Required Metrics

### Primary screening metrics

| Metric | Purpose | Gate threshold |
|---|---|---|
| `parse_success_rate` | Can the model produce valid verdicts? | >= 0.95 |
| `true_recall` | Does the prompt recover true statements? | Report, no hard gate |
| `false_recall` | Does the prompt recover false statements? | Report, no hard gate |
| `accuracy` | Overall correctness | Report, no hard gate |

### Collapse checks

| Check | Definition | Gate |
|---|---|---|
| All-true collapse | `true_recall >= 0.95 AND false_recall <= 0.10` | BLOCK |
| All-false collapse | `false_recall >= 0.95 AND true_recall <= 0.10` | BLOCK |
| Parse collapse | `parse_success_rate < 0.95` | BLOCK |
| Near-collapse warning | `parse_success_rate < 1.00` or `true_recall < 0.20` or `false_recall < 0.20` | WARNING |

### Auxiliary metrics (report but do not gate)

- `prompt_bytes` / `prompt_tokens_est`: confirm prompt identity
- `avg_time_secs`: note latency outliers but do not gate
- `avg_cost_usd`: note cost outliers but do not gate

## 8. Taxonomy Field Usage Rules

### Fields directly usable as screening dimensions (from self_audit_v1.md Section 4.1)

These 8 fields have sufficient variance across 9 prompts and may be used as grouping variables, comparison axes, or hypothesis generators in the screening analysis:

| Field | Values in corpus | Screening use |
|---|---|---|
| `prompt_bytes_bucket` | short:2, medium:4, long:3 | Length-grouped performance comparison |
| `rule_or_heuristic_block` | none:1, compact:4, extended:3, saturated:1 | Rule-density vs performance |
| `false_filter_orientation` | absent:1, low:1, medium:5, high:2 | False-filter tradeoff observation |
| `proof_like_true_support` | absent:1, weak:2, medium:4, strong:1 | True-support vs true_recall |
| `cheatsheet_density` | none:1, light:1, medium:2, heavy:4 | Density vs performance |
| `opening_strategy` | unknown:1, trivial_first:5, balanced:1, counterexample_first:1 | Strategy ordering effect |
| `ambiguity_handling` | unspecified:1, balanced:1, conservative_false:7 | Conservative bias observation |
| `verdict_contract` | relaxed:1, strict:8 | Format strictness effect (limited: 1:8 split) |

### Descriptive-only fields (10 low-variance fields per T09 Adjudication 3)

These fields are retained in the schema and candidate registry but must NOT be used as independent variables, shortlist decision criteria, or statistical model inputs:

**Zero-variance (7):** `system_goal_framing`, `finite_model_search_hint`, `identity_or_invariant_guidance`, `examples_before_rules`, `examples_block`, `provenance_status`, `post_release_relation`

**Near-zero/low-variance (3):** `ce_search_depth`, `counterexample_requirement`, `builds_on_public_work`

These may appear in descriptive tables or narrative notes, but any claim that they explain performance differences is forbidden for the current 9-prompt corpus.

### Reporting boundary (per T09 Adjudication 4)

- Extractor outputs report "extractor behavior."
- Manual coding reports "taxonomy truth."
- When both exist for the same field, manual coding is authoritative.
- When only manual exists, report directly but note it is not extractor-verified.
- Zero-variance fields report as "constant across corpus; no discriminative power."

## 9. Screening Pass/Fail Gates

### Gate 1: Parse stability

A candidate is BLOCKED if `parse_success_rate < 0.95`.

Rationale: A prompt that cannot produce parseable verdicts at least 95% of the time on a 64-problem smoke split is not reliable enough for the recomputed benchmark.

### Gate 2: Collapse detection

A candidate is BLOCKED if it exhibits all-true or all-false collapse (see Section 7 collapse checks).

Rationale: Collapse indicates the prompt fails to engage with the reasoning task and defaults to a single label. This is a fundamental failure mode, not a performance gradient.

### Gate 3: Structural representation (soft gate)

The final shortlist must collectively cover at least 3 of the following 4 structural axes:

1. Length diversity: at least one short, one medium, and one long prompt.
2. Rule density: at least two different `rule_or_heuristic_block` levels.
3. Opening strategy: at least two different `opening_strategy` values.
4. Provenance diversity: at least one local_contrast and one official_archetype.

If applying Gates 1-2 leaves fewer than 3 prompts or fails this structural coverage test, the shortlist rules (see `screening_shortlist_rules_v1.md`) specify tiebreaking.

## 10. Post-Screening Transition

After all 9 screening runs complete and the shortlist is selected:

1. T12 writes the screening summary report.
2. The shortlist (3-5 prompts) enters the recomputed benchmark (Stage B) under separate config.
3. Screening results are NOT used as model selection signals or performance claims in the paper.
4. Screening results MAY be used to justify why certain prompts were excluded from the main evaluation.

## 11. Config Reference

The machine-readable screening config is frozen in `configs/research/evaluation_matrix.example.json`, screening phase section. Changes to that config after T10 review require a Captain decision documented in `docs/05_decision_log.md`.
