# Review: T11_run_screening_on_selected_prompt_candidates

Verdict: PASS

## Summary

T11 worker executed the Stage A screening on all 9 text-ready local prompts using deepseek-chat via DeepSeek API, smoke split (64 problems), temperature=0, max_tokens=256, repeats=1. All 9 runs completed without API errors. All 4 required artifacts (run_config.json, summary.json, predictions.jsonl, prompt_hash_manifest.json) are present in every run directory. SHA256 hashes match corpus_v1.jsonl for all 9 prompts. Frozen config fields (temperature, max_tokens, repeats, prompt_set, dataset_set) are unmodified from T10 matrix values.

The screening results reveal a **screening failure**: all 9 candidates are eliminated by E1 or E3 gates. P0 (relaxed format) fails E1 parse collapse (parse_success_rate = 0.266). All 8 strict-format prompts fail E3 all-false collapse (false_recall 0.970-1.000, true_recall 0.000-0.032). Zero candidates survive elimination, so the shortlist cannot be formed per T10 shortlist rules Section 4 Step 3.

The worker correctly flagged this as a screening failure and escalated to Captain, without writing T12 shortlist conclusions or attempting to override the frozen elimination criteria.

## Blocking Issues

None.

The screening failure is not a worker defect—it is a legitimate experimental outcome. The worker correctly executed the frozen protocol, correctly applied the E1-E4 elimination rules, and correctly escalated when 0 candidates survived.

## Non-Blocking Issues

### N1. `summary.json` metric naming inconsistency with manifest

The `screening_execution_manifest_v1.md` uses `true_recall` / `false_recall` column headers, and `screening_results.json` uses `true_recall` / `false_recall` keys. These are mapped from `summary.json`'s `true_accuracy` / `false_accuracy`. The mapping is correct (true_accuracy = true_correct / true_total = true_recall), but the naming inconsistency between the source artifact and the consolidated report means any downstream consumer must know to translate. The manifest does document this implicitly via the "Per-Run Results" table column headers.

**Impact: low.** The values are correct; only the key names differ.

### N2. `_run_screening.py` left in artifacts directory

The temporary execution script `_run_screening.py` is present in `artifacts/research_runs/screening/`. It is clearly labeled as temporary and is not a required artifact per T10 matrix. However, its presence in the screening directory means it will be co-located with run artifacts unless cleaned up.

**Impact: very low.** The script is self-contained, does not import anything outside the project, and is clearly marked as temporary. It provides useful reproducibility documentation.

### N3. `summary.json` missing `true_recall` / `false_recall` keys

The `summary.json` files produced by `run_complete_prompt_eval` use `true_accuracy` and `false_accuracy` instead of `true_recall` and `false_recall` as defined in T10's `required_metrics`. The worker correctly computed the recall values in `screening_results.json` and the manifest by mapping `true_accuracy` → `true_recall`, `false_accuracy` → `false_recall`. But the raw artifacts don't match T10's metric naming exactly.

**Impact: low.** The values are semantically identical and correctly mapped. The naming gap is in the existing `run_complete_prompt_eval` output, not in the worker's screening logic. A future cleanup could add aliases.

### N4. `.claude/settings.json` tool permission noise

Same as T08/T09/T10 reviews. This is IDE-autoaccumulated tool permission state and is unrelated to T11's screening execution.

**Impact: none for research state.** Should not enter formal commits.

### N5. P0 elapsed time (263s) is 5-6x longer than other prompts

P0 takes ~263 seconds while all strict-format prompts take 40-65 seconds. This is likely because deepseek-chat generates long reasoning text for P0's relaxed format (47/64 responses are multi-paragraph and unparsed), consuming more output tokens. The worker did not flag this anomaly, but it is explainable by the format difference.

**Impact: very low.** The timing is real and consistent with the parse failure mode. Not an error.

## Missing Tests

None. T11 is an execution task, not a code modification task. The verification performed is adequate:

- `validate-layout` pass
- Artifact completeness check (9 dirs × 4 files) pass
- predictions.jsonl row count (64 each) pass
- SHA256 match (all 9) pass
- summary.json metrics present (all 9) pass

Reviewer independently verified:

- E1/E3 elimination criteria applied correctly (Python cross-check against raw data)
- P0 parse rate: 17 parsed / 47 unparsed from predictions.jsonl — confirmed
- P1.2.2 false_recall = 32/33 = 0.9697 from raw predictions — confirmed
- All 9 SHA256 hashes match across corpus_v1.jsonl, manifest files, and live recomputation — confirmed
- All 9 run_configs have temperature=0, max_tokens=256, repeats=1 — confirmed
- `_run_screening.py` writes only to artifacts directory — confirmed

