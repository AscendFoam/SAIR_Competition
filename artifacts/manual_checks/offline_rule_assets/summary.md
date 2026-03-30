# Offline Rule Assets

- Tagged dataset: `artifacts\manual_checks\offline_rule_assets\tagged.jsonl`
- Error summary: `artifacts\manual_checks\offline_rule_assets\error.json`
- Output path: `artifacts\manual_checks\offline_rule_assets\assets.jsonl`
- Asset count: `2`

| Rule ID | Family | Support True | Support False | True Rate | Mainline Acc | Opportunity | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| OA_TRUE_SINGLETON_LHS_TO_BINARY | singleton_collapse | 2 | 0 | 1.0000 | 0.1000 | 1.8000 | candidate_offline |
| OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS | singleton_collapse | 1 | 0 | 1.0000 | 0.2000 | 0.8000 | needs_review |

## Recommendation

Prioritize the top offline assets with clean true support and low current mainline slice accuracy: OA_TRUE_SINGLETON_LHS_TO_BINARY(support_true=2, mainline_acc=0.1000), OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS(support_true=1, mainline_acc=0.2000). Keep them offline-first; do not promote wording into P1_2_3 without a dedicated smoke branch.

## Rule Details

### OA_TRUE_SINGLETON_LHS_TO_BINARY

- Family: `singleton_collapse`
- Trigger tags: `EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY`
- Rule type: `positive_collapse`
- Confidence: `medium`
- Support: true=2, false=0, true_rate=1.0000
- Current mainline slice accuracy: `0.1000`
- Current mainline slice true accuracy: `0.1000`
- Status: `candidate_offline`
- Prompt policy: `do_not_inherit_wording`
- Rule text: If Equation 1 has the narrow shape x = T with x absent from T and T is binary, treat this as a singleton-collapse family and record it as a safe offline TRUE asset.
- Notes: Core singleton-collapse entry point. Keep offline unless smoke proves wording stability.
- Support examples: `p1, p2`
- Failure examples: `none`
- Mainline error buckets: `RULE_MISSING=9`

### OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS

- Family: `singleton_collapse`
- Trigger tags: `EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS`
- Rule type: `positive_collapse`
- Confidence: `low`
- Support: true=1, false=0, true_rate=1.0000
- Current mainline slice accuracy: `0.2000`
- Current mainline slice true accuracy: `0.2000`
- Status: `needs_review`
- Prompt policy: `do_not_inherit_wording`
- Rule text: If singleton-collapse already fires and Equation 2 keeps the same left-hand-side skeleton, treat the case as a high-confidence TRUE family for offline use.
- Notes: Useful for same-left-hand-side true families mined from P1_2_5.
- Support examples: `p1`
- Failure examples: `none`
- Mainline error buckets: `RULE_MISSING=8`
