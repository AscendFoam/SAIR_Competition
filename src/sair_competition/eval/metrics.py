from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Iterable

@dataclass(slots=True)
class EvalMetrics:
    total: int
    parsed: int
    parse_success_rate: float
    correct: int
    accuracy: float
    true_total: int
    true_correct: int
    false_total: int
    false_correct: int
    true_accuracy: float | None = None
    false_accuracy: float | None = None
    by_source: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        import json

        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


def _safe_rate(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def compute_metrics(records: Iterable[dict]) -> EvalMetrics:
    """Compute basic metrics from eval records."""

    rows = list(records)
    total = len(rows)
    parsed = sum(1 for row in rows if row.get("parsed", True))
    correct = sum(1 for row in rows if row.get("prediction") is not None and row.get("prediction") == row.get("answer"))

    true_rows = [row for row in rows if row.get("answer") is True]
    false_rows = [row for row in rows if row.get("answer") is False]
    true_correct = sum(1 for row in true_rows if row.get("prediction") is True)
    false_correct = sum(1 for row in false_rows if row.get("prediction") is False)

    by_source_counter: Counter[str] = Counter()
    by_source_correct: Counter[str] = Counter()
    for row in rows:
        source = row.get("source")
        if not source:
            continue
        by_source_counter[source] += 1
        if row.get("prediction") is not None and row.get("prediction") == row.get("answer"):
            by_source_correct[source] += 1

    by_source = {
        source: by_source_correct[source] / count
        for source, count in by_source_counter.items()
        if count > 0
    }

    return EvalMetrics(
        total=total,
        parsed=parsed,
        parse_success_rate=_safe_rate(parsed, total) or 0.0,
        correct=correct,
        accuracy=_safe_rate(correct, total) or 0.0,
        true_total=len(true_rows),
        true_correct=true_correct,
        true_accuracy=_safe_rate(true_correct, len(true_rows)),
        false_total=len(false_rows),
        false_correct=false_correct,
        false_accuracy=_safe_rate(false_correct, len(false_rows)),
        by_source=by_source,
    )
