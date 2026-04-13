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
            "main_status": primary_asset.get("status"),
            "main_prompt_policy": primary_asset.get("prompt_policy"),
            "main_follow_up_action": primary_asset.get("follow_up_action"),
            "main_notes": primary_asset.get("notes"),
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
    """通过集合包含关系构建轴间的父子层级。

    Args:
        canonical_axes: 规范轴列表，每个轴包含 row_keys 等字段。
            函数会原地修改各轴的 parent_axis_id、child_axis_ids 和 axis_depth 字段。

    Returns:
        None: 直接修改 canonical_axes 中各轴的层级关系字段。
    """
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
    """沿父链计算轴深度（根轴深度为 0）。

    Args:
        axis: 目标轴字典，需包含 axis_id 字段。
        axis_by_id: 以 axis_id 为键的轴字典映射。

    Returns:
        int: 从当前轴到根轴的层级深度。
    """
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
    """获取从根到当前轴的完整谱系链。

    Args:
        axis: 目标轴字典。
        axis_by_id: 以 axis_id 为键的轴字典映射。

    Returns:
        list[dict]: 从根轴到当前轴有序排列的轴列表。
    """
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
    """返回用于排序的特异性键（深度越深、行数越少越优先）。

    Args:
        axis: 目标轴字典。

    Returns:
        tuple: 排序元组，按深度降序、行数升序、排名升序、优先级降序排列。
    """
    return (
        -_axis_depth_value(axis),
        _axis_row_count(axis),
        _axis_rank_index(axis),
        -_axis_priority_score(axis),
    )


def _is_actionable_review_row(row: dict) -> bool:
    """判断行是否为可操作的审查行（answer=True, prediction!=True, error 属于 RULE_MISSING 或 HARD_COMPOSITION）。

    Args:
        row: 数据行字典，需包含 answer、prediction 等字段。

    Returns:
        bool: 若该行为可操作的审查行则返回 True，否则返回 False。
    """
    if row.get("answer") is not True:
        return False
    if row.get("prediction") is True:
        return False
    return infer_error_category(row) in {"RULE_MISSING", "HARD_COMPOSITION"}


def _boundary_family_tags(row: dict, axis: dict, axis_by_id: dict[str, dict]) -> list[str]:
    """返回行中不属于轴谱系覆盖范围的额外家族标签。

    Args:
        row: 数据行字典，需包含 family_tags 字段。
        axis: 当前分配的轴字典。
        axis_by_id: 以 axis_id 为键的轴字典映射。

    Returns:
        list[str]: 行中存在但未出现在轴谱系触发标签中的家族标签列表。
    """
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
    """根据深度和行数返回审查优先级 P0/P1/P2。

    Args:
        axis: 目标轴字典，需包含 axis_depth 和 row_count 字段。

    Returns:
        str: 审查优先级字符串，"P0"（最高）、"P1" 或 "P2"。
    """
    if _axis_depth_value(axis) >= 2 or _axis_row_count(axis) <= 2:
        return "P0"
    if _axis_depth_value(axis) == 1:
        return "P1"
    return "P2"


def _suggested_next_action(axis: dict) -> str:
    """根据轴特征建议下一步动作。

    Args:
        axis: 目标轴字典，需包含 axis_depth 和 row_count 字段。

    Returns:
        str: 建议动作字符串，如 "expand_family_tagger"、"collect_more_examples"
            或 "prepare_programmatic_positive_signal"。
    """
    preferred_action = axis.get("main_follow_up_action")
    if preferred_action:
        return str(preferred_action)
    if _axis_depth_value(axis) >= 1:
        return "expand_family_tagger"
    if _axis_row_count(axis) <= 2:
        return "collect_more_examples"
    return "prepare_programmatic_positive_signal"


def _annotation_questions(row: dict, axis: dict, axis_by_id: dict[str, dict]) -> list[str]:
    """生成人工标注时的引导问题列表。

    Args:
        row: 数据行字典。
        axis: 当前分配的轴字典。
        axis_by_id: 以 axis_id 为键的轴字典映射。

    Returns:
        list[str]: 用于引导人工标注审查的问题字符串列表。
    """
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
    next_action = _suggested_next_action(axis)
    if next_action == "prepare_programmatic_positive_signal":
        questions.append("Check whether this axis should feed an implicit positive programmatic signal instead of prompt wording.")
    elif axis["axis_depth"] >= 1:
        questions.append("Check whether this child axis is stable enough to promote into the family tagger.")
    else:
        questions.append("Check whether this axis should stay as a broader offline asset while collecting more examples.")
    return questions


