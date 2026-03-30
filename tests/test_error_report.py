from pathlib import Path

from sair_competition.analysis.error_report import analyze_prediction_errors, infer_error_category
from sair_competition.data.io import write_jsonl


def test_infer_error_category_format() -> None:
    row = {"parsed": False}
    assert infer_error_category(row) == "FORMAT"


def test_infer_error_category_false_filter_weak() -> None:
    row = {
        "parsed": True,
        "prediction": True,
        "answer": False,
        "equation1": "x = y",
        "equation2": "x * y = z * w",
        "source": "normal",
    }
    assert infer_error_category(row) == "FALSE_FILTER_WEAK"


def test_analyze_prediction_errors_summarizes_family_tags(tmp_path: Path) -> None:
    predictions_path = tmp_path / "predictions.jsonl"
    output_dir = tmp_path / "analysis"
    write_jsonl(
        predictions_path,
        [
            {
                "parsed": True,
                "prediction": True,
                "answer": False,
                "equation1": "x = (y * z)",
                "equation2": "a = (b * c)",
                "source": "normal",
                "family_tags": ["EQ1_SINGLETON_COLLAPSE_LHS", "EQ1_DISJOINT_SIDES"],
            }
        ],
    )

    summary = analyze_prediction_errors(predictions_path=predictions_path, output_dir=output_dir)

    assert summary["family_tag_summary"]["EQ1_SINGLETON_COLLAPSE_LHS"]["row_count"] == 1
    assert summary["family_tag_summary"]["EQ1_SINGLETON_COLLAPSE_LHS"]["error_buckets"]["RULE_CONFLICT"] == 1
    assert summary["focus_group_summary"]["singleton_collapse"]["row_count"] == 1
    assert summary["focus_group_summary"]["singleton_collapse"]["error_buckets"]["RULE_CONFLICT"] == 1
