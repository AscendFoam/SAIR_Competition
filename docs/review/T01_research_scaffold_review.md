# T01_research_scaffold Review

Reviewer: Claude Code (normal review)
Date: 2026-05-12

## Verdict: PASS

## Summary

Worker has created all 18 scaffold files listed in the task's Allowed Files, plus the required `docs/07_handoff.md` update. No forbidden scope violations detected. All JSON/YAML files parse cleanly. All scaffold files correctly mark themselves as seed/planning state rather than completed work.

## Blocking issues

None.

## Non-blocking issues

1. **`evaluation_matrix.example.json` line 91: `repeats` field is a string `"1-3"` rather than a number.** The screening and post-release phases also use this string form. This is acceptable for an example/template file (it communicates a range), but the actual runner config schema should resolve this to an integer when the time comes. No action needed now.

2. **`corpus_sources.example.json` line 56: minor typo in `storage_policy`.** The value reads `"store_metadata_first_then check license before mirroring prompt text"` — there's a space instead of underscore before "check". Purely cosmetic in an example file.

3. **YAML taxonomy field naming inconsistency with experiment plan.** The experiment plan section 6.2 uses snake_case names like `has_magma_reset`, `has_trivial_magma_rule`, `has_false_filters`. The YAML uses higher-level grouped categories like `system_goal_framing`, `safety_or_guardrail_block`. This is a design choice rather than an error — the YAML is arguably cleaner for a seed scaffold — but future taxonomy coders should document the mapping from the original feature list in section 6.2 to the YAML field names, to avoid confusion.

4. **Taxonomy does not include `compression_style` or `ce_search_depth`.** The experiment plan section 6.2 lists `compression_style: natural_language / symbolic / hybrid` under length features and `ce_search_depth: implicit / shallow / explicit_multi_step` under counterexample strategy. The YAML uses `cheatsheet_density` instead of `compression_style` (close enough semantically) and omits `ce_search_depth` entirely. This is minor since the taxonomy is a seed and can be extended, but worth noting for Phase 2 manual coding.

5. **`docs/review/` and `docs/for_human/` directories did not exist.** This is not a worker issue — these are reviewer output directories. Created during this review session.

## Missing tests or verification

1. **Worker report does not include the PowerShell JSONL validation command.** The task spec requires running `Get-Content ... | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }`. The worker's report lists this as pass, but this review independently re-verified using Python (`json.loads` on each line) and confirmed all 3 lines parse correctly with `example_only: true`.

2. **`validate-layout` was re-verified during this review** and passes — the new directories do not break existing layout checks.

3. No automated tests are expected for this task (scaffold only), and the task correctly does not modify `src/` or `tests/`.

## Suspicious implementation details

None found. All files are clearly marked as scaffold/seed/example. No pseudo-data, no mock results, no forward-dated completion claims.

Specifically verified:
- `prompt_corpus_manifest.json`: `status: "seed_scaffold_not_collected"`, `corpus_size: 0`, `ready_prompt_count: 0` — honest.
- `raw_index.example.jsonl`: all 3 records have `example_only: true` — not pretending to be real corpus entries.
- `reports/paper/outline.md`: explicitly states "状态：planning scaffold，非结果定稿" and "Not-Yet-Supported Claims" section is present and honest.
- `reports/research/corpus_audit/summary.md`: corpus size listed as `0`, status as `seed scaffold only`.
- `docs/07_handoff.md`: updated to "待 reviewer 按 normal 类型审查", does not mark T01 as completed.

## Scope compliance

- Allowed files: All 18 paths in the Allowed Files list are present. No extra files outside the allowed scope.
- Forbidden scope: No changes to `src/`, `tests/`, `prompts/complete/`, `artifacts/`. No network access, no API eval, no downloaded data. `docs/04_task_board.md` is not modified. T01 is not marked as completed.
- `docs/07_handoff.md`: Updated within allowed scope, correctly records worker execution status without marking completion.

## Recommended next action

1. Captain marks T01 as complete in `docs/04_task_board.md`.
2. Proceed to T02 (Paper outline v0 and contribution list extraction) and/or T03 (Prompt corpus candidate register v0 and provenance rules). Note: the paper outline v0 has already been produced as part of T01; T02 may focus on refining it with contribution list extraction from the docx report.
3. When Phase 2 (taxonomy manual coding) begins, create a mapping document between the experiment plan section 6.2 feature names and the YAML field names.
4. Decide whether `data/external/*` and `data/interim/*` scaffold files need to be force-added to git if they are currently gitignored.
