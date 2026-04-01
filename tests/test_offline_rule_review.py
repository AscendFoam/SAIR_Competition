import json
from pathlib import Path

from sair_competition.analysis.offline_rule_review import (
    build_offline_rule_review_set,
    consolidate_offline_rule_axes,
)
from sair_competition.data.io import read_jsonl, write_jsonl


def test_consolidate_offline_rule_axes_merges_exact_duplicate_assets(tmp_path: Path) -> None:
    predictions_path = tmp_path / "predictions.jsonl"
    audit_summary_path = tmp_path / "audit_summary.json"
    output_dir = tmp_path / "axis_summary"

    write_jsonl(
        predictions_path,
        [
            {
                "problem_id": "p1",
                "equation1": "x = (y * z)",
                "equation2": "x = (a * b)",
                "answer": True,
                "prediction": False,
                "parsed": True,
                "source": "normal",
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                    "EQ1_DISJOINT_SIDES_VAR_BINARY",
                    "EQ1_CONSTANT_OPERATION_VAR_BINARY",
                ],
                "offline_rule_asset_ids": [
                    "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                    "OA_TRUE_DISJOINT_VAR_BINARY",
                    "OA_TRUE_CONSTANT_VAR_BINARY",
                ],
            },
            {
                "problem_id": "p2",
                "equation1": "x = (u * v)",
                "equation2": "x = (c * d)",
                "answer": True,
                "prediction": False,
                "parsed": True,
                "source": "normal",
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                    "EQ1_DISJOINT_SIDES_VAR_BINARY",
                    "EQ1_CONSTANT_OPERATION_VAR_BINARY",
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                    "EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS",
                    "EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS",
                    "SHARED_LHS_ALPHA",
                ],
                "offline_rule_asset_ids": [
                    "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                    "OA_TRUE_DISJOINT_VAR_BINARY",
                    "OA_TRUE_CONSTANT_VAR_BINARY",
                    "OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS",
                    "OA_TRUE_DISJOINT_WITH_TARGET_SHARED_LHS",
                    "OA_TRUE_CONSTANT_WITH_TARGET_SHARED_LHS",
                ],
            },
            {
                "problem_id": "p3",
                "equation1": "x * y = z * (w * u)",
                "equation2": "x * x = (y * z) * w",
                "answer": True,
                "prediction": False,
                "parsed": True,
                "source": "normal",
                "family_tags": [
                    "EQ1_DISJOINT_SIDES_BINARY_BINARY",
                ],
                "offline_rule_asset_ids": [
                    "OA_TRUE_DISJOINT_BINARY_BINARY",
                ],
            },
        ],
    )
    audit_summary_path.write_text(
        json.dumps(
            {
                "ranked_assets": [
                    {
                        "rule_id": "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                        "family_focus_group": "singleton_collapse",
                        "primary_tag": "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                        "trigger_tags": ["EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY"],
                        "priority_score": 10.0,
                    },
                    {
                        "rule_id": "OA_TRUE_DISJOINT_VAR_BINARY",
                        "family_focus_group": "disjoint_sides",
                        "primary_tag": "EQ1_DISJOINT_SIDES_VAR_BINARY",
                        "trigger_tags": ["EQ1_DISJOINT_SIDES_VAR_BINARY"],
                        "priority_score": 10.0,
                    },
                    {
                        "rule_id": "OA_TRUE_CONSTANT_VAR_BINARY",
                        "family_focus_group": "constant_operation_candidate",
                        "primary_tag": "EQ1_CONSTANT_OPERATION_VAR_BINARY",
                        "trigger_tags": ["EQ1_CONSTANT_OPERATION_VAR_BINARY"],
                        "priority_score": 10.0,
                    },
                    {
                        "rule_id": "OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS",
                        "family_focus_group": "singleton_collapse",
                        "primary_tag": "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                        "trigger_tags": ["EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS"],
                        "priority_score": 7.0,
                    },
                    {
                        "rule_id": "OA_TRUE_DISJOINT_WITH_TARGET_SHARED_LHS",
                        "family_focus_group": "disjoint_sides",
                        "primary_tag": "EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS",
                        "trigger_tags": ["EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS"],
                        "priority_score": 7.0,
                    },
                    {
                        "rule_id": "OA_TRUE_CONSTANT_WITH_TARGET_SHARED_LHS",
                        "family_focus_group": "constant_operation_candidate",
                        "primary_tag": "EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS",
                        "trigger_tags": ["EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS"],
                        "priority_score": 7.0,
                    },
                    {
                        "rule_id": "OA_TRUE_DISJOINT_BINARY_BINARY",
                        "family_focus_group": "disjoint_sides",
                        "primary_tag": "EQ1_DISJOINT_SIDES_BINARY_BINARY",
                        "trigger_tags": ["EQ1_DISJOINT_SIDES_BINARY_BINARY"],
                        "priority_score": 3.0,
                    },
                ]
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    summary = consolidate_offline_rule_axes(
        predictions_path=predictions_path,
        audit_summary_path=audit_summary_path,
        output_dir=output_dir,
    )

    assert summary["canonical_axis_count"] == 3
    assert summary["canonical_axes"][0]["main_axis_rule_id"] == "OA_TRUE_SINGLETON_LHS_TO_BINARY"
    assert summary["canonical_axes"][0]["alias_rule_ids"] == [
        "OA_TRUE_DISJOINT_VAR_BINARY",
        "OA_TRUE_CONSTANT_VAR_BINARY",
    ]
    assert summary["canonical_axes"][1]["parent_main_axis_rule_id"] == "OA_TRUE_SINGLETON_LHS_TO_BINARY"
    assert (output_dir / "summary.md").exists()


def test_build_offline_rule_review_set_assigns_rows_to_most_specific_axis(tmp_path: Path) -> None:
    predictions_path = tmp_path / "predictions.jsonl"
    consolidation_summary_path = tmp_path / "consolidation_summary.json"
    output_dir = tmp_path / "review_set"

    write_jsonl(
        predictions_path,
        [
            {
                "problem_id": "p_base",
                "equation1": "x = (y * z)",
                "equation2": "x * y = (a * b) * c",
                "answer": True,
                "prediction": False,
                "parsed": True,
                "source": "normal",
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                    "EQ1_DISJOINT_SIDES_VAR_BINARY",
                    "EQ1_CONSTANT_OPERATION_VAR_BINARY",
                ],
                "offline_rule_asset_ids": [
                    "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                    "OA_TRUE_DISJOINT_VAR_BINARY",
                    "OA_TRUE_CONSTANT_VAR_BINARY",
                ],
            },
            {
                "problem_id": "p_shared",
                "equation1": "x = (u * v)",
                "equation2": "x = (c * d)",
                "answer": True,
                "prediction": False,
                "parsed": True,
                "source": "normal",
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                    "EQ1_DISJOINT_SIDES_VAR_BINARY",
                    "EQ1_CONSTANT_OPERATION_VAR_BINARY",
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                    "EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS",
                    "EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS",
                    "SHARED_LHS_ALPHA",
                ],
                "offline_rule_asset_ids": [
                    "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                    "OA_TRUE_DISJOINT_VAR_BINARY",
                    "OA_TRUE_CONSTANT_VAR_BINARY",
                    "OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS",
                    "OA_TRUE_DISJOINT_WITH_TARGET_SHARED_LHS",
                    "OA_TRUE_CONSTANT_WITH_TARGET_SHARED_LHS",
                ],
            },
            {
                "problem_id": "p_newvar",
                "equation1": "x = (u * v)",
                "equation2": "x = (c * (d * w))",
                "answer": True,
                "prediction": False,
                "parsed": True,
                "source": "normal",
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                    "EQ1_DISJOINT_SIDES_VAR_BINARY",
                    "EQ1_CONSTANT_OPERATION_VAR_BINARY",
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                    "EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS",
                    "EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS",
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_NEW_VARS",
                    "EQ1_CONSTANT_OPERATION_WITH_TARGET_NEW_VARS",
                    "SHARED_LHS_ALPHA",
                    "EQ2_INTRODUCES_NEW_VARS",
                ],
                "offline_rule_asset_ids": [
                    "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                    "OA_TRUE_DISJOINT_VAR_BINARY",
                    "OA_TRUE_CONSTANT_VAR_BINARY",
                    "OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS",
                    "OA_TRUE_DISJOINT_WITH_TARGET_SHARED_LHS",
                    "OA_TRUE_CONSTANT_WITH_TARGET_SHARED_LHS",
                    "OA_TRUE_SINGLETON_WITH_TARGET_NEW_VARS",
                    "OA_TRUE_CONSTANT_WITH_TARGET_NEW_VARS",
                ],
            },
        ],
    )
    consolidation_summary_path.write_text(
        json.dumps(
            {
                "canonical_axes": [
                    {
                        "axis_id": "AXIS_01",
                        "main_axis_rule_id": "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                        "alias_rule_ids": [
                            "OA_TRUE_DISJOINT_VAR_BINARY",
                            "OA_TRUE_CONSTANT_VAR_BINARY",
                        ],
                        "merged_trigger_tags": [
                            "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                            "EQ1_DISJOINT_SIDES_VAR_BINARY",
                            "EQ1_CONSTANT_OPERATION_VAR_BINARY",
                        ],
                        "row_keys": ["p_base", "p_shared", "p_newvar"],
                        "row_count": 3,
                        "rank_index": 0,
                        "priority_score": 10.0,
                        "parent_axis_id": None,
                        "parent_main_axis_rule_id": None,
                        "axis_depth": 0,
                    },
                    {
                        "axis_id": "AXIS_02",
                        "main_axis_rule_id": "OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS",
                        "alias_rule_ids": [
                            "OA_TRUE_DISJOINT_WITH_TARGET_SHARED_LHS",
                            "OA_TRUE_CONSTANT_WITH_TARGET_SHARED_LHS",
                        ],
                        "merged_trigger_tags": [
                            "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                            "EQ1_DISJOINT_SIDES_WITH_TARGET_SHARED_LHS",
                            "EQ1_CONSTANT_OPERATION_WITH_TARGET_SHARED_LHS",
                        ],
                        "row_keys": ["p_shared", "p_newvar"],
                        "row_count": 2,
                        "rank_index": 1,
                        "priority_score": 7.0,
                        "parent_axis_id": "AXIS_01",
                        "parent_main_axis_rule_id": "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                        "axis_depth": 1,
                    },
                    {
                        "axis_id": "AXIS_03",
                        "main_axis_rule_id": "OA_TRUE_SINGLETON_WITH_TARGET_NEW_VARS",
                        "alias_rule_ids": [
                            "OA_TRUE_CONSTANT_WITH_TARGET_NEW_VARS",
                        ],
                        "merged_trigger_tags": [
                            "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_NEW_VARS",
                            "EQ1_CONSTANT_OPERATION_WITH_TARGET_NEW_VARS",
                        ],
                        "row_keys": ["p_newvar"],
                        "row_count": 1,
                        "rank_index": 2,
                        "priority_score": 3.0,
                        "parent_axis_id": "AXIS_02",
                        "parent_main_axis_rule_id": "OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS",
                        "axis_depth": 2,
                    },
                ]
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    summary = build_offline_rule_review_set(
        predictions_path=predictions_path,
        consolidation_summary_path=consolidation_summary_path,
        output_dir=output_dir,
    )
    rows = read_jsonl(output_dir / "review_set.jsonl")
    rows_by_problem_id = {row["problem_id"]: row for row in rows}

    assert summary["review_row_count"] == 3
    assert rows_by_problem_id["p_base"]["review_axis_rule_id"] == "OA_TRUE_SINGLETON_LHS_TO_BINARY"
    assert rows_by_problem_id["p_shared"]["review_axis_rule_id"] == "OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS"
    assert rows_by_problem_id["p_newvar"]["review_axis_rule_id"] == "OA_TRUE_SINGLETON_WITH_TARGET_NEW_VARS"
    assert rows_by_problem_id["p_newvar"]["review_priority"] == "P0"
    template_text = (output_dir / "p0_p1_review_template.md").read_text(encoding="utf-8")
    assert "## Session Metadata" in template_text
    assert "`Axis-Level Decision`" in template_text
