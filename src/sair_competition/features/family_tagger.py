from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.parse.equations import (
    canonicalize_equation,
    canonicalize_variables,
    count_binary_ops,
    extract_variables,
    split_equation,
)


FAMILY_TAG_TAXONOMY = {
    "EQ1_SINGLETON_COLLAPSE_LHS": "Equation 1 has a lone variable on the left that does not appear on the right.",
    "EQ1_SINGLETON_COLLAPSE_RHS": "Equation 1 has a lone variable on the right that does not appear on the left.",
    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY": "Equation 1 matches a narrow singleton-collapse shape: lone variable on the left, binary term on the right.",
    "EQ1_SINGLETON_COLLAPSE_RHS_TO_BINARY": "Equation 1 matches a narrow singleton-collapse shape: lone variable on the right, binary term on the left.",
    "EQ1_SINGLETON_COLLAPSE_WITH_DISJOINT_SIDES": "Singleton-collapse case where the two sides of Equation 1 are also variable-disjoint.",
    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS": "Singleton-collapse case where Equation 2 keeps the same left-hand-side skeleton.",
    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_NEW_VARS": "Singleton-collapse case where Equation 2 introduces variables not seen in Equation 1.",
    "EQ1_DISJOINT_SIDES": "The two sides of Equation 1 use disjoint variable sets.",
    "EQ1_DISJOINT_SIDES_VAR_BINARY": "Disjoint-sides case where one side is a lone variable and the other side is a binary term.",
    "EQ1_DISJOINT_SIDES_BINARY_BINARY": "Disjoint-sides case where both sides of Equation 1 are binary terms.",
    "EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS": "Disjoint-sides case where Equation 2 keeps the same left-hand-side skeleton.",
    "EQ1_DISJOINT_SIDES_WITH_TARGET_NEW_VARS": "Disjoint-sides case where Equation 2 introduces new variables.",
    "EQ1_CONSTANT_OPERATION_CANDIDATE": "Equation 1 combines disjoint variable sets with at least one binary side, a narrow constant-operation candidate.",
    "EQ1_CONSTANT_OPERATION_VAR_BINARY": "Constant-operation candidate with a variable-vs-binary Equation 1 shape.",
    "EQ1_CONSTANT_OPERATION_BINARY_BINARY": "Constant-operation candidate with a binary-vs-binary Equation 1 shape.",
    "EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS": "Constant-operation candidate where Equation 2 keeps the same left-hand-side skeleton.",
    "EQ1_CONSTANT_OPERATION_WITH_TARGET_NEW_VARS": "Constant-operation candidate where Equation 2 introduces new variables.",
    "TARGET_TAUTOLOGY": "Equation 2 is tautological after alpha-normalization.",
    "TARGET_ALPHA_EQ_EQ1": "Equation 2 is alpha-equivalent to Equation 1.",
    "SHARED_LHS_ALPHA": "Equation 1 and Equation 2 have alpha-equivalent left-hand sides.",
    "SHARED_RHS_ALPHA": "Equation 1 and Equation 2 have alpha-equivalent right-hand sides.",
    "EQ2_INTRODUCES_NEW_VARS": "Equation 2 uses variables that do not appear in Equation 1.",
    "EQ2_MORE_COMPLEX": "Equation 2 has strictly more binary operations than Equation 1.",
}


FAMILY_FOCUS_GROUPS = {
    "singleton_collapse": {
        "label": "Singleton collapse",
        "tags": [
            "EQ1_SINGLETON_COLLAPSE_LHS",
            "EQ1_SINGLETON_COLLAPSE_RHS",
            "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
            "EQ1_SINGLETON_COLLAPSE_RHS_TO_BINARY",
            "EQ1_SINGLETON_COLLAPSE_WITH_DISJOINT_SIDES",
            "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
            "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_NEW_VARS",
        ],
    },
    "disjoint_sides": {
        "label": "Disjoint sides",
        "tags": [
            "EQ1_DISJOINT_SIDES",
            "EQ1_DISJOINT_SIDES_VAR_BINARY",
            "EQ1_DISJOINT_SIDES_BINARY_BINARY",
            "EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS",
            "EQ1_DISJOINT_SIDES_WITH_TARGET_NEW_VARS",
        ],
    },
    "constant_operation_candidate": {
        "label": "Constant-operation candidate",
        "tags": [
            "EQ1_CONSTANT_OPERATION_CANDIDATE",
            "EQ1_CONSTANT_OPERATION_VAR_BINARY",
            "EQ1_CONSTANT_OPERATION_BINARY_BINARY",
            "EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS",
            "EQ1_CONSTANT_OPERATION_WITH_TARGET_NEW_VARS",
        ],
    },
}


