# T06_corpus_audit_public_private_boundary Review

Reviewer: Claude Code (normal review)
Date: 2026-05-16

## Verdict: PASS

## Summary

Worker produced a clear, well-scoped public/private asset boundary note (`public_private_boundary.md`) and updated the corpus audit summary, manifest, provenance rules, and handoff to reflect T06 requirements. All 11 `corpus_v1` records are accurately classified into 4 asset classes (9 text-ready, 1 metadata-only, 1 structure-only, 0 excluded). T07/T10 gating rules are explicit and machine-checkable. T05 counts are preserved without modification. No forbidden scope violations. No external prompt text mirrored. No eval run. No over-engineering.

## Blocking issues

None.

## Non-blocking issues

1. **Handoff `eval-eligible now: 9` vs manifest `eligible_count: 10` terminology overlap.** The handoff uses "eval-eligible now" to mean "can enter eval immediately" (text-ready + path + hash = 9), while the manifest's `eligible_count` includes the GitHub metadata-only record (`eligible_for_recompute: true` = 10). These are semantically different (provenance-eligible vs eval-ready-now), and the boundary note's Direct Recompute Gate section explains the distinction clearly. Not blocking because the boundary note is the authoritative reference and it unambiguously requires all 5 conditions. However, a future worker scanning handoff numbers alone might be confused. Consider adding a parenthetical in handoff like `(text-ready with hash only; eligible_count in manifest = 10 includes metadata-only)` if a later task revisits handoff.

2. **Summary.md "Remaining Risks" renumbered from T05 version.** The original T05-era risks listed "(1) reviewer confirm corpus_v1 口径" as the first risk. T06 drops that risk (now resolved by the boundary note itself) and adds "(4) schema drift risk" as a new item. This is correct and appropriate — T06 resolved risk #1 and R16 (schema drift) is newly prominent now that `corpus_v1` is declared authoritative. Not blocking, just noting the transition for traceability.

3. **Manifest `records_present` includes a path outside `data/`.** The list now includes `reports/research/corpus_audit/public_private_boundary.md`, which is in `reports/` not `data/`. This is a reasonable governance cross-reference, and the field name `records_present` is not strictly defined as "only data paths." However, if a future automated tool assumes all `records_present` entries are in `data/`, it would break. Low risk, not blocking.

4. **`public_private_boundary.md` table row for excluded records says "0" count.** The table documents the excluded class as a placeholder for future rejected assets. This is a good defensive choice — it pre-emptively documents the class without fabricating records. Not blocking.

## Missing tests or verification

1. **Worker verification commands independently re-confirmed:**
   - `validate-layout`: passes (independently re-run).
   - `prompt_corpus_manifest.json`: valid JSON (independently re-confirmed).
   - Boundary note key patterns (`text-ready`, `metadata-only`, `structure-only`, `post-release analysis`, `direct recompute`): 22 occurrences found (independently re-confirmed).
   - Summary key patterns (`T05 review`, `authoritative`, `policy-exempt`, `token`): 8 occurrences found (independently re-confirmed).
   - All pattern matches verified as substantive (not just cross-references to missing content).

2. **Asset class table accuracy verified against `corpus_v1.jsonl`.**
   - 9 text-ready records: confirmed. All have `text_ready=true`, non-empty `prompt_text_path`, non-empty `prompt_sha256`.
   - 1 metadata-only record (`public_placeholder_ce_first_github`): confirmed. `text_ready=false`, `eligible_for_recompute=true`, `prompt_text_path=""`.
   - 1 structure-only record (`public_placeholder_contributor_prompt`): confirmed. `text_ready=false`, `eligible_for_recompute=false`, `prompt_text_path=""`.
   - 0 excluded records: confirmed.

3. **Direct Recompute Gate conditions verified.** All 5 conditions listed in the boundary note map to real `corpus_v1.jsonl` fields, and the count of 9 is correct.

4. **T07/T10 gating rules verified.** The boundary note's "T07 may not" list correctly blocks: inferring missing text from metadata-only records, promoting structure-only records, and using `prompt_tokens_est = 0` for length-bucket claims. The T10 section correctly restricts screening to direct-recompute-ready records only.

