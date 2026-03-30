from __future__ import annotations

import json
from pathlib import Path

from sair_competition.data.io import read_jsonl, write_jsonl


def attach_family_tags_to_predictions(
    predictions_path: str | Path,
    tagged_dataset_path: str | Path,
    output_path: str | Path,
) -> dict:
    """Backfill family tags/signals into an existing predictions file."""

    prediction_rows = read_jsonl(predictions_path)
    tagged_rows = read_jsonl(tagged_dataset_path)

    tagged_by_problem_id = {
        str(row["problem_id"]): row for row in tagged_rows if row.get("problem_id") is not None
    }
    tagged_by_equations = {
        _equation_key(row): row for row in tagged_rows if row.get("equation1") and row.get("equation2")
    }

    enriched_rows: list[dict] = []
    matched = 0
    unmatched = 0

    for row in prediction_rows:
        tagged_row = None
        if row.get("problem_id") is not None:
            tagged_row = tagged_by_problem_id.get(str(row["problem_id"]))
        if tagged_row is None:
            tagged_row = tagged_by_equations.get(_equation_key(row))

        enriched_row = dict(row)
        if tagged_row is not None:
            matched += 1
            enriched_row["family_tags"] = tagged_row.get("family_tags") or []
            enriched_row["family_signals"] = tagged_row.get("family_signals") or {}
        else:
            unmatched += 1
            enriched_row.setdefault("family_tags", [])
            enriched_row.setdefault("family_signals", {})
        enriched_rows.append(enriched_row)

    target = Path(output_path)
    write_jsonl(target, enriched_rows)

    summary = {
        "predictions_path": str(predictions_path),
        "tagged_dataset_path": str(tagged_dataset_path),
        "output_path": str(target),
        "row_count": len(prediction_rows),
        "matched_rows": matched,
        "unmatched_rows": unmatched,
    }
    (target.parent / "attach_family_tags_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def _equation_key(row: dict) -> tuple[str, str]:
    return (
        str(row.get("equation1") or ""),
        str(row.get("equation2") or ""),
    )
