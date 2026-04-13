from pathlib import Path

import pytest

from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.features.family_tagger import (
    FAMILY_TAG_TAXONOMY,
    build_family_annotation,
    tag_problem_families,
)


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
    assert "EQ2_MORE_COMPLEX" not in summary["tag_counts"]


@pytest.mark.parametrize(
    ("equation1", "equation2"),
    [
        ("x = (y * (z * z)) * z", "x = y * (x * ((z * w) * u))"),
        ("x = y * (y * ((z * z) * y))", "x = (y * (z * x)) * (z * w)"),
    ],
)
def test_target_shared_lhs_and_new_vars_hits_expected_examples(equation1: str, equation2: str) -> None:
    annotation = build_family_annotation(equation1, equation2)

    assert "TARGET_SHARED_LHS_AND_NEW_VARS" in annotation["family_tags"]
    assert annotation["family_signals"]["eq2_rhs_reuses_eq1_lhs_var"] is True


@pytest.mark.parametrize(
    ("equation1", "equation2"),
    [
        ("x = (y * (z * z)) * z", "x = y * (x * ((z * w) * u))"),
        ("x = y * (y * ((z * z) * y))", "x = (y * (z * x)) * (z * w)"),
    ],
)
def test_target_shared_lhs_and_new_vars_singleton_source_hits_clean_true_examples(
    equation1: str,
    equation2: str,
) -> None:
    annotation = build_family_annotation(equation1, equation2)

    assert "TARGET_SHARED_LHS_AND_NEW_VARS_SINGLETON_SOURCE" in annotation["family_tags"]
    assert annotation["family_signals"]["eq1_rhs_eq1_lhs_var_count"] == 0
    assert annotation["family_signals"]["eq2_rhs_eq1_lhs_var_count"] == 1


def test_target_shared_lhs_and_new_vars_full_carry_single_x_isolated_to_full_carry_example() -> None:
    annotation = build_family_annotation(
        "x = y * (((x * x) * z) * w)",
        "x = (y * (z * (w * u))) * x",
    )

    assert "TARGET_SHARED_LHS_AND_NEW_VARS_FULL_CARRY_SINGLE_X" in annotation["family_tags"]
    assert annotation["family_signals"]["eq2_rhs_reuses_all_non_lhs_eq1_vars"] is True
    assert annotation["family_signals"]["eq2_rhs_eq1_lhs_var_count"] == 1


@pytest.mark.parametrize(
    ("equation1", "equation2"),
    [
        ("x = y * (x * ((x * x) * y))", "x = y * (x * ((x * z) * w))"),
        ("x = (y * (x * x)) * (y * y)", "x = (y * y) * (x * (z * x))"),
    ],
)
def test_target_shared_lhs_and_new_vars_x_repeat_single_anchor_hits_false_boundary_examples(
    equation1: str,
    equation2: str,
) -> None:
    annotation = build_family_annotation(equation1, equation2)

    assert "TARGET_SHARED_LHS_AND_NEW_VARS_X_REPEAT_SINGLE_ANCHOR" in annotation["family_tags"]
    assert annotation["family_signals"]["eq2_rhs_eq1_lhs_var_count"] >= 2
    assert annotation["family_signals"]["eq2_rhs_retained_non_lhs_eq1_var_count"] == 1


@pytest.mark.parametrize(
    ("equation1", "equation2"),
    [
        ("x = x * ((y * (x * x)) * z)", "x = (y * y) * ((x * z) * w)"),
        ("x = ((y * x) * (z * y)) * x", "x = y * (((z * x) * x) * w)"),
    ],
)
def test_target_shared_lhs_and_new_vars_x_heavy_two_anchor_hits_false_boundary_examples(
    equation1: str,
    equation2: str,
) -> None:
    annotation = build_family_annotation(equation1, equation2)

    assert "TARGET_SHARED_LHS_AND_NEW_VARS_X_HEAVY_TWO_ANCHOR" in annotation["family_tags"]
    assert annotation["family_signals"]["eq1_rhs_eq1_lhs_var_count"] >= 2
    assert annotation["family_signals"]["eq2_rhs_retained_non_lhs_eq1_var_count"] == 2


@pytest.mark.parametrize(
    ("equation1", "equation2"),
    [
        ("x = y * (y * ((y * z) * y))", "x = (((y * z) * x) * x) * y"),
        ("x = ((y * z) * (z * z)) * w", "x = ((y * x) * x) * (z * x)"),
        ("x = y * ((z * y) * (y * w))", "x = y * (((x * x) * x) * y)"),
    ],
)
def test_target_lhs_amplification_hits_expected_examples(equation1: str, equation2: str) -> None:
    annotation = build_family_annotation(equation1, equation2)

    assert "TARGET_LHS_AMPLIFICATION" in annotation["family_tags"]
    assert annotation["family_signals"]["eq2_rhs_eq1_lhs_var_count"] >= 2
    assert annotation["family_signals"]["eq2_rhs_retains_non_lhs_eq1_var"] is True


