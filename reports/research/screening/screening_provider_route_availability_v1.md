# Screening Provider Route Availability v1

Date: 2026-05-23
Task: T12b_run_screening_on_non_deepseek_provider
Purpose: Document which non-DeepSeek provider routes were assessed and whether any is locally usable for a Stage A screening rerun.

## Assessment Method

All locally accessible API routes were checked against three criteria:
1. An API key is present in `.env` or environment variables.
2. The required client library is installed.
3. The provider/model can produce parseable TRUE/FALSE output at the frozen `max_tokens=256` budget.

## Route Assessment Table

| Provider | Model | API Key Available? | Library Available? | Previously Tested? | Usable? |
|---|---|---|---|---|---|
| MiniMax | MiniMax-M2.7 | Yes (MINIMAX_API_KEY) | No (`openai` not installed) | Yes (T12 prep) | **No** — returns empty output on all 64 problems per prompt; user confirmed "minimax不可用" |
| ZhipuAI | glm-4.7-flash | **Yes** (ZHIPU_API_KEY in .env) | **Yes** (`zai-sdk` installed in gemini_api conda env) | **Yes (T12b execution)** | **Yes** — fully usable with thinking disabled; 64/64 parse rate across all prompts; 8/9 candidates survive elimination |
| Google | gemini-3-flash-preview | **No** (no GOOGLE_API_KEY or equivalent) | No (`google-genai` not installed) | No | **No** — no credentials configured; free tier but rate-limited |

## Details

### MiniMax (MiniMax-M2.7)

- API key `MINIMAP_API_KEY` exists in `.env` with base URL `https://api.minimaxi.com/v1`.
- Provider was tested during T12 preparation: all 64 problems per prompt returned empty strings, yielding `parse_success_rate` between 0.00 and 0.016.
- The model cannot produce parseable output at `max_tokens=256` for the equational-theories task.
- The `openai` Python package is not installed, but the API is OpenAI-compatible and could be called via `urllib` — however the empty-output behavior is a model-level limitation, not a library-availability issue.
- User explicitly confirmed "minimax不可用" (MiniMax is not usable).

### ZhipuAI (glm-4.7-flash)

- **Status: USABLE — successfully tested in T12b execution.**
- API key `ZHIPU_API_KEY` present in `.env` (variable name: `ZHIPU_API_KEY`).
- `zai-sdk` package installed in `gemini_api` conda environment.
- Model requires `thinking={"type": "disabled"}` at the frozen `max_tokens=256` budget (same pattern as DeepSeek v4-flash), otherwise all tokens consumed by reasoning.
- With thinking disabled: 100% parse rate on all 9 prompts. 8/9 candidates survive E1-E4 elimination.
- Screening completed: 9/9 runs, 0 API failures, ~53 minutes total wall time.
- This is the only tested non-DeepSeek route that produces usable output.

### Google (gemini-3-flash-preview)

- No GOOGLE_API_KEY found in `.env` or environment variables.
- The `google-genai` Python package is installed in the `gemini_api` conda environment but no API key is available.
- Free tier exists but is rate-limited. Network/VPN constraints also apply.
- Not tested. Would need API key before use.

## Conclusion

**One genuinely non-DeepSeek provider route is locally usable: ZhipuAI (glm-4.7-flash, thinking disabled).** Full screening rerun completed successfully with 8/9 candidates surviving elimination. The cross-provider evidence gap (R27) is now resolved.

ZhipuAI is the only locally tested non-DeepSeek route that produces usable output:
- MiniMax: tested, empty output (unusable)
- ZhipuAI: tested, works with thinking disabled
- Google: not tested (no API key, VPN constraints)

## Implication for Captain Decision

The cross-provider evidence gap noted in R27 is now **resolved**. Captain can proceed with the following options:

1. ✅ **Test a non-DeepSeek provider** — **Done.** ZhipuAI glm-4.7-flash works and produces 8 survivors.
2. ❌ **Relax E3 all-false collapse threshold** — **No longer needed.** E3 passes correctly on ZhipuAI.
3. ❓ **Expand screening dataset** — Optional, not required for shortlist.
4. ❓ **Accept all-false collapse as finding** — Partially: the finding is now provider-specific (DeepSeek collapses, ZhipuAI does not).
5. **→ Proceed to shortlist formation** — Now possible with 8 candidates on ZhipuAI.