def _build_review_note(row: dict, axis: dict) -> str:
    """为审查行构建摘要说明文本。

    Args:
        row: 数据行字典。
        axis: 当前分配的轴字典。

    Returns:
        str: 描述该行归属及去重情况的摘要说明字符串。
    """
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
    """为每个轴构建审查桶摘要，包含分配行数、边界标签和示例等信息。

    Args:
        rows: 全部数据行列表。
        canonical_axes: 规范轴列表。
        bucket_counter: 以 axis_id 为键的已分配行数计数器。
        axis_by_id: 以 axis_id 为键的轴字典映射。
        assigned_axis_by_row_key: 以行键为键、分配的 axis_id 为值的映射。

    Returns:
        list[dict]: 每个轴对应的审查桶摘要字典列表。
    """
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
    """构建轴合并建议，汇总顶部轴的别名数、行数和 true miss 数。

    Args:
        canonical_axes: 已排序的规范轴列表。

    Returns:
        dict: 包含 top_axis_rule_ids 列表和 summary 文本的建议字典。
    """
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
    """构建审查优先级建议，按优先级和分配行数排序后给出顶部审查桶。

    Args:
        bucket_summary: 审查桶摘要列表，每个元素包含 review_priority、assigned_review_rows 等字段。

    Returns:
        dict: 包含 top_review_axis_rule_ids 列表和 summary 文本的建议字典。
    """
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
    """将轴合并摘要转为 Markdown 格式文本。

    Args:
        summary: 轴合并摘要字典，包含 canonical_axes、recommendation 等字段。

    Returns:
        str: 格式化的 Markdown 字符串，包含汇总表格和各轴详细信息。
    """
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
                f"- Main status: `{axis.get('main_status') or 'n/a'}`",
                f"- Prompt policy: `{axis.get('main_prompt_policy') or 'n/a'}`",
                f"- Suggested follow-up: `{_suggested_next_action(axis)}`",
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
    """生成标注清单 Markdown 文本，按优先级分组列出所有审查行。

    Args:
        review_rows: 审查行列表，每行包含 review_priority、problem_id、annotation_questions 等字段。

    Returns:
        str: 格式化的 Markdown 标注清单字符串。
    """
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
    """生成 P0/P1 审查模板 Markdown 文本，包含轴级和行级决策框架。

    Args:
        review_rows: 审查行列表，仅筛选 review_priority 为 P0 或 P1 的行。

    Returns:
        str: 格式化的 Markdown 审查模板字符串，包含会话元数据、轴级决策和行级审查结构。
    """
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
    """安全获取轴的行数。

    Args:
        axis: 轴字典，可能包含 row_count 或 row_keys 字段。

    Returns:
        int: 轴对应的行数，若 row_count 不存在则从 row_keys 推算。
    """
    row_count = axis.get("row_count")
    if row_count is not None:
        return int(row_count)
    return len(axis.get("row_keys") or [])


def _axis_depth_value(axis: dict) -> int:
    """安全获取轴深度值。

    Args:
        axis: 轴字典，可能包含 axis_depth 字段。

    Returns:
        int: 轴深度值，若字段不存在或为 None 则返回 0。
    """
    return int(axis.get("axis_depth") or 0)


def _axis_rank_index(axis: dict) -> int:
    """安全获取轴排名索引。

    Args:
        axis: 轴字典，可能包含 rank_index 字段。

    Returns:
        int: 排名索引值，若字段不存在或为 None 则返回 0。
    """
    return int(axis.get("rank_index") or 0)


def _axis_priority_score(axis: dict) -> float:
    """安全获取轴优先级分数。

    Args:
        axis: 轴字典，可能包含 priority_score 字段。

    Returns:
        float: 优先级分数，若字段不存在或为 None 则返回 0.0。
    """
    return float(axis.get("priority_score") or 0.0)


