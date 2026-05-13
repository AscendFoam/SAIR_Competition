# T04_external_prompt_source_collection Review

Reviewer: Claude Code (normal review)
Date: 2026-05-13

## Verdict: PASS

## Summary

Worker completed all five T04 required outputs: (1) git tracking via `.gitignore` narrow allowlist, (2) raw index with verified provenance for 2 external sources, (3) candidate register updates filling source URL/author/license for both public placeholders, (4) manifest and audit summary updates, (5) handoff update. All files are within the allowed list. No forbidden scope violations. No external prompt text was copied. Independent verification confirms all local prompt files exist with correct hashes, all JSON/JSONL parses cleanly, git tracking works (`git add --dry-run` succeeds), and `validate-layout` passes.

## Blocking issues

None.

## Non-blocking issues

1. **`direct_recompute_count=10` blends "eligibility" with "text-ready" semantics.** The GitHub placeholder has `recompute_eligibility: direct_recompute` but `storage_status: metadata_only` and no local text. The provenance_rules.md explains the nuance, and the worker's final report flags it, but downstream tasks or readers could reasonably expect `direct_recompute_count` to mean "text is available now." The manifest notes section partially addresses this, but a future task (T05) should consider splitting this into `eligible_count` vs `text_ready_count` or adding a clarifying field.

2. **Contributor network provenance is anchored to a LinkedIn post, not a stable first-party page.** The source URL `https://www.linkedin.com/posts/sairfoundation_...` is a social media post by SAIR, not the Contributor Network itself. The worker correctly treats this as host-level provenance only, and keeps the entry `structure_only`. However, LinkedIn posts can be deleted or edited, making this a fragile provenance anchor. T05+ should look for a more stable first-party URL (e.g., SAIR official site or competition platform page) if one becomes available.

3. **No second GitHub/paper external candidate was added beyond the existing placeholders.** The task scope focused on verifying existing placeholders, and the raw_index correctly records both. However, the experiment plan (section 5.1 Tier 2) envisions collecting multiple GitHub repos and paper-described prompts. T04 appropriately limits itself to the two T03 placeholders. Future tasks (T05/T06) should actively seek additional external candidates to reach the 8-12 analyzable prompt target.

4. **`raw_index.example.jsonl` was not updated to match the new `raw_index.jsonl` schema.** The example file uses the old T03 corpus schema (with `prompt_id`, `prompt_sha256`, `builds_on_public_work`, etc.) while the actual `raw_index.jsonl` uses the T04-mandated schema (with `source_id`, `prompt_text_storage`, `recommended_register_action`). The example and the real file serve different purposes (schema illustration vs real data), so this is acceptable for T04 but could confuse future readers. T05 could align the example.

5. **`provenance_rules.md` last paragraph still references "T04-T06" for future work.** This is a minor editorial note — the rules document correctly scopes itself as v0 and points to future tasks for full corpus cleaning. No action required.

## Missing tests or verification

1. **Worker verification commands independently re-confirmed:**
   - `validate-layout`: passes.
   - `prompt_corpus_manifest.json`: valid JSON, `status` is not `"completed"`, `corpus_size` is 0.
   - `raw_index.jsonl`: 2 lines, both parse as valid JSON with all required fields (`source_id`, `source_type`, `source_url`, `author_or_team`, `retrieved_or_checked_on`, `license_or_tos_note`, `prompt_text_storage`, `recommended_register_action`, `notes`).
   - `candidate_register_v0.jsonl`: 11 lines, all parse as valid JSON with required fields.
   - Git tracking: `git add --dry-run` succeeds for all 4 governance files. `git check-ignore` (no -v) returns exit code 1 (not ignored).

2. **SHA256 hash spot-check confirmed.** `P1.2.5_minimal_rule_missing_hard_composition.txt` hash `44c88222...` matches the candidate register entry and the experiment plan's RC1 reference.

3. **All 9 local prompt file paths verified on disk.**

4. **External source URL verified via web search.** `https://github.com/israelcazares/sair-prompt-engineering` exists, is public, and carries MIT license — consistent with the raw_index record.

