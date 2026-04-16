from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from sair_competition.data.io import read_jsonl


DEFAULT_SIGNAL_KEYS = [
    "eq1_lhs_lone_var_absent_from_rhs",
    "shared_lhs_alpha",
    "eq1_singleton_side",
    "eq1_disjoint_shape",
    "eq1_rhs_eq1_lhs_var_count",
    "eq1_rhs_non_lhs_eq1_var_count",
    "eq2_rhs_reuses_eq1_lhs_var",
    "eq2_rhs_eq1_lhs_var_count",
    "eq2_rhs_retains_non_lhs_eq1_var",
    "eq2_rhs_retained_non_lhs_eq1_var_count",
    "eq2_rhs_has_lhs_amplification_anchor",
    "eq2_rhs_new_var_count",
    "eq2_rhs_reuses_all_non_lhs_eq1_vars",
]


def prepare_positive_signal_candidate(
    tagged_dataset_path: str | Path,
    target_tag: str,
    output_dir: str | Path,
    boundary_tags: list[str] | None = None,
    rule_assets_path: str | Path | None = None,
    signal_keys: list[str] | None = None,
) -> dict:
    """Prepare an offline positive-signal candidate report for a target family tag."""

    rows = read_jsonl(tagged_dataset_path)
    boundary_tags = boundary_tags or []
    signal_keys = signal_keys or list(DEFAULT_SIGNAL_KEYS)

    target_rows = [row for row in rows if target_tag in set(row.get("family_tags") or [])]
    if not target_rows:
        raise ValueError(f"No rows matched target tag: {target_tag}")

    target_summary = _row_summary(target_rows)
    target_ids = [_row_label(row) for row in target_rows]
    target_id_set = set(target_ids)

    boundary_summaries = []
    for boundary_tag in boundary_tags:
        boundary_rows = [
            row
            for row in rows
            if boundary_tag in set(row.get("family_tags") or []) and target_tag not in set(row.get("family_tags") or [])
        ]
        boundary_summaries.append(
            {
                "boundary_tag": boundary_tag,
                **_row_summary(boundary_rows),
                "example_ids": [_row_label(row) for row in boundary_rows[:12]],
            }
        )

    signal_profile = _build_signal_profile(target_rows, signal_keys)
    overlap_summary = _build_asset_overlap_summary(rows, target_id_set, rule_assets_path)

    summary = {
        "tagged_dataset_path": str(tagged_dataset_path),
        "target_tag": target_tag,
        "boundary_tags": boundary_tags,
        "target_summary": target_summary,
        "target_ids": target_ids,
        "target_source_answer_breakdown": _source_answer_breakdown(target_rows),
        "signal_profile": signal_profile,
        "boundary_summaries": boundary_summaries,
        "asset_overlap_summary": overlap_summary,
        "recommendation": _build_recommendation(target_summary, boundary_summaries, overlap_summary),
    }

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_root / "summary.md").write_text(_to_markdown(summary), encoding="utf-8")
    return summary


def _row_summary(rows: list[dict]) -> dict:
    answer_counter = Counter(row.get("answer") for row in rows)
    source_counter = Counter(row.get("source") or "unknown" for row in rows)
    split_counter = Counter(row.get("split") or "unknown" for row in rows)
    total = len(rows)
    true_count = int(answer_counter.get(True, 0))
    false_count = int(answer_counter.get(False, 0))
    return {
        "row_count": total,
        "true_count": true_count,
        "false_count": false_count,
        "true_rate": (true_count / total) if total else None,
        "split_counts": dict(sorted(split_counter.items())),
        "source_counts": dict(sorted(source_counter.items())),
        "example_ids": [_row_label(row) for row in rows[:12]],
    }


def _source_answer_breakdown(rows: list[dict]) -> dict[str, dict[str, int]]:
    summary: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        source = row.get("source") or "unknown"
        answer = "true" if row.get("answer") is True else "false"
        summary[source][answer] += 1
    return {source: dict(counter) for source, counter in sorted(summary.items())}


def _build_signal_profile(rows: list[dict], signal_keys: list[str]) -> dict[str, dict]:
    profile: dict[str, dict] = {}
    for key in signal_keys:
        values = [row.get("family_signals", {}).get(key) for row in rows if key in (row.get("family_signals") or {})]
        if not values:
            continue
        unique_values = list(dict.fromkeys(_normalize_signal_value(value) for value in values))
        if len(unique_values) == 1:
            profile[key] = {"kind": "invariant", "value": unique_values[0]}
            continue

        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            profile[key] = {
                "kind": "numeric_range",
                "min": min(values),
                "max": max(values),
                "unique_values": sorted({int(value) if isinstance(value, bool) else value for value in values})[:12],
            }
            continue

        profile[key] = {
            "kind": "categorical",
            "unique_values": unique_values[:12],
        }
    return profile


