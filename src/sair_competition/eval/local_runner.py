from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from sair_competition.config.env import resolve_openai_compatible_settings
from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.eval.metrics import compute_metrics
from sair_competition.eval.parser import parse_bool_output
from sair_competition.eval.openai_compatible import OpenAICompatibleClient
from sair_competition.prompting.compose import load_text
from sair_competition.prompting.render import render_complete_prompt_for_problem


def run_complete_prompt_eval(
    dataset_path: str | Path,
    prompt_path: str | Path,
    output_dir: str | Path,
    dotenv_path: str | Path,
    model: str | None = None,
    limit: int | None = None,
    temperature: float = 0.0,
    max_tokens: int = 256,
) -> dict:
    """Run a complete prompt against a local dataset using an OpenAI-compatible API."""

    rows = read_jsonl(dataset_path)
    if limit is not None:
        rows = rows[:limit]

    prompt_template = load_text(prompt_path)
    settings = resolve_openai_compatible_settings(dotenv_path=dotenv_path, model=model)
    client = OpenAICompatibleClient(settings)

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    prediction_rows: list[dict] = []
    parse_counter: Counter[str] = Counter()
    for row in rows:
        prompt = render_complete_prompt_for_problem(
            complete_prompt_text=prompt_template,
            equation1=row["equation1"],
            equation2=row["equation2"],
        )
        completion = client.complete(prompt=prompt, temperature=temperature, max_tokens=max_tokens)
        parsed = parse_bool_output(completion.raw_output)
        parsed_ok = parsed is not None
        if parsed_ok:
            parse_counter["parsed"] += 1
        else:
            parse_counter["unparsed"] += 1

        prediction_rows.append(
            {
                "problem_id": row["problem_id"],
                "source": row["source"],
                "split": row.get("split"),
                "equation1": row["equation1"],
                "equation2": row["equation2"],
                "answer": row["answer"],
                "prediction": parsed,
                "parsed": parsed_ok,
                "raw_output": completion.raw_output,
                "latency_seconds": completion.latency_seconds,
                "prompt_path": str(prompt_path),
                "model": settings.model,
                "provider": settings.provider_name,
            }
        )

    metrics = compute_metrics(prediction_rows)
    write_jsonl(output_root / "predictions.jsonl", prediction_rows)

    summary = {
        "dataset_path": str(dataset_path),
        "prompt_path": str(prompt_path),
        "dotenv_path": str(dotenv_path),
        "provider": settings.provider_name,
        "model": settings.model,
        "row_count": len(prediction_rows),
        "parse_counter": dict(parse_counter),
        "metrics": metrics.to_dict(),
    }
    (output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
