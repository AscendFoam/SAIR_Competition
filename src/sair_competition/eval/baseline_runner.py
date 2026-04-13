from __future__ import annotations

import json
from pathlib import Path

from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.eval.baselines import BaselinePredictor, get_baseline_predictors
from sair_competition.eval.metrics import compute_metrics


def run_baseline_suite(
    dataset_path: str | Path,
    output_dir: str | Path,
    predictor_names: list[str] | None = None,
    prompt_path: str | Path | None = None,
) -> dict:
    """Run one or more baseline predictors against a dataset or frozen split."""

    rows = read_jsonl(dataset_path)
    predictors = _select_predictors(predictor_names)
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    suite_summary: dict[str, dict] = {
        "dataset_path": str(dataset_path),
        "prompt_path": str(prompt_path) if prompt_path else None,
        "row_count": len(rows),
        "predictors": {},
    }

    for predictor in predictors:
        prediction_rows: list[dict] = []
        for row in rows:
            prediction = predictor.predict(row)
            prediction_rows.append(
                {
                    "problem_id": row["problem_id"],
                    "source": row["source"],
                    "split": row.get("split"),
                    "equation1": row.get("equation1"),
                    "equation2": row.get("equation2"),
                    "answer": row["answer"],
                    "prediction": prediction,
                    "parsed": True,
                    "baseline": predictor.name,
                    "family_tags": row.get("family_tags") or [],
                    "family_signals": row.get("family_signals") or {},
                }
            )

        metrics = compute_metrics(prediction_rows)
        write_jsonl(output_root / f"{predictor.name}_predictions.jsonl", prediction_rows)
        predictor_summary = {
            "description": predictor.description,
            "metrics": metrics.to_dict(),
        }
        suite_summary["predictors"][predictor.name] = predictor_summary

    (output_root / "summary.json").write_text(json.dumps(suite_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return suite_summary


def _select_predictors(predictor_names: list[str] | None) -> list[BaselinePredictor]:
    """按名称选择预测器子集，或返回全部预测器。

    Args:
        predictor_names: 预测器名称列表，为 ``None`` 时返回全部。

    Returns:
        匹配的预测器实例列表。

    Raises:
        KeyError: 指定名称不存在时抛出。
    """
    all_predictors = {predictor.name: predictor for predictor in get_baseline_predictors()}
    if not predictor_names:
        return list(all_predictors.values())

    selected: list[BaselinePredictor] = []
    for name in predictor_names:
        if name not in all_predictors:
            available = ", ".join(sorted(all_predictors))
            raise KeyError(f"Unknown predictor '{name}'. Available predictors: {available}")
        selected.append(all_predictors[name])
    return selected
