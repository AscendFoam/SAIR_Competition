from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Iterable

@dataclass(slots=True)
class EvalMetrics:
    """评估指标汇总数据类。

    包含准确率、解析成功率、True/False 类别准确率及按数据来源分组的准确率。

    Attributes:
        total: 总样本数。
        parsed: 成功解析的样本数。
        parse_success_rate: 解析成功率。
        correct: 预测正确的样本数。
        accuracy: 总体准确率。
        true_total: 真实标签为 True 的样本数。
        true_correct: True 样本中预测正确数。
        false_total: 真实标签为 False 的样本数。
        false_correct: False 样本中预测正确数。
        true_accuracy: True 类准确率，无 True 样本时为 ``None``。
        false_accuracy: False 类准确率，无 False 样本时为 ``None``。
        by_source: 按数据来源分组的准确率字典。
    """

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
        """将指标转换为普通字典。"""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """将指标序列化为 JSON 字符串。

        Args:
            indent: JSON 缩进空格数，默认 2。

        Returns:
            格式化后的 JSON 字符串。
        """
        import json

        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


def _safe_rate(numerator: int, denominator: int) -> float | None:
    """安全除法，分母为零时返回 ``None``。"""
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
