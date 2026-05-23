# Review: T12_rerun_screening_with_alternate_low_cost_model

Verdict: PASS

## Summary

T12 worker re-ran the frozen Stage A screening on all 9 text-ready local prompts using `deepseek-v4-flash` (thinking disabled) via DeepSeek API. The screening protocol was kept frozen: same 9 prompts, same `smoke.jsonl` (64 problems), temperature=0, max_tokens=256, repeats=1, same E1-E4 elimination thresholds. All 9 runs completed without API errors. All 4 required artifacts present in every run directory. SHA256 hashes match corpus_v1.jsonl for all 9 prompts.

The screening failure from T11 is confirmed: 0 surviving candidates on the alternate model. P0 eliminated by E1 (parse_success_rate = 0.2344, comparable to T11's 0.2656). 8 strict-format prompts eliminated by E3 (all-false collapse with false_recall 0.970-1.000, true_recall 0.000-0.032, numerically near-identical to T11 values).

The worker produced the required deliverables:
1. 9 run directories under `artifacts/research_runs/screening_second_model/`
2. `reports/research/screening/screening_second_model_manifest_v1.md`
3. `reports/research/screening/screening_model_comparison_note_v1.md`
4. Updated `reports/research/screening/README.md` and `docs/07_handoff.md`

## Blocking Issues

None.

The confirmed screening failure across two models is a legitimate experimental finding, not a worker defect. The worker correctly kept the protocol frozen and honestly reported the zero-survivor outcome.

## Non-Blocking Issues

### N1. Both tested models are from the same provider (DeepSeek)

The task asked for "one alternate provider/model route." The worker chose `deepseek-v4-flash` which is a different model architecture from `deepseek-chat`, but both are served by the same DeepSeek API provider. The manifest and comparison note both honestly document this limitation. However, the near-identical results may reflect a provider-level pattern rather than a universal one.

**Impact: low.** The worker correctly identified this risk in the comparison note: "the all-false behavior may be a provider-level pattern specific to DeepSeek's training data or system prompt handling." The manifest documents the alternative models tested and failed (MiniMax-M2.7, deepseek-reasoner, deepseek-v4-flash with thinking). This is an execution constraint, not a design flaw — the worker had limited local API access.

### N2. `thinking_disabled: true` is an execution-level parameter not present in T10 design

The `run_config.json` includes `"thinking_disabled": true` which is absent from T10's frozen config. The manifest explains this is required because `deepseek-v4-flash` defaults to reasoning mode, consuming all 256 tokens in `reasoning_tokens` with empty `content`. Disabling thinking produces content-only output within the same budget.

**Impact: very low.** This is a legitimate execution-level adaptation to make the alternate model compatible with the frozen `max_tokens=256` constraint. The task package explicitly permits "execution-level decisions" about "which one alternate provider/model route is available." The adaptation is fully documented and does not change the screening protocol's design intent.

### N3. `temperature` field type differs between T11 and T12 configs

T11 `run_config.json` records `"temperature": 0` (integer), while T12 records `"temperature": 0.0` (float). This is a cosmetic difference in JSON serialization, not a behavioral change.

**Impact: none.** Both values are semantically identical.

### N4. `_run_screening_second_model.py` left in artifacts directory

Same pattern as T11. The temporary execution script is clearly labeled as such. Provides reproducibility documentation.

**Impact: very low.** Consistent with T11 precedent where N2 was accepted.

### N5. `.claude/settings.json` tool permission noise

Same as T08/T09/T10/T11 reviews. IDE-autoaccumulated tool permission state unrelated to research deliverables.

**Impact: none for research state.** Should not enter formal commits.

### N6. Handoff document accumulates historical overrides

The handoff now contains multiple Captain Override sections (T10, T11, T12). Some stale context is removed (e.g., old T10 worker scope, old reviewer focus section), which is appropriate cleanup. But the document is getting long and the section numbering has shifted (Section 7 "Reviewer focus" removed, Section 8 "Captain action" removed, Section 9 renumbered to Section 7).

**Impact: low.** The content is accurate and the cleanup removes stale information. Future doc hygiene could reorganize, but no information is lost.

## Missing Tests

None. T12 is an execution task, not a code modification task. Verification performed is adequate:

- `validate-layout` pass
- All 9 directories contain 4 required artifacts: pass
- Each `predictions.jsonl` has 64 rows: pass
- All 9 SHA256 hashes match corpus_v1.jsonl: pass
- Manifest and comparison note exist and are consistent with on-disk artifacts: pass

Reviewer independently verified:

- Frozen config fields match T11 (temperature, max_tokens, dataset, prompt_set, repeats): confirmed
- P0 raw outputs contain real reasoning text (LaTeX, magma counterexample attempts): confirmed
- P1.2.5 raw outputs are single-token "false": confirmed
- Latency distribution is realistic (P0: 181s, strict-format: 38-63s): confirmed
- E1/E3 elimination criteria correctly applied from manifest values: confirmed
- No forbidden files modified (src/, tests/, prompts/, configs/, data/ untouched): confirmed

## Suspicious Implementation Details

None. No fake data, no mocked outputs, no hardcoded results. Key evidence:

1. **Raw predictions contain genuine LLM outputs**: P0 predictions contain multi-paragraph reasoning text with LaTeX notation and magma construction attempts, clearly from `deepseek-v4-flash`. Strict-format prompts produce clean single-token "false" responses. Both output styles are realistic for their respective prompt formats.

2. **Latency distribution is realistic**: P0 (relaxed format, long outputs) takes 181 seconds while strict-format prompts (single-token output) take 38-63 seconds. This 3-5x ratio is consistent with output length differences.

3. **Numerical near-identity with T11 is explainable**: 8 of 9 prompts have *identical* true_recall and false_recall between T11 and T12 (P1.2.2 differs by 1 count). This could seem suspicious but is plausible given: (a) same provider, (b) same frozen protocol, (c) deterministic temperature=0, (d) the all-false behavior is clearly systematic rather than random.

4. **Execution script makes real API calls**: `_run_screening_second_model.py` uses `urllib.request` to call the DeepSeek `/chat/completions` endpoint with real API keys from `.env`. No stub, no mock, no cached responses.

5. **No forbidden file modifications**: src/, tests/, prompts/complete/, data/, configs/research/ all untouched. Only allowed files modified.

6. **Screening failure honestly reported**: Worker did not attempt to relax thresholds, suppress results, or fabricate a shortlist. The escalation to Captain is correct per shortlist rules.

## Allowed Files Compliance

Worker modified/created files within allowed list:

- `artifacts/research_runs/screening_second_model/<9 prompt_ids>/` (new, each with 4 required artifacts) ✓
- `artifacts/research_runs/screening_second_model/screening_second_model_results.json` (new) ✓
- `artifacts/research_runs/screening_second_model/_run_screening_second_model.py` (new) ✓ — temporary execution script, consistent with T11 precedent
- `reports/research/screening/screening_second_model_manifest_v1.md` (new) ✓
- `reports/research/screening/screening_model_comparison_note_v1.md` (new) ✓
- `reports/research/screening/README.md` (updated) ✓
- `docs/07_handoff.md` (updated) ✓

## Forbidden Scope Compliance

- Did not edit any T10 design file or `configs/research/evaluation_matrix.example.json` ✓
- Did not edit `src/`, `tests/`, `prompts/complete/`, `data/` ✓
- Did not alter T11 artifacts in `artifacts/research_runs/screening/` ✓
- Did not change screening `prompt_set`, `dataset_set`, `repeats`, `temperature`, `max_tokens`, `reasoning_mode`, or elimination thresholds ✓
- Did not use released final evaluation subsets ✓
- Did not write a shortlist-facing summary claiming a shortlist exists ✓
- Did not update `docs/04_task_board.md` ✓

## Recommended Next Action

T12 review through (assuming PASS):

1. **Captain must decide** whether to:
   - (a) Test a genuinely different provider (OpenAI, Google, etc.) to determine if all-false collapse is DeepSeek-specific or universal
   - (b) Relax E3 thresholds with documented rationale
   - (c) Accept all-false collapse as a research finding and redesign shortlist strategy around structural diversity rather than recall balance
   - (d) Redesign the screening protocol entirely

2. **Research value**: The cross-model consistency of the all-false finding (two different DeepSeek architectures producing numerically identical verdict distributions) is itself a meaningful research result. It suggests provider-level systematic bias in formal equational reasoning, which could contribute to paper claims about model-prompt interaction.

3. **No shortlist-facing work should proceed** until Captain resolves the screening failure. The worker correctly stopped at the escalation boundary.

4. **Deferred T11 warnings (N1, N3)** regarding metric naming drift between `summary.json` and screening-facing terminology remain outstanding and should be tracked in `docs/08_risks_and_open_questions.md`.