def _axis_true_miss_count(axis: dict, axis_rows: list[dict]) -> int:
    """获取轴中 true miss（answer=True 但 prediction 不为 True）的数量。

    Args:
        axis: 轴字典，可能包含 true_miss_count 字段。
        axis_rows: 轴对应的数据行列表，作为备选计算来源。

    Returns:
        int: true miss 数量，优先使用轴中缓存值，否则从行数据重新计算。
    """
    true_miss_count = axis.get("true_miss_count")
    if true_miss_count is not None:
        return int(true_miss_count)
    return sum(1 for row in axis_rows if row.get("answer") is True and row.get("prediction") is not True)


def _axis_recoverable_error_count(axis: dict, axis_rows: list[dict]) -> int:
    """获取轴中可恢复错误数（RULE_MISSING 和 HARD_COMPOSITION 类别之和）。

    Args:
        axis: 轴字典，可能包含 recoverable_error_count 字段。
        axis_rows: 轴对应的数据行列表，作为备选计算来源。

    Returns:
        int: 可恢复错误数量，优先使用轴中缓存值，否则从行数据重新计算。
    """
    recoverable_error_count = axis.get("recoverable_error_count")
    if recoverable_error_count is not None:
        return int(recoverable_error_count)
    return sum(
        1
        for row in axis_rows
        if infer_error_category(row) in {"RULE_MISSING", "HARD_COMPOSITION"}
    )


def _review_summary_to_markdown(summary: dict) -> str:
    """将审查集摘要转为 Markdown 格式文本。

    Args:
        summary: 审查集摘要字典，包含 bucket_summary、recommendation 等字段。

    Returns:
        str: 格式化的 Markdown 字符串，包含审查桶汇总表格和详细信息。
    """
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
    """收集错误类别计数，排除正确预测（CORRECT）的行。

    Args:
        rows: 数据行列表，每行将通过 infer_error_category 推断错误类别。

    Returns:
        Counter[str]: 以错误类别名称为键、出现次数为值的计数器。
    """
    buckets: Counter[str] = Counter()
    for row in rows:
        category = infer_error_category(row)
        if category == "CORRECT":
            continue
        buckets[category] += 1
    return buckets


def _load_json(path: str | Path) -> dict:
    """加载 JSON 文件并解析为字典。

    Args:
        path: JSON 文件路径，支持字符串或 Path 对象。

    Returns:
        dict: 解析后的 JSON 内容字典。
    """
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _row_key(row: dict) -> str:
    """生成行唯一键，优先使用 problem_id，否则拼接 source 和 equation 信息。

    Args:
        row: 数据行字典，可能包含 problem_id、source、equation1、equation2 字段。

    Returns:
        str: 该行的唯一标识字符串。
    """
    if row.get("problem_id"):
        return str(row["problem_id"])
    return f"{row.get('source', 'unknown')}::{row.get('equation1', '')} => {row.get('equation2', '')}"


def _row_label(row: dict) -> str:
    """生成行标签文本，优先使用 problem_id，否则拼接 equation 信息。

    Args:
        row: 数据行字典，可能包含 problem_id、equation1、equation2 字段。

    Returns:
        str: 用于展示的行标签字符串。
    """
    if row.get("problem_id"):
        return str(row["problem_id"])
    return f"{row.get('equation1', '')} => {row.get('equation2', '')}"


def _unique_preserving_order(items) -> list[str]:
    """对可迭代对象去重并保持原始出现顺序。

    Args:
        items: 可迭代对象，元素将被转为字符串后去重。

    Returns:
        list[str]: 去重后的字符串列表，保持首次出现的顺序。
    """
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
    """格式化错误桶为字符串，按计数降序和名称升序排列。

    Args:
        buckets: 以错误类别名称为键、计数为值的字典。

    Returns:
        str: 格式化后的字符串，如 "RULE_MISSING=3, HARD_COMPOSITION=1"；若为空则返回 "none"。
    """
    if not buckets:
        return "none"
    return ", ".join(f"{name}={count}" for name, count in sorted(buckets.items(), key=lambda item: (-item[1], item[0])))


def _fmt_rate(value: float | None) -> str:
    """格式化比率为 4 位小数字符串。

    Args:
        value: 待格式化的数值，可以为 None。

    Returns:
        str: 保留 4 位小数的字符串；若值为 None 则返回 "n/a"。
    """
    if value is None:
        return "n/a"
    return f"{value:.4f}"
