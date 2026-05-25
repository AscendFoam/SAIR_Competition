# Screening Third Route Execution Manifest v1

Date: 2026-05-23
Task: T12b_run_screening_on_non_deepseek_provider
Status: Execution complete. 9/9 runs completed. 0 API failures. 8 surviving candidates.

## Execution Config

| Field | Value |
|---|---|
| provider_route | `zhipuai` (ZhipuAI API via zai-sdk) |
| model | `glm-4.7-flash` |
| thinking_mode | `disabled` (required; glm-4.7-flash defaults to reasoning mode which consumes all max_tokens in reasoning_tokens, leaving no content output) |
| temperature | 0 |
| max_tokens | 256 |
| dataset | `data/interim/splits/smoke.jsonl` (64 problems: 31 true, 33 false) |
| repeats | 1 |
| total runs | 9 |
| completed runs | 9 |
| failed runs | 0 |

### Note on thinking_disabled

glm-4.7-flash is a reasoning-capable model that defaults to producing `reasoning_tokens` within the `max_tokens` budget. With `max_tokens=256`, all 256 tokens are consumed by reasoning, leaving the `content` field empty. Setting `thinking={"type": "disabled"}` disables reasoning mode, allowing the model to produce content-only output within the same `max_tokens=256` budget. This is an execution-level parameter to make the third-route model compatible with the frozen T10 config, not a design change to the screening protocol.

## Run Directory Layout

```
artifacts/research_runs/screening_third_route/
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
├── screening_third_route_results.json
└── _run_screening_third_route.py (temporary execution script)
```

## Per-Run Results

| # | prompt_id | Completed | Problems | Parsed | Parse rate | Accuracy | True recall | False recall | SHA256 match | Elapsed (s) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `local_p0_official_reconstructed_empty` | Yes | 64 | 64 | 1.0000 | 0.516 | 0.129 | 0.879 | Yes | 1194.2 |
| 2 | `local_p1_1_1_strict_first_draft` | Yes | 64 | 64 | 1.0000 | 0.516 | 0.000 | 1.000 | Yes | 100.9 |
| 3 | `local_p1_2_2_implicit_guardrail_v1` | Yes | 64 | 64 | 1.0000 | 0.594 | 0.548 | 0.636 | Yes | 174.6 |
| 4 | `local_p1_2_3_implicit_guardrail_v2` | Yes | 64 | 64 | 1.0000 | 0.547 | 0.581 | 0.515 | Yes | 197.6 |
| 5 | `local_p1_2_5_minimal_rule_missing_hard_composition` | Yes | 64 | 64 | 1.0000 | 0.562 | 0.710 | 0.424 | Yes | 111.3 |
| 6 | `local_p1_2_8_narrow_singleton_families` | Yes | 64 | 64 | 1.0000 | 0.562 | 0.645 | 0.485 | Yes | 83.2 |
| 7 | `local_p2_0_0_official_balanced_strict_v0` | Yes | 64 | 64 | 1.0000 | 0.594 | 0.839 | 0.364 | Yes | 265.2 |
| 8 | `local_p2_0_1_official_counterexample_first_strict_v0` | Yes | 64 | 64 | 1.0000 | 0.672 | 0.710 | 0.636 | Yes | 726.5 |
| 9 | `local_p2_0_2_official_fast_filters_strict_v0` | Yes | 64 | 64 | 1.0000 | 0.594 | 0.645 | 0.545 | Yes | 303.4 |

## Artifact Verification

All 9 run directories contain all 4 required artifacts:
- `run_config.json`: present in all 9 directories
- `summary.json`: present in all 9 directories
- `predictions.jsonl`: present in all 9 directories (64 rows each)
- `prompt_hash_manifest.json`: present in all 9 directories, `sha256_match = true` for all

## Shortlist Rules Application (E1-E4)

### E1: Parse failure (parse_success_rate < 0.95)

- All 9 prompts achieve parse_success_rate = 1.0.
- **No candidate triggers E1.** (Notable contrast with DeepSeek: P0 previously collapsed at 0.23-0.27)

### E2: All-true collapse (true_recall >= 0.95 AND false_recall <= 0.10)

- No candidate triggers E2.

### E3: All-false collapse (false_recall >= 0.95 AND true_recall <= 0.10)

- **P1.1.1**: false_recall = 1.000, true_recall = 0.000 → **ELIMINATED**
- All other 7 strict-format prompts have false_recall between 0.364 and 0.636 and true_recall between 0.548 and 0.839 → **PASS E3**
- P0 (relaxed format): false_recall = 0.879, true_recall = 0.129 → **PASS E3** (both metrics below collapse thresholds)

### E4: Non-reproducible execution

- All 9 runs completed and produced all artifacts. SHA256 matches confirmed for all.
- No candidate triggers E4.

### Elimination summary

- Eliminated by E1: 0
- Eliminated by E3: 1 (P1.1.1)
- **Surviving candidates: 8**

### Key finding

The all-false collapse observed on DeepSeek models (T11, T12) is **provider-specific, not protocol-wide**. On ZhipuAI glm-4.7-flash, the screening protocol produces 8 surviving candidates, including all 7 surviving strict-format prompts plus P0 (which now achieves 100% parse rate).

## Execution Facts for T12b Summary

1. Provider: ZhipuAI API (`glm-4.7-flash` model, thinking disabled) via `zai-sdk`
2. Dataset: `data/interim/splits/smoke.jsonl` (64 problems: 31 true, 33 false)
3. All runs completed without API errors or retries
4. Total wall time: ~3157 seconds (~52.6 minutes) — notably slower than DeepSeek runs (~9 minutes)
5. The consolidated results are saved in `artifacts/research_runs/screening_third_route/screening_third_route_results.json`
