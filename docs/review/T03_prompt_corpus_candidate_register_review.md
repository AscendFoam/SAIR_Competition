# T03_prompt_corpus_candidate_register Review

Reviewer: Claude Code (normal review)
Date: 2026-05-12

## Verdict: PASS

## Summary

Worker has produced a valid candidate register v0 with 11 entries covering all mandatory prompts, comprehensive provenance rules, an updated manifest, and the required T01/T02 hygiene followups. All 9 local prompt file hashes and byte sizes were independently verified as correct. No forbidden scope violations. All JSON/JSONL files parse cleanly. Status fields honestly reflect that this is a candidate register, not a completed corpus.

## Blocking issues

None.

## Non-blocking issues

1. **`data/` files are gitignored.** `data/interim/*` and `data/external/*` are excluded by `.gitignore`, so `candidate_register_v0.jsonl`, `provenance_rules.md`, `prompt_corpus_manifest.json`, and `raw_index.example.jsonl` are on disk but untracked. The worker correctly noted this in their risks section. Captain should decide whether to force-add these files to git or adjust `.gitignore` rules before T04. This is a governance decision, not a worker defect.

2. **`prompt_tokens_est` is 0 for all 11 candidates.** The worker acknowledged this and left it for a future task to decide whether to introduce a tokenizer or use rough estimates. Acceptable for v0 since token counts are not required by the task schema; they were listed as optional in the experiment plan's corpus schema (section 5.2).

3. **External placeholders have no actual source URLs, author names, or license confirmations.** Both `public_placeholder_ce_first_github` and `public_placeholder_contributor_prompt` use generic placeholder descriptions. This is explicitly deferred to T04 per provenance_rules.md section "Candidate Register v0 Scope", and is consistent with the task's instruction not to download external data or access the network.

4. **`storage_policy` typo in `configs/research/corpus_sources.example.json` line 59 remains unfixed.** The worker addressed the T01 review followup by not propagating the typo to any new T03 file — `candidate_register_v0.jsonl` uses `storage_status` and `recompute_eligibility` as separate clean fields, and `provenance_rules.md` uses properly named section headers. The original typo in `configs/research/` persists as expected (modifying that directory is forbidden). This is an acceptable resolution per the task instruction: "raw_index.example.jsonl 或 T03 新规则中处理...不必修改 configs/research/".

5. **Candidate register has 0 `official` source_type entries.** The three P2.0.* prompts are classified as `local` with `candidate_role: official_archetype`, which is accurate — they are local strict adaptations of official archetypes, not direct copies of official releases. The worker's attribution notes explain this correctly. No issue, but future corpus expansion should note whether any direct `official` source entries become available.

## Missing tests or verification

1. **Worker's verification commands all re-confirmed during this review:**
   - `candidate_register_v0.jsonl`: all 11 lines parse; all required fields (`candidate_id`, `source_type`, `source_ref`, `prompt_text_path`, `prompt_sha256`, `prompt_bytes`, `storage_status`, `recompute_eligibility`, `post_release_relation`, `license_or_tos_note`, `attribution_note`, `candidate_role`, `notes`) are present on every line.
   - `raw_index.example.jsonl`: all lines parse.
   - `prompt_corpus_manifest.json`: valid JSON, `status` is not `"completed"`, `corpus_size` is 0.
   - `outline.md`: no `D:/Codes` absolute path matches found.
   - `contribution_list.md`: `unsupported_do_not_claim` present on line 66.

2. **Hash verification independently confirmed.** All 9 local prompt files exist on disk at the paths recorded in the register. SHA256 hashes and byte counts were independently computed and match exactly for all 9 entries.

3. **No automated tests expected** — this task does not modify `src/` or `tests/`.

## Suspicious implementation details

None found. Specifically verified:

- `prompt_corpus_manifest.json`: `status: "candidate_register_v0_not_cleaned"`, `corpus_size: 0`, `ready_prompt_count: 0` — honest.
- `candidate_register_v0.jsonl`: all local entries have real file paths with verified hashes; public placeholders have empty `prompt_sha256` and `prompt_bytes: 0` — no fake data.
- `provenance_rules.md`: clearly scoped as "candidate-register hygiene v0，非 completed corpus policy".
- `reports/research/corpus_audit/summary.md`: corpus size is still 0; candidate register size listed separately as 11.
- `docs/07_handoff.md`: correctly records "Worker 已完成...待 reviewer 审查", does not mark T03 as completed.
- `reports/paper/outline.md`: absolute Windows path fixed to relative link.
- `reports/paper/contribution_list.md`: C8 added as `unsupported_do_not_claim` with proper justification.

## Scope compliance

- **Allowed files**: All 8 changed files are within the allowed list. No extra files.
- **Forbidden scope**: No changes to `src/`, `tests/`, `prompts/complete/`, `configs/research/`, `artifacts/`. No network access, no API eval, no downloaded data, no copied external prompt text. Task not marked as completed. Candidate register not written as completed corpus.
- **Mandatory prompt coverage**: All 5 explicitly required prompts are present (P1.2.3, P1.2.5, P2.0.0, P2.0.1, P2.0.2). Plus a baseline (P0), 4 additional local contrast candidates, and 2 public placeholders. Total 11, within the 8-12 target range.

## Mandatory prompt coverage detail

| Required by task | Candidate ID | Present |
|---|---|---|
| P1.2.3_implicit_guardrail_v2 | local_p1_2_3_implicit_guardrail_v2 | Yes |
| P1.2.5_minimal_rule_missing_hard_composition | local_p1_2_5_minimal_rule_missing_hard_composition | Yes |
| P2.0.0_official_balanced_strict_v0 | local_p2_0_0_official_balanced_strict_v0 | Yes |
| P2.0.1_official_counterexample_first_strict_v0 | local_p2_0_1_official_counterexample_first_strict_v0 | Yes |
| P2.0.2_official_fast_filters_strict_v0 | local_p2_0_2_official_fast_filters_strict_v0 | Yes |
| minimal / no-cheatsheet baseline | local_p0_official_reconstructed_empty | Yes |

## Candidate role distribution

- baseline: 1
- local_contrast: 5
- official_archetype: 3
- public_placeholder: 2

## Recommended next action

1. Captain marks T03 as complete in `docs/04_task_board.md`.
2. Evaluate whether Phase 0 exit criteria are satisfied and, if so, proceed to T04 (collect external prompt candidates into raw index).
3. Decide on git tracking strategy for `data/interim/prompt_corpus/` and `data/external/prompt_corpus/` files before T04 adds more entries.
4. T04 should focus on filling in actual source URLs, authors, and license confirmations for the two public placeholders, and potentially adding more external candidates.
