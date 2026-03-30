from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from sair_competition.data.io import read_jsonl
from sair_competition.eval.metrics import compute_metrics
from sair_competition.features.family_tagger import FAMILY_FOCUS_GROUPS
from sair_competition.parse.equations import canonicalize_equation, count_binary_ops, extract_variables


def analyze_prediction_errors(predictions_path: str | Path, output_dir: str | Path) -> dict:
    """Build a lightweight error report from prediction rows."""

    rows = read_jsonl(predictions_path)
    metrics = compute_metrics(rows)
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    error_buckets: Counter[str] = Counter()
    by_source: dict[str, Counter[str]] = defaultdict(Counter)
    family_tag_rows: Counter[str] = Counter()
    hard_examples: list[dict] = []

    for row in rows:
        category = infer_error_category(row)
        family_tags = list(dict.fromkeys(row.get("family_tags") or []))
        for tag in family_tags:
            family_tag_rows[tag] += 1
        if category == "CORRECT":
            continue
        error_buckets[category] += 1
        by_source[row.get("source") or "unknown"][category] += 1
        if len(hard_examples) < 25:
            hard_examples.append(
                {
                    "problem_id": row.get("problem_id"),
                    "source": row.get("source"),
                    "answer": row.get("answer"),
                    "prediction": row.get("prediction"),
                    "parsed": row.get("parsed"),
                    "category": category,
                    "equation1": row.get("equation1"),
                    "equation2": row.get("equation2"),
                    "family_tags": family_tags,
                    "raw_output_preview": (row.get("raw_output") or "")[:500],
                }
            )

    summary = {
        "predictions_path": str(predictions_path),
        "row_count": len(rows),
        "metrics": metrics.to_dict(),
        "error_buckets": dict(error_buckets),
        "error_buckets_by_source": {source: dict(counter) for source, counter in by_source.items()},
        "family_tag_summary": _build_family_tag_summary(rows, family_tag_rows),
        "focus_group_summary": _build_focus_group_summary(rows),
        "sample_errors": hard_examples,
    }
    (output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_root / "summary.md").write_text(_to_markdown(summary), encoding="utf-8")
    return summary


def infer_error_category(row: dict) -> str:
    if not row.get("parsed", True):
        return "FORMAT"
    prediction = row.get("prediction")
    answer = row.get("answer")
    if prediction == answer:
        return "CORRECT"

    equation1 = row.get("equation1", "")
    equation2 = row.get("equation2", "")
    eq1_vars = extract_variables(equation1)
    eq2_vars = extract_variables(equation2)
    eq1_ops = count_binary_ops(equation1)
    eq2_ops = count_binary_ops(equation2)

    if prediction is True and answer is False:
        if len(eq2_vars) > len(eq1_vars) or eq2_ops > eq1_ops + 1:
            return "FALSE_FILTER_WEAK"
        return "RULE_CONFLICT"

    if prediction is False and answer is True:
        if canonicalize_equation(equation1) == canonicalize_equation(equation2):
            return "RULE_MISSING"
        if (row.get("source") or "").startswith("hard"):
            return "HARD_COMPOSITION"
        return "RULE_MISSING"

    return "MODEL_SPECIFIC"


def _build_family_tag_summary(rows: list[dict], family_tag_rows: Counter[str]) -> dict[str, dict]:
    summary: dict[str, dict] = {}
    for tag, row_count in sorted(family_tag_rows.items(), key=lambda item: (-item[1], item[0])):
        subset = [row for row in rows if tag in set(row.get("family_tags") or [])]
        subset_metrics = compute_metrics(subset)
        error_buckets = _collect_error_buckets(subset)
        summary[tag] = {
            "row_count": row_count,
            "metrics": subset_metrics.to_dict(),
            "error_count": sum(error_buckets.values()),
            "error_buckets": dict(error_buckets),
        }
    return summary


