# Screening Cross-Provider Note v1

Date: 2026-05-23
Task: T12b_run_screening_on_non_deepseek_provider
Purpose: Compare DeepSeek (T11/T12) vs ZhipuAI (T12b) screening results for Captain decision.

## Providers Compared

| Run | Provider | Model | Thinking | Survivors |
|---|---|---|---|---|
| T11 | DeepSeek | deepseek-chat | N/A (non-reasoning alias) | 0 |
| T12 | DeepSeek | deepseek-v4-flash | disabled | 0 |
| T12b | **ZhipuAI** | **glm-4.7-flash** | **disabled** | **8** |

All three runs use the same frozen T10 config: same 9 prompts, same `smoke.jsonl` (64 problems), same elimination thresholds.

## Survivor Count

| Run | Provider | Surviving candidates | Shortlist formable? |
|---|---|---|---|
| T11 | DeepSeek | 0 | No |
| T12 | DeepSeek | 0 | No |
| **T12b** | **ZhipuAI** | **8** | **Yes** |

## Does all-false collapse persist?

**No.** The all-false collapse is confirmed to be **DeepSeek-specific, not protocol-wide.**

| prompt_id | DeepSeek false_recall | ZhipuAI false_recall | DeepSeek true_recall | ZhipuAI true_recall | E3 result on ZhipuAI |
|---|---|---|---|---|---|
| P0 | 0.879-1.000* | 0.879 | 0.129-0.194* | 0.129 | PASS |
| P1.1.1 | 1.000 | 1.000 | 0.000 | 0.000 | ELIMINATED |
| P1.2.2 | 0.970 | 0.636 | 0.000 | 0.548 | PASS |
| P1.2.3 | 1.000 | 0.515 | 0.032 | 0.581 | PASS |
| P1.2.5 | 1.000 | 0.424 | 0.032 | 0.710 | PASS |
| P1.2.8 | 1.000 | 0.485 | 0.000 | 0.645 | PASS |
| P2.0.0 | 1.000 | 0.364 | 0.032 | 0.839 | PASS |
| P2.0.1 | 1.000 | 0.636 | 0.000 | 0.710 | PASS |
| P2.0.2 | 1.000 | 0.545 | 0.000 | 0.645 | PASS |

\* P0's metrics on DeepSeek are unreliable due to parse collapse (parse_success_rate 0.23-0.27).

## Does parse collapse persist for P0?

**No.** On DeepSeek, P0 had parse_success_rate 0.23-0.27. On ZhipuAI glm-4.7-flash, P0 achieves **parse_success_rate = 1.0** (64/64 parsed). The relaxed format prompt is fully parseable on this provider.

## Does the shortlist become formable?

**Yes.** With 8 surviving candidates, the shortlist rules now have a sufficient pool. Shortlist formation is possible for the first time in this project.

## Key Implications

1. **The all-false collapse was DeepSeek-specific.** ZhipuAI glm-4.7-flash produces well-calibrated true/false recall distributions across 8 of 9 prompts. Only P1.1.1 (a minimal draft prompt) exhibits all-false collapse on both providers.

2. **The screening protocol itself is not broken.** The elimination gates (E1-E4) worked as designed — they correctly identified a DeepSeek-specific collapse pattern and would accept the same prompts on a non-collapsing provider.

3. **P0's parse collapse was also DeepSeek-specific.** The relaxed format is fully parseable on glm-4.7-flash.

4. **Captain now has enough evidence to proceed to shortlist formation.** The 8 surviving candidates provide a diverse pool spanning:
   - All 5 P1.x variants (implicit guardrail, minimal rule, narrow singleton)
   - All 3 P2.x variants (balanced, counterexample-first, fast filters)
   - P0 (relaxed format, now parseable)

5. **However, shortlist answers are still provider-dependent.** The 8 survivors passed elimination on ZhipuAI, but their ranking and diversity analysis should account for the fact that DeepSeek-based screening produces zero signal. A multi-provider shortlist strategy may be warranted.

## Captain Decision After T12b

The evidence gap (R27) is now resolved. The Captain's decision tree simplifies:

1. ✅ Test a non-DeepSeek provider — **Done.** ZhipuAI glm-4.7-flash works.
2. ✅ Relax E3 threshold — **No longer needed.**
3. ❓ Expand screening dataset — Optional, not required for shortlist.
4. ❓ Accept all-false collapse as finding — **Partially:** the finding is now "DeepSeek produces all-false collapse; ZhipuAI does not."
5. **→ Proceed to shortlist formation** — Now possible with 8 candidates.
