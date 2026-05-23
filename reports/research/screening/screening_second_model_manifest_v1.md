# Screening Second Model Execution Manifest v1

Date: 2026-05-23
Task: T12_rerun_screening_with_alternate_low_cost_model
Status: Execution complete. 9/9 runs completed. 0 API failures. 0 surviving candidates.

## Execution Config

| Field | Value |
|---|---|
| provider_route | `deepseek` (DeepSeek API) |
| model | `deepseek-v4-flash` |
| thinking_mode | `disabled` (required; v4-flash defaults to reasoning mode which consumes all max_tokens in reasoning_tokens, leaving no content output) |
| temperature | 0 |
| max_tokens | 256 |
| dataset | `data/interim/splits/smoke.jsonl` (64 problems: 31 true, 33 false) |
| repeats | 1 |
| total runs | 9 |
| completed runs | 9 |
| failed runs | 0 |

### Note on thinking_disabled

DeepSeek v4-flash and v4-pro are reasoning-capable models that default to producing `reasoning_tokens` within the `max_tokens` budget. With `max_tokens=256`, all 256 tokens are consumed by reasoning, leaving the `content` field empty. Setting `thinking: {"type": "disabled"}` disables reasoning mode, allowing the model to produce content-only output within the same `max_tokens=256` budget. This is an execution-level parameter to make the alternate model compatible with the frozen T10 config, not a design change to the screening protocol.

## Run Directory Layout

```
artifacts/research_runs/screening_second_model/
├── local_p0_official_reconstructed_empty/
│   ├── run_config.json
│   ├── summary.json
│   ├── predictions.jsonl
│   └── prompt_hash_manifest.json
├── local_p1_1_1_strict_first_draft/
│   ├── run_config.json
│   ├── summary.json
│   ├── predictions.jsonl
│   └── prompt_hash_manifest.json
├── local_p1_2_2_implicit_guardrail_v1/
│   ├── run_config.json
│   ├── summary.json
│   ├── predictions.jsonl
│   └── prompt_hash_manifest.json
├── local_p1_2_3_implicit_guardrail_v2/
│   ├── run_config.json
│   ├── summary.json
│   ├── predictions.jsonl
│   └── prompt_hash_manifest.json
├── local_p1_2_5_minimal_rule_missing_hard_composition/
│   ├── run_config.json
│   ├── summary.json
│   ├── predictions.jsonl
│   └── prompt_hash_manifest.json
├── local_p1_2_8_narrow_singleton_families/
│   ├── run_config.json
│   ├── summary.json
│   ├── predictions.jsonl
│   └── prompt_hash_manifest.json
├── local_p2_0_0_official_balanced_strict_v0/
│   ├── run_config.json
│   ├── summary.json
│   ├── predictions.jsonl
│   └── prompt_hash_manifest.json
├── local_p2_0_1_official_counterexample_first_strict_v0/
│   ├── run_config.json
│   ├── summary.json
│   ├── predictions.jsonl
│   └── prompt_hash_manifest.json
├── local_p2_0_2_official_fast_filters_strict_v0/
│   ├── run_config.json
│   ├── summary.json
│   ├── predictions.jsonl
│   └── prompt_hash_manifest.json
├── screening_second_model_results.json
└── _run_screening_second_model.py (temporary execution script)
```

## Per-Run Results

