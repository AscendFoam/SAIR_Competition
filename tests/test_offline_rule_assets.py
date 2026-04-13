import json
from pathlib import Path

from sair_competition.analysis.offline_rule_assets import (
    attach_offline_rule_assets,
    audit_offline_rule_assets,
    build_offline_rule_assets,
)
from sair_competition.data.io import read_jsonl, write_jsonl


def test_build_offline_rule_assets_generates_ranked_bundle(tmp_path: Path) -> None:
    tagged_dataset_path = tmp_path / "smoke_tagged.jsonl"
    output_path = tmp_path / "rule_assets.jsonl"
    report_path = tmp_path / "summary.md"
    error_summary_path = tmp_path / "error_summary.json"

    write_jsonl(
        tagged_dataset_path,
        [
            {
                "problem_id": "p1",
                "equation1": "x = (y * z)",
                "equation2": "x = (a * b)",
                "answer": True,
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                ],
            },
            {
                "problem_id": "p2",
                "equation1": "x = (y * z)",
                "equation2": "x = (c * d)",
                "answer": True,
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                ],
            },
            {
                "problem_id": "p3",
                "equation1": "x = (y * z)",
                "equation2": "x = (u * v)",
                "answer": True,
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                ],
            },
        ],
    )
    error_summary_path.write_text(
        json.dumps(
            {
                "family_tag_summary": {
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY": {
                        "metrics": {
                            "accuracy": 0.1,
                            "true_accuracy": 0.1,
                        },
                        "error_buckets": {"RULE_MISSING": 9},
                    },
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS": {
                        "metrics": {
                            "accuracy": 0.2,
                            "true_accuracy": 0.2,
                        },
                        "error_buckets": {"RULE_MISSING": 8},
                    },
                }
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    summary = build_offline_rule_assets(
        tagged_dataset_path=tagged_dataset_path,
        output_path=output_path,
        error_summary_path=error_summary_path,
        report_path=report_path,
    )
    rows = read_jsonl(output_path)

    assert summary["asset_count"] >= 2
    assert rows[0]["rule_id"] == "OA_TRUE_SINGLETON_LHS_TO_BINARY"
    assert rows[0]["support_true_count"] == 3
    assert rows[0]["current_mainline_error_buckets"]["RULE_MISSING"] == 9
    assert report_path.exists()


def test_build_offline_rule_assets_includes_target_child_and_amplification_assets(tmp_path: Path) -> None:
    tagged_dataset_path = tmp_path / "smoke_tagged.jsonl"
    output_path = tmp_path / "rule_assets.jsonl"
    report_path = tmp_path / "summary.md"
    error_summary_path = tmp_path / "error_summary.json"

    write_jsonl(
        tagged_dataset_path,
        [
            {
                "problem_id": "p_newvar_1",
                "equation1": "x = (y * z)",
                "equation2": "x = y * (x * (z * w))",
                "answer": True,
                "family_tags": [
                    "TARGET_SHARED_LHS_AND_NEW_VARS",
                    "TARGET_SHARED_LHS_AND_NEW_VARS_SINGLETON_SOURCE",
                ],
            },
            {
                "problem_id": "p_newvar_2",
                "equation1": "x = (u * v)",
                "equation2": "x = u * (x * (v * w))",
                "answer": True,
                "family_tags": [
                    "TARGET_SHARED_LHS_AND_NEW_VARS",
                    "TARGET_SHARED_LHS_AND_NEW_VARS_SINGLETON_SOURCE",
                ],
            },
            {
                "problem_id": "p_amp_1",
                "equation1": "x = (y * z)",
                "equation2": "x = ((y * x) * x) * z",
                "answer": True,
                "family_tags": [
                    "TARGET_LHS_AMPLIFICATION",
                    "TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR",
                ],
            },
            {
                "problem_id": "p_amp_2",
                "equation1": "x = (a * b)",
                "equation2": "x = (a * ((x * x) * x))",
                "answer": True,
                "family_tags": [
                    "TARGET_LHS_AMPLIFICATION",
                    "TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR",
                ],
            },
            {
                "problem_id": "p_amp_3",
                "equation1": "x = (m * n)",
                "equation2": "x = (((m * x) * x) * x) * n",
                "answer": True,
                "family_tags": [
                    "TARGET_LHS_AMPLIFICATION",
                    "TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR",
                ],
            },
        ],
    )
    error_summary_path.write_text(
        json.dumps(
            {
                "family_tag_summary": {
                    "TARGET_SHARED_LHS_AND_NEW_VARS_SINGLETON_SOURCE": {
                        "metrics": {
                            "accuracy": 0.0,
                            "true_accuracy": 0.0,
                        },
                        "error_buckets": {"RULE_MISSING": 2},
                    },
                    "TARGET_LHS_AMPLIFICATION": {
                        "metrics": {
                            "accuracy": 0.0,
                            "true_accuracy": 0.0,
                        },
                        "error_buckets": {"RULE_MISSING": 3},
                    },
                    "TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR": {
                        "metrics": {
                            "accuracy": 0.0,
                            "true_accuracy": 0.0,
                        },
                        "error_buckets": {"RULE_MISSING": 2},
                    },
                    "TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR": {
                        "metrics": {
                            "accuracy": 0.0,
                            "true_accuracy": 0.0,
                        },
                        "error_buckets": {"RULE_MISSING": 1},
                    },
                }
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    summary = build_offline_rule_assets(
        tagged_dataset_path=tagged_dataset_path,
        output_path=output_path,
        error_summary_path=error_summary_path,
        report_path=report_path,
    )
    rows = read_jsonl(output_path)
    rows_by_id = {row["rule_id"]: row for row in rows}

    assert summary["asset_count"] >= 2
    assert rows_by_id["OA_TRUE_TARGET_SHARED_NEW_VARS_SINGLETON_SOURCE"]["support_true_count"] == 2
    assert rows_by_id["OA_TRUE_TARGET_SHARED_NEW_VARS_SINGLETON_SOURCE"]["status"] == "candidate_offline"
    assert rows_by_id["OA_TRUE_TARGET_LHS_AMPLIFICATION"]["support_true_count"] == 3
    assert rows_by_id["OA_TRUE_TARGET_LHS_AMPLIFICATION"]["current_mainline_error_buckets"]["RULE_MISSING"] == 3
    assert rows_by_id["OA_TRUE_TARGET_LHS_AMPLIFICATION"]["follow_up_action"] is None
    assert rows_by_id["OA_TRUE_TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR"]["support_true_count"] == 2
    assert rows_by_id["OA_TRUE_TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR"]["follow_up_action"] == (
        "prepare_programmatic_positive_signal"
    )
    assert rows_by_id["OA_TRUE_TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR"]["support_true_count"] == 1
    assert rows_by_id["OA_TRUE_TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR"]["follow_up_action"] is None


def test_attach_offline_rule_assets_matches_trigger_tags(tmp_path: Path) -> None:
    tagged_rows_path = tmp_path / "tagged_rows.jsonl"
    rule_assets_path = tmp_path / "rule_assets.jsonl"
    output_path = tmp_path / "tagged_rows_with_assets.jsonl"

    write_jsonl(
        tagged_rows_path,
        [
            {
                "problem_id": "p1",
                "equation1": "x = (y * z)",
                "equation2": "x = (a * b)",
                "answer": True,
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                ],
            },
            {
                "problem_id": "p2",
                "equation1": "(x * y) = z",
                "equation2": "x = y",
                "answer": False,
                "family_tags": [],
            },
        ],
    )
    write_jsonl(
        rule_assets_path,
        [
            {
                "rule_id": "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                "family_focus_group": "singleton_collapse",
                "trigger_tags": ["EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY"],
            },
            {
                "rule_id": "OA_TRUE_DISJOINT_VAR_BINARY",
                "family_focus_group": "disjoint_sides",
                "trigger_tags": ["EQ1_DISJOINT_SIDES_VAR_BINARY"],
            },
        ],
    )

    summary = attach_offline_rule_assets(
        input_path=tagged_rows_path,
        rule_assets_path=rule_assets_path,
        output_path=output_path,
    )
    rows = read_jsonl(output_path)

    assert summary["matched_row_count"] == 1
    assert rows[0]["offline_rule_asset_ids"] == ["OA_TRUE_SINGLETON_LHS_TO_BINARY"]
    assert rows[0]["offline_rule_asset_groups"] == ["singleton_collapse"]
    assert rows[1]["offline_rule_asset_ids"] == []


def test_audit_offline_rule_assets_ranks_missed_true_assets_first(tmp_path: Path) -> None:
    predictions_path = tmp_path / "predictions.jsonl"
    rule_assets_path = tmp_path / "rule_assets.jsonl"
    output_dir = tmp_path / "audit"

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
                    "EQ1_SINGLETON_COLLAPSE_WITH_TARGET_SHARED_LHS",
                ],
            },
            {
                "problem_id": "p2",
                "equation1": "x = (u * v)",
                "equation2": "x = (c * d)",
                "answer": True,
                "prediction": False,
                "parsed": True,
                "source": "hard2",
                "family_tags": [
                    "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                ],
            },
            {
                "problem_id": "p3",
                "equation1": "(x * y) = z",
                "equation2": "(a * b) = c",
                "answer": True,
                "prediction": True,
                "parsed": True,
                "source": "normal",
                "family_tags": [
                    "EQ1_DISJOINT_SIDES_VAR_BINARY",
                ],
            },
        ],
    )
    write_jsonl(
        rule_assets_path,
        [
            {
                "rule_id": "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                "family_focus_group": "singleton_collapse",
                "primary_tag": "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY",
                "trigger_tags": ["EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY"],
                "status": "active_offline",
                "prompt_policy": "do_not_inherit_wording",
                "follow_up_action": "prepare_programmatic_positive_signal",
                "opportunity_score": 10.0,
            },
            {
                "rule_id": "OA_TRUE_DISJOINT_VAR_BINARY",
                "family_focus_group": "disjoint_sides",
                "primary_tag": "EQ1_DISJOINT_SIDES_VAR_BINARY",
                "trigger_tags": ["EQ1_DISJOINT_SIDES_VAR_BINARY"],
                "status": "candidate_offline",
                "prompt_policy": "do_not_inherit_wording",
                "opportunity_score": 2.0,
            },
        ],
    )

    summary = audit_offline_rule_assets(
        predictions_path=predictions_path,
        rule_assets_path=rule_assets_path,
        output_dir=output_dir,
    )

    assert summary["audited_asset_count"] == 2
    assert summary["ranked_assets"][0]["rule_id"] == "OA_TRUE_SINGLETON_LHS_TO_BINARY"
    assert summary["ranked_assets"][0]["follow_up_action"] == "prepare_programmatic_positive_signal"
    assert summary["ranked_assets"][0]["true_miss_count"] == 2
    assert summary["ranked_assets"][0]["recoverable_error_count"] >= 1
    assert (output_dir / "summary.md").exists()