5. **No automated tests expected** — this task does not modify `src/` or `tests/`.

## Suspicious implementation details

None found. Specifically verified:

- **No inflation of corpus coverage.** The boundary note's opening section explicitly states "不代表完整 public prompt ecosystem coverage，也不代表任何后续 public release package 已经获批." The summary also states "corpus_v1 is a research snapshot, not complete public ecosystem coverage."
- **No silent count changes.** Manifest counts match T05 exactly: `corpus_v1_record_count=11`, `text_ready_count=9`, `eligible_count=10`, `metadata_only_count=1`, `structure_only_count=1`, `excluded_count=0`.
- **No fabricated token estimates.** Summary correctly states "prompt_tokens_est remains 0 for all 11 records" and downstream rules block token-based claims.
- **No external prompt text.** All diffs and the new file contain only governance prose, metadata references, and policy rules. No prompt text appears anywhere.
- **No release authorization overreach.** The boundary note explicitly states "this note does not grant public full-text release by itself" in the open issues section.
- **`provenance_rules.md` downstream gates align with boundary note.** The new "Downstream Use Gates" section in provenance_rules.md references the boundary note and restates the same rules.
- **Handoff correctly defers T07.** "T07 不能直接启动，需先 review T06 并继续遵守 corpus_v1 gating."

## Scope compliance

- **Allowed files (5 changed)**: `reports/research/corpus_audit/summary.md`, `reports/research/corpus_audit/public_private_boundary.md` (new), `data/interim/prompt_corpus/prompt_corpus_manifest.json`, `data/interim/prompt_corpus/provenance_rules.md`, `docs/07_handoff.md`. All within the allowed list.
- **Forbidden scope**: No changes to `src/`, `tests/`, `prompts/complete/`, `configs/research/`, `artifacts/`, `data/external/prompt_corpus/raw_index.jsonl`, `raw_index.example.jsonl`, `corpus_v1.jsonl`, `duplicate_report_v1.json`, `missing_metadata_report_v1.json`. No external prompt text mirrored. No API eval run. No promotion of metadata-only or structure-only records. No claim of complete ecosystem coverage. No modification of `docs/04_task_board.md`.

## Task requirement checklist

| Task requirement | Status |
|---|---|
| Corpus snapshot and status: post-release analysis, not complete coverage | Done |
| Asset classes with per-class properties (text, hash, T07, T10, release, attribution) | Done (table with 4 classes) |
| Explicit rule: text-ready + hash for direct recompute | Done (5-condition gate) |
| Explicit rule: metadata/structure-only blocked from eval | Done (T07 and T10 gate sections) |
| Explicit rule: released subsets are not prompt sources | Done (Public Release Boundary section) |
| Keep T05 counts intact | Done (all counts verified) |
| Mention T05 review verdict: PASS | Done |
| corpus_v1 as authoritative snapshot | Done |
| Aggregate 9 local missing source_url as policy-exempt | Done |
| List 2 actionable external gaps separately | Done |
| Token estimates unavailable, no length-bucket claims | Done |
| Manifest/provenance downstream-use notes | Done |
| Manifest reference to boundary note | Done |
| No count changes in manifest | Done (verified) |
| Handoff: T06 executed, pending review | Done |
| Handoff: changed files listed | Done |
| Handoff: no external text mirrored | Done |
| Handoff: T07/T10 gating rule | Done |
| Handoff: T07 needs review first | Done |

## Recommended next action

1. Captain marks T06 as complete in `docs/04_task_board.md`.
2. T07 (taxonomy) may proceed using the 9 text-ready records from `corpus_v1.jsonl` as the primary feature-coding pool, with the boundary note's gating rules as constraints.
3. T07 should backfill `prompt_tokens_est` before doing length-bucket analysis.
4. Consider a dedicated small task to mirror the MIT GitHub prompt file if external text-ready coverage becomes important for screening evaluation.
5. Continue seeking stable first-party URL for the contributor-network entry; if not found, maintain structure-only through paper limitation.
