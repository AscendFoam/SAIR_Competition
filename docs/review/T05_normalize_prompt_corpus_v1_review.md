# T05_normalize_prompt_corpus_v1 Review

Reviewer: Claude Code (normal review)
Date: 2026-05-13

## Verdict: PASS

## Summary

Worker produced `corpus_v1.jsonl` with 11 records normalized from candidate register v0, cleanly separating `text_ready` (9), `metadata_only` (1), and `structure_only` (1). The manifest now splits `eligible_count` (10) from `text_ready_count` (9), resolving the T04 review's non-blocking concern about ambiguous `direct_recompute_count`. Duplicate report and missing metadata report were generated as required. The `raw_index.example.jsonl` was aligned to the T04 schema. No external prompt text was mirrored. No forbidden scope violations. All local prompt hashes independently verified correct. All JSON/JSONL parses cleanly. `validate-layout` passes.

## Blocking issues

None.

## Non-blocking issues

1. **`candidate_register_v0.jsonl` is in the allowed files list but was not modified.** The task explicitly lists it as an allowed file, suggesting the worker could have updated it (e.g., to backfill `text_ready` or `eligible_for_recompute` fields for consistency). However, the task's Expected Output section does not explicitly require modifying it — only creating `corpus_v1.jsonl`. The register already contains correct provenance data from T04. Not modifying it is a reasonable conservative choice, but it means the register and corpus_v1 now have slightly different schemas (the register lacks `text_ready`, `eligible_for_recompute`, `corpus_inclusion_status`). Downstream tasks should treat `corpus_v1.jsonl` as the authoritative source.

2. **Missing metadata report flags 9 local records as `missing source_url` at severity `info`.** This is correct and well-documented — local records use `source_ref` and `prompt_text_path` as provenance anchors rather than external URLs. The policy_notes section explains this. However, the report could be slightly more concise by grouping identical records instead of repeating 9 nearly-identical entries. This is an aesthetic concern, not a correctness issue.

3. **`prompt_tokens_est` remains 0 for all 11 records.** The worker acknowledges this in the missing metadata report (`zero_token_estimate_count: 11`) and in handoff risks. This is acceptable for T05 since token estimation is not a blocking output. However, T07 (taxonomy coding) will likely need at least rough token estimates for length-bucket features. The audit summary correctly flags this under "Remaining Risks for T06."

4. **GitHub MIT source not mirrored in T05.** The worker explicitly chose not to mirror the external prompt text, keeping it metadata-only. This is a valid decision — the task says "GitHub MIT source may be imported only if the worker can preserve source URL, file path, license note, author/team, hash and attribution," which is permissive, not mandatory. The worker documented this choice clearly in manifest, audit, and handoff. If a future task mirrors the file, it should create the `raw_prompts/` directory and add the mirrored file with full provenance.

5. **`raw_index.example.jsonl` now has 3 example records instead of the original 2.** The added `example_paper_appendix_reference` is a useful addition since the schema supports `paper` as a source type. The example schema now uses the T04 field names (`source_id`, `prompt_text_storage`, `recommended_register_action`) instead of the old T03 fields (`prompt_id`, `prompt_sha256`, `builds_on_public_work`). This resolves the T04 review's non-blocking concern about schema misalignment.

6. **`raw_index.jsonl` had a minor notes field update only** — the GitHub record's notes were changed from "A later task may import..." to "T05 keeps this source metadata-only and does not mirror...". This is a clerical update reflecting T05's decision. No substantive data was altered.

## Missing tests or verification

1. **Worker verification commands independently re-confirmed:**
   - `validate-layout`: passes.
   - `prompt_corpus_manifest.json`: valid JSON. Contains `eligible_count`, `text_ready_count`, `mirrored_external_count` as separate fields.
   - `duplicate_report_v1.json`: valid JSON. Reports 0 duplicates by SHA256, source URL, candidate_id, and prompt_id.
   - `missing_metadata_report_v1.json`: valid JSON. 11 records, 9 policy-exempt (local records missing source_url), 2 actionable (external records missing hash/path).
   - `corpus_v1.jsonl`: 11 lines, all parse as valid JSON with all required fields.
   - `raw_index.jsonl`: 2 lines, both parse as valid JSON.
   - `raw_index.example.jsonl`: 3 lines, all parse as valid JSON.

2. **SHA256 hash verification independently confirmed.** All 9 text-ready records have hashes that match the actual files on disk. Hashes were recomputed from file contents and match exactly.

