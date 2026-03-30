# Offline Rule Asset Audit

- Predictions: `artifacts\manual_checks\offline_rule_assets_verification\tagged_with_assets.jsonl`
- Rule assets: `artifacts\manual_checks\offline_rule_assets_verification\rule_assets.jsonl`
- Audited asset count: `3`

| Rule ID | Rows | Accuracy | True Acc | Recoverable Errors | True Miss | False Positive | Priority |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| OA_TRUE_SINGLETON_LHS_TO_BINARY | 2 | 0.0000 | 0.0000 | 2 | 2 | 0 | 6.1800 |
| OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS | 1 | 0.0000 | 0.0000 | 1 | 1 | 0 | 3.0800 |
| OA_TRUE_DISJOINT_VAR_BINARY | 1 | 1.0000 | 1.0000 | 0 | 0 | 0 | 0.0000 |

## Recommendation

Prioritize offline assets that still map to missed true slices on the current mainline: OA_TRUE_SINGLETON_LHS_TO_BINARY(recoverable=2, true_miss=2, priority=6.1800), OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS(recoverable=1, true_miss=1, priority=3.0800), OA_TRUE_DISJOINT_VAR_BINARY(recoverable=0, true_miss=0, priority=0.0000). Keep them offline-first and use them to drive tagging, slicing, or future implicit injection experiments.

## Asset Details

### OA_TRUE_SINGLETON_LHS_TO_BINARY

- Family: `singleton_collapse`
- Primary tag: `EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY`
- Trigger tags: `EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY`
- Status: `candidate_offline`
- Prompt policy: `do_not_inherit_wording`
- Rows: `2`
- Accuracy: `0.0000`
- True accuracy: `0.0000`
- False accuracy: `n/a`
- Recoverable errors: `2`
- True misses: `2`
- False positives: `0`
- Error buckets: `RULE_MISSING=2`
- Priority score: `6.1800`
- Bundle opportunity score: `1.8000`
- Sample matches: `p1, p2`
- True miss examples: `p1, p2`
- False positive examples: `none`

### OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS

- Family: `singleton_collapse`
- Primary tag: `EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS`
- Trigger tags: `EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS`
- Status: `needs_review`
- Prompt policy: `do_not_inherit_wording`
- Rows: `1`
- Accuracy: `0.0000`
- True accuracy: `0.0000`
- False accuracy: `n/a`
- Recoverable errors: `1`
- True misses: `1`
- False positives: `0`
- Error buckets: `RULE_MISSING=1`
- Priority score: `3.0800`
- Bundle opportunity score: `0.8000`
- Sample matches: `p1`
- True miss examples: `p1`
- False positive examples: `none`

### OA_TRUE_DISJOINT_VAR_BINARY

- Family: `disjoint_sides`
- Primary tag: `EQ1_DISJOINT_SIDES_VAR_BINARY`
- Trigger tags: `EQ1_DISJOINT_SIDES_VAR_BINARY`
- Status: `needs_review`
- Prompt policy: `do_not_inherit_wording`
- Rows: `1`
- Accuracy: `1.0000`
- True accuracy: `1.0000`
- False accuracy: `n/a`
- Recoverable errors: `0`
- True misses: `0`
- False positives: `0`
- Error buckets: `none`
- Priority score: `0.0000`
- Bundle opportunity score: `0.0000`
- Sample matches: `p3`
- True miss examples: `none`
- False positive examples: `none`
