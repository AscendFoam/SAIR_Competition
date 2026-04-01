from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from sair_competition.analysis.error_report import infer_error_category
from sair_competition.data.io import read_jsonl, write_jsonl


def consolidate_offline_rule_axes(
    predictions_path: str | Path,
    audit_summary_path: str | Path,
    output_dir: str | Path,
) -> dict:
    """Collapse exact-overlap offline assets into canonical axes and recover subset hierarchy."""

    rows = read_jsonl(predictions_path)
    if not any("offline_rule_asset_ids" in row for row in rows):
        raise ValueError("Predictions must already include offline_rule_asset_ids. Run attach-offline-rule-assets first.")

    audit_summary = _load_json(audit_summary_path)
    ranked_assets = list(audit_summary.get("ranked_assets") or [])
    rank_by_rule_id = {asset["rule_id"]: index for index, asset in enumerate(ranked_assets)}
    row_by_key = {_row_key(row): row for row in rows}

    asset_row_keys: dict[str, set[str]] = {}
    for asset in ranked_assets:
        rule_id = asset["rule_id"]
        matched_keys = {
            row_key
            for row_key, row in row_by_key.items()
            if rule_id in set(row.get("offline_rule_asset_ids") or [])
        }
        if matched_keys:
            asset_row_keys[rule_id] = matched_keys

    signature_groups: dict[tuple[str, ...], list[dict]] = defaultdict(list)
    for asset in ranked_assets:
        rule_id = asset["rule_id"]
        matched_keys = asset_row_keys.get(rule_id) or set()
        if not matched_keys:
            continue
        signature_groups[tuple(sorted(matched_keys))].append(asset)

    grouped_items = sorted(
        signature_groups.items(),
        key=lambda item: min(rank_by_rule_id[asset["rule_id"]] for asset in item[1]),
    )

    canonical_axes: list[dict] = []
    exact_overlap_groups: list[dict] = []
    for index, (signature, grouped_assets) in enumerate(grouped_items, start=1):
        grouped_assets_sorted = sorted(grouped_assets, key=lambda asset: rank_by_rule_id[asset["rule_id"]])
        primary_asset = grouped_assets_sorted[0]
        matched_rows = [row_by_key[row_key] for row_key in signature]
        error_buckets = _collect_error_buckets(matched_rows)
        axis_id = f"AXIS_{index:02d}"

        axis = {
            "axis_id": axis_id,
            "main_axis_rule_id": primary_asset["rule_id"],
            "main_focus_group": primary_asset.get("family_focus_group"),
            "main_primary_tag": primary_asset.get("primary_tag"),
            "rank_index": rank_by_rule_id[primary_asset["rule_id"]],
            "merged_rule_ids": [asset["rule_id"] for asset in grouped_assets_sorted],
            "alias_rule_ids": [asset["rule_id"] for asset in grouped_assets_sorted[1:]],
            "merged_focus_groups": _unique_preserving_order(
                asset.get("family_focus_group")
                for asset in grouped_assets_sorted
                if asset.get("family_focus_group")
            ),
            "merged_primary_tags": _unique_preserving_order(
                asset.get("primary_tag")
                for asset in grouped_assets_sorted
                if asset.get("primary_tag")
            ),
            "merged_trigger_tags": _unique_preserving_order(
                tag
                for asset in grouped_assets_sorted
                for tag in (asset.get("trigger_tags") or [])
            ),
            "row_keys": list(signature),
            "row_count": len(signature),
            "error_count": sum(error_buckets.values()),
            "error_buckets": dict(error_buckets),
            "recoverable_error_count": error_buckets.get("RULE_MISSING", 0) + error_buckets.get("HARD_COMPOSITION", 0),
            "true_miss_count": sum(
                1 for row in matched_rows if row.get("answer") is True and row.get("prediction") is not True
            ),
            "false_positive_count": sum(
                1 for row in matched_rows if row.get("answer") is False and row.get("prediction") is True
            ),
            "priority_score": max(float(asset.get("priority_score") or 0.0) for asset in grouped_assets_sorted),
            "sample_matches": [_row_label(row) for row in matched_rows[:8]],
            "true_miss_examples": [
                _row_label(row)
                for row in matched_rows
                if row.get("answer") is True and row.get("prediction") is not True
            ][:8],
            "exact_duplicate_count": len(grouped_assets_sorted),
            "parent_axis_id": None,
            "parent_main_axis_rule_id": None,
            "child_axis_ids": [],
            "child_main_axis_rule_ids": [],
            "axis_depth": 0,
        }
        canonical_axes.append(axis)
        exact_overlap_groups.append(
            {
                "group_id": axis_id,
                "canonical_rule_id": primary_asset["rule_id"],
                "merged_rule_ids": [asset["rule_id"] for asset in grouped_assets_sorted],
                "row_count": len(signature),
                "relationship": "identical_row_support",
            }
        )

    _attach_parent_child_links(canonical_axes)
    ranked_axes = sorted(
        canonical_axes,
        key=lambda axis: (
            axis["priority_score"],
            axis["recoverable_error_count"],
            axis["true_miss_count"],
            axis["row_count"],
            -axis["rank_index"],
        ),
        reverse=True,
    )

    summary = {
        "predictions_path": str(predictions_path),
        "audit_summary_path": str(audit_summary_path),
        "output_dir": str(output_dir),
        "raw_asset_count": len(ranked_assets),
        "matched_asset_count": len(asset_row_keys),
        "exact_overlap_group_count": len(exact_overlap_groups),
        "canonical_axis_count": len(ranked_axes),
        "exact_overlap_groups": exact_overlap_groups,
        "canonical_axes": ranked_axes,
        "recommendation": _build_axis_recommendation(ranked_axes),
    }

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_root / "summary.md").write_text(_axis_summary_to_markdown(summary), encoding="utf-8")
    return summary


