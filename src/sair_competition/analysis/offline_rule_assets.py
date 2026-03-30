from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

from sair_competition.analysis.error_report import infer_error_category
from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.eval.metrics import compute_metrics


@dataclass(frozen=True, slots=True)
class RuleAssetTemplate:
    rule_id: str
    family_focus_group: str
    primary_tag: str
    trigger_tags: tuple[str, ...]
    rule_text: str
    rule_type: str
    notes: str


@dataclass(slots=True)
class OfflineRuleAsset:
    rule_id: str
    family_focus_group: str
    primary_tag: str
    trigger_tags: list[str]
    rule_text: str
    rule_type: str
    source: str
    confidence: str
    support_total: int
    support_true_count: int
    support_false_count: int
    support_true_rate: float | None
    support_examples: list[str] = field(default_factory=list)
    failure_examples: list[str] = field(default_factory=list)
    current_mainline_accuracy: float | None = None
    current_mainline_true_accuracy: float | None = None
    current_mainline_error_buckets: dict[str, int] = field(default_factory=dict)
    opportunity_score: float | None = None
    usage_mode: str = "offline_rule_asset"
    prompt_policy: str = "do_not_inherit_wording"
    status: str = "candidate_offline"
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


RULE_ASSET_TEMPLATES: tuple[RuleAssetTemplate, ...] = (
    RuleAssetTemplate(
        rule_id="OA_TRUE_SINGLETON_LHS_TO_BINARY",
        family_focus_group="singleton_collapse",
        primary_tag="EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
        trigger_tags=("EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",),
        rule_text=(
            "If Equation 1 has the narrow shape x = T with x absent from T and T is binary, "
            "treat this as a singleton-collapse family and record it as a safe offline TRUE asset."
        ),
        rule_type="positive_collapse",
        notes="Core singleton-collapse entry point. Keep offline unless smoke proves wording stability.",
    ),
    RuleAssetTemplate(
        rule_id="OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS",
        family_focus_group="singleton_collapse",
        primary_tag="EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
        trigger_tags=("EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",),
        rule_text=(
            "If singleton-collapse already fires and Equation 2 keeps the same left-hand-side skeleton, "
            "treat the case as a high-confidence TRUE family for offline use."
        ),
        rule_type="positive_collapse",
        notes="Useful for same-left-hand-side true families mined from P1_2_5.",
    ),
    RuleAssetTemplate(
        rule_id="OA_TRUE_SINGLETON_WITH_TARGET_NEW_VARS",
        family_focus_group="singleton_collapse",
        primary_tag="EQ1_SINGLETON_COLLAPSE_WITH_TARGET_NEW_VARS",
        trigger_tags=("EQ1_SINGLETON_COLLAPSE_WITH_TARGET_NEW_VARS",),
        rule_text=(
            "If singleton-collapse already fires, fresh variables introduced by Equation 2 do not block truth; "
            "keep this as an offline TRUE family rather than prompt wording."
        ),
        rule_type="positive_collapse",
        notes="Small but especially valuable because it guards against false heuristics based on new variables.",
    ),
    RuleAssetTemplate(
        rule_id="OA_TRUE_DISJOINT_VAR_BINARY",
        family_focus_group="disjoint_sides",
        primary_tag="EQ1_DISJOINT_SIDES_VAR_BINARY",
        trigger_tags=("EQ1_DISJOINT_SIDES_VAR_BINARY",),
        rule_text=(
            "If Equation 1 uses disjoint variable sets and has a variable-vs-binary shape, "
            "treat it as a narrow collapse family and store it as an offline TRUE asset."
        ),
        rule_type="positive_collapse",
        notes="This is the dominant disjoint-sides shape on smoke and is cleanly true-heavy.",
    ),
    RuleAssetTemplate(
        rule_id="OA_TRUE_DISJOINT_BINARY_BINARY",
        family_focus_group="disjoint_sides",
        primary_tag="EQ1_DISJOINT_SIDES_BINARY_BINARY",
        trigger_tags=("EQ1_DISJOINT_SIDES_BINARY_BINARY",),
        rule_text=(
            "If Equation 1 uses disjoint variable sets and both sides are binary terms, "
            "treat it as a rare but structurally strong offline TRUE family."
        ),
        rule_type="positive_collapse",
        notes="Low-support subfamily; keep as candidate until more data accumulates.",
    ),
    RuleAssetTemplate(
        rule_id="OA_TRUE_DISJOINT_WITH_TARGET_SHARED_LHS",
        family_focus_group="disjoint_sides",
        primary_tag="EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS",
        trigger_tags=("EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS",),
        rule_text=(
            "When disjoint-sides collapse already holds and Equation 2 keeps the same left-hand-side skeleton, "
            "store the pattern as an offline TRUE family."
        ),
        rule_type="positive_collapse",
        notes="High-support combination that is currently undercaptured by P1_2_3.",
    ),
    RuleAssetTemplate(
        rule_id="OA_TRUE_CONSTANT_VAR_BINARY",
        family_focus_group="constant_operation_candidate",
        primary_tag="EQ1_CONSTANT_OPERATION_VAR_BINARY",
        trigger_tags=("EQ1_CONSTANT_OPERATION_VAR_BINARY",),
        rule_text=(
            "If Equation 1 is a constant-operation candidate with a variable-vs-binary shape, "
            "store it as an offline TRUE family for future programmatic use."
        ),
        rule_type="positive_collapse",
        notes="Strong overlap with singleton/disjoint families, but still worth a separate asset view.",
    ),
    RuleAssetTemplate(
        rule_id="OA_TRUE_CONSTANT_WITH_TARGET_SHARED_LHS",
        family_focus_group="constant_operation_candidate",
        primary_tag="EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS",
        trigger_tags=("EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS",),
        rule_text=(
            "If constant-operation collapse is plausible and Equation 2 keeps the same left-hand-side skeleton, "
            "treat the pattern as an offline TRUE family candidate."
        ),
        rule_type="positive_collapse",
        notes="High-support combination that may later feed a feature or ranker, not prompt wording.",
    ),
    RuleAssetTemplate(
        rule_id="OA_TRUE_CONSTANT_WITH_TARGET_NEW_VARS",
        family_focus_group="constant_operation_candidate",
        primary_tag="EQ1_CONSTANT_OPERATION_WITH_TARGET_NEW_VARS",
        trigger_tags=("EQ1_CONSTANT_OPERATION_WITH_TARGET_NEW_VARS",),
        rule_text=(
            "If constant-operation collapse is already active, fresh variables in Equation 2 should not by themselves "
            "push the case toward false; keep this as an offline TRUE family asset."
        ),
        rule_type="positive_collapse",
        notes="Small-support corrective asset against overly strong false heuristics.",
    ),
)