5. **No automated tests expected** — this task does not modify `src/` or `tests/`.

## Suspicious implementation details

None found. Specifically verified:

- `prompt_corpus_manifest.json`: `status: "candidate_register_v0_provenance_checked_not_normalized"`, `corpus_size: 0`, `ready_prompt_count: 0` — honest.
- `candidate_register_v0.jsonl`: public placeholders have empty `prompt_sha256` and `prompt_bytes: 0` — no fake data. GitHub placeholder has real URL/author/license; contributor-network placeholder correctly flags unresolved attribution.
- `raw_index.jsonl`: GitHub entry has `prompt_text_storage: "allowed"` (MIT verified) and `recommended_register_action: "promote_direct"`; contributor-network entry has `prompt_text_storage: "structure_only"` and `recommended_register_action: "keep_structure_only"`. Both are conservative and defensible.
- `provenance_rules.md`: Git tracking strategy section added, scoped to governance files only. "Direct Recompute Eligibility" section honestly explains that `direct_recompute` can apply to "eligible but not yet imported" sources.
- `reports/research/corpus_audit/summary.md`: honestly reports `direct_recompute_candidates: 10` with notes explaining the eligibility vs text-ready distinction.
- `docs/07_handoff.md`: correctly records "Worker 已完成...待 reviewer 审查", does not mark T04 as completed.
- No external prompt text was copied into any file.
- No changes to `src/`, `tests/`, `prompts/complete/`, `configs/research/`, or `artifacts/`.

## Scope compliance

- **Allowed files (7 changed)**: `.gitignore`, `data/external/prompt_corpus/raw_index.jsonl`, `data/interim/prompt_corpus/candidate_register_v0.jsonl`, `data/interim/prompt_corpus/provenance_rules.md`, `data/interim/prompt_corpus/prompt_corpus_manifest.json`, `reports/research/corpus_audit/summary.md`, `docs/07_handoff.md`. All within the allowed list.
- **Forbidden scope**: No changes to `src/`, `tests/`, `prompts/complete/`, `configs/research/`, `artifacts/`. No API eval. No bulk data download. No external prompt text copied. No marking T04 as completed. No normalized corpus written as completed.
- **External Lookup Policy**: Only provenance metadata was looked up (GitHub repo URL, author, MIT license). No bulk data was downloaded.

## Git tracking detail

The `.gitignore` narrow allowlist pattern is:
```gitignore
!data/external/prompt_corpus/
data/external/prompt_corpus/*
!data/external/prompt_corpus/*.md
!data/external/prompt_corpus/*.jsonl
!data/interim/prompt_corpus/
data/interim/prompt_corpus/*
!data/interim/prompt_corpus/*.md
!data/interim/prompt_corpus/*.json
!data/interim/prompt_corpus/*.jsonl
```

This correctly: (a) un-ignores the directory itself, (b) re-ignores all contents, (c) un-ignores specific governance file extensions. Does not broadly open `data/raw/`, general `data/interim/`, or future `raw_prompts/` subdirectories. Confirmed via `git add --dry-run` for all 4 governance files.

## External provenance detail

| Source ID | Type | URL verified | Author verified | License confirmed | Storage | Register action |
|---|---|---|---|---|---|---|
| `github_public_prompt_repo_cazares_2026` | github | Yes (web search confirmed) | Yes | Yes (MIT) | allowed | promote_direct |
| `contributor_network_stage1_official_post_2026` | contributor_network | Yes (LinkedIn post) | Yes (SAIR, host-level) | No (storage rights unclear) | structure_only | keep_structure_only |

## Recommended next action

1. Captain marks T04 as complete in `docs/04_task_board.md`.
2. T05 should normalize direct-recompute candidates, decide whether to import the MIT-licensed GitHub prompt file, and distinguish `eligible` from `text_ready` in the manifest if the count causes confusion.
3. T05 should seek a more stable first-party URL for the contributor-network entry if available.
4. T05 should actively seek additional external candidates (other GitHub repos, paper-described prompts) to reach the 8-12 analyzable prompt target.