def build_offline_rule_review_set(
    predictions_path: str | Path,
    consolidation_summary_path: str | Path,
    output_dir: str | Path,
) -> dict:
    """Build a deduplicated review set by assigning each row to its most specific canonical axis."""

    rows = read_jsonl(predictions_path)
    consolidation_summary = _load_json(consolidation_summary_path)
    canonical_axes = list(consolidation_summary.get("canonical_axes") or [])
    axis_by_id = {axis["axis_id"]: axis for axis in canonical_axes}
    row_to_axes: dict[str, list[dict]] = defaultdict(list)
    for axis in canonical_axes:
        for row_key in axis.get("row_keys") or []:
            row_to_axes[row_key].append(axis)

    review_rows: list[dict] = []
    assigned_row_keys: set[str] = set()
    bucket_counter: Counter[str] = Counter()
    assigned_axis_by_row_key: dict[str, str] = {}

    for row in rows:
        row_key = _row_key(row)
        matching_axes = row_to_axes.get(row_key) or []
        if not matching_axes:
            continue

        primary_axis = sorted(matching_axes, key=_axis_specificity_sort_key)[0]
        assigned_axis_by_row_key[row_key] = primary_axis["axis_id"]
        if not _is_actionable_review_row(row):
            continue

        assigned_row_keys.add(row_key)
        bucket_counter[primary_axis["axis_id"]] += 1
        lineage = _axis_lineage(primary_axis, axis_by_id)
        review_rows.append(
            {
                "problem_id": row.get("problem_id"),
                "source": row.get("source"),
                "split": row.get("split"),
                "equation1": row.get("equation1"),
                "equation2": row.get("equation2"),
                "answer": row.get("answer"),
                "prediction": row.get("prediction"),
                "parsed": row.get("parsed", True),
                "error_category": infer_error_category(row),
                "review_axis_id": primary_axis["axis_id"],
                "review_axis_rule_id": primary_axis["main_axis_rule_id"],
                "review_axis_depth": primary_axis["axis_depth"],
                "review_axis_parent_rule_id": primary_axis.get("parent_main_axis_rule_id"),
                "review_axis_alias_rule_ids": list(primary_axis.get("alias_rule_ids") or []),
                "matched_canonical_axis_rule_ids": [axis["main_axis_rule_id"] for axis in matching_axes],
                "matched_offline_rule_asset_ids": list(row.get("offline_rule_asset_ids") or []),
                "family_tags": list(row.get("family_tags") or []),
                "axis_lineage_rule_ids": [axis["main_axis_rule_id"] for axis in lineage],
                "boundary_family_tags": _boundary_family_tags(row, primary_axis, axis_by_id),
                "review_priority": _review_priority(primary_axis),
                "suggested_next_action": _suggested_next_action(primary_axis),
                "annotation_questions": _annotation_questions(row, primary_axis, axis_by_id),
                "review_note": _build_review_note(row, primary_axis),
            }
        )

    review_rows_sorted = sorted(
        review_rows,
        key=lambda row: (
            row["review_priority"],
            row["review_axis_depth"] * -1,
            str(row.get("source") or ""),
            str(row.get("problem_id") or ""),
        ),
    )

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    review_set_path = output_root / "review_set.jsonl"
    write_jsonl(review_set_path, review_rows_sorted)
    checklist_path = output_root / "annotation_checklist.md"
    checklist_path.write_text(_review_checklist_to_markdown(review_rows_sorted), encoding="utf-8")
    p0_p1_template_path = output_root / "p0_p1_review_template.md"
    p0_p1_template_path.write_text(_p0_p1_review_template_to_markdown(review_rows_sorted), encoding="utf-8")

    bucket_summary = _build_review_bucket_summary(
        rows=rows,
        canonical_axes=canonical_axes,
        bucket_counter=bucket_counter,
        axis_by_id=axis_by_id,
        assigned_axis_by_row_key=assigned_axis_by_row_key,
    )
    summary = {
        "predictions_path": str(predictions_path),
        "consolidation_summary_path": str(consolidation_summary_path),
        "output_dir": str(output_dir),
        "review_set_path": str(review_set_path),
        "annotation_checklist_path": str(checklist_path),
        "p0_p1_review_template_path": str(p0_p1_template_path),
        "review_row_count": len(review_rows_sorted),
        "review_axis_count": sum(1 for count in bucket_counter.values() if count > 0),
        "assigned_row_count": len(assigned_row_keys),
        "bucket_summary": bucket_summary,
        "recommendation": _build_review_recommendation(bucket_summary),
    }
    (output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_root / "summary.md").write_text(_review_summary_to_markdown(summary), encoding="utf-8")
    return summary