@pytest.mark.parametrize(
    ("equation1", "equation2"),
    [
        ("x = y * (y * ((y * z) * y))", "x = (((y * z) * x) * x) * y"),
        ("x = ((y * z) * (z * z)) * w", "x = ((y * x) * x) * (z * x)"),
    ],
)
def test_target_lhs_amplification_multi_anchor_hits_high_confidence_examples(
    equation1: str,
    equation2: str,
) -> None:
    annotation = build_family_annotation(equation1, equation2)

    assert "TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR" in annotation["family_tags"]
    assert "TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR" not in annotation["family_tags"]
    assert annotation["family_signals"]["eq2_rhs_retained_non_lhs_eq1_var_count"] >= 2


def test_target_lhs_amplification_single_anchor_hits_boundary_example() -> None:
    annotation = build_family_annotation(
        "x = y * ((z * y) * (y * w))",
        "x = y * (((x * x) * x) * y)",
    )

    assert "TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR" in annotation["family_tags"]
    assert "TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR" not in annotation["family_tags"]
    assert annotation["family_signals"]["eq2_rhs_retained_non_lhs_eq1_var_count"] == 1


def test_target_lhs_amplification_excludes_single_slot_insertion_example() -> None:
    annotation = build_family_annotation(
        "x = y * (z * (z * (w * z)))",
        "x = y * (x * (z * (w * z)))",
    )

    assert "TARGET_LHS_AMPLIFICATION" not in annotation["family_tags"]
    assert annotation["family_signals"]["eq2_rhs_eq1_lhs_var_count"] == 1


@pytest.mark.parametrize(
    ("equation1", "equation2"),
    [
        ("x = y * (z * ((w * z) * w))", "x = ((x * x) * (y * y)) * y"),
        ("x = y * (z * (y * (y * z)))", "x = y * (((x * x) * x) * y)"),
    ],
)
def test_target_lhs_amplification_excludes_false_positives(equation1: str, equation2: str) -> None:
    annotation = build_family_annotation(equation1, equation2)

    assert "TARGET_LHS_AMPLIFICATION" not in annotation["family_tags"]
    assert annotation["family_signals"]["eq2_rhs_retains_non_lhs_eq1_var"] is True


def test_eq2_more_complex_is_removed_from_emitted_taxonomy_and_tags() -> None:
    annotation = build_family_annotation("x = (y * z)", "x = ((y * z) * w)")

    assert "EQ2_MORE_COMPLEX" not in FAMILY_TAG_TAXONOMY
    assert "EQ2_MORE_COMPLEX" not in annotation["family_tags"]
    assert annotation["family_signals"]["eq2_more_complex"] is True


def test_target_shared_lhs_and_new_vars_children_partition_smoke_examples() -> None:
    cases = [
        (
            "x = y * (((x * x) * z) * w)",
            "x = (y * (z * (w * u))) * x",
            {"TARGET_SHARED_LHS_AND_NEW_VARS_FULL_CARRY_SINGLE_X"},
        ),
        (
            "x = (y * (z * z)) * z",
            "x = y * (x * ((z * w) * u))",
            {"TARGET_SHARED_LHS_AND_NEW_VARS_SINGLETON_SOURCE"},
        ),
        (
            "x = y * (x * ((x * x) * y))",
            "x = y * (x * ((x * z) * w))",
            {"TARGET_SHARED_LHS_AND_NEW_VARS_X_REPEAT_SINGLE_ANCHOR"},
        ),
        (
            "x = x * ((y * (x * x)) * z)",
            "x = (y * y) * ((x * z) * w)",
            {"TARGET_SHARED_LHS_AND_NEW_VARS_X_HEAVY_TWO_ANCHOR"},
        ),
    ]

    child_tags = {
        "TARGET_SHARED_LHS_AND_NEW_VARS_SINGLETON_SOURCE",
        "TARGET_SHARED_LHS_AND_NEW_VARS_FULL_CARRY_SINGLE_X",
        "TARGET_SHARED_LHS_AND_NEW_VARS_X_REPEAT_SINGLE_ANCHOR",
        "TARGET_SHARED_LHS_AND_NEW_VARS_X_HEAVY_TWO_ANCHOR",
    }
    for equation1, equation2, expected_tags in cases:
        annotation = build_family_annotation(equation1, equation2)
        matched = child_tags.intersection(annotation["family_tags"])

        assert matched == expected_tags


def test_target_lhs_amplification_children_partition_smoke_examples() -> None:
    cases = [
        (
            "x = y * (y * ((y * z) * y))",
            "x = (((y * z) * x) * x) * y",
            {"TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR"},
        ),
        (
            "x = ((y * z) * (z * z)) * w",
            "x = ((y * x) * x) * (z * x)",
            {"TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR"},
        ),
        (
            "x = y * ((z * y) * (y * w))",
            "x = y * (((x * x) * x) * y)",
            {"TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR"},
        ),
    ]

    child_tags = {
        "TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR",
        "TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR",
    }
    for equation1, equation2, expected_tags in cases:
        annotation = build_family_annotation(equation1, equation2)
        matched = child_tags.intersection(annotation["family_tags"])

        assert matched == expected_tags
