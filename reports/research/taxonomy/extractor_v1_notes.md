# Extractor v1 Notes

Date: 2026-05-17 (updated 2026-05-18 by T09)
Task: T08_prompt_feature_extractor_skeleton
Module: `src/sair_competition/analysis/prompt_features.py`

## Scope Statement

This is a **skeleton** extractor, not full automation. Manual taxonomy coding
(`prompt_features_v1.jsonl`) remains the **authoritative reference**.  The
extractor produces structured feature records from prompt text files, but only
a subset of fields are rule-ized.  T09 self-audit has been completed.

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
| `counterexample_requirement` | "counterexample-first policy" / "falsification" / "counterexample" instruction keywords | 9/9 (after T09 adjudication) |
| `explicit_final_token` | "exactly one token" / "single token" patterns | Yes |

## Known Disagreements with Manual Coding

### ~~P2.0.2 counterexample_requirement~~ — Resolved by T09

- ~~Manual coding: `optional`~~ → T09 adjudication: `absent`
- Extractor output: `absent`
- The manual coding has been corrected to `absent` per T09 conflict resolution.
  P2.0.2 has no counterexample search instruction; the "stay conservative"
  fallback is an ambiguity-handling instruction, not a CE instruction.
- After T09 correction: extractor and manual coding now agree 9/9 on all
  rule-ized fields.

### P1.2.5 vs P1.2.8 rule_or_heuristic_block distinction

Both prompts contain "Singleton family A/B" rules, but only P1.2.5 is coded as
`saturated`. The extractor uses the presence of "override" (from P1.2.5's
"do not let later guardrails override it" clause) to distinguish `saturated`
from `extended`. This heuristic is specific to the current corpus and may need
revision if future prompts have different override patterns.

**T09 adjudication**: Accept as-is for skeleton scope. The distinction is
correct for all 9 current prompts. Manual coding remains authoritative if
future prompts reveal fragility. Documented in `conflict_resolution_v1.md`.

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

The following fields have zero or near-zero variance in the current 9-prompt
corpus and must not be used as independent variables in statistical models:

**Zero-variance (single value across all 9):**
- `system_goal_framing`: all true
- `finite_model_search_hint`: all false
- `identity_or_invariant_guidance`: all false
- `examples_before_rules`: all false
- `examples_block`: all none
- `provenance_status`: all local_project
- `post_release_relation`: all pre_release_design

**Near-zero-variance:**
- `ce_search_depth`: 8 implicit, 1 shallow
- `counterexample_requirement`: 8 absent, 1 encouraged (after T09 correction)
- `builds_on_public_work`: 6 none_declared, 3 official_only

**T09 policy**: Retain in schema and feature records. Exclude from regression
models and correlation analyses. May be used as descriptive labels and for
hypothesis generation. Re-evaluate after corpus expansion. See
`conflict_resolution_v1.md` Adjudication 3.

## Extractor vs Manual Reporting Boundary (T09)

**Rule**: Extractor outputs report "extractor behavior"; manual coding reports
"taxonomy truth." When both exist, manual coding is authoritative. When only
manual exists, report directly but note it is not extractor-verified. See
`conflict_resolution_v1.md` Adjudication 4.

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

T09 self-audit has been completed. Key outcomes:

1. Manual coding consistency: reviewed; single-coder bias acknowledged; mitigated by coder notes and extractor cross-check.
2. P2.0.2 disagreement: resolved; manual coding corrected to `absent`.
3. Low-variance fields: classified and excluded from statistical models.
4. Keyword heuristics: accepted for skeleton scope; reassess on corpus expansion.

The extractor now achieves 9/9 agreement with the corrected manual coding on
all 7 rule-ized fields. See `self_audit_v1.md` and `conflict_resolution_v1.md`.