def _attach_parent_child_links(canonical_axes: list[dict]) -> None:
    axis_by_id = {axis["axis_id"]: axis for axis in canonical_axes}
    row_sets = {axis["axis_id"]: set(axis["row_keys"]) for axis in canonical_axes}

    for child in canonical_axes:
        child_set = row_sets[child["axis_id"]]
        parent_candidates = [
            parent
            for parent in canonical_axes
            if parent["axis_id"] != child["axis_id"] and child_set < row_sets[parent["axis_id"]]
        ]
        if not parent_candidates:
            continue
        parent = min(parent_candidates, key=lambda axis: (len(row_sets[axis["axis_id"]]), axis["rank_index"]))
        child["parent_axis_id"] = parent["axis_id"]
        child["parent_main_axis_rule_id"] = parent["main_axis_rule_id"]

    for axis in canonical_axes:
        axis["child_axis_ids"] = []
        axis["child_main_axis_rule_ids"] = []

    for axis in canonical_axes:
        parent_axis_id = axis.get("parent_axis_id")
        if not parent_axis_id:
            continue
        parent = axis_by_id[parent_axis_id]
        parent["child_axis_ids"].append(axis["axis_id"])
        parent["child_main_axis_rule_ids"].append(axis["main_axis_rule_id"])

    for axis in canonical_axes:
        axis["axis_depth"] = _axis_depth(axis, axis_by_id)
        axis["child_axis_ids"] = sorted(axis["child_axis_ids"])
        axis["child_main_axis_rule_ids"] = _unique_preserving_order(axis["child_main_axis_rule_ids"])