| # | prompt_id | Completed | Problems | Parsed | Parse rate | Accuracy | True recall | False recall | SHA256 match | Elapsed (s) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `local_p0_official_reconstructed_empty` | Yes | 64 | 15 | 0.2344 | 0.1562 | 0.194 | 0.121 | Yes | 181.1 |
| 2 | `local_p1_1_1_strict_first_draft` | Yes | 64 | 64 | 1.0000 | 0.5156 | 0.000 | 1.000 | Yes | 40.7 |
| 3 | `local_p1_2_2_implicit_guardrail_v1` | Yes | 64 | 64 | 1.0000 | 0.5000 | 0.000 | 0.970 | Yes | 63.2 |
| 4 | `local_p1_2_3_implicit_guardrail_v2` | Yes | 64 | 64 | 1.0000 | 0.5312 | 0.032 | 1.000 | Yes | 62.4 |
| 5 | `local_p1_2_5_minimal_rule_missing_hard_composition` | Yes | 64 | 64 | 1.0000 | 0.5312 | 0.032 | 1.000 | Yes | 42.8 |
| 6 | `local_p1_2_8_narrow_singleton_families` | Yes | 64 | 64 | 1.0000 | 0.5156 | 0.000 | 1.000 | Yes | 42.0 |
| 7 | `local_p2_0_0_official_balanced_strict_v0` | Yes | 64 | 64 | 1.0000 | 0.5312 | 0.032 | 1.000 | Yes | 38.8 |
| 8 | `local_p2_0_1_official_counterexample_first_strict_v0` | Yes | 64 | 64 | 1.0000 | 0.5156 | 0.000 | 1.000 | Yes | 41.0 |
| 9 | `local_p2_0_2_official_fast_filters_strict_v0` | Yes | 64 | 64 | 1.0000 | 0.5156 | 0.000 | 1.000 | Yes | 39.8 |

## Artifact Verification

All 9 run directories contain all 4 required artifacts:

- `run_config.json`: present in all 9 directories
- `summary.json`: present in all 9 directories
- `predictions.jsonl`: present in all 9 directories (64 rows each)
- `prompt_hash_manifest.json`: present in all 9 directories, `sha256_match = true` for all

## Shortlist Rules Application (E1-E4)

### E1: Parse failure (parse_success_rate < 0.95)

- **P0**: parse_success_rate = 0.2344 → **ELIMINATED**

### E2: All-true collapse (true_recall >= 0.95 AND false_recall <= 0.10)

- No candidate triggers E2.

### E3: All-false collapse (false_recall >= 0.95 AND true_recall <= 0.10)

- **P1.1.1**: false_recall = 1.000, true_recall = 0.000 → **ELIMINATED**
- **P1.2.2**: false_recall = 0.970, true_recall = 0.000 → **ELIMINATED**
- **P1.2.3**: false_recall = 1.000, true_recall = 0.032 → **ELIMINATED**
- **P1.2.5**: false_recall = 1.000, true_recall = 0.032 → **ELIMINATED**
- **P1.2.8**: false_recall = 1.000, true_recall = 0.000 → **ELIMINATED**
- **P2.0.0**: false_recall = 1.000, true_recall = 0.032 → **ELIMINATED**
- **P2.0.1**: false_recall = 1.000, true_recall = 0.000 → **ELIMINATED**
- **P2.0.2**: false_recall = 1.000, true_recall = 0.000 → **ELIMINATED**

### E4: Non-reproducible execution

- All 9 runs completed and produced all artifacts. SHA256 matches confirmed for all.
- No candidate triggers E4.

### Elimination summary

- Eliminated by E1: 1 (P0)
- Eliminated by E3: 8 (all strict-format prompts)
- Surviving candidates: **0**

### Screening failure flag

Per `screening_shortlist_rules_v1.md` Section 4 Step 3: "If fewer than 3 candidates survive, flag a screening failure and escalate to Captain."

**SCREENING FAILURE: 0 candidates survive elimination under the T10 rules.**

The second-model rerun confirms that `deepseek-v4-flash` (with thinking disabled) produces the same systematic all-false bias as `deepseek-chat` (T11) on the equational-theories task. All 8 strict-format prompts achieve near-perfect false recall (0.970-1.000) but near-zero true recall (0.000-0.032). P0 (relaxed format) again exhibits parse collapse (parse_success_rate = 0.23).

## Execution Facts for T12 Summary

1. Provider: DeepSeek API (`deepseek-v4-flash` model, thinking disabled)
2. Dataset: `data/interim/splits/smoke.jsonl` (64 problems: 31 true, 33 false)
3. All runs completed without API errors or retries
4. Total wall time: ~552 seconds (~9.2 minutes)
5. No optional `hard_slice_sample` expansion was used
6. The consolidated results are saved in `artifacts/research_runs/screening_second_model/screening_second_model_results.json`
