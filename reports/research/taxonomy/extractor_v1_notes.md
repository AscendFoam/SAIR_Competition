# Extractor v1 Notes

Date: 2026-05-17
Task: T08_prompt_feature_extractor_skeleton
Module: `src/sair_competition/analysis/prompt_features.py`

## Scope Statement

This is a **skeleton** extractor, not full automation. Manual taxonomy coding
(`prompt_features_v1.jsonl`) remains the **authoritative reference**.  The
extractor produces structured feature records from prompt text files, but only
a subset of fields are rule-ized.  T09 self-audit is still required before
taxonomy results are used for statistical analysis.

## Rule-ized Fields (skeleton coverage)

The following 7 fields have keyword/pattern-based extraction rules that pass
focused tests against all 9 text-ready prompts:

| Field | Method | 9/9 match |
|---|---|---|
| `prompt_bytes_bucket` | Byte-count thresholds | Yes |
| `prompt_tokens_est_bucket` | round(bytes/4) thresholds | Yes |
| `verdict_contract` | "exactly one token" / "VERDICT:" patterns | Yes |
| `rule_or_heuristic_block` | "Mandatory TRUE checks" + "override" keywords | Yes |
| `opening_strategy` | "Counterexample-first" / "Balanced solve" / "Mandatory TRUE" / "Fast TRUE" keywords | Yes |
| `counterexample_requirement` | "counterexample-first policy" / "falsification" / "counterexample" instruction keywords | 8/9 (see below) |
| `explicit_final_token` | "exactly one token" / "single token" patterns | Yes |

## Known Disagreements with Manual Coding

### P2.0.2 counterexample_requirement

- Manual coding: `optional`
- Extractor output: `absent`
- Reason: P2.0.2 has no "counterexample" keyword in its text. The manual
  coder assigned "optional" based on implicit counterexample-like reasoning in
  the fast-false filters, but the skeleton extractor cannot detect this without
  deeper semantic analysis.
- Impact: Low. P2.0.2 is the only prompt with this discrepancy.

### P1.2.5 vs P1.2.8 rule_or_heuristic_block distinction

Both prompts contain "Singleton family A/B" rules, but only P1.2.5 is coded as
`saturated`. The extractor uses the presence of "override" (from P1.2.5's
"do not let later guardrails override it" clause) to distinguish `saturated`
from `extended`. This heuristic is specific to the current corpus and may need
revision if future prompts have different override patterns.

## Placeholder Fields (not yet rule-ized)

The following fields always return `unknown` / `None` and require manual review
or a future extractor version:

- `cheatsheet_density`
- `compression_style`
- `system_goal_framing`
- `stepwise_reasoning_block`
- `examples_block`
- `safety_or_guardrail_block`
- `verdict_positioning`
- `examples_before_rules`
- `finite_model_search_hint`
- `false_filter_orientation`
- `ce_search_depth`
- `proof_like_true_support`
- `identity_or_invariant_guidance`
- `ambiguity_handling`
- `parser_friendliness`
- `formatting_redundancy`
- `provenance_status`
- `builds_on_public_work`
- `post_release_relation`

## Low-Variance Fields

The following fields have low variance in the current 9-prompt corpus and
should not be treated as high-information features in screening or statistical
models, even after future extractor coverage:

- `ce_search_depth`: 8 implicit, 1 shallow
- `finite_model_search_hint`: all false
- `identity_or_invariant_guidance`: all false
- `examples_before_rules`: all false
- `examples_block`: all none
- `counterexample_requirement`: 7 absent, 1 encouraged, 1 optional (manual)

These fields are retained for future corpus expansion.

## Token Estimate Fix (T08)

T07 reviewer identified a wording inconsistency: `taxonomy_v1.md` described the
token estimate as `floor(prompt_bytes / 4)`, but the actual data used
`round(prompt_bytes / 4)`. The data values are:

| Prompt | Bytes | round(b/4) | floor(b/4) | Data |
|---|---|---|---|---|
| P0 | 511 | 128 | 127 | 128 |
| P1.1.1 | 2227 | 557 | 556 | 557 |
| P1.2.2 | 3454 | 864 | 863 | 864 |
| P2.0.2 | 1723 | 431 | 430 | 431 |

T08 has unified the wording to `round(prompt_bytes / 4)` in both
`taxonomy_v1.md` and the taxonomy YAML. No data values were changed. The
difference never affects bucketing for any of the 9 records.

## CLI Usage

Single-prompt mode:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli extract-prompt-features `
  --prompt-path prompts/complete/P1.1.1_strict_first_draft.txt `
  --prompt-id local_p1_1_1_strict_first_draft
```

Batch mode (all text-ready records from corpus):

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli extract-prompt-features `
  --corpus-path data/interim/prompt_corpus/corpus_v1.jsonl `
  --output-path data/interim/prompt_corpus/extractor_output_v1.jsonl
```

## Relationship to T09

T09 self-audit must review:
1. Manual coding consistency (single-coder bias)
2. Whether the extractor disagreements documented above are acceptable
3. Whether low-variance fields should be deprioritized in statistical models
4. Whether the keyword heuristics are robust enough for future corpus expansion

The extractor does not replace T09. It provides a rule-ized baseline that T09
can compare against.