def _axis_depth(axis: dict, axis_by_id: dict[str, dict]) -> int:
    depth = 0
    current = axis
    seen: set[str] = set()
    while current.get("parent_axis_id"):
        parent_axis_id = current["parent_axis_id"]
        if parent_axis_id in seen:
            break
        seen.add(parent_axis_id)
        parent = axis_by_id[parent_axis_id]
        depth += 1
        current = parent
    return depth


def _axis_lineage(axis: dict, axis_by_id: dict[str, dict]) -> list[dict]:
    lineage = [axis]
    current = axis
    seen: set[str] = {axis["axis_id"]}
    while current.get("parent_axis_id"):
        parent_axis_id = current["parent_axis_id"]
        if parent_axis_id in seen:
            break
        seen.add(parent_axis_id)
        current = axis_by_id[parent_axis_id]
        lineage.append(current)
    return list(reversed(lineage))


def _axis_specificity_sort_key(axis: dict) -> tuple:
    return (
        -_axis_depth_value(axis),
        _axis_row_count(axis),
        _axis_rank_index(axis),
        -_axis_priority_score(axis),
    )


def _is_actionable_review_row(row: dict) -> bool:
    if row.get("answer") is not True:
        return False
    if row.get("prediction") is True:
        return False
    return infer_error_category(row) in {"RULE_MISSING", "HARD_COMPOSITION"}


def _boundary_family_tags(row: dict, axis: dict, axis_by_id: dict[str, dict]) -> list[str]:
    lineage = _axis_lineage(axis, axis_by_id)
    axis_tags = {
        tag
        for lineage_axis in lineage
        for tag in (lineage_axis.get("merged_trigger_tags") or [])
    }
    return [
        tag
        for tag in row.get("family_tags") or []
        if tag not in axis_tags
    ]


def _review_priority(axis: dict) -> str:
    if _axis_depth_value(axis) >= 2 or _axis_row_count(axis) <= 2:
        return "P0"
    if _axis_depth_value(axis) == 1:
        return "P1"
    return "P2"


def _suggested_next_action(axis: dict) -> str:
    if _axis_depth_value(axis) >= 1:
        return "expand_family_tagger"
    if _axis_row_count(axis) <= 2:
        return "collect_more_examples"
    return "prepare_programmatic_positive_signal"


def _annotation_questions(row: dict, axis: dict, axis_by_id: dict[str, dict]) -> list[str]:
    questions = [
        f"Confirm whether `{axis['main_axis_rule_id']}` should remain the canonical axis for this row.",
    ]
    boundary_tags = _boundary_family_tags(row, axis, axis_by_id)
    if boundary_tags:
        questions.append(
            "Decide whether these extra tags should become a narrower child tag: "
            + ", ".join(boundary_tags)
            + "."
        )
    if axis["axis_depth"] >= 1:
        questions.append("Check whether this child axis is stable enough to promote into the family tagger.")
    else:
        questions.append("Check whether this axis should feed an implicit positive programmatic signal instead of prompt wording.")
    return questions


def _build_review_note(row: dict, axis: dict) -> str:
    return (
        f"{_row_label(row)} is a missed-true example assigned to `{axis['main_axis_rule_id']}` "
        f"after deduplicating overlapping offline assets."
    )


