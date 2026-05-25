# T12b Review Explanation (For Human)

## 1. Task in Plain Language

T11 and T12 both ran screening tests on DeepSeek models — and both produced zero surviving prompts. Every single strict-format prompt developed an "all-false bias" (answering FALSE to everything), and the relaxed-format P0 couldn't even produce parseable answers. The big question hanging over the project was: **Is this a DeepSeek-specific problem, or do all AI models behave this way with our prompts?**

T12b's job was to find and test one genuinely non-DeepSeek AI provider to answer this question definitively. If the all-false collapse happens on every provider, the screening protocol itself is flawed. If it only happens on DeepSeek, the protocol is fine and we can proceed with a working provider.

The answer turned out to be the latter: **on ZhipuAI's glm-4.7-flash model, 8 out of 9 prompts pass the screening gates.** The all-false collapse is a DeepSeek-specific problem. The project can now form a shortlist and proceed to full evaluation.

## 2. What the Implementation Did

### Goal

Find one non-DeepSeek AI provider, run the exact same frozen screening test on the same 9 prompts with the same settings, and report whether the all-false collapse persists.

### Task Flow

1. **Provider availability check**: The worker checked three non-DeepSeek routes:
   - **MiniMax (MiniMax-M2.7)**: API key exists, but the model returns empty output at max_tokens=256 — unusable (confirmed earlier in T12 prep, user also confirmed "minimax不可用")
   - **ZhipuAI (glm-4.7-flash)**: API key in .env, `zai-sdk` installed in `gemini_api` conda env — **works** with thinking disabled
   - **Google (gemini-3-flash-preview)**: No API key configured, VPN constraints — not tested

2. **Execution**: Ran all 9 prompts through `glm-4.7-flash` (thinking disabled) on the same 64-problem smoke dataset. Each run produced 4 artifacts: run_config.json, summary.json, predictions.jsonl, prompt_hash_manifest.json. Total wall time: ~53 minutes (significantly slower than DeepSeek's ~9 minutes).

3. **Results analysis**: Applied the same E1-E4 elimination rules. Result: **8 survivors** (only P1.1.1 eliminated by E3 — it produces all-false on both providers, suggesting the prompt itself is genuinely too minimal).

4. **Deliverables**: Wrote the third-route manifest, cross-provider comparison note, and provider route availability assessment.

### Code/Config Changes

- **New artifacts**: 9 run directories under `artifacts/research_runs/screening_third_route/`, each containing real API call results
- **New execution script**: `_run_screening_third_route.py` — uses `zai-sdk`'s `ZhipuAiClient` for real HTTP calls
- **New reports**: `screening_third_route_manifest_v1.md` (per-run results), `screening_cross_provider_note_v1.md` (T11/T12/T12b three-way comparison), `screening_provider_route_availability_v1.md` (which non-DeepSeek routes exist and work)
- **Updated**: `reports/research/screening/README.md`, `docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`
- **Side effect**: `llm_api_example.py` was updated with ZhipuAI API examples (outside allowed files, flagged as non-blocking issue)

### Significance for Future Development

This task resolved the most critical uncertainty blocking the project. The consequences are:

1. **Milestone 3 is now unblocked.** The screening protocol works correctly on ZhipuAI. 8 candidates survive, which exceeds the Milestone 3 exit criteria of 3-5 shortlist candidates.

2. **The screening protocol itself is validated.** The E1-E4 gates correctly identified DeepSeek-specific collapse and would have accepted the same prompts on a non-collapsing provider. No protocol redesign is needed.

3. **DeepSeek collapse is a research finding.** Per the experiment plan (`docs/02_experiment_plan.md`), hypotheses H2 ("longer, more complex prompts don't necessarily perform better") and H4 ("public-split optimal prompts may show significant robustness gaps") are supported by this provider-level bias discovery. The paper can include this as a meaningful contribution about model-prompt interaction in formal reasoning domains.

4. **P1.1.1 is genuinely problematic.** It's the only prompt that produces all-false collapse on both DeepSeek and ZhipuAI. This suggests the prompt is structurally too minimal (it's a "strict first draft" with very few instructions), which is itself a finding about prompt complexity thresholds.

