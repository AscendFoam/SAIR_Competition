from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Iterable, TypeVar

T = TypeVar("T")


def read_jsonl(path: str | Path) -> list[dict]:
    """Read a JSONL file into a list of dictionaries."""

    rows: list[dict] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: str | Path, rows: Iterable[dict | object]) -> None:
    """Write dictionaries or dataclass instances to JSONL."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        for row in rows:
            payload = asdict(row) if is_dataclass(row) else row
            handle.write(json.dumps(payload, ensure_ascii=False))
            handle.write("\n")


def load_models(path: str | Path, model_cls: type[T]) -> list[T]:
    """Load a JSONL file into dataclass or class instances via keyword args."""

    return [model_cls(**row) for row in read_jsonl(path)]
