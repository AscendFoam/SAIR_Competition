# Screening Shortlist Rules v1

Date: 2026-05-18
Task: T10_build_screening_evaluation_matrix
Companion: `screening_matrix_v1.md`, `screening_candidate_registry_v1.md`

## 1. Purpose

These rules govern how screening results are translated into a shortlist of 3-5 prompts for the recomputed benchmark (Stage B). They must be applied mechanically by T12 after all 9 screening runs complete.

## 2. Elimination Conditions

A candidate is **eliminated** from shortlist consideration if any of the following is true:

### E1: Parse failure

`parse_success_rate < 0.95`

Rationale: A prompt that fails to produce parseable verdicts on at least 95% of 64 smoke problems is not reliable enough for the full benchmark.

### E2: All-true collapse

`true_recall >= 0.95 AND false_recall <= 0.10`

Rationale: The prompt defaults to TRUE regardless of problem content. It does not engage with the reasoning task.

### E3: All-false collapse

`false_recall >= 0.95 AND true_recall <= 0.10`

Rationale: The prompt defaults to FALSE regardless of problem content. It does not engage with the reasoning task.

### E4: Non-reproducible execution

The screening run fails to produce all required artifacts (run_config.json, summary.json, predictions.jsonl, prompt_hash_manifest.json), or the prompt file hash does not match the expected SHA256 in corpus_v1.jsonl.

Rationale: A run that cannot be verified cannot enter the benchmark.

## 3. Inclusion Conditions

A candidate that passes all elimination checks is **eligible** for the shortlist. Eligibility does not guarantee inclusion.

To be **included** in the shortlist, a candidate must additionally:

### I1: Pass at least one structural uniqueness test

The candidate must be the sole representative of at least one structural characteristic among the remaining eligible candidates:

- Only candidate with `rule_or_heuristic_block = none` (P0)
- Only candidate with `opening_strategy = counterexample_first` (P2.0.1)
- Only candidate with `opening_strategy = balanced` (P2.0.0)
- Only candidate with `rule_or_heuristic_block = saturated` (P1.2.5)
- Only candidate with `verdict_contract = relaxed` (P0)

Or, if no uniqueness applies, the candidate must represent a distinct point on one of the following axes among remaining eligible candidates:

- Different `prompt_bytes_bucket` (short / medium / long)
- Different `rule_or_heuristic_block` level (none / compact / extended / saturated)
- Different `false_filter_orientation` (absent / low / medium / high)
- Different `proof_like_true_support` (absent / weak / medium / strong)

### I2: Represent a distinct structural type

The candidate must not be a near-duplicate of an already-included candidate. Two candidates are near-duplicates if they share all of:

- Same `prompt_bytes_bucket`
- Same `rule_or_heuristic_block`
- Same `opening_strategy`
- Same `false_filter_orientation`
- Same `proof_like_true_support`

## 4. Shortlist Assembly Procedure

### Step 1: Elimination

Apply E1-E4 to all 9 candidates. Remove eliminated candidates.

### Step 2: Structural anchors

From the remaining eligible candidates, identify structural anchors:

1. If P0 survives: include P0 as the baseline anchor.
2. If P2.0.0 survives: include P2.0.0 as the balanced-strategy anchor.
3. If P2.0.1 survives: include P2.0.1 as the CE-first-strategy anchor.
4. If P1.2.5 survives: include P1.2.5 as the rule-saturated anchor.

These 4 anchors are included if they pass elimination, because each represents a structural type with no other representative.

### Step 3: Fill remaining slots

If anchors cover fewer than 3 prompts, fill from the remaining eligible pool in this priority order:

1. **P1.2.3** (guardrail-heavy mainline, extended rules, long) — if it survives, it fills the "mature guardrail-heavy" slot.
2. **P2.0.2** (fast-filters, short, compact) — if it survives, it fills the "short compact strict" slot and provides a length contrast.
3. **P1.1.1** (early strict draft, medium, compact) — contrasts with P1.2.3/P1.2.5 on rule density.
4. **P1.2.2** (pre-mainline guardrail, medium, extended) — contrasts with P1.2.3 on guardrail strengthening.
5. **P1.2.8** (narrow singleton, long, extended) — contrasts with P1.2.2 on anti-bias content.

Priority rationale: candidates higher in the list cover structural axes not already covered by anchors.

### Step 4: Cap at 5

If more than 5 candidates survive elimination and pass inclusion checks, apply the structural coverage test (Section 5). Remove the lowest-priority candidate from Step 3 until the shortlist has 5 or fewer prompts.

If fewer than 3 candidates survive, flag a screening failure and escalate to Captain. The screening matrix may need revision.

## 5. Structural Coverage Test

The final shortlist must collectively satisfy at least 3 of 4 coverage criteria:

| Criterion | Requirement |
|---|---|
| Length diversity | At least one short, one medium, and one long prompt |
| Rule density | At least two different `rule_or_heuristic_block` levels |
| Opening strategy | At least two different `opening_strategy` values |
| Provenance diversity | At least one `local_contrast` and one `official_archetype` |

If the shortlist after Step 4 fails to meet 3 of 4 criteria, T12 must flag the gap in the screening report but may still proceed if at least 3 candidates survive elimination. The coverage test is a reporting requirement, not a blocking gate.

## 6. Collapse Handling

### All-true collapse

If a candidate exhibits all-true collapse (E2), it is eliminated regardless of accuracy. An all-true prompt may have high accuracy on balanced splits by chance, but it is not performing the intended task.

### All-false collapse

If a candidate exhibits all-false collapse (E3), it is eliminated regardless of accuracy. Same rationale as E2.

### Near-collapse warning

If a candidate has `parse_success_rate < 1.00` or `true_recall < 0.20` or `false_recall < 0.20` but does not trigger E1-E3, it receives a WARNING. The candidate remains eligible, but T12 must note the warning in the screening report.

Multiple warnings on the same candidate suggest the prompt is fragile and should be scrutinized during the recomputed benchmark.

## 7. Deduplication

If two or more surviving candidates are near-duplicates per I2, keep only one. The tiebreaker is:

1. Higher `parse_success_rate` wins.
2. If tied, higher `accuracy` wins.
3. If tied, the candidate with more taxonomy fields at distinct values from the rest of the shortlist wins.
4. If still tied, the earlier prompt_id in alphabetical order wins.

Rationale: near-duplicate prompts that perform identically provide no additional structural information. Keeping only one reduces benchmark cost without losing coverage.

## 8. Target Shortlist Size

Target: **3-5 prompts.**

- Minimum 3: needed to make any cross-prompt structural comparison.
- Maximum 5: cost control for the recomputed benchmark (Stage B uses 3+ splits x 2+ models x 1-3 repeats).
- If exactly 3 survive elimination, no further trimming is needed.
- If 4-5 survive, apply structural coverage test and report.
- If 6+ survive, apply Step 4 cap and document which candidates were dropped.

## 9. Special Cases

### P0 elimination

If P0 (minimal baseline) is eliminated by E1-E4, it is removed from the shortlist but must still be reported in the screening summary as a baseline failure. The absence of a baseline in the shortlist must be noted as a coverage gap.

### All Family C eliminated

If all 3 official archetype candidates (P2.0.0, P2.0.1, P2.0.2) are eliminated, the shortlist loses all `official_archetype` provenance representation. This must be flagged as a provenance diversity failure.

### All long prompts eliminated

If all 3 long-bucket candidates (P1.2.3, P1.2.8, P1.2.5) are eliminated, the shortlist has no long-prompt representation. Length-effect conclusions will be limited to short/medium prompts. This must be flagged.
