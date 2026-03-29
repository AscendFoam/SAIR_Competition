from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from sair_competition.data.io import read_jsonl
from sair_competition.paths import REPO_ROOT


@dataclass(slots=True)
class CandidateSnapshot:
    candidate_id: str
    candidate_dir: str
    prompt_path: str
    prompt_bytes: int | None
    model: str
    provider: str
    row_count: int
    accuracy: float
    true_accuracy: float | None
    false_accuracy: float | None
    balanced_accuracy: float | None
    parse_success_rate: float
    average_latency_seconds: float | None
    error_buckets: dict[str, int]

    def to_dict(self) -> dict:
        return asdict(self)


def compare_candidate_runs(
    candidate_dirs: list[str | Path],
    output_dir: str | Path,
    baseline_dir: str | Path | None = None,
) -> dict:
    """Compare multiple candidate run directories and write a summary report."""

    snapshots = [_load_candidate_snapshot(Path(candidate_dir)) for candidate_dir in candidate_dirs]
    ranked = sorted(
        snapshots,
        key=lambda item: (
            item.balanced_accuracy if item.balanced_accuracy is not None else -1.0,
            item.accuracy,
            item.parse_success_rate,
        ),
        reverse=True,
    )

    baseline_snapshot = _load_candidate_snapshot(Path(baseline_dir)) if baseline_dir else None
    deltas = _compute_deltas(ranked, baseline_snapshot)

    summary = {
        "candidate_count": len(ranked),
        "baseline_dir": str(baseline_dir) if baseline_dir else None,
        "ranked_candidates": [candidate.to_dict() for candidate in ranked],
        "deltas_vs_baseline": deltas,
        "recommendation": _build_recommendation(ranked, baseline_snapshot),
    }

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "comparison.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_root / "comparison.md").write_text(_to_markdown(summary), encoding="utf-8")
    return summary


def _load_candidate_snapshot(candidate_dir: Path) -> CandidateSnapshot:
    summary_path = candidate_dir / "summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"Candidate summary not found: {summary_path}")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    metrics = summary["metrics"]
    prompt_path = summary.get("prompt_path") or ""
    prompt_bytes = _resolve_prompt_size(prompt_path)
    average_latency_seconds = _compute_average_latency(candidate_dir / "predictions.jsonl")
    analysis_buckets = _load_error_buckets(candidate_dir)

    return CandidateSnapshot(
        candidate_id=candidate_dir.name,
        candidate_dir=str(candidate_dir),
        prompt_path=prompt_path,
        prompt_bytes=prompt_bytes,
        model=summary.get("model") or "unknown",
        provider=summary.get("provider") or "unknown",
        row_count=summary.get("row_count") or 0,
        accuracy=metrics.get("accuracy") or 0.0,
        true_accuracy=metrics.get("true_accuracy"),
        false_accuracy=metrics.get("false_accuracy"),
        balanced_accuracy=_balanced_accuracy(metrics.get("true_accuracy"), metrics.get("false_accuracy")),
        parse_success_rate=metrics.get("parse_success_rate") or 0.0,
        average_latency_seconds=average_latency_seconds,
        error_buckets=analysis_buckets,
    )


def _balanced_accuracy(true_accuracy: float | None, false_accuracy: float | None) -> float | None:
    if true_accuracy is None or false_accuracy is None:
        return None
    return (true_accuracy + false_accuracy) / 2


def _resolve_prompt_size(prompt_path: str) -> int | None:
    if not prompt_path:
        return None
    path = Path(prompt_path)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.exists():
        return None
    return len(path.read_text(encoding="utf-8").encode("utf-8"))


def _compute_average_latency(predictions_path: Path) -> float | None:
    if not predictions_path.exists():
        return None
    rows = read_jsonl(predictions_path)
    latencies = [float(row["latency_seconds"]) for row in rows if row.get("latency_seconds") is not None]
    if not latencies:
        return None
    return sum(latencies) / len(latencies)


def _load_error_buckets(candidate_dir: Path) -> dict[str, int]:
    analysis_dir = candidate_dir.parent / f"{candidate_dir.name}_analysis"
    summary_path = analysis_dir / "summary.json"
    if not summary_path.exists():
        return {}
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    return dict(summary.get("error_buckets") or {})


def _compute_deltas(
    ranked: list[CandidateSnapshot],
    baseline_snapshot: CandidateSnapshot | None,
) -> list[dict]:
    if baseline_snapshot is None:
        return []

    deltas: list[dict] = []
    for candidate in ranked:
        deltas.append(
            {
                "candidate_id": candidate.candidate_id,
                "accuracy_delta": round(candidate.accuracy - baseline_snapshot.accuracy, 6),
                "true_accuracy_delta": _round_delta(candidate.true_accuracy, baseline_snapshot.true_accuracy),
                "false_accuracy_delta": _round_delta(candidate.false_accuracy, baseline_snapshot.false_accuracy),
                "balanced_accuracy_delta": _round_delta(candidate.balanced_accuracy, baseline_snapshot.balanced_accuracy),
                "parse_success_rate_delta": round(
                    candidate.parse_success_rate - baseline_snapshot.parse_success_rate,
                    6,
                ),
            }
        )
    return deltas


