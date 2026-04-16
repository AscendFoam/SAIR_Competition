from pathlib import Path

from sair_competition.analysis.positive_signal_candidate import prepare_positive_signal_candidate
from sair_competition.data.io import write_jsonl


def test_prepare_positive_signal_candidate_builds_boundary_and_overlap_summary(tmp_path: Path) -> None:
    tagged_dataset_path = tmp_path / "tagged.jsonl"
    rule_assets_path = tmp_path / "assets.jsonl"
    output_dir = tmp_path / "report"

    write_jsonl(
        tagged_dataset_path,
        [
            {
                "problem_id": "p_true_a",
                "source": "normal",
                "split": "dev",
                "answer": True,
                "family_tags": [
                    "TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR",
                    "EQ1_SINGLETON_COLLAPSE_LHS",
                ],
                "family_signals": {
                    "eq1_lhs_lone_var_absent_from_rhs": True,
                    "eq2_rhs_retained_non_lhs_eq1_var_count": 2,
                    "eq2_rhs_eq1_lhs_var_count": 3,
                },
            },
            {
                "problem_id": "p_true_b",
                "source": "normal",
                "split": "dev",
                "answer": True,
                "family_tags": [
                    "TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR",
                    "EQ1_SINGLETON_COLLAPSE_LHS",
                    "EQ1_DISJOINT_SIDES",
                ],
                "family_signals": {
                    "eq1_lhs_lone_var_absent_from_rhs": True,
                    "eq2_rhs_retained_non_lhs_eq1_var_count": 4,
                    "eq2_rhs_eq1_lhs_var_count": 2,
                },
            },
            {
                "problem_id": "p_boundary",
                "source": "normal",
                "split": "dev",
                "answer": False,
                "family_tags": ["TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR"],
                "family_signals": {
                    "eq1_lhs_lone_var_absent_from_rhs": True,
                    "eq2_rhs_retained_non_lhs_eq1_var_count": 1,
                },
            },
        ],
    )
    write_jsonl(
        rule_assets_path,
        [
            {
                "rule_id": "OA_TRUE_TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR",
                "primary_tag": "TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR",
                "trigger_tags": ["TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR"],
                "follow_up_action": "prepare_programmatic_positive_signal",
            },
            {
                "rule_id": "OA_TRUE_SINGLETON_LHS_TO_BINARY",
                "primary_tag": "EQ1_SINGLETON_COLLAPSE_LHS",
                "trigger_tags": ["EQ1_SINGLETON_COLLAPSE_LHS"],
                "follow_up_action": None,
            },
        ],
    )

    summary = prepare_positive_signal_candidate(
        tagged_dataset_path=tagged_dataset_path,
        target_tag="TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR",
        output_dir=output_dir,
        boundary_tags=["TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR"],
        rule_assets_path=rule_assets_path,
    )

    assert summary["target_summary"]["row_count"] == 2
    assert summary["target_summary"]["false_count"] == 0
    assert summary["boundary_summaries"][0]["false_count"] == 1
    assert summary["signal_profile"]["eq1_lhs_lone_var_absent_from_rhs"]["value"] is True
    assert summary["asset_overlap_summary"][0]["rule_id"] == "OA_TRUE_TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR"
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "summary.md").exists()