def _build_focus_group_summary(rows: list[dict]) -> dict[str, dict]:
    summary: dict[str, dict] = {}
    for group_name, config in FAMILY_FOCUS_GROUPS.items():
        group_tags = set(config["tags"])
        subset = [row for row in rows if group_tags.intersection(set(row.get("family_tags") or []))]
        subset_metrics = compute_metrics(subset)
        error_buckets = _collect_error_buckets(subset)
        summary[group_name] = {
            "label": config["label"],
            "row_count": len(subset),
            "metrics": subset_metrics.to_dict(),
            "error_count": sum(error_buckets.values()),
            "error_buckets": dict(error_buckets),
            "tags": list(config["tags"]),
        }
    return summary


def _collect_error_buckets(rows: list[dict]) -> Counter[str]:
    buckets: Counter[str] = Counter()
    for row in rows:
        category = infer_error_category(row)
        if category == "CORRECT":
            continue
        buckets[category] += 1
    return buckets


def _to_markdown(summary: dict) -> str:
    lines = [
        "# Error Analysis Summary",
        "",
        f"- Predictions: `{summary['predictions_path']}`",
        f"- Rows: `{summary['row_count']}`",
        f"- Accuracy: `{summary['metrics']['accuracy']:.4f}`",
        f"- Parse success rate: `{summary['metrics']['parse_success_rate']:.4f}`",
        "",
        "## Error Buckets",
        "",
    ]
    for category, count in sorted(summary["error_buckets"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{category}`: {count}")

    lines.extend(
        [
            "",
            "## Focused Family Slices",
            "",
        ]
    )
    for group_name, details in summary.get("focus_group_summary", {}).items():
        bucket_text = ", ".join(
            f"{name}={count}"
            for name, count in sorted(details["error_buckets"].items(), key=lambda item: (-item[1], item[0]))
        )
        if not bucket_text:
            bucket_text = "none"
        metrics = details["metrics"]
        lines.append(
            "- `{label}`: rows={rows}, accuracy={accuracy:.4f}, true={true_acc}, false={false_acc}, errors={errors}, buckets={buckets}".format(
                label=details["label"],
                rows=details["row_count"],
                accuracy=metrics["accuracy"],
                true_acc=_fmt_rate(metrics.get("true_accuracy")),
                false_acc=_fmt_rate(metrics.get("false_accuracy")),
                errors=details["error_count"],
                buckets=bucket_text,
            )
        )

    lines.extend(
        [
            "",
            "## Error Buckets By Family Tag",
            "",
        ]
    )
    for tag, details in summary.get("family_tag_summary", {}).items():
        bucket_text = ", ".join(
            f"{name}={count}"
            for name, count in sorted(details["error_buckets"].items(), key=lambda item: (-item[1], item[0]))
        )
        if not bucket_text:
            bucket_text = "none"
        lines.append(
            "- `{tag}`: rows={rows}, accuracy={accuracy:.4f}, true={true_acc}, false={false_acc}, errors={errors}, buckets={buckets}".format(
                tag=tag,
                rows=details["row_count"],
                accuracy=details["metrics"]["accuracy"],
                true_acc=_fmt_rate(details["metrics"].get("true_accuracy")),
                false_acc=_fmt_rate(details["metrics"].get("false_accuracy")),
                errors=details["error_count"],
                buckets=bucket_text,
            )
        )

    lines.extend(
        [
            "",
            "## Sample Errors",
            "",
        ]
    )
    for sample in summary["sample_errors"][:10]:
        lines.extend(
            [
                f"### {sample['problem_id']}",
                "",
                f"- Source: `{sample['source']}`",
                f"- Category: `{sample['category']}`",
                f"- Answer: `{sample['answer']}`",
                f"- Prediction: `{sample['prediction']}`",
                f"- Parsed: `{sample['parsed']}`",
                f"- Equation 1: `{sample['equation1']}`",
                f"- Equation 2: `{sample['equation2']}`",
                f"- Family tags: `{', '.join(sample['family_tags']) if sample['family_tags'] else 'none'}`",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def _fmt_rate(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.4f}"
