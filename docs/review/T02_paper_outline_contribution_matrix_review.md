# T02_paper_outline_contribution_matrix Review

Reviewer: Claude Code (normal review)
Date: 2026-05-12

## Verdict: PASS

## Summary

Worker has refined `reports/paper/outline.md` from a high-level scaffold into a detailed paper design document, created a new `contribution_list.md` with 7 contributions tracked by status and evidence, and created a new `claim_evidence_matrix.md` with 12 claims each having explicit allowed/forbidden wording. All changes stay within the Allowed Files scope. No forbidden modifications detected.

## Blocking issues

None.

## Non-blocking issues

1. **`contribution_list.md` does not use `unsupported_do_not_claim` status.** All 7 contributions are either `supported_by_existing_assets` (C1, C2, C3, C7) or `planned_needs_data` (C4, C5, C6). The worker notes this is intentional since all contributions have at least planning-level support. This is reasonable, but the task spec explicitly lists this as a required status value — it should appear at least once (even for a "straw man" contribution that was considered and rejected) to demonstrate the classification is active. Consider adding a note in the contribution list or a C8 entry showing a claim that was deliberately excluded and marked `unsupported_do_not_claim` (e.g., "Stage1 prompt tuning can beat the leaderboard ceiling").

2. **C7 contribution is borderline.** C7 ("Stage1 已有工程资产足以支持后续科研") reads more like internal project justification than a paper contribution. The worker acknowledges this in the "nearest competing work" field ("这更像内部项目总结"). This is fine as a tracked item — it prevents the claim from accidentally leaking into the paper's result section — but it might be clearer to demote C7 from the main contribution list and keep it as a setup/motivation note instead.

3. **Outline link to contribution_list.md uses absolute Windows path.** Line 47 of `outline.md` has `[contribution_list.md](D:/Codes/Math/SAIR_Competition/reports/paper/contribution_list.md)` — this should be a relative path like `contribution_list.md` for portability.

4. **Abstract draft uses future tense but the research framing is already largely done.** The abstract says "We plan to study" which is appropriate for a planning document. However, the framing, corpus schema, taxonomy seed, and eval protocol are already in place. A slightly more specific abstract could say "We introduce a provenance-aware corpus schema and feature taxonomy, and plan to evaluate..." to reflect the scaffold that already exists. This is a minor wording preference.

## Missing tests or verification

1. **All required text pattern checks verified.** The task spec requires 4 pattern checks:
   - `outline.md`: "post-release analysis", "Not-Yet-Supported", "claim" — all present (7 matches).
   - `contribution_list.md`: three status values — all present (4 `supported_by_existing_assets`, 3 `planned_needs_data`, 0 `unsupported_do_not_claim`).
   - `claim_evidence_matrix.md`: "forbidden wording", "released final evaluation subsets", "compression_style", "ce_search_depth" — all present (19 matches).

2. **`validate-layout` passes.** No existing functionality broken.

3. **Task spec requires checking for taxonomy mapping, `compression_style`, `ce_search_depth` as prerequisites.** All three are explicitly addressed in the claim matrix (CL4, CL5) and the outline's Not-Yet-Supported Claims section.

## Suspicious implementation details

None found. Key honesty checks:

- `outline.md`: Abstract draft explicitly states "this is a design target rather than a completed empirical result". Core claim section says "目前还不能把方法效果写成既有结果".
- `contribution_list.md`: C4, C5, C6 honestly marked as `planned_needs_data`. Each entry names the missing artifacts explicitly.
- `claim_evidence_matrix.md`: CL11 (feature-aware distillation) has zero current evidence, only a method plan. Forbidden wording precisely matches the task spec requirement.
- `docs/07_handoff.md`: Updated to "待 reviewer 按 normal 类型审查", does not mark T02 complete.
- No empirical results are written as completed facts anywhere.

## Scope compliance

- Allowed files: All 5 allowed paths (`reports/paper/README.md`, `outline.md`, `contribution_list.md`, `claim_evidence_matrix.md`, `docs/07_handoff.md`) are present and modified/created.
- Forbidden scope: No changes to `src/`, `tests/`, `prompts/complete/`, `configs/research/`, `data/`, `artifacts/`, `docs/04_task_board.md`.
- `docs/07_handoff.md`: Updated within scope. Section 6 explicitly says "先完成 T02 状态切换，再进入 T03".

## Task spec compliance checklist

| Requirement | Status |
|---|---|
| Refined outline with abstract draft | Done |
| Refined outline with core claim | Done |
| Refined outline with RQ list | Done (carried from T01) |
| Refined outline with contribution list summary | Done |
| Refined outline with section skeleton | Done (carried from T01) |
| Refined outline with planned tables and figures | Done (tables new, figures refined) |
| Refined outline with evidence status | Done (expanded) |
| Refined outline with not-yet-supported claims | Done (expanded with 2 new items) |
| Refined outline with post-release analysis caveat | Done (explicit section) |
| Contribution list with contribution id | Done (C1-C7) |
| Contribution list with source in local docs | Done |
| Contribution list with required evidence | Done |
| Contribution list with current status (3 values) | Partial (2 of 3 values used) |
| Contribution list with competing work/objection | Done |
| Contribution list covers 6 required areas | Done (all 6 covered plus C7) |
| Claim matrix with claim id | Done (CL1-CL12) |
| Claim matrix with claim text | Done |
| Claim matrix with linked RQ | Done |
| Claim matrix with needed artifact | Done |
| Claim matrix with current evidence | Done |
| Claim matrix with missing evidence | Done |
| Claim matrix with allowed/forbidden wording | Done |
| Claim matrix: distillation claim forbidden | Done (CL11) |
| Claim matrix: released subsets constrained | Done (CL7) |
| Claim matrix: taxonomy mapping as prerequisite | Done (CL4) |
| Claim matrix: compression_style/ce_search_depth gap | Done (CL5) |
| Handoff update | Done |

## Recommended next action

1. Captain marks T02 as complete in `docs/04_task_board.md`.
2. Fix the absolute path link in `outline.md` line 47 (change to relative path). This can be done as a minor patch during T03 or as a standalone fix.
3. Consider whether C7 should be demoted from the main contribution list to a setup note.
4. Proceed to T03 (Prompt corpus candidate register v0).
5. Before T07, create the explicit taxonomy field mapping document referenced in CL4.
