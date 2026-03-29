import json
from pathlib import Path

from sair_competition.analysis.experiment_report import compare_candidate_runs


def test_compare_candidate_runs_ranks_by_balanced_accuracy(tmp_path: Path) -> None:
    base = _make_candidate(
        tmp_path,
        "candidate_a",
        accuracy=0.6,
        true_accuracy=0.4,
        false_accuracy=0.8,
        error_buckets={"RULE_MISSING": 2},
        latency_values=[1.0, 2.0],
    )
    better = _make_candidate(
        tmp_path,
        "candidate_b",
        accuracy=0.55,
        true_accuracy=0.7,
        false_accuracy=0.7,
        error_buckets={"RULE_CONFLICT": 1},
        latency_values=[3.0, 5.0],
    )

    output_dir = tmp_path / "report"
    summary = compare_candidate_runs(
        candidate_dirs=[base, better],
        baseline_dir=base,
        output_dir=output_dir,
    )

    assert summary["ranked_candidates"][0]["candidate_id"] == "candidate_b"
    assert summary["recommendation"]["best_candidate_id"] == "candidate_b"
    assert (output_dir / "comparison.json").exists()
    assert (output_dir / "comparison.md").exists()


def _make_candidate(
    root: Path,
    name: str,
    accuracy: float,
    true_accuracy: float,
    false_accuracy: float,
    error_buckets: dict[str, int],
    latency_values: list[float],
) -> Path:
    candidate_dir = root / name
    candidate_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = root / f"{name}.txt"
    prompt_path.write_text("true", encoding="utf-8")

    summary = {
        "prompt_path": str(prompt_path),
        "provider": "deepseek",
        "model": "deepseek-chat",
        "row_count": len(latency_values),
        "metrics": {
            "accuracy": accuracy,
            "true_accuracy": true_accuracy,
            "false_accuracy": false_accuracy,
            "parse_success_rate": 1.0,
        },
    }
    (candidate_dir / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
    (candidate_dir / "predictions.jsonl").write_text(
        "\n".join(json.dumps({"latency_seconds": value}) for value in latency_values),
        encoding="utf-8",
    )

    analysis_dir = root / f"{name}_analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    (analysis_dir / "summary.json").write_text(
        json.dumps({"error_buckets": error_buckets}),
        encoding="utf-8",
    )
    return candidate_dir
