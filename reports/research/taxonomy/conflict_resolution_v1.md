# Conflict Resolution v1

Date: 2026-05-18
Task: T09_taxonomy_self_audit_and_conflict_resolution
Input: `self_audit_v1.md`, `extractor_v1_notes.md`, `prompt_features_v1.jsonl`, T07/T08 reviews

## Adjudication 1: P2.0.2 `counterexample_requirement`

### Dispute

- Manual coding (T07): `optional`
- Extractor output (T08): `absent`
- Reason: P2.0.2 prompt text contains no "counterexample" keyword. The manual coder assigned "optional" based on the "Fast FALSE filters" section and the "stay conservative" fallback, which implicitly encourage counterexample-like reasoning (searching for a magma that satisfies Eq1 but violates Eq2). The extractor cannot detect this without semantic analysis.

### Adjudication

**Authoritative value: `absent`**

Rationale:

1. P2.0.2's "Fast FALSE filters" are structural heuristics (new variables, extra symmetry), not counterexample search instructions. The prompt does not direct the model to *construct* or *search for* counterexamples.
2. The "stay conservative" fallback is an ambiguity-handling instruction, not a counterexample instruction. It tells the model to default conservatively when unresolved, not to actively search for counterexamples.
3. The taxonomy defines `counterexample_requirement` as "Strength of the counterexample search instruction." P2.0.2 has no such instruction. The manual coding conflated "has false-filter heuristics" with "encourages counterexample search."
4. The extractor's keyword-based heuristic correctly returns `absent` for prompts that lack explicit counterexample instructions.

### Action

Change `prompt_features_v1.jsonl` P2.0.2 record: `counterexample_requirement` from `optional` to `absent`.

Update the `coder_note` to document this adjudication.

---

## Adjudication 2: `rule_or_heuristic_block` `override` heuristic fragility

### Issue

The extractor distinguishes `saturated` from `extended` by checking for the "override" keyword (from P1.2.5's "do not let later guardrails override it"). This is a fragile, corpus-specific heuristic.

### Adjudication

**Accept the current heuristic as-is for T08 skeleton scope.**

Rationale:

1. The distinction is correct for all 9 current prompts (P1.2.5 = saturated, P1.2.2/P1.2.3/P1.2.8 = extended).
2. No prompt in the current corpus has an "override" clause without being saturated, nor a saturated prompt without an "override" clause.
3. The heuristic is clearly documented as fragile in `extractor_v1_notes.md` (lines 42-48).
4. Corpus expansion (adding external prompts) will require reassessment, but that is a future task, not a T09 blocker.
5. Manual coding remains authoritative. If the extractor misclassifies a future prompt, the manual override takes precedence.

### Action

No code change. Add a note to `extractor_v1_notes.md` confirming this adjudication.

---

## Adjudication 3: Low-variance field policy

### Issue

Several taxonomy fields have zero or near-zero variance across the 9 coded prompts. The question is whether to retain, deprioritize, or mark as descriptive-only.

### Classification

**Group A: Zero-variance fields (7 fields, single value)**

`system_goal_framing` (all true), `finite_model_search_hint` (all false), `identity_or_invariant_guidance` (all false), `examples_before_rules` (all false), `examples_block` (all none), `provenance_status` (all local_project), `post_release_relation` (all pre_release_design)

**Group B: Near-zero-variance fields (1 field)**

`ce_search_depth` (8 implicit, 1 shallow)

**Group C: Low-variance categorical fields (2 fields)**

`counterexample_requirement` (after adjudication: 8 absent, 1 encouraged), `builds_on_public_work` (6 none_declared, 3 official_only)

### Adjudication

**Policy: Retain in schema, exclude from statistical models, use as descriptive labels only.**

1. All 10 fields remain in `prompt_feature_taxonomy.yaml` and `prompt_features_v1.jsonl`. No fields are removed.
2. These fields must not be used as independent variables in regression models, correlation analyses, or paired tests for the current 9-prompt corpus.
3. These fields may be used for:
   - Descriptive tables (showing that all prompts share certain characteristics)
   - Hypothesis generation (e.g., "if future prompts include examples, does `examples_block` affect parse rate?")
   - Schema continuity with future corpus expansion
4. After corpus expansion adds external prompts, re-evaluate variance. Fields that gain sufficient variance (>= 3 distinct values, no single value > 80%) may be promoted to Group 4.1 in a future self-audit.

### Action

No data changes. Document this policy in `extractor_v1_notes.md` and `self_audit_v1.md`.

---

## Adjudication 4: Extractor stability vs manual alignment reporting boundary

### Issue

T08 tests verify "extractor behavior stability" (same output for same input) rather than "alignment with manual coding." The P2.0.2 test uses `absent` (extractor output) as the expected value, not `optional` (manual coding). How should reports distinguish these two types of claims?

### Adjudication

**Adopt explicit separation: extractor outputs report "extractor behavior"; manual coding reports "taxonomy truth."**

Reporting rules for T10/T19:

1. **Extractor output**: May be reported as "automated feature extraction result." State the extractor version (`T08_v1_skeleton`) and note that it covers only 7 of 26 feature fields.
2. **Manual coding**: Should be reported as "human-coded taxonomy." State the coder identity (`T07 manual coding, single coder`) and note the absence of inter-annotator agreement.
3. **When both exist for the same field**: Report the manual coding as authoritative, with the extractor agreement rate as a supporting quality metric.
4. **When only manual exists**: Report the manual coding directly, noting it is not extractor-verified.
5. **When neither is reliable**: Zero-variance fields (per Adjudication 3) should be reported as "constant across corpus; no discriminative power" rather than as feature values.

### Action

No code or data changes. Document this boundary in `extractor_v1_notes.md`.

---

## Adjudication 5: Minimal corrections to `prompt_features_v1.jsonl`

### Assessment

After reviewing all 9 records against the extractor output and the adjudication above, the following corrections are warranted:

### Correction 1: P2.0.2 `counterexample_requirement`

- Current: `optional`
- Corrected: `absent`
- Justification: Adjudication 1 above. The prompt has no counterexample search instruction.

### No other corrections

All other 8 records have:
- All rule-ized fields matching extractor output exactly
- All manual-only fields within allowed_values per taxonomy YAML
- No internal contradictions between `manual_coding_note` and coded values
- No violations of the T06 boundary gate

### Action

Apply Correction 1 to `prompt_features_v1.jsonl`. Update `coder_note` for the P2.0.2 record to reference this adjudication.

---

## Summary of Adjudications

| Issue | Decision | Data change? | Code change? |
|---|---|---|---|
| P2.0.2 `counterexample_requirement` | `optional` → `absent` | Yes (1 field, 1 record) | No |
| `rule_or_heuristic_block` heuristic | Accept as-is | No | No |
| Low-variance fields | Retain, exclude from models, descriptive-only | No | No |
| Extractor vs manual reporting boundary | Explicit separation in reports | No | No |
| Other `prompt_features_v1.jsonl` values | No corrections needed | No | No |

All adjudications are T09 worker decisions, subject to reviewer verification.