def _build_review_bucket_summary(
    rows: list[dict],
    canonical_axes: list[dict],
    bucket_counter: Counter[str],
    axis_by_id: dict[str, dict],
    assigned_axis_by_row_key: dict[str, str],
) -> list[dict]:
    row_by_key = {_row_key(row): row for row in rows}
    buckets: list[dict] = []
    for axis in sorted(canonical_axes, key=_axis_specificity_sort_key):
        axis_row_keys = [row_key for row_key in axis.get("row_keys") or [] if row_key in row_by_key]
        axis_rows = [row_by_key[row_key] for row_key in axis_row_keys]
        row_keys = [
            row_key
            for row_key, axis_id in assigned_axis_by_row_key.items()
            if axis_id == axis["axis_id"]
        ]
        actionable_rows = [
            row_by_key[row_key]
            for row_key in row_keys
            if row_key in row_by_key and _is_actionable_review_row(row_by_key[row_key])
        ]
        correct_anchor_rows = [
            row_by_key[row_key]
            for row_key in row_keys
            if row_key in row_by_key
            and row_by_key[row_key].get("answer") is True
            and row_by_key[row_key].get("prediction") is True
        ][:2]
        bucket = {
            "axis_id": axis["axis_id"],
            "main_axis_rule_id": axis["main_axis_rule_id"],
            "parent_main_axis_rule_id": axis.get("parent_main_axis_rule_id"),
            "axis_depth": _axis_depth_value(axis),
            "row_count": _axis_row_count(axis),
            "assigned_review_rows": bucket_counter.get(axis["axis_id"], 0),
            "recoverable_error_count": _axis_recoverable_error_count(axis, axis_rows),
            "true_miss_count": _axis_true_miss_count(axis, axis_rows),
            "merged_rule_ids": list(axis.get("merged_rule_ids") or []),
            "boundary_focus_tags": _unique_preserving_order(
                tag
                for row in actionable_rows
                for tag in _boundary_family_tags(row, axis, axis_by_id)
            ),
            "correct_anchor_examples": [_row_label(row) for row in correct_anchor_rows],
            "actionable_examples": [_row_label(row) for row in actionable_rows[:8]],
            "suggested_next_action": _suggested_next_action(axis),
            "review_priority": _review_priority(axis),
        }
        buckets.append(bucket)
    return buckets


def _build_axis_recommendation(canonical_axes: list[dict]) -> dict:
    if not canonical_axes:
        return {"summary": "No canonical axes were found."}

    top_axes = canonical_axes[:3]
    summary = "Count overlapping offline assets once under their canonical main axis: "
    summary += ", ".join(
        (
            f"{axis['main_axis_rule_id']}(aliases={len(axis['alias_rule_ids'])}, "
            f"rows={axis['row_count']}, true_miss={axis['true_miss_count']})"
        )
        for axis in top_axes
    )
    summary += ". Use child axes only as narrower buckets, not as extra copies of the same opportunity."
    return {
        "top_axis_rule_ids": [axis["main_axis_rule_id"] for axis in top_axes],
        "summary": summary,
    }


def _build_review_recommendation(bucket_summary: list[dict]) -> dict:
    active_buckets = [bucket for bucket in bucket_summary if bucket["assigned_review_rows"] > 0]
    if not active_buckets:
        return {"summary": "No actionable review rows were assigned to canonical axes."}

    ordered = sorted(
        active_buckets,
        key=lambda bucket: (
            bucket["review_priority"],
            bucket["assigned_review_rows"] * -1,
            bucket["axis_depth"] * -1,
            bucket["main_axis_rule_id"],
        ),
    )
    summary = "Start the next review pass from the most specific canonical buckets: "
    summary += ", ".join(
        f"{bucket['main_axis_rule_id']}(priority={bucket['review_priority']}, rows={bucket['assigned_review_rows']})"
        for bucket in ordered[:4]
    )
    summary += ". Each row now appears once, under its most specific axis."
    return {
        "top_review_axis_rule_ids": [bucket["main_axis_rule_id"] for bucket in ordered[:4]],
        "summary": summary,
    }