3. **Field consistency verified.** For all 9 text-ready records: `text_ready=true`, `eligible_for_recompute=true`, `corpus_inclusion_status=included_text_ready`, `prompt_sha256` is non-empty, `prompt_text_path` is non-empty. For the GitHub placeholder: `text_ready=false`, `eligible_for_recompute=true`, `corpus_inclusion_status=included_metadata_only`, `prompt_sha256=""`, `prompt_text_path=""`. For the contributor-network placeholder: `text_ready=false`, `eligible_for_recompute=false`, `corpus_inclusion_status=included_structure_only`, `prompt_sha256=""`, `prompt_text_path=""`. All consistent — no contradictions.

4. **Manifest counts verified.** `eligible_count=10` (9 local + 1 GitHub eligible), `text_ready_count=9` (local only), `mirrored_external_count=0`, `metadata_only_count=1`, `structure_only_count=1`, `excluded_count=0`. All match `corpus_v1.jsonl` contents.

5. **No automated tests expected** — this task does not modify `src/` or `tests/`.

## Suspicious implementation details

None found. Specifically verified:

- `prompt_corpus_manifest.json`: `status: "corpus_v1_normalized_not_taxonomy_coded"`, `corpus_size: 11`, `ready_prompt_count: 9` — honest progression from T04's `corpus_size: 0`.
- `corpus_v1.jsonl`: all records have the required schema fields. The two non-text-ready records correctly have `text_ready: false` with no fake hashes or paths.
- `duplicate_report_v1.json`: correctly reports 0 duplicates. The note about `prompt_id` matching `candidate_id` is a fair observation for future reruns.
- `missing_metadata_report_v1.json`: the 9 local records missing `source_url` are correctly flagged at `severity: info` with clear policy justification. The 2 external records are correctly flagged as `actionable`.
- `raw_index.example.jsonl`: schema now matches `raw_index.jsonl` (uses `source_id` not `prompt_id`, uses T04-mandated fields). Resolves T04 review non-blocking issue #4.
- `provenance_rules.md`: new "Corpus v1 Status Semantics" section clearly explains the distinction between `eligible_for_recompute` and `text_ready`. This directly addresses the T04 review's non-blocking issue #1.
- `reports/research/corpus_audit/summary.md`: honestly reports status, counts, duplicate summary, missing metadata, and remaining risks.
- `docs/07_handoff.md`: correctly records worker execution status, changed files, corpus summary, and reviewer focus. Does not mark T05 as completed.
- No changes to `src/`, `tests/`, `prompts/complete/`, `configs/research/`, `artifacts/`.
- No external prompt text copied.
- No API eval run.

## Scope compliance

- **Allowed files (9 changed)**: `data/external/prompt_corpus/raw_index.example.jsonl`, `data/external/prompt_corpus/raw_index.jsonl`, `data/interim/prompt_corpus/corpus_v1.jsonl` (new), `data/interim/prompt_corpus/duplicate_report_v1.json` (new), `data/interim/prompt_corpus/missing_metadata_report_v1.json` (new), `data/interim/prompt_corpus/prompt_corpus_manifest.json`, `data/interim/prompt_corpus/provenance_rules.md`, `reports/research/corpus_audit/summary.md`, `docs/07_handoff.md`. All within the allowed list. Note: `candidate_register_v0.jsonl` was allowed but not modified — acceptable.
- **Forbidden scope**: No changes to `src/`, `tests/`, `prompts/complete/`, `configs/research/`, `artifacts/`. No API eval. No released subset usage for prompt selection. No external prompt text copied. Contributor Network placeholder kept structure-only. Corpus not written as complete coverage. T05 not marked as completed.

## T04 non-blocking followups resolution

| T04 review non-blocking issue | T05 resolution |
|---|---|
| #1: `direct_recompute_count` blends eligibility with text-ready | **Resolved.** Manifest now has separate `eligible_count` (10) and `text_ready_count` (9). `provenance_rules.md` adds "Corpus v1 Status Semantics" section. |
| #4: `raw_index.example.jsonl` schema misalignment | **Resolved.** Example now uses T04 schema fields with 3 illustrative records. |
| #2, #3: fragile LinkedIn provenance, few external candidates | Not in T05 scope; acknowledged as remaining risk. |

## Recommended next action

1. Captain marks T05 as complete in `docs/04_task_board.md`.
2. T06 should restate corpus audit and public/private asset boundary against `corpus_v1`.
3. T07 (taxonomy) should backfill `prompt_tokens_est` before doing length-bucket analysis.
4. Consider a dedicated small task to mirror the MIT GitHub prompt file if external text-ready coverage becomes important for screening evaluation.
5. Continue seeking stable first-party URL for the contributor-network entry.
