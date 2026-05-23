# T12 Review Explanation (For Human)

## 1. Task in Plain Language

T11 ran a "screening test" — like a first-round audition — on 9 different prompt candidates using the DeepSeek API's `deepseek-chat` model. The result was surprising: **every single candidate failed**. One prompt (P0) couldn't even produce parseable yes/no answers, and the other 8 all developed a pathological bias of answering "FALSE" to everything — getting nearly 100% of the false cases right but almost 0% of the true cases.

The big question was: **Is this a DeepSeek-specific problem, or do all models behave this way?** If only DeepSeek's model has this bias, we could just switch to another model and the screening might work. If it's universal, we need to rethink our entire approach.

T12's job was simple: re-run the exact same screening test with a *different model* to see if the same failure happens. If it does, the problem runs deeper than one model. If it doesn't, we know it's DeepSeek-specific and can proceed with the working model.

## 2. What the Implementation Did

### Goal

Re-run the frozen Stage A screening on all 9 text-ready local prompts using a different model than `deepseek-chat`, while keeping everything else identical (same dataset, same temperature, same token limit, same elimination rules).

### Task Flow

1. **Model selection**: The worker tried several alternative models:
   - `MiniMax-M2.7`: Produced empty outputs (0-1.6% parse rate) — unusable
   - `deepseek-reasoner`: All 256 tokens consumed by internal reasoning, leaving no visible answer — unusable
   - `deepseek-v4-flash` (thinking enabled): Same problem as deepseek-reasoner — unusable
   - `deepseek-v4-flash` (thinking **disabled**): Produces clean content-only outputs within the 256-token budget — **viable**

2. **Execution**: Ran all 9 prompts through `deepseek-v4-flash` (thinking disabled) on the same 64-problem smoke dataset. Each run produced 4 artifacts: run_config.json, summary.json, predictions.jsonl, prompt_hash_manifest.json.

3. **Results analysis**: Applied the same E1-E4 elimination rules. Result: 0 survivors, same as T11.

4. **Deliverables**: Wrote the second-model manifest and a comparison note documenting that the two models produce nearly identical results.

### Code/Config Changes

- **New artifacts**: 9 run directories under `artifacts/research_runs/screening_second_model/`, each containing real API call results
- **New execution script**: `_run_screening_second_model.py` — a temporary script that makes real HTTP calls to the DeepSeek API
- **New reports**: `screening_second_model_manifest_v1.md` (per-run results and elimination verdicts) and `screening_model_comparison_note_v1.md` (T11 vs T12 side-by-side)
- **Updated**: `reports/research/screening/README.md` and `docs/07_handoff.md` to reflect T12 completion

### Significance for Future Development

This task resolved a critical uncertainty from T11. We now know:

- **The all-false collapse is not a single-model fluke.** Two different DeepSeek model architectures (`deepseek-chat` and `deepseek-v4-flash`) produce *numerically identical* results. This strongly suggests the bias is provider-level, not model-specific.
- **The project cannot proceed to shortlist formation under current rules.** The screening failure is confirmed across two models, so no candidates can advance to Stage B (full evaluation) until Captain makes a decision.
- **The next critical decision point** is whether to test a non-DeepSeek provider (which would conclusively determine if the bias is universal) or to rethink the screening strategy entirely.

From the experiment plan perspective (`docs/02_experiment_plan.md`), this finding actually supports research hypotheses H2 and H4: "longer, more complex prompts don't necessarily perform better" and "public-split optimal prompts may show significant robustness gaps." The systematic FALSE bias across prompts of varying structure is itself a research finding about model-prompt interaction in formal reasoning domains.

## 3. Why This Review Result?

**Verdict: PASS**

The review verdict is PASS because:

1. **Task goal met**: The worker re-ran the frozen screening with an alternate model, produced all required artifacts, and honestly reported the zero-survivor outcome.

2. **No fake data**: I verified the raw prediction files contain real LLM outputs — P0's predictions contain multi-paragraph LaTeX reasoning that could only come from an actual API call, not a mock. P1.2.5 produces clean "false" single-token outputs consistent with the strict format.

3. **Protocol integrity maintained**: Temperature=0, max_tokens=256, same dataset, same 9 prompts, same elimination thresholds. The only permitted variable (model) was changed. An execution-level adaptation (`thinking_disabled`) was needed and is honestly documented.

4. **Forbidden scope respected**: No changes to src/, tests/, prompts/, data/, configs/, or task_board. T11 artifacts left untouched.

5. **Honest escalation**: The worker correctly stopped at the escalation boundary and did not attempt to write a shortlist, relax thresholds, or claim any candidates survived.

### Non-blocking concerns noted

- Both tested models are from the same DeepSeek provider, so we still don't know if non-DeepSeek models behave differently (N1)
- The `thinking_disabled` parameter is a necessary execution adaptation, not in the original T10 design but legitimately within T12's "execution-level decisions" scope (N2)
- Minor cosmetic issues: temperature field type (int vs float), execution script left in artifacts, settings.json noise (N3-N5)
- These are all low-impact and consistent with precedents from T11 review

## 4. Worker's Own Documentation Assessment

The worker wrote `docs/07_handoff.md` (updated), `screening_second_model_manifest_v1.md`, and `screening_model_comparison_note_v1.md`. Assessment:

- **Manifest is thorough and accurate**: Per-run results table, elimination rule application, artifact verification all match what I independently verified from the raw data. No discrepancies found.
- **Comparison note is honest and well-structured**: Correctly reports the near-identical results, correctly identifies the provider-level pattern hypothesis, correctly lists Captain's decision options.
- **Handoff update is clean**: Removes stale T10/T11 worker-scope sections that are no longer relevant, adds T12 execution facts, updates the "must read" list. No premature claims about shortlist or next task.
- **One minor gap**: The comparison note mentions MiniMax-M2.7 and deepseek-reasoner as "tested but failed" alternatives, but these exploratory attempts are not formally documented as artifacts. This is acceptable given the task only requires one alternate model's formal results, and the attempts are honestly reported.

No errors or misrepresentations found in the worker's documentation.