5. **Provider choice matters for future work.** ZhipuAI is ~5-6x slower than DeepSeek for the same workload (53 min vs 9 min). Stage B (full evaluation on larger datasets) will take proportionally longer. Captain should factor this into planning.

## 3. Why This Review Result?

**Verdict: PASS**

The review verdict is PASS because:

1. **Task goal met**: The worker found a genuinely non-DeepSeek provider (ZhipuAI), ran the frozen screening, produced all required artifacts, and honestly reported the 8-survivor outcome.

2. **No fake data**: I verified the raw prediction files contain real LLM outputs from `glm-4.7-flash`. P0's predictions contain multi-paragraph LaTeX reasoning with Cayley tables and magma construction attempts — clearly genuine model output. P1.2.5 produces mixed true/false tokens (not the all-false pattern from DeepSeek). P1.1.1 produces all-false (correctly triggering E3 on both providers).

3. **Protocol integrity maintained**: Temperature=0, max_tokens=256, same dataset, same 9 prompts, same elimination thresholds. Only the provider/model was changed (which is the entire point of T12b). The `thinking_disabled` parameter is a legitimate execution-level adaptation consistent with T12 precedent.

4. **Genuinely non-DeepSeek**: ZhipuAI is a completely different provider from DeepSeek, using a different API, different SDK (`zai-sdk`), and a different model architecture (`glm-4.7-flash`). This conclusively resolves the cross-provider evidence gap (R27).

5. **Forbidden scope respected**: No changes to src/, tests/, prompts/, data/, configs/, or task_board. T11/T12 artifacts untouched.

6. **Honest reporting**: The worker correctly reports that P1.1.1 still fails E3 (all-false on both providers), correctly identifies this as a prompt-level issue rather than provider-level, and does not attempt to claim all 9 candidates survive.

### Non-blocking concerns noted

- Two files were modified outside the allowed list: `docs/08_risks_and_open_questions.md` (R25/R27 status updates) and `llm_api_example.py` (ZhipuAI examples added). Both are low-impact and accurate, but technically outside scope (N1, N2).
- The `thinking_disabled` parameter and float temperature are execution-level cosmetic issues consistent with T12 precedent (N4, N5).
- Execution script and settings.json noise are consistent with T11/T12 precedent (N3, N6).
- ZhipuAI latency is 5-6x higher than DeepSeek, relevant for Stage B planning (N8).

## 4. Worker's Own Documentation Assessment

The worker wrote the required deliverables: `screening_third_route_manifest_v1.md`, `screening_cross_provider_note_v1.md`, `screening_provider_route_availability_v1.md`, and updated `docs/07_handoff.md` and `docs/08_risks_and_open_questions.md`. Assessment:

- **Manifest is thorough and accurate**: Per-run results table matches the summary.json files I independently verified. Elimination rule application is correct. The key finding (8 survivors, P1.1.1 only E3 elimination) is prominently documented.

- **Cross-provider note is well-structured**: The three-way comparison table (T11/T12/T12b) clearly shows the dramatic difference between DeepSeek and ZhipuAI. The implications section correctly identifies that the protocol is not broken and that shortlist formation is now possible.

- **Provider availability note is honest**: Correctly documents that MiniMax was tested but unusable, Google was not tested (no API key), and only ZhipuAI produced usable output. This transparency is important for Captain's judgment about evidence completeness.

- **Handoff update is comprehensive**: Updates all sections to reflect T12b results, correctly marks R27 as resolved, correctly identifies shortlist formation as the next step.

- **Risk document update is accurate**: R25 correctly updated to "PARTIALLY RESOLVED" (DeepSeek still collapses, but it no longer blocks Milestone 3). R27 correctly marked as "RESOLVED".

- **Minor gap**: The worker summary mentions attempting Google Gemini but does not document what specific step was taken to check for the API key (just says "no API key configured"). This is acceptable — the provider availability note covers this adequately.

No errors or misrepresentations found in the worker's documentation.