def _round_delta(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    return round(left - right, 6)


def _build_recommendation(
    ranked: list[CandidateSnapshot],
    baseline_snapshot: CandidateSnapshot | None,
) -> dict:
    if not ranked:
        return {"summary": "No candidate runs were supplied."}

    best = ranked[0]
    summary = (
        f"Best balanced candidate is {best.candidate_id} "
        f"(balanced_accuracy={_fmt_rate(best.balanced_accuracy)}, "
        f"accuracy={_fmt_rate(best.accuracy)}, "
        f"parse_success_rate={_fmt_rate(best.parse_success_rate)})."
    )
    if baseline_snapshot is not None:
        accuracy_delta = best.accuracy - baseline_snapshot.accuracy
        balanced_delta = (
            None
            if best.balanced_accuracy is None or baseline_snapshot.balanced_accuracy is None
            else best.balanced_accuracy - baseline_snapshot.balanced_accuracy
        )
        summary += (
            f" Compared with baseline {baseline_snapshot.candidate_id}, "
            f"accuracy_delta={_fmt_signed_rate(accuracy_delta)} and "
            f"balanced_accuracy_delta={_fmt_signed_rate(balanced_delta)}."
        )

    return {
        "best_candidate_id": best.candidate_id,
        "summary": summary,
    }


def _fmt_rate(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.4f}"


def _fmt_signed_rate(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.4f}"


def _to_markdown(summary: dict) -> str:
    lines = [
        "# Candidate Comparison",
        "",
        f"- Candidate count: `{summary['candidate_count']}`",
    ]
    if summary["baseline_dir"]:
        lines.append(f"- Baseline dir: `{summary['baseline_dir']}`")
    lines.extend(
        [
            "",
            "## Ranking",
            "",
            "| Candidate | Accuracy | True Acc | False Acc | Balanced Acc | Parse | Avg Latency (s) | Prompt Bytes |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for candidate in summary["ranked_candidates"]:
        lines.append(
            "| {candidate_id} | {accuracy} | {true_accuracy} | {false_accuracy} | {balanced_accuracy} | {parse} | {latency} | {prompt_bytes} |".format(
                candidate_id=candidate["candidate_id"],
                accuracy=_fmt_rate(candidate["accuracy"]),
                true_accuracy=_fmt_rate(candidate["true_accuracy"]),
                false_accuracy=_fmt_rate(candidate["false_accuracy"]),
                balanced_accuracy=_fmt_rate(candidate["balanced_accuracy"]),
                parse=_fmt_rate(candidate["parse_success_rate"]),
                latency=_fmt_rate(candidate["average_latency_seconds"]),
                prompt_bytes=candidate["prompt_bytes"] if candidate["prompt_bytes"] is not None else "n/a",
            )
        )

    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            summary["recommendation"]["summary"],
            "",
            "## Error Buckets",
            "",
        ]
    )

    for candidate in summary["ranked_candidates"]:
        bucket_text = ", ".join(
            f"{name}={count}"
            for name, count in sorted(candidate["error_buckets"].items(), key=lambda item: (-item[1], item[0]))
        )
        if not bucket_text:
            bucket_text = "none"
        lines.append(f"- `{candidate['candidate_id']}`: {bucket_text}")

    if summary["deltas_vs_baseline"]:
        lines.extend(
            [
                "",
                "## Deltas Vs Baseline",
                "",
            ]
        )
        for delta in summary["deltas_vs_baseline"]:
            lines.append(
                "- `{candidate_id}`: accuracy={accuracy_delta}, true={true_accuracy_delta}, false={false_accuracy_delta}, balanced={balanced_accuracy_delta}, parse={parse_success_rate_delta}".format(
                    candidate_id=delta["candidate_id"],
                    accuracy_delta=_fmt_signed_rate(delta["accuracy_delta"]),
                    true_accuracy_delta=_fmt_signed_rate(delta["true_accuracy_delta"]),
                    false_accuracy_delta=_fmt_signed_rate(delta["false_accuracy_delta"]),
                    balanced_accuracy_delta=_fmt_signed_rate(delta["balanced_accuracy_delta"]),
                    parse_success_rate_delta=_fmt_signed_rate(delta["parse_success_rate_delta"]),
                )
            )

    return "\n".join(lines).strip() + "\n"
