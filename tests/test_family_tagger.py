from pathlib import Path

from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.features.family_tagger import build_family_annotation, tag_problem_families


def test_build_family_annotation_detects_singleton_and_disjoint_tags() -> None:
    annotation = build_family_annotation("x = (y * z)", "x = (a * b)")

    assert "EQ1_SINGLETON_COLLAPSE_LHS" in annotation["family_tags"]
    assert "EQ1_SINGLETON_COLLAPSE_LHS_TO_BINARY" in annotation["family_tags"]
    assert "EQ1_SINGLETON_COLLAPSE_WITH_DISJOINT_SIDES" in annotation["family_tags"]
    assert "EQ1_DISJOINT_SIDES" in annotation["family_tags"]
    assert "EQ1_DISJOINT_SIDES_VAR_BINARY" in annotation["family_tags"]
    assert "EQ1_CONSTANT_OPERATION_VAR_BINARY" in annotation["family_tags"]
    assert annotation["family_signals"]["eq1_disjoint_shape"] == "var_to_binary"
    assert annotation["family_signals"]["eq1_side_vars_disjoint"] is True


def test_tag_problem_families_writes_tagged_dataset_and_summary(tmp_path: Path) -> None:
    dataset_path = tmp_path / "dataset.jsonl"
    tagged_path = tmp_path / "tagged.jsonl"
    summary_dir = tmp_path / "summary"
    write_jsonl(
        dataset_path,
        [
            {
                "problem_id": "p1",
                "equation1": "x = (y * z)",
                "equation2": "a = (b * c)",
                "answer": True,
                "source": "normal",
                "split": "smoke",
            },
            {
                "problem_id": "p2",
                "equation1": "(x * y) = (y * x)",
                "equation2": "x = x",
                "answer": False,
                "source": "hard1",
                "split": "smoke",
            },
        ],
    )

    summary = tag_problem_families(dataset_path=dataset_path, output_path=tagged_path, summary_dir=summary_dir)
    rows = read_jsonl(tagged_path)

    assert rows[0]["family_tags"]
    assert summary["tag_counts"]["EQ1_SINGLETON_COLLAPSE_LHS"] == 1
    assert summary["tag_counts"]["TARGET_TAUTOLOGY"] == 1
    assert summary["focus_group_summary"]["singleton_collapse"]["row_count"] == 1
    assert summary["focus_group_summary"]["disjoint_sides"]["row_count"] == 1
