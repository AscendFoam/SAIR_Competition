from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.features.problem_features import build_problem_features


PUBLIC_PROBLEM_FILES = [
    ("normal.jsonl", "normal"),
    ("hard1.jsonl", "hard1"),
    ("hard2.jsonl", "hard2"),
]


def prepare_public_dataset(raw_dir: str | Path, interim_dir: str | Path) -> dict:
    """Normalize official public problem files and sidecar metadata."""

    raw_root = Path(raw_dir)
    interim_root = Path(interim_dir)
    interim_root.mkdir(parents=True, exist_ok=True)

    prepared_rows: list[dict] = []
    source_counts: Counter[str] = Counter()
    label_counts: Counter[bool] = Counter()
    duplicate_ids: list[str] = []
    seen_ids: set[str] = set()

    for filename, source in PUBLIC_PROBLEM_FILES:
        path = raw_root / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing required public problem file: {path}")

        for row in read_jsonl(path):
            problem_id = row["id"]
            if problem_id in seen_ids:
                duplicate_ids.append(problem_id)
            seen_ids.add(problem_id)

            answer = bool(row["answer"])
            features = build_problem_features(row["equation1"], row["equation2"])
            prepared_rows.append(
                {
                    "problem_id": problem_id,
                    "index": row.get("index"),
                    "source": source,
                    "difficulty": row.get("difficulty"),
                    "equation1": row["equation1"],
                    "equation2": row["equation2"],
                    "answer": answer,
                    "split": None,
                    "metadata": {
                        **features,
                        "raw_file": filename,
                    },
                }
            )
            source_counts[source] += 1
            label_counts[answer] += 1

    prepared_rows.sort(key=lambda row: (row["source"], int(row.get("index") or 0), row["problem_id"]))
    write_jsonl(interim_root / "public_all.jsonl", prepared_rows)

    _normalize_jsonl_sidecar(raw_root / "benchmarks.jsonl", interim_root / "benchmarks_registry.jsonl")
    _normalize_jsonl_sidecar(raw_root / "prompt_templates.jsonl", interim_root / "prompt_templates_registry.jsonl")
    _normalize_jsonl_sidecar(raw_root / "leaderboard.jsonl", interim_root / "leaderboard_snapshot.jsonl")
    _normalize_models_csv(raw_root / "models.csv", interim_root / "model_registry.jsonl")

    summary = {
        "total_problems": len(prepared_rows),
        "source_counts": dict(source_counts),
        "label_counts": {
            "true": label_counts[True],
            "false": label_counts[False],
        },
        "duplicate_problem_ids": duplicate_ids,
        "problem_files": [filename for filename, _ in PUBLIC_PROBLEM_FILES],
        "auxiliary_files_detected": sorted(
            [
                path.name
                for path in raw_root.iterdir()
                if path.is_file() and path.name not in {filename for filename, _ in PUBLIC_PROBLEM_FILES}
            ]
        ),
        "outputs": {
            "public_all": str(interim_root / "public_all.jsonl"),
            "benchmarks_registry": str(interim_root / "benchmarks_registry.jsonl"),
            "prompt_templates_registry": str(interim_root / "prompt_templates_registry.jsonl"),
            "leaderboard_snapshot": str(interim_root / "leaderboard_snapshot.jsonl"),
            "model_registry": str(interim_root / "model_registry.jsonl"),
        },
    }

    (interim_root / "public_dataset_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def build_split_manifest(split_rows: dict[str, list[dict]]) -> dict:
    """Create a split summary for reporting and reproducibility."""

    manifest: dict[str, dict] = {}
    for split_name, rows in split_rows.items():
        by_source = Counter(row["source"] for row in rows)
        by_label = Counter(bool(row["answer"]) for row in rows)
        by_source_and_label: dict[str, dict[str, int]] = defaultdict(lambda: {"true": 0, "false": 0})
        for row in rows:
            source_bucket = by_source_and_label[row["source"]]
            source_bucket["true" if row["answer"] else "false"] += 1

        manifest[split_name] = {
            "count": len(rows),
            "by_source": dict(by_source),
            "by_label": {
                "true": by_label[True],
                "false": by_label[False],
            },
            "by_source_and_label": dict(by_source_and_label),
        }
    return manifest


def _normalize_jsonl_sidecar(input_path: Path, output_path: Path) -> None:
    """将辅助 JSONL 文件原样拷贝到目标路径。

    如果输入文件不存在则静默跳过。

    Args:
        input_path: 原始 JSONL 文件路径。
        output_path: 标准化后的输出路径。
    """
    if not input_path.exists():
        return
    rows = read_jsonl(input_path)
    write_jsonl(output_path, rows)


def _normalize_models_csv(input_path: Path, output_path: Path) -> None:
    """将 CSV 模型注册表文件转换为 JSONL 格式。

    如果输入文件不存在则静默跳过。

    Args:
        input_path: 原始 CSV 文件路径。
        output_path: 转换后的 JSONL 输出路径。
    """
    if not input_path.exists():
        return

    rows: list[dict] = []
    with input_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(dict(row))
    write_jsonl(output_path, rows)

