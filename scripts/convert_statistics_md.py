from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


EXPECTED_PREFIX = ["Details", "▾"]
OUTPUT_COLUMNS = [
    "record_order",
    "rank",
    "team_name",
    "team_index",
    "score",
    "avg_accuracy_pct",
    "avg_f1_pct",
    "parse_rate_pct",
    "avg_cost_usd",
    "cheatsheet_size_kb",
]


def split_blocks(text: str) -> list[dict[str, object]]:
    blocks: list[dict[str, object]] = []
    current: list[str] = []
    start_line: int | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.strip():
            if start_line is None:
                start_line = line_number
            current.append(line)
            continue

        if current:
            blocks.append(
                {
                    "start_line": start_line,
                    "end_line": line_number - 1,
                    "lines": current,
                }
            )
            current = []
            start_line = None

    if current:
        blocks.append(
            {
                "start_line": start_line,
                "end_line": len(text.splitlines()),
                "lines": current,
            }
        )

    return blocks


def parse_int(text: str) -> int:
    return int(text.replace(",", ""))


def parse_pct(text: str) -> float:
    return float(text.rstrip("%"))


def parse_usd(text: str) -> float:
    return float(text.lstrip("$"))


def parse_kb(text: str) -> float:
    return float(text.removesuffix(" KB"))


def parse_record(record_order: int, values: list[str]) -> dict[str, object]:
    return {
        "record_order": record_order,
        "rank": parse_int(values[0]),
        "team_name": values[1],
        "team_index": values[2],
        "score": parse_int(values[3]),
        "avg_accuracy_pct": parse_pct(values[4]),
        "avg_f1_pct": parse_pct(values[5]),
        "parse_rate_pct": parse_pct(values[6]),
        "avg_cost_usd": parse_usd(values[7]),
        "cheatsheet_size_kb": parse_kb(values[8]),
    }


def convert(input_path: Path, csv_path: Path, jsonl_path: Path, issues_path: Path) -> dict[str, int]:
    blocks = split_blocks(input_path.read_text(encoding="utf-8"))
    if not blocks:
        raise ValueError(f"No non-empty blocks found in {input_path}")

    header_block = blocks[0]
    header_lines = header_block["lines"]
    if not isinstance(header_lines, list) or len(header_lines) != 11:
        raise ValueError("Header block does not match the expected 11-line format.")

    issues: list[dict[str, object]] = []
    records: list[dict[str, object]] = []

    for block_index, block in enumerate(blocks[1:], start=1):
        lines = block["lines"]
        if not isinstance(lines, list):
            continue

        if len(lines) != 11:
            issues.append(
                {
                    "block_index": block_index,
                    "start_line": block["start_line"],
                    "end_line": block["end_line"],
                    "issue": "unexpected_block_length",
                    "expected_length": 11,
                    "actual_length": len(lines),
                    "raw_lines": lines,
                }
            )
            continue

        if lines[:2] != EXPECTED_PREFIX:
            issues.append(
                {
                    "block_index": block_index,
                    "start_line": block["start_line"],
                    "end_line": block["end_line"],
                    "issue": "unexpected_prefix",
                    "expected_prefix": EXPECTED_PREFIX,
                    "actual_prefix": lines[:2],
                    "raw_lines": lines,
                }
            )
            continue

        try:
            records.append(parse_record(record_order=len(records) + 1, values=lines[2:]))
        except ValueError as exc:
            issues.append(
                {
                    "block_index": block_index,
                    "start_line": block["start_line"],
                    "end_line": block["end_line"],
                    "issue": "value_parse_error",
                    "error": str(exc),
                    "raw_lines": lines,
                }
            )

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(records)

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    issues_payload = {
        "input_path": str(input_path),
        "header_block": {
            "start_line": header_block["start_line"],
            "end_line": header_block["end_line"],
            "raw_lines": header_lines,
        },
        "record_count": len(records),
        "issue_count": len(issues),
        "issues": issues,
    }
    issues_path.write_text(
        json.dumps(issues_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return {
        "record_count": len(records),
        "issue_count": len(issues),
        "block_count": len(blocks),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert docs/statistics.md into structured CSV and JSONL tables."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("docs/statistics.md"),
        help="Input markdown-like statistics file.",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=Path("docs/statistics_table.csv"),
        help="CSV output path.",
    )
    parser.add_argument(
        "--jsonl-output",
        type=Path,
        default=Path("docs/statistics_table.jsonl"),
        help="JSONL output path.",
    )
    parser.add_argument(
        "--issues-output",
        type=Path,
        default=Path("docs/statistics_parse_issues.json"),
        help="Path for parse issues and anomaly report.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    summary = convert(args.input, args.csv_output, args.jsonl_output, args.issues_output)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
