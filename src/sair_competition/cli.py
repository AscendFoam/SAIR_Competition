from __future__ import annotations

import argparse
from pathlib import Path

from .data.public_data import prepare_public_dataset
from .data.splits import make_frozen_splits
from .analysis.error_taxonomy import ERROR_TAXONOMY
from .analysis.error_report import analyze_prediction_errors
from .analysis.experiment_report import compare_candidate_runs
from .eval.baseline_runner import run_baseline_suite
from .eval.local_runner import run_complete_prompt_eval
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


def prepare_public_data_command(raw_dir: Path, interim_dir: Path) -> int:
    summary = prepare_public_dataset(raw_dir=raw_dir, interim_dir=interim_dir)
    print(json_dumps(summary))
    return 0


def make_splits_command(
    dataset_path: Path,
    output_dir: Path,
    smoke: int,
    dev: int,
    holdout: int,
    audit: int,
    seed: int,
) -> int:
    manifest = make_frozen_splits(
        dataset_path=dataset_path,
        output_dir=output_dir,
        split_targets={
            "smoke": smoke,
            "dev": dev,
            "holdout": holdout,
            "audit": audit,
        },
        seed=seed,
    )
    print(json_dumps(manifest))
    return 0


def run_baseline_eval_command(
    dataset_path: Path,
    output_dir: Path,
    predictors: list[str] | None,
    prompt_path: Path | None,
) -> int:
    summary = run_baseline_suite(
        dataset_path=dataset_path,
        output_dir=output_dir,
        predictor_names=predictors,
        prompt_path=prompt_path,
    )
    print(json_dumps(summary))
    return 0


def run_complete_prompt_eval_command(
    dataset_path: Path,
    prompt_path: Path,
    output_dir: Path,
    dotenv_path: Path,
    model: str | None,
    limit: int | None,
    temperature: float,
    max_tokens: int,
) -> int:
    summary = run_complete_prompt_eval(
        dataset_path=dataset_path,
        prompt_path=prompt_path,
        output_dir=output_dir,
        dotenv_path=dotenv_path,
        model=model,
        limit=limit,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    print(json_dumps(summary))
    return 0


def analyze_errors_command(predictions_path: Path, output_dir: Path) -> int:
    summary = analyze_prediction_errors(predictions_path=predictions_path, output_dir=output_dir)
    print(json_dumps(summary))
    return 0


def compare_candidates_command(
    candidate_dirs: list[str],
    output_dir: Path,
    baseline_dir: str | None,
) -> int:
    summary = compare_candidate_runs(
        candidate_dirs=candidate_dirs,
        output_dir=output_dir,
        baseline_dir=baseline_dir,
    )
    print(json_dumps(summary))
    return 0


def json_dumps(payload: dict) -> str:
    import json

    return json.dumps(payload, ensure_ascii=False, indent=2)


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

    prepare = subparsers.add_parser("prepare-public-data", help="Normalize official public problem files.")
    prepare.add_argument("--raw-dir", default="data/raw")
    prepare.add_argument("--interim-dir", default="data/interim")

    split = subparsers.add_parser("make-splits", help="Create deterministic frozen splits.")
    split.add_argument("--dataset-path", default="data/interim/public_all.jsonl")
    split.add_argument("--output-dir", default="data/interim/splits")
    split.add_argument("--smoke", type=int, default=64)
    split.add_argument("--dev", type=int, default=824)
    split.add_argument("--holdout", type=int, default=254)
    split.add_argument("--audit", type=int, default=127)
    split.add_argument("--seed", type=int, default=20260322)

    baseline = subparsers.add_parser("run-baseline-eval", help="Run baseline predictors on a dataset or split.")
    baseline.add_argument("--dataset-path", default="data/interim/public_all.jsonl")
    baseline.add_argument("--output-dir", default="artifacts/candidates/baseline_eval")
    baseline.add_argument("--predictor", action="append", dest="predictors")
    baseline.add_argument("--prompt-path", default=None)

    complete = subparsers.add_parser("run-complete-prompt-eval", help="Run a complete prompt via an OpenAI-compatible API.")
    complete.add_argument("--dataset-path", default="data/interim/splits/smoke.jsonl")
    complete.add_argument("--prompt-path", required=True)
    complete.add_argument("--output-dir", default="artifacts/candidates/complete_prompt_eval")
    complete.add_argument("--dotenv-path", default=".env")
    complete.add_argument("--model", default=None)
    complete.add_argument("--limit", type=int, default=None)
    complete.add_argument("--temperature", type=float, default=0.0)
    complete.add_argument("--max-tokens", type=int, default=256)

    analyze = subparsers.add_parser("analyze-errors", help="Analyze prediction rows from a baseline or API eval.")
    analyze.add_argument("--predictions-path", required=True)
    analyze.add_argument("--output-dir", required=True)

    compare = subparsers.add_parser("compare-candidates", help="Compare multiple candidate experiment runs.")
    compare.add_argument("--candidate-dir", action="append", dest="candidate_dirs", required=True)
    compare.add_argument("--output-dir", required=True)
    compare.add_argument("--baseline-dir", default=None)

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
    if args.command == "prepare-public-data":
        return prepare_public_data_command(
            raw_dir=Path(args.raw_dir),
            interim_dir=Path(args.interim_dir),
        )
    if args.command == "make-splits":
        return make_splits_command(
            dataset_path=Path(args.dataset_path),
            output_dir=Path(args.output_dir),
            smoke=args.smoke,
            dev=args.dev,
            holdout=args.holdout,
            audit=args.audit,
            seed=args.seed,
        )
    if args.command == "run-baseline-eval":
        return run_baseline_eval_command(
            dataset_path=Path(args.dataset_path),
            output_dir=Path(args.output_dir),
            predictors=args.predictors,
            prompt_path=Path(args.prompt_path) if args.prompt_path else None,
        )
    if args.command == "run-complete-prompt-eval":
        return run_complete_prompt_eval_command(
            dataset_path=Path(args.dataset_path),
            prompt_path=Path(args.prompt_path),
            output_dir=Path(args.output_dir),
            dotenv_path=Path(args.dotenv_path),
            model=args.model,
            limit=args.limit,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
    if args.command == "analyze-errors":
        return analyze_errors_command(
            predictions_path=Path(args.predictions_path),
            output_dir=Path(args.output_dir),
        )
    if args.command == "compare-candidates":
        return compare_candidates_command(
            candidate_dirs=args.candidate_dirs,
            output_dir=Path(args.output_dir),
            baseline_dir=args.baseline_dir,
        )
    if args.command == "show-error-taxonomy":
        return show_error_taxonomy()
    if args.command == "demo-metrics":
        return demo_metrics()
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