def _build_asset_overlap_summary(
    rows: list[dict],
    target_id_set: set[str],
    rule_assets_path: str | Path | None,
) -> list[dict]:
    if not rule_assets_path:
        return []

    assets = _load_rule_assets(rule_assets_path)
    overlap_rows: list[dict] = []
    for asset in assets:
        trigger_tags = set(asset.get("trigger_tags") or [])
        if not trigger_tags:
            continue
        matched_ids = {
            _row_label(row)
            for row in rows
            if trigger_tags.issubset(set(row.get("family_tags") or []))
        }
        overlap_count = len(target_id_set & matched_ids)
        if overlap_count == 0:
            continue
        overlap_rows.append(
            {
                "rule_id": asset.get("rule_id"),
                "primary_tag": asset.get("primary_tag"),
                "overlap_count": overlap_count,
                "target_coverage": overlap_count / len(target_id_set) if target_id_set else None,
                "matched_row_count": len(matched_ids),
                "jaccard": overlap_count / len(target_id_set | matched_ids) if (target_id_set | matched_ids) else None,
                "follow_up_action": asset.get("follow_up_action"),
            }
        )

    return sorted(
        overlap_rows,
        key=lambda row: (row["overlap_count"], row["target_coverage"] or 0.0, row["jaccard"] or 0.0),
        reverse=True,
    )


def _load_rule_assets(path: str | Path) -> list[dict]:
    target = Path(path)
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return read_jsonl(target)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return [payload]
    raise ValueError(f"Unsupported rule asset format: {path}")


def _build_recommendation(target_summary: dict, boundary_summaries: list[dict], overlap_summary: list[dict]) -> dict:
    clean_target = target_summary["false_count"] == 0
    false_heavy_boundaries = [
        item["boundary_tag"]
        for item in boundary_summaries
        if item["row_count"] > 0 and item["false_count"] > item["true_count"]
    ]
    top_overlaps = [item["rule_id"] for item in overlap_summary[:5]]
    return {
        "is_clean_target": clean_target,
        "support_total": target_summary["row_count"],
        "false_heavy_boundary_tags": false_heavy_boundaries,
        "top_overlapping_rule_ids": top_overlaps,
        "suggested_status": (
            "ready_for_offline_programmatic_preparation"
            if clean_target and target_summary["row_count"] >= 5
            else "keep_observing"
        ),
    }


def _normalize_signal_value(value):
    if isinstance(value, list):
        return list(value)
    return value


def _row_label(row: dict) -> str:
    return str(row.get("problem_id") or "<unknown>")


def _to_markdown(summary: dict) -> str:
    target = summary["target_summary"]
    lines = [
        "# Positive Signal Candidate Preparation",
        "",
        f"- Dataset: `{summary['tagged_dataset_path']}`",
        f"- Target tag: `{summary['target_tag']}`",
        f"- Rows: `{target['row_count']}`",
        f"- True / False: `{target['true_count']} / {target['false_count']}`",
        f"- True rate: `{_fmt_rate(target['true_rate'])}`",
        "",
        "## Trigger Snapshot",
        "",
    ]

    for key, details in summary["signal_profile"].items():
        if details["kind"] == "invariant":
            lines.append(f"- `{key}`: invariant = `{details['value']}`")
        elif details["kind"] == "numeric_range":
            values = ", ".join(str(value) for value in details["unique_values"])
            lines.append(f"- `{key}`: min=`{details['min']}`, max=`{details['max']}`, values=`{values}`")
        else:
            values = ", ".join(str(value) for value in details["unique_values"])
            lines.append(f"- `{key}`: values=`{values}`")

    lines.extend(
        [
            "",
            "## Hit List",
            "",
            f"- All hit ids: `{', '.join(summary['target_ids'])}`",
            f"- Source/answer breakdown: `{json.dumps(summary['target_source_answer_breakdown'], ensure_ascii=False)}`",
            "",
            "## Boundary Tags",
            "",
        ]
    )

    if not summary["boundary_summaries"]:
        lines.append("- none")
    else:
        for item in summary["boundary_summaries"]:
            lines.append(
                "- `{tag}`: rows={rows}, true={true_count}, false={false_count}, true_rate={true_rate}, examples=`{examples}`".format(
                    tag=item["boundary_tag"],
                    rows=item["row_count"],
                    true_count=item["true_count"],
                    false_count=item["false_count"],
                    true_rate=_fmt_rate(item["true_rate"]),
                    examples=", ".join(item["example_ids"]) if item["example_ids"] else "none",
                )
            )

    lines.extend(
        [
            "",
            "## Asset Overlap",
            "",
        ]
    )

    if not summary["asset_overlap_summary"]:
        lines.append("- none")
    else:
        for item in summary["asset_overlap_summary"][:12]:
            lines.append(
                "- `{rule_id}`: overlap={overlap}, target_coverage={coverage}, jaccard={jaccard}, matched_rows={rows}, follow_up={follow_up}".format(
                    rule_id=item["rule_id"],
                    overlap=item["overlap_count"],
                    coverage=_fmt_rate(item["target_coverage"]),
                    jaccard=_fmt_rate(item["jaccard"]),
                    rows=item["matched_row_count"],
                    follow_up=item["follow_up_action"] or "none",
                )
            )

    recommendation = summary["recommendation"]
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            f"- Suggested status: `{recommendation['suggested_status']}`",
            f"- Clean target: `{recommendation['is_clean_target']}`",
            f"- False-heavy boundary tags: `{', '.join(recommendation['false_heavy_boundary_tags']) if recommendation['false_heavy_boundary_tags'] else 'none'}`",
            f"- Top overlapping rule ids: `{', '.join(recommendation['top_overlapping_rule_ids']) if recommendation['top_overlapping_rule_ids'] else 'none'}`",
        ]
    )
    return "\n".join(lines) + "\n"


def _fmt_rate(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.4f}"