def build_offline_rule_assets(
    tagged_dataset_path: str | Path,
    output_path: str | Path,
    error_summary_path: str | Path | None = None,
    report_path: str | Path | None = None,
) -> dict:
    """Build a machine-readable bundle of offline rule assets from tagged families."""

    rows = read_jsonl(tagged_dataset_path)
    error_summary = _load_optional_json(error_summary_path)

    assets: list[OfflineRuleAsset] = []
    for template in RULE_ASSET_TEMPLATES:
        matching_rows = [
            row for row in rows if _matches_all_tags(row.get("family_tags") or [], template.trigger_tags)
        ]
        if not matching_rows:
            continue

        true_rows = [row for row in matching_rows if row.get("answer") is True]
        false_rows = [row for row in matching_rows if row.get("answer") is False]
        slice_metrics, slice_buckets = _extract_mainline_slice(error_summary, template.primary_tag)

        asset = OfflineRuleAsset(
            rule_id=template.rule_id,
            family_focus_group=template.family_focus_group,
            primary_tag=template.primary_tag,
            trigger_tags=list(template.trigger_tags),
            rule_text=template.rule_text,
            rule_type=template.rule_type,
            source=_build_source(tagged_dataset_path, error_summary_path),
            confidence=_infer_confidence(true_count=len(true_rows), false_count=len(false_rows)),
            support_total=len(matching_rows),
            support_true_count=len(true_rows),
            support_false_count=len(false_rows),
            support_true_rate=_safe_rate(len(true_rows), len(matching_rows)),
            support_examples=[_row_label(row) for row in true_rows[:8]],
            failure_examples=[_row_label(row) for row in false_rows[:5]],
            current_mainline_accuracy=slice_metrics.get("accuracy"),
            current_mainline_true_accuracy=slice_metrics.get("true_accuracy"),
            current_mainline_error_buckets=slice_buckets,
            opportunity_score=_compute_opportunity_score(
                support_true_count=len(true_rows),
                support_false_count=len(false_rows),
                current_mainline_accuracy=slice_metrics.get("accuracy"),
            ),
            status=_infer_status(
                true_count=len(true_rows),
                false_count=len(false_rows),
                current_mainline_accuracy=slice_metrics.get("accuracy"),
            ),
            notes=template.notes,
        )
        assets.append(asset)

    ranked_assets = sorted(
        assets,
        key=lambda asset: (
            asset.opportunity_score if asset.opportunity_score is not None else -1.0,
            asset.support_true_count,
            asset.rule_id,
        ),
        reverse=True,
    )

    target = Path(output_path)
    write_jsonl(target, [asset.to_dict() for asset in ranked_assets])

    summary = {
        "tagged_dataset_path": str(tagged_dataset_path),
        "error_summary_path": str(error_summary_path) if error_summary_path else None,
        "output_path": str(target),
        "asset_count": len(ranked_assets),
        "ranked_rule_assets": [asset.to_dict() for asset in ranked_assets],
        "recommendation": _build_recommendation(ranked_assets),
    }

    report_target = Path(report_path) if report_path else target.with_suffix(".md")
    report_target.parent.mkdir(parents=True, exist_ok=True)
    report_target.write_text(_to_markdown(summary), encoding="utf-8")
    (report_target.with_suffix(".json")).write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def load_offline_rule_assets(path: str | Path) -> list[dict]:
    """Load offline rule assets from a JSONL bundle."""

    return read_jsonl(path)