def _axis_summary_to_markdown(summary: dict) -> str:
    lines = [
        "# Offline Rule Axis Consolidation",
        "",
        f"- Predictions: `{summary['predictions_path']}`",
        f"- Audit summary: `{summary['audit_summary_path']}`",
        f"- Raw assets: `{summary['raw_asset_count']}`",
        f"- Canonical axes: `{summary['canonical_axis_count']}`",
        f"- Exact-overlap groups: `{summary['exact_overlap_group_count']}`",
        "",
        "| Axis | Main Rule | Aliases | Rows | True Miss | Parent | Priority |",
        "| --- | --- | --- | ---: | ---: | --- | ---: |",
    ]

    for axis in summary["canonical_axes"]:
        alias_text = ", ".join(axis["alias_rule_ids"]) if axis["alias_rule_ids"] else "none"
        parent_text = axis["parent_main_axis_rule_id"] or "root"
        lines.append(
            "| {axis_id} | {main_rule} | {aliases} | {rows} | {true_miss} | {parent} | {priority} |".format(
                axis_id=axis["axis_id"],
                main_rule=axis["main_axis_rule_id"],
                aliases=alias_text,
                rows=axis["row_count"],
                true_miss=axis["true_miss_count"],
                parent=parent_text,
                priority=_fmt_rate(axis["priority_score"]),
            )
        )

    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            summary["recommendation"]["summary"],
            "",
            "## Axis Details",
            "",
        ]
    )

    for axis in summary["canonical_axes"]:
        lines.extend(
            [
                f"### {axis['axis_id']} / {axis['main_axis_rule_id']}",
                "",
                f"- Main focus group: `{axis['main_focus_group']}`",
                f"- Merged rules: `{', '.join(axis['merged_rule_ids'])}`",
                f"- Merged trigger tags: `{', '.join(axis['merged_trigger_tags']) if axis['merged_trigger_tags'] else 'none'}`",
                f"- Parent axis: `{axis['parent_main_axis_rule_id'] or 'root'}`",
                f"- Child axes: `{', '.join(axis['child_main_axis_rule_ids']) if axis['child_main_axis_rule_ids'] else 'none'}`",
                f"- Rows: `{axis['row_count']}`",
                f"- True misses: `{axis['true_miss_count']}`",
                f"- Recoverable errors: `{axis['recoverable_error_count']}`",
                f"- Error buckets: `{_format_buckets(axis['error_buckets'])}`",
                f"- Sample matches: `{', '.join(axis['sample_matches']) if axis['sample_matches'] else 'none'}`",
                f"- True miss examples: `{', '.join(axis['true_miss_examples']) if axis['true_miss_examples'] else 'none'}`",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def _review_checklist_to_markdown(review_rows: list[dict]) -> str:
    lines = [
        "# Offline Rule Annotation Checklist",
        "",
        "Use this checklist together with `review_set.jsonl`.",
        "",
    ]

    current_priority = None
    for row in review_rows:
        if row["review_priority"] != current_priority:
            current_priority = row["review_priority"]
            lines.extend(
                [
                    f"## {current_priority}",
                    "",
                ]
            )
        lines.extend(
            [
                f"### [ ] {row.get('problem_id') or row['review_note']}",
                "",
                f"- Axis: `{row['review_axis_rule_id']}`",
                f"- Parent axis: `{row.get('review_axis_parent_rule_id') or 'root'}`",
                f"- Suggested action: `{row['suggested_next_action']}`",
                f"- Error: `{row['error_category']}`",
                f"- Equation 1: `{row['equation1']}`",
                f"- Equation 2: `{row['equation2']}`",
                f"- Boundary tags: `{', '.join(row['boundary_family_tags']) if row['boundary_family_tags'] else 'none'}`",
                f"- Questions: `{' | '.join(row['annotation_questions'])}`",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def _p0_p1_review_template_to_markdown(review_rows: list[dict]) -> str:
    target_rows = [row for row in review_rows if row["review_priority"] in {"P0", "P1"}]
    grouped_rows: dict[str, dict[str, list[dict]]] = {"P0": defaultdict(list), "P1": defaultdict(list)}
    for row in target_rows:
        grouped_rows[row["review_priority"]][row["review_axis_rule_id"]].append(row)

    lines = [
        "# P0 P1 Review Template",
        "",
        "Use this template to review the highest-priority rows first.",
        "Recommended workflow: axis-level judgment first, then row-level confirmation, then backfill whether the result should feed tagger expansion or a more implicit programmatic signal.",
        "",
        "## Session Metadata",
        "",
        "- Reviewer: `________________`",
        "- Review date: `________________`",
        "- Candidate / branch: `________________`",
        "- Related report / summary: `________________`",
        "",
    ]

    for priority in ["P0", "P1"]:
        axis_groups = grouped_rows[priority]
        if not axis_groups:
            continue
        lines.extend(
            [
                f"## {priority}",
                "",
            ]
        )
        for axis_rule_id, rows in axis_groups.items():
            sample_row = rows[0]
            boundary_union = _unique_preserving_order(
                tag
                for row in rows
                for tag in (row.get("boundary_family_tags") or [])
            )
            lines.extend(
                [
                    f"### Axis / {axis_rule_id}",
                    "",
                    f"- Parent axis: `{sample_row.get('review_axis_parent_rule_id') or 'root'}`",
                    f"- Suggested action: `{sample_row['suggested_next_action']}`",
                    f"- Rows in this bucket: `{len(rows)}`",
                    f"- Boundary tag union: `{', '.join(boundary_union) if boundary_union else 'none'}`",
                    "",
                    "`Axis-Level Decision`",
                    "- [ ] Keep the current canonical axis",
                    "- [ ] Split out a narrower child axis",
                    "- [ ] Merge this bucket back into a parent / sibling axis",
                    "Canonical axis after review: `________________`",
                    "Candidate child axis / child tag: `________________`",
                    "",
                    "`Program Decision`",
                    "- [ ] Extend the family tagger",
                    "- [ ] Prepare an implicit/programmatic positive signal",
                    "- [ ] Keep this bucket as observation only for now",
                    "Owner / next step: `________________`",
                    "Axis-level notes: `________________`",
                    "",
                ]
            )
            for row in rows:
                lines.extend(
                    [
                        f"#### [ ] {row.get('problem_id') or row['review_note']}",
                        "",
                        f"- Equation 1: `{row['equation1']}`",
                        f"- Equation 2: `{row['equation2']}`",
                        f"- Boundary tags: `{', '.join(row['boundary_family_tags']) if row['boundary_family_tags'] else 'none'}`",
                        f"- Matched offline assets: `{', '.join(row['matched_offline_rule_asset_ids']) if row['matched_offline_rule_asset_ids'] else 'none'}`",
                        "",
                        "`Row Verdict`",
                        "- [ ] Supports the current axis as-is",
                        "- [ ] Suggests a narrower structural subtype",
                        "- [ ] Looks misassigned and should move axes",
                        "Proposed subtype / destination axis: `________________`",
                        "",
                        "`Evidence`",
                        "Shared structural cue: `________________`",
                        "Why the current prompt missed it: `________________`",
                        "Tagger / injection relevance: `________________`",
                        "",
                        "`Boundary Review`",
                        "Keep / split / drop decision: `________________`",
                        "",
                        "`Conclusion`",
                        "Row conclusion: `________________`",
                        "Follow-up needed: `________________`",
                        "Notes: `________________`",
                        "",
                    ]
                )

        lines.extend(
            [
                "`Priority Summary`",
                "- [ ] This priority bucket is fully reviewed",
                "Merged conclusion for this priority: `________________`",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def _axis_row_count(axis: dict) -> int:
    row_count = axis.get("row_count")
    if row_count is not None:
        return int(row_count)
    return len(axis.get("row_keys") or [])


def _axis_depth_value(axis: dict) -> int:
    return int(axis.get("axis_depth") or 0)


def _axis_rank_index(axis: dict) -> int:
    return int(axis.get("rank_index") or 0)


def _axis_priority_score(axis: dict) -> float:
    return float(axis.get("priority_score") or 0.0)


def _axis_true_miss_count(axis: dict, axis_rows: list[dict]) -> int:
    true_miss_count = axis.get("true_miss_count")
    if true_miss_count is not None:
        return int(true_miss_count)
    return sum(1 for row in axis_rows if row.get("answer") is True and row.get("prediction") is not True)


def _axis_recoverable_error_count(axis: dict, axis_rows: list[dict]) -> int:
    recoverable_error_count = axis.get("recoverable_error_count")
    if recoverable_error_count is not None:
        return int(recoverable_error_count)
    return sum(
        1
        for row in axis_rows
        if infer_error_category(row) in {"RULE_MISSING", "HARD_COMPOSITION"}
    )


def _review_summary_to_markdown(summary: dict) -> str:
    lines = [
        "# Offline Rule Review Set",
        "",
        f"- Predictions: `{summary['predictions_path']}`",
        f"- Consolidation summary: `{summary['consolidation_summary_path']}`",
        f"- Review set: `{summary['review_set_path']}`",
        f"- Annotation checklist: `{summary['annotation_checklist_path']}`",
        f"- P0/P1 template: `{summary['p0_p1_review_template_path']}`",
        f"- Review rows: `{summary['review_row_count']}`",
        f"- Active review buckets: `{summary['review_axis_count']}`",
        "",
        "| Axis | Priority | Assigned Rows | Depth | Suggested Action | Boundary Tags |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ]

    for bucket in summary["bucket_summary"]:
        if bucket["assigned_review_rows"] <= 0:
            continue
        boundary_text = ", ".join(bucket["boundary_focus_tags"]) if bucket["boundary_focus_tags"] else "none"
        lines.append(
            "| {axis} | {priority} | {rows} | {depth} | {action} | {boundary} |".format(
                axis=bucket["main_axis_rule_id"],
                priority=bucket["review_priority"],
                rows=bucket["assigned_review_rows"],
                depth=bucket["axis_depth"],
                action=bucket["suggested_next_action"],
                boundary=boundary_text,
            )
        )

    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            summary["recommendation"]["summary"],
            "",
            "## Bucket Details",
            "",
        ]
    )

    for bucket in summary["bucket_summary"]:
        if bucket["assigned_review_rows"] <= 0:
            continue
        lines.extend(
            [
                f"### {bucket['main_axis_rule_id']}",
                "",
                f"- Priority: `{bucket['review_priority']}`",
                f"- Parent axis: `{bucket['parent_main_axis_rule_id'] or 'root'}`",
                f"- Assigned review rows: `{bucket['assigned_review_rows']}`",
                f"- Suggested action: `{bucket['suggested_next_action']}`",
                f"- Boundary focus tags: `{', '.join(bucket['boundary_focus_tags']) if bucket['boundary_focus_tags'] else 'none'}`",
                f"- Actionable examples: `{', '.join(bucket['actionable_examples']) if bucket['actionable_examples'] else 'none'}`",
                f"- Correct anchor examples: `{', '.join(bucket['correct_anchor_examples']) if bucket['correct_anchor_examples'] else 'none'}`",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def _collect_error_buckets(rows: list[dict]) -> Counter[str]:
    buckets: Counter[str] = Counter()
    for row in rows:
        category = infer_error_category(row)
        if category == "CORRECT":
            continue
        buckets[category] += 1
    return buckets


def _load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _row_key(row: dict) -> str:
    if row.get("problem_id"):
        return str(row["problem_id"])
    return f"{row.get('source', 'unknown')}::{row.get('equation1', '')} => {row.get('equation2', '')}"


def _row_label(row: dict) -> str:
    if row.get("problem_id"):
        return str(row["problem_id"])
    return f"{row.get('equation1', '')} => {row.get('equation2', '')}"


def _unique_preserving_order(items) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for item in items:
        if not item:
            continue
        value = str(item)
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _format_buckets(buckets: dict[str, int]) -> str:
    if not buckets:
        return "none"
    return ", ".join(f"{name}={count}" for name, count in sorted(buckets.items(), key=lambda item: (-item[1], item[0])))


def _fmt_rate(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.4f}"
