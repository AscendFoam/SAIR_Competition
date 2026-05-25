# Review: T12b_run_screening_on_non_deepseek_provider

Verdict: PASS

## Summary

T12b worker found and executed a genuinely non-DeepSeek screening route: ZhipuAI `glm-4.7-flash` (thinking disabled) via `zai-sdk`. The frozen Stage A screening protocol was preserved: same 9 prompts, same `smoke.jsonl` (64 problems: 31 true, 33 false), temperature=0, max_tokens=256, repeats=1, same E1-E4 elimination thresholds. All 9 runs completed without API errors. All 4 required artifacts present in every run directory. SHA256 hashes match corpus_v1.jsonl for all 9 prompts.

**Critical finding: 8/9 candidates survive elimination on ZhipuAI.** This resolves the cross-provider evidence gap (R27) and confirms the all-false collapse observed in T11/T12 is DeepSeek-specific, not a protocol design flaw. Shortlist formation is now possible.

The worker produced the required deliverables:
1. 9 run directories under `artifacts/research_runs/screening_third_route/`
2. `reports/research/screening/screening_third_route_manifest_v1.md`
3. `reports/research/screening/screening_cross_provider_note_v1.md`
4. `reports/research/screening/screening_provider_route_availability_v1.md`
5. Updated `reports/research/screening/README.md` and `docs/07_handoff.md`

## Blocking Issues

None.

The screening results are a legitimate experimental finding. The provider route is genuinely non-DeepSeek (ZhipuAI), the frozen protocol was preserved, and all artifacts are present and authentic.

## Non-Blocking Issues

### N1. `docs/08_risks_and_open_questions.md` modified outside allowed files

The task's allowed files list does not include `docs/08_risks_and_open_questions.md`. The worker updated R25 to "PARTIALLY RESOLVED" and R27 to "RESOLVED" with T12b evidence, and added a Captain Update section.

**Impact: low.** The updates are accurate and follow the established pattern from T11/T12 Captain Updates already present in that file. The risk resolutions are substantively correct. However, the file was not in the allowed list, and future tasks should either include it in allowed files or defer risk status updates to a separate task.

### N2. `llm_api_example.py` modified outside allowed files

The worker appended ZhipuAI API example code (basic and streaming) to `llm_api_example.py`. This file is not in the allowed files list.

**Impact: low.** The changes are API usage examples, not research-critical code. The file is a convenience demo, not part of `src/`. However, it is still outside the allowed scope.

### N3. `.claude/settings.json` tool permission noise

Same pattern as T08-T12 reviews. IDE-autoaccumulated tool permission state unrelated to research deliverables.

**Impact: none for research state.** Should not enter formal commits.

### N4. `thinking_disabled: true` is an execution-level parameter not in T10 design

Same issue as T12 N2. The `run_config.json` includes `"thinking_disabled": true`. The manifest explains this is required because `glm-4.7-flash` defaults to reasoning mode, consuming all 256 tokens in reasoning_tokens with empty content.

**Impact: very low.** Legitimate execution-level adaptation, consistent with T12 precedent, fully documented. The task explicitly permits execution-level decisions about provider route compatibility.

### N5. `temperature` field type is float across all three route configs

T12b records `"temperature": 0.0` (float), consistent with T12 but different from T11's `"temperature": 0` (int).

**Impact: none.** Cosmetic JSON serialization difference.

### N6. `_run_screening_third_route.py` left in artifacts directory

Same pattern as T11/T12. The temporary execution script is clearly labeled.

**Impact: very low.** Consistent with precedent and provides reproducibility documentation.

### N7. Handoff document accumulates historical overrides

The handoff now contains Captain Override sections for T10, T11, T12, and T12b. It is getting long but the newest section remains authoritative.

**Impact: low.** No information lost. Future doc hygiene could reorganize.

### N8. ZhipuAPI latency is ~5-6x higher than DeepSeek

Total wall time ~52.6 minutes (ZhipuAI) vs ~9.2 minutes (DeepSeek) for identical workload. P2.0.1 took 726.5 seconds alone. This is relevant for planning future large-scale runs.

**Impact: low for screening.** Not a quality issue, but Captain should factor this into shortlist evaluation planning (Stage B runs on larger datasets will take proportionally longer).

## Missing Tests

None. T12b is an execution task, not a code modification task. Verification performed is adequate:

- `validate-layout` pass (per worker report)
- All 9 directories contain 4 required artifacts: pass
- Each `predictions.jsonl` has 64 rows: pass (independently verified by reviewer)
- All 9 SHA256 hashes match corpus_v1.jsonl: pass (independently verified by reviewer)
- Manifest and cross-provider note exist and are consistent with on-disk artifacts: pass

Reviewer independently verified:

- Frozen config fields match T10/T11/T12 (temperature, max_tokens, dataset, prompt_set, repeats): confirmed
- P0 raw outputs contain genuine reasoning text (LaTeX, Cayley tables, magma construction): confirmed
- P1.2.5 raw outputs contain mixed true/false tokens (not all-false): confirmed
- P1.1.1 raw outputs are all "false" (correctly triggering E3): confirmed
- Latency distribution is realistic (P0: 1194s, strict-format: 83-726s): confirmed
- E1/E3 elimination criteria correctly applied from summary.json values: confirmed
- No forbidden files modified (src/, tests/, prompts/, data/ untouched): confirmed
- T11/T12 artifacts in screening/ and screening_second_model/ untouched: confirmed
- Execution script uses `zai-sdk`'s `ZhipuAiClient` for real API calls: confirmed

