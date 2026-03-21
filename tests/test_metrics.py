from sair_competition.eval.metrics import compute_metrics


def test_compute_metrics_basic_counts() -> None:
    metrics = compute_metrics(
        [
            {"answer": True, "prediction": True, "parsed": True, "source": "normal"},
            {"answer": False, "prediction": False, "parsed": True, "source": "normal"},
            {"answer": False, "prediction": True, "parsed": True, "source": "hard2"},
            {"answer": True, "prediction": None, "parsed": False, "source": "hard1"},
        ]
    )

    assert metrics.total == 4
    assert metrics.parsed == 3
    assert metrics.correct == 2
    assert metrics.true_total == 2
    assert metrics.false_total == 2
    assert metrics.by_source["normal"] == 1.0