## Suspicious Implementation Details

None. No fake data, no mocked outputs, no hardcoded results. Key evidence:

1. **Raw predictions contain real LLM outputs**: P0's predictions contain multi-paragraph reasoning text that clearly comes from deepseek-chat (LaTeX notation, magma counterexample attempts). P1.2.3's predictions are single-word "false" responses. These are genuine API outputs.

2. **Latency distribution is realistic**: strict-format prompts (single-token output) take 40-65 seconds; P0 (multi-paragraph output) takes 263 seconds. This is consistent with deepseek-chat's output behavior.

3. **Frozen config fields preserved**: temperature=0, max_tokens=256, reasoning_mode="default", repeats=1 across all 9 run_configs. Provider route is `deepseek` with model `deepseek-chat`. No deviations from T10 matrix.

4. **Screening failure honestly reported**: Worker did not attempt to relax thresholds, suppress results, or fabricate a shortlist. The escalation to Captain is correct per shortlist rules Section 4 Step 3.

5. **No forbidden file modifications**: src/, tests/, prompts/complete/, configs/, docs/04_task_board.md, data/ all untouched. Only allowed files modified: artifacts/research_runs/screening/, reports/research/screening/README.md, reports/research/screening/screening_execution_manifest_v1.md, docs/07_handoff.md.

6. **Manifest correctly documents E1-E4 application**: Each elimination is listed with the exact metric values and the triggered rule. E2 (all-true) is correctly noted as not triggered by any candidate. E4 is correctly noted as not triggered (all artifacts present, all SHA256 matches).

## Allowed Files Compliance

Worker modified/created files within allowed list:

- `artifacts/research_runs/screening/<9 prompt_ids>/` (new, each with 4 required artifacts) ✓
- `artifacts/research_runs/screening/screening_results.json` (new) ✓ — allowed as part of `artifacts/research_runs/screening/`
- `artifacts/research_runs/screening/_run_screening.py` (new) ✓ — temporary execution script, within artifacts directory
- `reports/research/screening/screening_execution_manifest_v1.md` (new) ✓
- `reports/research/screening/README.md` (updated) ✓
- `docs/07_handoff.md` (updated) ✓

## Forbidden Scope Compliance

- Did not edit `configs/research/evaluation_matrix.example.json` or any T10 design file ✓
- Did not edit `src/`, `tests/`, `prompts/complete/` ✓
- Did not run released-subset analysis or any Stage B / Stage C evaluation ✓
- Did not write the T12 screening summary ✓
- Did not change the candidate pool away from 9 text-ready local prompts ✓
- Did not change screening `prompt_set`, `dataset_set`, `repeats`, `temperature`, `max_tokens`, or `reasoning_mode` ✓
- Did not update `docs/04_task_board.md` ✓

## Recommended Next Action

T11 review through (assuming PASS):

1. **Captain must decide** on the screening failure before T12 can proceed. The core question is: `deepseek-chat` exhibits systematic all-false bias on this task — does this reflect a model limitation that invalidates the screening, or a genuine finding about prompt behavior on this model?

2. **Recommended Captain options** (in priority order):
   - **Option A: Switch screening model.** Re-run T11 with a different model (e.g., GPT-4o-mini, Qwen, or another provider). This is the cleanest path: keep the frozen protocol unchanged, only vary the model. The deepseek-chat results become a supplementary "model-specific bias" finding.
   - **Option B: Accept deepseek-chat as one data point and add a second model.** Keep the existing results, add a second screening run with a different model. This provides model-comparison data but doubles screening cost.
   - **Option C: Relax E3 thresholds.** Document rationale and loosen the all-false collapse gate. This is the least principled option and should only be considered if all tested models show similar bias patterns.

3. **Research value note**: The deepseek-chat all-false finding is itself a research result. If consistent across models (e.g., most models default to FALSE on equational reasoning), it suggests a systematic conservative bias in LLM formal reasoning — potentially paper contribution C3/C4 material.

4. **T12 should not start** until Captain resolves the screening model question.

5. **P0 parse failure is expected behavior**: The relaxed-format baseline produces multi-word responses that fail the strict TRUE/FALSE parser. This confirms the taxonomy prediction that `verdict_contract = relaxed` prompts have higher parse risk.
