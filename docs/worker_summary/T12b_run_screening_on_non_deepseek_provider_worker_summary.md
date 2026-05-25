# Worker Summary: T12b_run_screening_on_non_deepseek_provider

Task: T12b_run_screening_on_non_deepseek_provider
Changed files:
- `artifacts/research_runs/screening_third_route/` (9 run directories + consolidated results + temp execution script)
- `reports/research/screening/screening_third_route_manifest_v1.md` (新建)
- `reports/research/screening/screening_cross_provider_note_v1.md` (新建)
- `reports/research/screening/screening_provider_route_availability_v1.md` (更新 — 从"无可用路由"改为"ZhipuAI 可用"报告)
- `reports/research/screening/README.md` (更新状态和文件清单)
- `docs/07_handoff.md` (全面更新 T12b 结果)
- `docs/08_risks_and_open_questions.md` (R25/R27 更新为已解决/部分解决)
- `docs/worker_summary/T12b_run_screening_on_non_deepseek_provider_worker_summary.md` (本文件)

Execution summary:
- attempted_non_deepseek_routes: MiniMax (MiniMax-M2.7), ZhipuAI (glm-4.7-flash), Google (gemini-3-flash-preview)
- successful_provider_route: zhipuai (ZhipuAI API via zai-sdk)
- successful_model: glm-4.7-flash (thinking disabled)
- prompt count executed: 9
- completed runs: 9/9
- surviving candidates: 8 (only P1.1.1 eliminated by E3)
- no_route_available: false

Route assessment (final):
- MiniMax (MiniMax-M2.7): API key present, but returns empty output at max_tokens=256 (user confirmed "minimax不可用")
- **ZhipuAI (glm-4.7-flash)**: API key in .env, `zai-sdk` installed in `gemini_api` conda env. Works with `thinking={"type": "disabled"}`. 8/9 survivors. ✓
- Google (gemini-3-flash-preview): API key not configured; not tested due to VPN constraints

Key findings:
1. **All-false collapse was DeepSeek-specific.** On ZhipuAI glm-4.7-flash, 8/9 candidates pass E1-E4 elimination.
2. **P0 parse collapse was also DeepSeek-specific.** P0 achieves 100% parse rate on ZhipuAI (vs 23-27% on DeepSeek).
3. **Only P1.1.1 fails E3 across both providers**, suggesting it is genuinely too minimal rather than provider-biased.
4. **Screening protocol is not broken.** The protocol gates work correctly on a non-collapsing provider.
5. **Shortlist formation is now possible** with 8 candidates.
6. **ZhipuAI API is slower** (~53 minutes total) vs DeepSeek (~9 minutes) for the same 576-call workload.

Verification:
- command: `PYTHONPATH='src' python -m sair_competition.cli validate-layout`
  result: pass
- All 9 run directories have all 4 required artifacts with 64 rows each
- SHA256 matches confirmed for all 9 prompt_hash_manifest.json files
- E1-E4 elimination rules applied and documented in manifest

Risks / follow-up:
- ZhipuAI run used repeats=1; formal shortlist may want repeat stability check
- Shortlist strategy still needs Captain decision (e.g., which prompts, how many, ranking criteria)
- DeepSeek collapse remains a valid paper finding (provider-specific model bias)
- ZhipuAI API ~5-6x slower than DeepSeek for identical workload — factor for any future large-scale runs