def attach_offline_rule_assets(
    input_path: str | Path,
    rule_assets_path: str | Path,
    output_path: str | Path,
) -> dict:
    """Attach matching offline rule-asset ids to rows that already carry family tags."""

    rows = read_jsonl(input_path)
    rule_assets = load_offline_rule_assets(rule_assets_path)

    enriched_rows: list[dict] = []
    matched_row_count = 0
    asset_match_counts: Counter[str] = Counter()

    for row in rows:
        matched_assets = match_offline_rule_assets(row, rule_assets)
        enriched_row = dict(row)
        enriched_row["offline_rule_asset_ids"] = [asset["rule_id"] for asset in matched_assets]
        enriched_row["offline_rule_asset_groups"] = _unique_preserving_order(
            asset["family_focus_group"] for asset in matched_assets if asset.get("family_focus_group")
        )
        enriched_row["offline_rule_asset_match_count"] = len(matched_assets)
        if matched_assets:
            matched_row_count += 1
        for asset in matched_assets:
            asset_match_counts[asset["rule_id"]] += 1
        enriched_rows.append(enriched_row)

    target = Path(output_path)
    write_jsonl(target, enriched_rows)

    summary = {
        "input_path": str(input_path),
        "rule_assets_path": str(rule_assets_path),
        "output_path": str(target),
        "row_count": len(rows),
        "matched_row_count": matched_row_count,
        "unmatched_row_count": len(rows) - matched_row_count,
        "asset_match_counts": dict(asset_match_counts),
    }
    (target.parent / "attach_offline_rule_assets_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def audit_offline_rule_assets(
    predictions_path: str | Path,
    rule_assets_path: str | Path,
    output_dir: str | Path,
) -> dict:
    """Audit how each offline rule asset behaves on a prediction file."""

    rows = read_jsonl(predictions_path)
    rule_assets = load_offline_rule_assets(rule_assets_path)
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    asset_summaries: list[dict] = []
    for asset in rule_assets:
        subset = [row for row in rows if row_matches_offline_rule_asset(row, asset)]
        if not subset:
            continue

        metrics = compute_metrics(subset).to_dict()
        error_buckets = _collect_error_buckets(subset)
        true_miss_examples = [
            _row_label(row)
            for row in subset
            if row.get("answer") is True and row.get("prediction") is not True
        ][:8]
        false_positive_examples = [
            _row_label(row)
            for row in subset
            if row.get("answer") is False and row.get("prediction") is True
        ][:8]
        summary_row = {
            "rule_id": asset["rule_id"],
            "family_focus_group": asset.get("family_focus_group"),
            "primary_tag": asset.get("primary_tag"),
            "trigger_tags": list(asset.get("trigger_tags") or []),
            "status": asset.get("status"),
            "prompt_policy": asset.get("prompt_policy"),
            "row_count": len(subset),
            "metrics": metrics,
            "error_count": sum(error_buckets.values()),
            "error_buckets": dict(error_buckets),
            "true_miss_count": sum(
                1 for row in subset if row.get("answer") is True and row.get("prediction") is not True
            ),
            "false_positive_count": sum(
                1 for row in subset if row.get("answer") is False and row.get("prediction") is True
            ),
            "recoverable_error_count": error_buckets.get("RULE_MISSING", 0) + error_buckets.get("HARD_COMPOSITION", 0),
            "bundle_opportunity_score": asset.get("opportunity_score"),
            "priority_score": _compute_audit_priority(asset, error_buckets, subset),
            "true_miss_examples": true_miss_examples,
            "false_positive_examples": false_positive_examples,
            "sample_matches": [_row_label(row) for row in subset[:8]],
        }
        asset_summaries.append(summary_row)

    ranked_assets = sorted(
        asset_summaries,
        key=lambda item: (
            item["priority_score"],
            item["recoverable_error_count"],
            item["true_miss_count"],
            item["row_count"],
            item["rule_id"],
        ),
        reverse=True,
    )

    summary = {
        "predictions_path": str(predictions_path),
        "rule_assets_path": str(rule_assets_path),
        "output_dir": str(output_root),
        "audited_asset_count": len(ranked_assets),
        "ranked_assets": ranked_assets,
        "recommendation": _build_audit_recommendation(ranked_assets),
    }
    (output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_root / "summary.md").write_text(_audit_to_markdown(summary), encoding="utf-8")
    return summary


