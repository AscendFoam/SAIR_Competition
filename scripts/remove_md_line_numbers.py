from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


LINE_NUMBER_PATTERN = re.compile(r"^\s*\d+\s*$")


@dataclass
class FileResult:
    path: Path
    removed_lines: int
    changed: bool


def clean_text(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    kept_lines: list[str] = []
    removed_lines = 0

    for line in lines:
        if LINE_NUMBER_PATTERN.match(line):
            removed_lines += 1
            continue
        kept_lines.append(line)

    return "".join(kept_lines), removed_lines


def iter_markdown_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() == ".md" else []
    return sorted(path for path in target.rglob("*.md") if path.is_file())


def process_paths(target: Path, dry_run: bool) -> list[FileResult]:
    results: list[FileResult] = []

    for path in iter_markdown_files(target):
        original_text = path.read_text(encoding="utf-8")
        cleaned_text, removed_lines = clean_text(original_text)
        changed = cleaned_text != original_text

        if changed and not dry_run:
            path.write_text(cleaned_text, encoding="utf-8")

        results.append(
            FileResult(
                path=path,
                removed_lines=removed_lines,
                changed=changed,
            )
        )

    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Remove standalone numeric line-number rows from markdown files."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=Path("docs/model_cheatsheet"),
        help="Markdown file or directory to clean. Defaults to docs/model_cheatsheet.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    results = process_paths(args.target, dry_run=args.dry_run)
    changed_files = [result for result in results if result.changed]

    summary = {
        "target": str(args.target),
        "dry_run": args.dry_run,
        "scanned_files": len(results),
        "changed_files": len(changed_files),
        "removed_lines": sum(result.removed_lines for result in results),
        "files": [
            {
                "path": str(result.path),
                "removed_lines": result.removed_lines,
            }
            for result in changed_files
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
