# Screening Model Comparison Note v1

Date: 2026-05-23
Task: T12_rerun_screening_with_alternate_low_cost_model
Purpose: Compare T11 (deepseek-chat) vs T12 (deepseek-v4-flash) screening results for Captain decision.

## Models Compared

| Run | Model | Provider | API config |
|---|---|---|---|
| T11 | `deepseek-chat` | DeepSeek | temperature=0, max_tokens=256 |
| T12 | `deepseek-v4-flash` | DeepSeek | temperature=0, max_tokens=256, thinking=disabled |

Both use the same frozen T10 config: same 9 prompts, same `smoke.jsonl` (64 problems), same elimination thresholds.

## Survivor Count

| Model | Surviving candidates | Shortlist formable? |
|---|---|---|
| T11 deepseek-chat | 0 | No |
| T12 deepseek-v4-flash | 0 | No |

## Does all-false collapse persist?

**Yes.** All 8 strict-format prompts exhibit all-false collapse on both models:

| prompt_id | T11 false_recall | T12 false_recall | T11 true_recall | T12 true_recall |
|---|---|---|---|---|
| P1.1.1 | 1.000 | 1.000 | 0.000 | 0.000 |
| P1.2.2 | 0.970 | 0.970 | 0.000 | 0.000 |
| P1.2.3 | 1.000 | 1.000 | 0.032 | 0.032 |
| P1.2.5 | 1.000 | 1.000 | 0.032 | 0.032 |
| P1.2.8 | 1.000 | 1.000 | 0.000 | 0.000 |
| P2.0.0 | 1.000 | 1.000 | 0.032 | 0.032 |
| P2.0.1 | 1.000 | 1.000 | 0.000 | 0.000 |
| P2.0.2 | 1.000 | 1.000 | 0.000 | 0.000 |

The true_recall and false_recall values are **numerically identical** between T11 and T12 for 8 of 9 prompts (P1.2.2 differs by 1 false_correct out of 33). This is not a coincidence — it means both models produce nearly identical verdict distributions on this task.

## Does parse collapse persist for P0?

**Yes.** P0 (relaxed format) shows parse collapse on both models:

| Metric | T11 (deepseek-chat) | T12 (deepseek-v4-flash) |
|---|---|---|
| parse_success_rate | 0.2656 (17/64) | 0.2344 (15/64) |

Both models produce multi-word or non-TRUE/FALSE responses when the format is relaxed.

## Is the shortlist formable?

**No.** With 0 surviving candidates on both models, the shortlist cannot be formed under the current T10 elimination rules. Captain must decide next steps before any shortlist-facing summary can be written.

## Additional finding: model-level vs provider-level behavior

The near-identical results between `deepseek-chat` and `deepseek-v4-flash` (which use different model architectures) suggest the all-false behavior may be a provider-level pattern specific to DeepSeek's training data or system prompt handling for the equational-theories domain, rather than an artifact of a single model architecture. However, with only one provider tested, this cannot be confirmed.

Alternative provider routes tested during T12 preparation:
- **MiniMax-M2.7**: All 64 outputs per prompt returned empty strings (parse_success_rate = 0.00-0.016). The model appears unable to produce parseable content for this task at max_tokens=256.
- **deepseek-reasoner / deepseek-v4-flash (thinking enabled)**: All 256 max_tokens consumed by reasoning_tokens, leaving content field empty.

Only `deepseek-v4-flash` with `thinking=disabled` produced parseable output, confirming the all-false collapse is not a reasoning-mode artifact.

## Captain decision required

The screening protocol has now been executed on two different DeepSeek models with identical results: 0 survivors. Possible next steps:

1. **Test a non-DeepSeek provider** (e.g., OpenAI GPT-4o-mini, Google Gemini Flash) to determine if all-false collapse is DeepSeek-specific or universal for this task format.
2. **Relax E3 threshold** (e.g., raise true_recall floor from 0.10 to 0.05, or lower false_recall ceiling from 0.95 to 0.90) with documented rationale.
3. **Expand screening dataset** to include harder slices where all-false strategies perform worse.
4. **Accept all-false collapse as a finding** and proceed with a different shortlist strategy (e.g., select candidates based on parse stability and structural diversity rather than recall balance).
5. **Redesign screening protocol** entirely.