def match_offline_rule_assets(row: dict, rule_assets: list[dict]) -> list[dict]:
    """Return the offline rule assets whose trigger tags all fire for the row."""

    matched_assets = [asset for asset in rule_assets if row_matches_offline_rule_asset(row, asset)]
    return sorted(matched_assets, key=lambda asset: asset["rule_id"])


def row_matches_offline_rule_asset(row: dict, asset: dict) -> bool:
    existing_asset_ids = set(row.get("offline_rule_asset_ids") or [])
    if asset.get("rule_id") in existing_asset_ids:
        return True
    row_tags = row.get("family_tags") or []
    required_tags = tuple(asset.get("trigger_tags") or [])
    if not required_tags:
        return False
    return _matches_all_tags(row_tags, required_tags)


def _matches_all_tags(row_tags: list[str], required_tags: tuple[str, ...]) -> bool:
    row_tag_set = set(row_tags)
    return all(tag in row_tag_set for tag in required_tags)


def _build_source(tagged_dataset_path: str | Path, error_summary_path: str | Path | None) -> str:
    if error_summary_path:
        return f"{tagged_dataset_path} + {error_summary_path}"
    return str(tagged_dataset_path)


def _load_optional_json(path: str | Path | None) -> dict:
    if path is None:
        return {}
    target = Path(path)
    if not target.exists():
        return {}
    return json.loads(target.read_text(encoding="utf-8"))


def _extract_mainline_slice(error_summary: dict, primary_tag: str) -> tuple[dict, dict[str, int]]:
    family_tag_summary = error_summary.get("family_tag_summary") or {}
    details = family_tag_summary.get(primary_tag) or {}
    return details.get("metrics") or {}, details.get("error_buckets") or {}


def _infer_confidence(true_count: int, false_count: int) -> str:
    if false_count == 0 and true_count >= 10:
        return "high"
    if false_count == 0 and true_count >= 2:
        return "medium"
    if false_count <= 1 and true_count >= 5:
        return "medium"
    return "low"


def _infer_status(true_count: int, false_count: int, current_mainline_accuracy: float | None) -> str:
    if false_count == 0 and true_count >= 10 and (current_mainline_accuracy is None or current_mainline_accuracy < 0.5):
        return "active_offline"
    if false_count == 0 and true_count >= 2:
        return "candidate_offline"
    return "needs_review"


