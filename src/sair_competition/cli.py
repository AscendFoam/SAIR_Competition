from __future__ import annotations

import argparse
from pathlib import Path

from .analysis.error_taxonomy import ERROR_TAXONOMY
from .eval.metrics import compute_metrics
from .eval.parser import parse_bool_output
from .paths import REPO_ROOT
from .prompting.compose import build_complete_prompt

EXPECTED_PATHS = [
    "data/raw",
    "data/interim",
    "data/interim/splits",
    "data/external",
    "prompts/templates",
    "prompts/cheatsheets",
    "prompts/complete",
    "configs/models",
    "configs/eval",
    "configs/prompts",
    "reports/daily",
    "reports/experiments",
    "reports/release",
    "artifacts/candidates",
    "artifacts/final",
    "artifacts/backups",
    "src/sair_competition",
    "tests",
]


def validate_layout(repo_root: Path = REPO_ROOT) -> int:
    """Validate that the expected repository skeleton exists."""

    missing: list[str] = []
    print("Repository Layout Validation")
    print("=" * 32)
    for relative_path in EXPECTED_PATHS:
        target = repo_root / relative_path
        exists = target.exists()
        status = "OK" if exists else "MISSING"
        print(f"{relative_path:<30} {status}")
        if not exists:
            missing.append(relative_path)

    if missing:
        return 1

    print("Layout looks good.")
    return 0


def build_complete_prompt_command(
    template_path: Path,
    cheatsheet_path: Path,
    output_path: Path,
    equation1: str = "{ equation1 }",
    equation2: str = "{ equation2 }",
) -> int:
    """Render a complete prompt from a template and cheatsheet."""

    rendered = build_complete_prompt(
        template_path=template_path,
        cheatsheet_path=cheatsheet_path,
        variables={
            "equation1": equation1,
            "equation2": equation2,
        },
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(f"Wrote complete prompt: {output_path}")
    print(f"Byte size: {len(rendered.encode('utf-8'))}")
    return 0


def parse_output(raw_output: str) -> int:
    """Parse a raw model output into a boolean prediction if possible."""

    parsed = parse_bool_output(raw_output)
    if parsed is None:
        print("Could not parse output as true/false.")
        return 1

    print(f"Parsed value: {parsed}")
    return 0


def show_error_taxonomy() -> int:
    """Print the default error taxonomy used for experiment logging."""

    print("Error Taxonomy")
    print("=" * 14)
    for code, description in ERROR_TAXONOMY.items():
        print(f"{code:<18} {description}")
    return 0


def demo_metrics() -> int:
    """Show an example metrics computation for sanity checking the toolchain."""

    records = [
        {"answer": True, "prediction": True, "parsed": True, "source": "normal"},
        {"answer": False, "prediction": True, "parsed": True, "source": "hard2"},
        {"answer": False, "prediction": False, "parsed": True, "source": "normal"},
        {"answer": True, "prediction": None, "parsed": False, "source": "hard1"},
    ]
    metrics = compute_metrics(records)
    print(metrics.to_json(indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Utilities for the SAIR competition workspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-layout", help="Validate the repository layout.")
    validate.add_argument("repo_root", nargs="?", default=str(REPO_ROOT))

    build_prompt = subparsers.add_parser("build-complete-prompt", help="Render a complete prompt.")
    build_prompt.add_argument("template_path")
    build_prompt.add_argument("cheatsheet_path")
    build_prompt.add_argument("output_path")
    build_prompt.add_argument("--equation1", default="{ equation1 }")
    build_prompt.add_argument("--equation2", default="{ equation2 }")

    parse = subparsers.add_parser("parse-output", help="Parse a raw model output.")
    parse.add_argument("raw_output")

    subparsers.add_parser("show-error-taxonomy", help="Show the default error taxonomy.")
    subparsers.add_parser("demo-metrics", help="Print a demo metrics object.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "validate-layout":
        return validate_layout(Path(args.repo_root))
    if args.command == "build-complete-prompt":
        return build_complete_prompt_command(
            template_path=Path(args.template_path),
            cheatsheet_path=Path(args.cheatsheet_path),
            output_path=Path(args.output_path),
            equation1=args.equation1,
            equation2=args.equation2,
        )
    if args.command == "parse-output":
        return parse_output(args.raw_output)
    if args.command == "show-error-taxonomy":
        return show_error_taxonomy()
    if args.command == "demo-metrics":
        return demo_metrics()
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