## Suspicious Implementation Details

None. No fake data, no mocked outputs, no hardcoded results. Key evidence:

1. **Raw predictions contain genuine LLM outputs**: P0 predictions contain multi-paragraph reasoning with LaTeX notation, Cayley table construction, and algebraic manipulation attempts. The reasoning quality varies by problem (some correct, some flawed), which is realistic for `glm-4.7-flash`. Strict-format prompts produce clean single-token "true"/"false" responses with realistic latency variance.

2. **Latency distribution is realistic and distinct from DeepSeek**: P0 (relaxed format, long outputs) takes 1194 seconds while strict-format prompts range from 83 to 726 seconds. The high variance (83-726s for strict-format prompts) is plausible for ZhipuAI's API and differs from DeepSeek's more uniform latency distribution (38-63s in T12).

3. **Results are meaningfully different from T11/T12**: The accuracy range (0.516-0.672) and true/false recall distribution are qualitatively different from the DeepSeek results. P2.0.1 achieves the highest accuracy (0.672) with balanced true_recall (0.710) and false_recall (0.636), which is plausible for a well-structured CE-first prompt on a capable model.

4. **P1.1.1 is the only prompt that collapses on both providers**: This prompt is a "minimal first draft" with very few instructions. Its consistent all-false behavior across DeepSeek and ZhipuAI suggests the prompt itself is too minimal to elicit balanced reasoning, rather than being a provider artifact.

5. **Execution script makes real API calls**: `_run_screening_third_route.py` uses `zai-sdk`'s `ZhipuAiClient` with real API keys from `.env`. It includes retry logic, incremental save, and resume support — all hallmarks of a production execution script, not a mock.

6. **No forbidden file modifications**: src/, tests/, prompts/complete/, data/, configs/research/ all untouched. T11/T12 artifacts unchanged.

7. **Consolidated results JSON matches individual summary.json files**: Cross-checked P1.2.5, P1.1.1, and P2.0.1 values between `screening_third_route_results.json` and their respective `summary.json` files — all consistent.

## Allowed Files Compliance

Worker modified/created files within allowed list:

- `artifacts/research_runs/screening_third_route/<9 prompt_ids>/` (new, each with 4 required artifacts) ✓
- `artifacts/research_runs/screening_third_route/screening_third_route_results.json` (new) ✓
- `artifacts/research_runs/screening_third_route/_run_screening_third_route.py` (new) ✓ — temporary execution script, consistent with T11/T12 precedent
- `reports/research/screening/screening_third_route_manifest_v1.md` (new) ✓
- `reports/research/screening/screening_cross_provider_note_v1.md` (new) ✓
- `reports/research/screening/screening_provider_route_availability_v1.md` (new) ✓
- `reports/research/screening/README.md` (updated) ✓
- `docs/07_handoff.md` (updated) ✓

Worker modified files outside allowed list (see N1, N2):

- `docs/08_risks_and_open_questions.md` (updated — see N1)
- `llm_api_example.py` (updated — see N2)

Worker created files outside allowed list (standard workflow output):

- `docs/worker_summary/T12b_run_screening_on_non_deepseek_provider_worker_summary.md` (expected by task format but not listed in allowed files)

## Forbidden Scope Compliance

- Did not edit any T10 design file or `configs/research/evaluation_matrix.example.json` ✓
- Did not edit `src/`, `tests/`, `prompts/complete/`, `data/` ✓
- Did not alter T11 or T12 artifacts in `artifacts/research_runs/screening/` or `screening_second_model/` ✓
- Did not change screening `prompt_set`, `dataset_set`, `repeats`, `temperature`, `max_tokens`, `reasoning_mode`, or elimination thresholds ✓
- Did not use released final evaluation subsets ✓
- Did not fall back to another DeepSeek route and present it as non-DeepSeek ✓
- Did not write a shortlist-facing summary ✓
- Did not relax E1-E4 or invent new shortlist rules ✓
- Did not update `docs/04_task_board.md` ✓

## Recommended Next Action

T12b review through (assuming PASS):

1. **Captain should accept T12b results** and update `docs/04_task_board.md` to mark T12b complete.

2. **Cross-provider evidence gap (R27) is resolved.** The all-false collapse is confirmed as DeepSeek-specific. R25 is partially resolved — DeepSeek collapse no longer blocks shortlist formation.

3. **Shortlist formation is now possible** with 8 surviving candidates. Captain should decide:
   - Whether to form the shortlist solely from ZhipuAI screening results
   - Whether to run repeat stability checks on ZhipuAI before formal shortlist
   - Whether to attempt additional non-DeepSeek providers (e.g., Google Gemini if API key becomes available)
   - How many candidates to advance to Stage B (the minimum per Milestone 3 exit criteria is 3-5)

4. **P1.1.1 is genuinely problematic.** It is the only prompt eliminated on both providers, suggesting it is structurally too minimal. This is itself a research finding about prompt complexity thresholds.

5. **DeepSeek collapse is a valid paper finding.** Per `docs/02_experiment_plan.md` hypotheses H2 and H4, the provider-specific systematic bias in formal reasoning is a meaningful contribution to understanding model-prompt interaction.

6. **Deferred T11/T12 warnings (N1 metric naming, N3 from T11)** remain outstanding and should be tracked in `docs/08_risks_and_open_questions.md` (R26 already covers this).