def _compute_opportunity_score(
    support_true_count: int,
    support_false_count: int,
    current_mainline_accuracy: float | None,
) -> float | None:
    if support_true_count + support_false_count == 0:
        return None
    cleanliness = support_true_count / max(support_true_count + support_false_count, 1)
    gap = 1.0 if current_mainline_accuracy is None else max(0.0, 1.0 - current_mainline_accuracy)
    return round(cleanliness * gap * support_true_count, 6)


def _row_label(row: dict) -> str:
    if row.get("problem_id"):
        return str(row["problem_id"])
    return f"{row.get('equation1', '')} => {row.get('equation2', '')}"


def _safe_rate(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def _build_recommendation(assets: list[OfflineRuleAsset]) -> dict:
    if not assets:
        return {"summary": "No offline rule assets were generated."}

    top_assets = assets[:3]
    summary = "Prioritize the top offline assets with clean true support and low current mainline slice accuracy: "
    summary += ", ".join(
        f"{asset.rule_id}(support_true={asset.support_true_count}, mainline_acc={_fmt_rate(asset.current_mainline_accuracy)})"
        for asset in top_assets
    )
    summary += ". Keep them offline-first; do not promote wording into P1_2_3 without a dedicated smoke branch."
    return {
        "top_rule_ids": [asset.rule_id for asset in top_assets],
        "summary": summary,
    }


def _build_audit_recommendation(asset_summaries: list[dict]) -> dict:
    if not asset_summaries:
        return {"summary": "No offline rule assets matched the provided predictions."}

    top_assets = asset_summaries[:3]
    summary = "Prioritize offline assets that still map to missed true slices on the current mainline: "
    summary += ", ".join(
        (
            f"{asset['rule_id']}(recoverable={asset['recoverable_error_count']}, "
            f"true_miss={asset['true_miss_count']}, priority={_fmt_rate(asset['priority_score'])})"
        )
        for asset in top_assets
    )
    summary += ". Keep them offline-first and use them to drive tagging, slicing, or future implicit injection experiments."
    return {
        "top_rule_ids": [asset["rule_id"] for asset in top_assets],
        "summary": summary,
    }


def _to_markdown(summary: dict) -> str:
    lines = [
        "# Offline Rule Assets",
        "",
        f"- Tagged dataset: `{summary['tagged_dataset_path']}`",
        f"- Error summary: `{summary['error_summary_path']}`",
        f"- Output path: `{summary['output_path']}`",
        f"- Asset count: `{summary['asset_count']}`",
        "",
        "| Rule ID | Family | Support True | Support False | True Rate | Mainline Acc | Opportunity | Status |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for asset in summary["ranked_rule_assets"]:
        lines.append(
            "| {rule_id} | {family} | {true_count} | {false_count} | {true_rate} | {mainline_acc} | {opportunity} | {status} |".format(
                rule_id=asset["rule_id"],
                family=asset["family_focus_group"],
                true_count=asset["support_true_count"],
                false_count=asset["support_false_count"],
                true_rate=_fmt_rate(asset["support_true_rate"]),
                mainline_acc=_fmt_rate(asset["current_mainline_accuracy"]),
                opportunity=_fmt_rate(asset["opportunity_score"]),
                status=asset["status"],
            )
        )

    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            summary["recommendation"]["summary"],
            "",
            "## Rule Details",
            "",
        ]
    )

    for asset in summary["ranked_rule_assets"]:
        lines.extend(
            [
                f"### {asset['rule_id']}",
                "",
                f"- Family: `{asset['family_focus_group']}`",
                f"- Trigger tags: `{', '.join(asset['trigger_tags'])}`",
                f"- Rule type: `{asset['rule_type']}`",
                f"- Confidence: `{asset['confidence']}`",
                f"- Support: true={asset['support_true_count']}, false={asset['support_false_count']}, true_rate={_fmt_rate(asset['support_true_rate'])}",
                f"- Current mainline slice accuracy: `{_fmt_rate(asset['current_mainline_accuracy'])}`",
                f"- Current mainline slice true accuracy: `{_fmt_rate(asset['current_mainline_true_accuracy'])}`",
                f"- Status: `{asset['status']}`",
                f"- Prompt policy: `{asset['prompt_policy']}`",
                f"- Rule text: {asset['rule_text']}",
                f"- Notes: {asset['notes']}",
                f"- Support examples: `{', '.join(asset['support_examples']) if asset['support_examples'] else 'none'}`",
                f"- Failure examples: `{', '.join(asset['failure_examples']) if asset['failure_examples'] else 'none'}`",
                f"- Mainline error buckets: `{_format_buckets(asset['current_mainline_error_buckets'])}`",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def _audit_to_markdown(summary: dict) -> str:
    lines = [
        "# Offline Rule Asset Audit",
        "",
        f"- Predictions: `{summary['predictions_path']}`",
        f"- Rule assets: `{summary['rule_assets_path']}`",
        f"- Audited asset count: `{summary['audited_asset_count']}`",
        "",
        "| Rule ID | Rows | Accuracy | True Acc | Recoverable Errors | True Miss | False Positive | Priority |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for asset in summary["ranked_assets"]:
        lines.append(
            "| {rule_id} | {rows} | {accuracy} | {true_acc} | {recoverable} | {true_miss} | {false_positive} | {priority} |".format(
                rule_id=asset["rule_id"],
                rows=asset["row_count"],
                accuracy=_fmt_rate(asset["metrics"]["accuracy"]),
                true_acc=_fmt_rate(asset["metrics"].get("true_accuracy")),
                recoverable=asset["recoverable_error_count"],
                true_miss=asset["true_miss_count"],
                false_positive=asset["false_positive_count"],
                priority=_fmt_rate(asset["priority_score"]),
            )
        )

    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            summary["recommendation"]["summary"],
            "",
            "## Asset Details",
            "",
        ]
    )

    for asset in summary["ranked_assets"]:
        lines.extend(
            [
                f"### {asset['rule_id']}",
                "",
                f"- Family: `{asset['family_focus_group']}`",
                f"- Primary tag: `{asset['primary_tag']}`",
                f"- Trigger tags: `{', '.join(asset['trigger_tags']) if asset['trigger_tags'] else 'none'}`",
                f"- Status: `{asset['status']}`",
                f"- Prompt policy: `{asset['prompt_policy']}`",
                f"- Rows: `{asset['row_count']}`",
                f"- Accuracy: `{_fmt_rate(asset['metrics']['accuracy'])}`",
                f"- True accuracy: `{_fmt_rate(asset['metrics'].get('true_accuracy'))}`",
                f"- False accuracy: `{_fmt_rate(asset['metrics'].get('false_accuracy'))}`",
                f"- Recoverable errors: `{asset['recoverable_error_count']}`",
                f"- True misses: `{asset['true_miss_count']}`",
                f"- False positives: `{asset['false_positive_count']}`",
                f"- Error buckets: `{_format_buckets(asset['error_buckets'])}`",
                f"- Priority score: `{_fmt_rate(asset['priority_score'])}`",
                f"- Bundle opportunity score: `{_fmt_rate(asset.get('bundle_opportunity_score'))}`",
                f"- Sample matches: `{', '.join(asset['sample_matches']) if asset['sample_matches'] else 'none'}`",
                f"- True miss examples: `{', '.join(asset['true_miss_examples']) if asset['true_miss_examples'] else 'none'}`",
                f"- False positive examples: `{', '.join(asset['false_positive_examples']) if asset['false_positive_examples'] else 'none'}`",
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


def _compute_audit_priority(asset: dict, error_buckets: Counter[str], rows: list[dict]) -> float:
    recoverable = error_buckets.get("RULE_MISSING", 0) + error_buckets.get("HARD_COMPOSITION", 0)
    true_misses = sum(1 for row in rows if row.get("answer") is True and row.get("prediction") is not True)
    false_positives = sum(1 for row in rows if row.get("answer") is False and row.get("prediction") is True)
    bundle_opportunity = float(asset.get("opportunity_score") or 0.0)
    return round((recoverable * 2.0) + true_misses + (0.1 * bundle_opportunity) - false_positives, 6)


def _unique_preserving_order(items: list[str] | tuple[str, ...] | object) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for item in items:
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
