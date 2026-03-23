from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.data.public_data import build_split_manifest


def make_frozen_splits(
    dataset_path: str | Path,
    output_dir: str | Path,
    split_targets: dict[str, int],
    seed: int = 20260322,
) -> dict:
    """Create deterministic stratified splits with exact target sizes."""

    dataset = read_jsonl(dataset_path)
    total = len(dataset)
    if sum(split_targets.values()) != total:
        raise ValueError(
            f"Split target sizes sum to {sum(split_targets.values())}, but dataset contains {total} rows."
        )

    grouped = _group_and_shuffle(dataset, seed=seed)
    remaining_groups = {key: rows[:] for key, rows in grouped.items()}
    split_rows: dict[str, list[dict]] = {}

    for split_name, split_size in split_targets.items():
        allocations = _apportion_counts(
            {key: len(rows) for key, rows in remaining_groups.items()},
            split_size,
        )
        current_rows: list[dict] = []
        for key in sorted(remaining_groups):
            take_count = allocations.get(key, 0)
            if take_count <= 0:
                continue
            chosen = remaining_groups[key][:take_count]
            remaining_groups[key] = remaining_groups[key][take_count:]
            for row in chosen:
                enriched = dict(row)
                enriched["split"] = split_name
                current_rows.append(enriched)
        current_rows.sort(key=lambda row: (row["source"], int(row.get("index") or 0), row["problem_id"]))
        split_rows[split_name] = current_rows

    leftovers = sum(len(rows) for rows in remaining_groups.values())
    if leftovers != 0:
        raise RuntimeError(f"Expected no leftover rows after split allocation, found {leftovers}")

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    for split_name, rows in split_rows.items():
        write_jsonl(output_root / f"{split_name}.jsonl", rows)

    manifest = {
        "seed": seed,
        "dataset_path": str(dataset_path),
        "split_targets": split_targets,
        "splits": build_split_manifest(split_rows),
    }
    (output_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def _group_and_shuffle(rows: list[dict], seed: int) -> dict[tuple[str, bool], list[dict]]:
    grouped: dict[tuple[str, bool], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["source"], bool(row["answer"]))].append(row)

    for key, group_rows in grouped.items():
        group_rows.sort(key=lambda row: row["problem_id"])
        random.Random(f"{seed}:{key[0]}:{int(key[1])}").shuffle(group_rows)
    return grouped


def _apportion_counts(group_sizes: dict[tuple[str, bool], int], target_total: int) -> dict[tuple[str, bool], int]:
    if target_total == 0:
        return {key: 0 for key in group_sizes}

    total_available = sum(group_sizes.values())
    if target_total > total_available:
        raise ValueError(f"Cannot allocate {target_total} rows from only {total_available} available rows.")

    quotas: dict[tuple[str, bool], float] = {}
    allocations: dict[tuple[str, bool], int] = {}
    remainders: list[tuple[float, tuple[str, bool]]] = []

    for key, size in group_sizes.items():
        exact = (size / total_available) * target_total if total_available else 0.0
        floor_value = min(size, int(exact))
        quotas[key] = exact
        allocations[key] = floor_value
        remainders.append((exact - floor_value, key))

    allocated = sum(allocations.values())
    remaining = target_total - allocated
    for _, key in sorted(remainders, key=lambda item: (-item[0], item[1][0], item[1][1])):
        if remaining == 0:
            break
        if allocations[key] < group_sizes[key]:
            allocations[key] += 1
            remaining -= 1

    if remaining != 0:
        raise RuntimeError("Failed to apportion exact split counts.")

    return allocations

