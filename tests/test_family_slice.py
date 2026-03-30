from pathlib import Path

from sair_competition.analysis.family_slice import attach_family_tags_to_predictions
from sair_competition.data.io import read_jsonl, write_jsonl


def test_attach_family_tags_to_predictions_matches_by_problem_id(tmp_path: Path) -> None:
    predictions_path = tmp_path / "predictions.jsonl"
    tagged_dataset_path = tmp_path / "tagged.jsonl"
    output_path = tmp_path / "out" / "predictions.jsonl"

    write_jsonl(
        predictions_path,
        [
            {
                "problem_id": "p1",
                "equation1": "x = (y * z)",
                "equation2": "x = (a * b)",
                "prediction": False,
                "answer": True,
                "parsed": True,
            }
        ],
    )
    write_jsonl(
        tagged_dataset_path,
        [
            {
                "problem_id": "p1",
                "equation1": "x = (y * z)",
                "equation2": "x = (a * b)",
                "family_tags": ["EQ1_SINGLETON_COLLAPSE_LHS"],
                "family_signals": {"eq1_singleton_side": "lhs"},
            }
        ],
    )

    summary = attach_family_tags_to_predictions(
        predictions_path=predictions_path,
        tagged_dataset_path=tagged_dataset_path,
        output_path=output_path,
    )
    rows = read_jsonl(output_path)

    assert summary["matched_rows"] == 1
    assert rows[0]["family_tags"] == ["EQ1_SINGLETON_COLLAPSE_LHS"]
    assert rows[0]["family_signals"]["eq1_singleton_side"] == "lhs"