def build_family_annotation(equation1: str, equation2: str) -> dict[str, object]:
    """Attach lightweight structural family tags for offline labeling."""

    lhs1, rhs1 = split_equation(equation1)
    lhs2, rhs2 = split_equation(equation2)

    lhs1_vars = set(extract_variables(lhs1))
    rhs1_vars = set(extract_variables(rhs1))
    lhs2_vars = set(extract_variables(lhs2))
    rhs2_vars = set(extract_variables(rhs2))
    eq1_vars = lhs1_vars | rhs1_vars
    eq2_vars = lhs2_vars | rhs2_vars

    lhs1_kind = _classify_side(lhs1)
    rhs1_kind = _classify_side(rhs1)
    lhs2_kind = _classify_side(lhs2)
    rhs2_kind = _classify_side(rhs2)

    signals = {
        "eq1_var_count": len(eq1_vars),
        "eq2_var_count": len(eq2_vars),
        "eq1_op_count": count_binary_ops(equation1),
        "eq2_op_count": count_binary_ops(equation2),
        "eq1_lhs_kind": lhs1_kind,
        "eq1_rhs_kind": rhs1_kind,
        "eq2_lhs_kind": lhs2_kind,
        "eq2_rhs_kind": rhs2_kind,
        "eq1_side_vars_disjoint": lhs1_vars.isdisjoint(rhs1_vars),
        "eq1_side_vars_equal": lhs1_vars == rhs1_vars,
        "eq1_lhs_lone_var_absent_from_rhs": _is_lone_var_absent(lhs1, lhs1_kind, rhs1_vars),
        "eq1_rhs_lone_var_absent_from_lhs": _is_lone_var_absent(rhs1, rhs1_kind, lhs1_vars),
        "target_tautology": canonicalize_variables(lhs2) == canonicalize_variables(rhs2),
        "target_alpha_eq_eq1": canonicalize_equation(equation1) == canonicalize_equation(equation2),
        "shared_lhs_alpha": canonicalize_variables(lhs1) == canonicalize_variables(lhs2),
        "shared_rhs_alpha": canonicalize_variables(rhs1) == canonicalize_variables(rhs2),
        "eq2_introduces_new_vars": bool(eq2_vars - eq1_vars),
        "eq2_more_complex": count_binary_ops(equation2) > count_binary_ops(equation1),
    }
    signals["eq1_disjoint_shape"] = _shape_pair(lhs1_kind, rhs1_kind) if signals["eq1_side_vars_disjoint"] else "none"
    signals["eq1_singleton_side"] = _singleton_side(signals)
    signals["eq1_constant_candidate_shape"] = (
        signals["eq1_disjoint_shape"]
        if signals["eq1_side_vars_disjoint"] and (lhs1_kind == "binary" or rhs1_kind == "binary")
        else "none"
    )

    tag_set: set[str] = set()
    if signals["eq1_lhs_lone_var_absent_from_rhs"]:
        tag_set.add("EQ1_SINGLETON_COLLAPSE_LHS")
    if signals["eq1_rhs_lone_var_absent_from_lhs"]:
        tag_set.add("EQ1_SINGLETON_COLLAPSE_RHS")
    if signals["eq1_lhs_lone_var_absent_from_rhs"] and rhs1_kind == "binary":
        tag_set.add("EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY")
    if signals["eq1_rhs_lone_var_absent_from_lhs"] and lhs1_kind == "binary":
        tag_set.add("EQ1_SINGLETON_COLLAPSE_RHS_TO_BINARY")
    if signals["eq1_side_vars_disjoint"]:
        tag_set.add("EQ1_DISJOINT_SIDES")
        if signals["eq1_disjoint_shape"] in {"var_to_binary", "binary_to_var"}:
            tag_set.add("EQ1_DISJOINT_SIDES_VAR_BINARY")
        if signals["eq1_disjoint_shape"] == "binary_to_binary":
            tag_set.add("EQ1_DISJOINT_SIDES_BINARY_BINARY")
    if signals["eq1_side_vars_disjoint"] and (lhs1_kind == "binary" or rhs1_kind == "binary"):
        tag_set.add("EQ1_CONSTANT_OPERATION_CANDIDATE")
        if signals["eq1_constant_candidate_shape"] in {"var_to_binary", "binary_to_var"}:
            tag_set.add("EQ1_CONSTANT_OPERATION_VAR_BINARY")
        if signals["eq1_constant_candidate_shape"] == "binary_to_binary":
            tag_set.add("EQ1_CONSTANT_OPERATION_BINARY_BINARY")
    if signals["target_tautology"]:
        tag_set.add("TARGET_TAUTOLOGY")
    if signals["target_alpha_eq_eq1"]:
        tag_set.add("TARGET_ALPHA_EQ_EQ1")
    if signals["shared_lhs_alpha"]:
        tag_set.add("SHARED_LHS_ALPHA")
    if signals["shared_rhs_alpha"]:
        tag_set.add("SHARED_RHS_ALPHA")
    if signals["eq2_introduces_new_vars"]:
        tag_set.add("EQ2_INTRODUCES_NEW_VARS")
    if signals["eq2_more_complex"]:
        tag_set.add("EQ2_MORE_COMPLEX")
    if signals["eq1_singleton_side"] != "none" and signals["eq1_side_vars_disjoint"]:
        tag_set.add("EQ1_SINGLETON_COLLAPSE_WITH_DISJOINT_SIDES")
    if signals["eq1_singleton_side"] != "none" and signals["shared_lhs_alpha"]:
        tag_set.add("EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS")
    if signals["eq1_singleton_side"] != "none" and signals["eq2_introduces_new_vars"]:
        tag_set.add("EQ1_SINGLETON_COLLAPSE_WITH_TARGET_NEW_VARS")
    if signals["eq1_side_vars_disjoint"] and signals["shared_lhs_alpha"]:
        tag_set.add("EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS")
    if signals["eq1_side_vars_disjoint"] and signals["eq2_introduces_new_vars"]:
        tag_set.add("EQ1_DISJOINT_SIDES_WITH_TARGET_NEW_VARS")
    if "EQ1_CONSTANT_OPERATION_CANDIDATE" in tag_set and signals["shared_lhs_alpha"]:
        tag_set.add("EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS")
    if "EQ1_CONSTANT_OPERATION_CANDIDATE" in tag_set and signals["eq2_introduces_new_vars"]:
        tag_set.add("EQ1_CONSTANT_OPERATION_WITH_TARGET_NEW_VARS")

    ordered_tags = [tag for tag in FAMILY_TAG_TAXONOMY if tag in tag_set]
    return {
        "family_tags": ordered_tags,
        "family_signals": signals,
    }


def tag_problem_families(
    dataset_path: str | Path,
    output_path: str | Path,
    summary_dir: str | Path | None = None,
) -> dict:
    """Write a tagged dataset plus a compact family summary report."""

    rows = read_jsonl(dataset_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    summary_root = Path(summary_dir) if summary_dir else target.parent / f"{target.stem}_family_summary"
    summary_root.mkdir(parents=True, exist_ok=True)

    annotated_rows: list[dict] = []
    tag_counts: Counter[str] = Counter()
    tag_counts_by_answer: dict[str, Counter[str]] = defaultdict(Counter)
    tag_samples: dict[str, list[dict]] = defaultdict(list)
    tagged_row_count = 0
    focus_group_rows: dict[str, set[str]] = {name: set() for name in FAMILY_FOCUS_GROUPS}
    focus_group_answer_counts: dict[str, Counter[str]] = defaultdict(Counter)

    for row in rows:
        annotation = build_family_annotation(row["equation1"], row["equation2"])
        tagged_row = dict(row)
        tagged_row["family_tags"] = annotation["family_tags"]
        tagged_row["family_signals"] = annotation["family_signals"]
        annotated_rows.append(tagged_row)

        if annotation["family_tags"]:
            tagged_row_count += 1
        answer_key = _answer_key(row.get("answer"))
        for tag in annotation["family_tags"]:
            tag_counts[tag] += 1
            tag_counts_by_answer[tag][answer_key] += 1
            if len(tag_samples[tag]) < 3:
                tag_samples[tag].append(
                    {
                        "problem_id": row.get("problem_id"),
                        "source": row.get("source"),
                        "split": row.get("split"),
                        "equation1": row.get("equation1"),
                        "equation2": row.get("equation2"),
                        "answer": row.get("answer"),
                    }
                )
        for group_name, config in FAMILY_FOCUS_GROUPS.items():
            group_tags = set(config["tags"])
            if group_tags.intersection(annotation["family_tags"]):
                focus_group_rows[group_name].add(_row_key(row))
                focus_group_answer_counts[group_name][answer_key] += 1

    write_jsonl(target, annotated_rows)

    summary = {
        "dataset_path": str(dataset_path),
        "output_path": str(target),
        "row_count": len(rows),
        "tagged_row_count": tagged_row_count,
        "untagged_row_count": len(rows) - tagged_row_count,
        "unique_tag_count": len(tag_counts),
        "focus_group_summary": {
            group_name: {
                "label": config["label"],
                "row_count": len(focus_group_rows[group_name]),
                "true_count": focus_group_answer_counts[group_name].get("true", 0),
                "false_count": focus_group_answer_counts[group_name].get("false", 0),
                "tags": list(config["tags"]),
            }
            for group_name, config in FAMILY_FOCUS_GROUPS.items()
        },
        "tag_counts": dict(tag_counts),
        "tag_counts_by_answer": {tag: dict(counter) for tag, counter in tag_counts_by_answer.items()},
        "tag_samples": dict(tag_samples),
    }
    (summary_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (summary_root / "summary.md").write_text(_to_markdown(summary), encoding="utf-8")
    return summary


def _classify_side(side: str) -> str:
    compact = _strip_outer_parens(side.replace(" ", ""))
    variables = extract_variables(compact)
    if count_binary_ops(compact) == 0 and len(variables) == 1 and compact == variables[0]:
        return "var"
    if count_binary_ops(compact) > 0:
        return "binary"
    return "unknown"


def _shape_pair(left_kind: str, right_kind: str) -> str:
    if left_kind == "var" and right_kind == "binary":
        return "var_to_binary"
    if left_kind == "binary" and right_kind == "var":
        return "binary_to_var"
    if left_kind == "binary" and right_kind == "binary":
        return "binary_to_binary"
    if left_kind == "var" and right_kind == "var":
        return "var_to_var"
    return "other"


def _singleton_side(signals: dict[str, object]) -> str:
    if signals["eq1_lhs_lone_var_absent_from_rhs"]:
        return "lhs"
    if signals["eq1_rhs_lone_var_absent_from_lhs"]:
        return "rhs"
    return "none"


def _is_lone_var_absent(side: str, side_kind: str, other_side_vars: set[str]) -> bool:
    if side_kind != "var":
        return False
    variables = extract_variables(side)
    if len(variables) != 1:
        return False
    return variables[0] not in other_side_vars


def _strip_outer_parens(text: str) -> str:
    candidate = text
    while candidate.startswith("(") and candidate.endswith(")") and _has_balanced_outer_parens(candidate):
        candidate = candidate[1:-1].strip()
    return candidate


def _has_balanced_outer_parens(text: str) -> bool:
    depth = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        if depth == 0 and index != len(text) - 1:
            return False
    return depth == 0


def _answer_key(answer: bool | None) -> str:
    if answer is True:
        return "true"
    if answer is False:
        return "false"
    return "unknown"


def _row_key(row: dict) -> str:
    problem_id = row.get("problem_id")
    if problem_id:
        return str(problem_id)
    return f"{row.get('equation1', '')} => {row.get('equation2', '')}"


def _to_markdown(summary: dict) -> str:
    lines = [
        "# Family Tag Summary",
        "",
        f"- Dataset: `{summary['dataset_path']}`",
        f"- Tagged dataset: `{summary['output_path']}`",
        f"- Rows: `{summary['row_count']}`",
        f"- Tagged rows: `{summary['tagged_row_count']}`",
        f"- Untagged rows: `{summary['untagged_row_count']}`",
        "",
        "## Focus Groups",
        "",
        "| Focus Group | Rows | True | False | Included Tags |",
        "| --- | ---: | ---: | ---: | --- |",
    ]

    for group_name, group_summary in summary["focus_group_summary"].items():
        lines.append(
            "| {label} | {rows} | {true_count} | {false_count} | {tags} |".format(
                label=group_summary["label"],
                rows=group_summary["row_count"],
                true_count=group_summary["true_count"],
                false_count=group_summary["false_count"],
                tags=", ".join(group_summary["tags"]),
            )
        )

    lines.extend(
        [
            "",
            "## All Tags",
            "",
        "| Tag | Count | True | False | Description |",
        "| --- | ---: | ---: | ---: | --- |",
        ]
    )

    for tag, count in sorted(summary["tag_counts"].items(), key=lambda item: (-item[1], item[0])):
        by_answer = summary["tag_counts_by_answer"].get(tag, {})
        lines.append(
            "| {tag} | {count} | {true_count} | {false_count} | {description} |".format(
                tag=tag,
                count=count,
                true_count=by_answer.get("true", 0),
                false_count=by_answer.get("false", 0),
                description=FAMILY_TAG_TAXONOMY.get(tag, ""),
            )
        )

    if summary["tag_samples"]:
        lines.extend(
            [
                "",
                "## Samples",
                "",
            ]
        )
        for tag, samples in sorted(summary["tag_samples"].items()):
            lines.append(f"### {tag}")
            lines.append("")
            for sample in samples:
                lines.append(
                    "- `{problem_id}` ({source}/{split}) answer={answer}: `{equation1}` => `{equation2}`".format(
                        problem_id=sample.get("problem_id") or "unknown",
                        source=sample.get("source") or "unknown",
                        split=sample.get("split") or "n/a",
                        answer=sample.get("answer"),
                        equation1=sample.get("equation1"),
                        equation2=sample.get("equation2"),
                    )
                )
            lines.append("")

    return "\n".join(lines).strip() + "\n"
