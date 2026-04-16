from __future__ import annotations

import argparse
from pathlib import Path

from .data.public_data import prepare_public_dataset
from .data.splits import make_frozen_splits
from .analysis.error_taxonomy import ERROR_TAXONOMY
from .analysis.error_report import analyze_prediction_errors
from .analysis.experiment_report import compare_candidate_runs
from .analysis.family_slice import attach_family_tags_to_predictions
from .analysis.offline_rule_assets import (
    attach_offline_rule_assets,
    audit_offline_rule_assets,
    build_offline_rule_assets,
)
from .analysis.positive_signal_candidate import prepare_positive_signal_candidate
from .analysis.offline_rule_review import (
    build_offline_rule_review_set,
    consolidate_offline_rule_axes,
)
from .eval.baseline_runner import run_baseline_suite
from .eval.local_runner import run_complete_prompt_eval
from .eval.metrics import compute_metrics
from .eval.parser import parse_bool_output
from .features.family_tagger import FAMILY_TAG_TAXONOMY, tag_problem_families
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


def show_family_tag_taxonomy() -> int:
    """Print the default structural family tags used for offline labeling."""

    print("Family Tag Taxonomy")
    print("=" * 19)
    for code, description in FAMILY_TAG_TAXONOMY.items():
        print(f"{code:<30} {description}")
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
    """CLI 命令：标准化公开数据集。

    Args:
        raw_dir: 原始数据目录路径。
        interim_dir: 标准化后的中间数据输出目录路径。

    Returns:
        int: 成功返回 0。
    """
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
    """CLI 命令：创建确定性数据拆分。

    Args:
        dataset_path: 数据集文件路径。
        output_dir: 拆分结果输出目录路径。
        smoke: smoke 拆分的样本数量。
        dev: dev 拆分的样本数量。
        holdout: holdout 拆分的样本数量。
        audit: audit 拆分的样本数量。
        seed: 随机种子，用于保证拆分的可复现性。

    Returns:
        int: 成功返回 0。
    """
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
    """CLI 命令：运行基线预测器评估。

    Args:
        dataset_path: 数据集文件路径。
        output_dir: 评估结果输出目录路径。
        predictors: 要运行的预测器名称列表，为 None 时运行全部预测器。
        prompt_path: 自定义 prompt 模板路径，为 None 时使用默认模板。

    Returns:
        int: 成功返回 0。
    """
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
    provider: str,
    model: str | None,
    limit: int | None,
    temperature: float,
    max_tokens: int,
) -> int:
    """CLI 命令：通过 API 运行完整 prompt 评估。

    Args:
        dataset_path: 数据集文件路径。
        prompt_path: 完整 prompt 模板文件路径。
        output_dir: 评估结果输出目录路径。
        dotenv_path: 环境变量文件路径，用于加载 API 密钥。
        model: 模型名称，为 None 时使用默认模型。
        limit: 限制评估的样本数量，为 None 时不限制。
        temperature: 生成温度参数。
        max_tokens: 最大生成 token 数。

    Returns:
        int: 成功返回 0。
    """
    summary = run_complete_prompt_eval(
        dataset_path=dataset_path,
        prompt_path=prompt_path,
        output_dir=output_dir,
        dotenv_path=dotenv_path,
        provider_name=provider,
        model=model,
        limit=limit,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    print(json_dumps(summary))
    return 0


def analyze_errors_command(predictions_path: Path, output_dir: Path) -> int:
    """CLI 命令：分析预测错误。

    Args:
        predictions_path: 预测结果文件路径。
        output_dir: 错误分析报告输出目录路径。

    Returns:
        int: 成功返回 0。
    """
    summary = analyze_prediction_errors(predictions_path=predictions_path, output_dir=output_dir)
    print(json_dumps(summary))
    return 0


def attach_family_tags_command(
    predictions_path: Path,
    tagged_dataset_path: Path,
    output_path: Path,
) -> int:
    """CLI 命令：回填家族标签到预测文件。

    Args:
        predictions_path: 预测结果文件路径。
        tagged_dataset_path: 已标注家族标签的数据集文件路径。
        output_path: 回填标签后的输出文件路径。

    Returns:
        int: 成功返回 0。
    """
    summary = attach_family_tags_to_predictions(
        predictions_path=predictions_path,
        tagged_dataset_path=tagged_dataset_path,
        output_path=output_path,
    )
    print(json_dumps(summary))
    return 0


def build_offline_rule_assets_command(
    tagged_dataset_path: Path,
    output_path: Path,
    error_summary_path: Path | None,
    report_path: Path | None,
) -> int:
    """CLI 命令：构建离线规则资产。

    Args:
        tagged_dataset_path: 已标注家族标签的数据集文件路径。
        output_path: 离线规则资产输出文件路径。
        error_summary_path: 错误摘要文件路径，为 None 时不使用。
        report_path: 报告输出文件路径，为 None 时不生成报告。

    Returns:
        int: 成功返回 0。
    """
    summary = build_offline_rule_assets(
        tagged_dataset_path=tagged_dataset_path,
        output_path=output_path,
        error_summary_path=error_summary_path,
        report_path=report_path,
    )
    print(json_dumps(summary))
    return 0


def attach_offline_rule_assets_command(
    input_path: Path,
    rule_assets_path: Path,
    output_path: Path,
) -> int:
    """CLI 命令：附加离线规则资产 ID 到数据行。

    Args:
        input_path: 已标注家族标签的输入数据文件路径。
        rule_assets_path: 离线规则资产文件路径。
        output_path: 附加规则资产后的输出文件路径。

    Returns:
        int: 成功返回 0。
    """
    summary = attach_offline_rule_assets(
        input_path=input_path,
        rule_assets_path=rule_assets_path,
        output_path=output_path,
    )
    print(json_dumps(summary))
    return 0


def audit_offline_rule_assets_command(
    predictions_path: Path,
    rule_assets_path: Path,
    output_dir: Path,
) -> int:
    """CLI 命令：审计离线规则资产表现。

    Args:
        predictions_path: 预测结果文件路径。
        rule_assets_path: 离线规则资产文件路径。
        output_dir: 审计结果输出目录路径。

    Returns:
        int: 成功返回 0。
    """
    summary = audit_offline_rule_assets(
        predictions_path=predictions_path,
        rule_assets_path=rule_assets_path,
        output_dir=output_dir,
    )
    print(json_dumps(summary))
    return 0


def consolidate_offline_rule_axes_command(
    predictions_path: Path,
    audit_summary_path: Path,
    output_dir: Path,
) -> int:
    """CLI 命令：合并重叠离线规则资产为规范轴。

    Args:
        predictions_path: 预测结果文件路径。
        audit_summary_path: 审计摘要文件路径。
        output_dir: 合并结果输出目录路径。

    Returns:
        int: 成功返回 0。
    """
    summary = consolidate_offline_rule_axes(
        predictions_path=predictions_path,
        audit_summary_path=audit_summary_path,
        output_dir=output_dir,
    )
    print(json_dumps(summary))
    return 0


def build_offline_rule_review_set_command(
    predictions_path: Path,
    consolidation_summary_path: Path,
    output_dir: Path,
) -> int:
    """CLI 命令：构建去重审查集。

    Args:
        predictions_path: 预测结果文件路径。
        consolidation_summary_path: 合并摘要文件路径。
        output_dir: 审查集输出目录路径。

    Returns:
        int: 成功返回 0。
    """
    summary = build_offline_rule_review_set(
        predictions_path=predictions_path,
        consolidation_summary_path=consolidation_summary_path,
        output_dir=output_dir,
    )
    print(json_dumps(summary))
    return 0


def compare_candidates_command(
    candidate_dirs: list[str],
    output_dir: Path,
    baseline_dir: str | None,
) -> int:
    """CLI 命令：对比多个实验候选运行。

    Args:
        candidate_dirs: 候选实验目录路径列表。
        output_dir: 对比报告输出目录路径。
        baseline_dir: 基线实验目录路径，为 None 时不指定基线。

    Returns:
        int: 成功返回 0。
    """
    summary = compare_candidate_runs(
        candidate_dirs=candidate_dirs,
        output_dir=output_dir,
        baseline_dir=baseline_dir,
    )
    print(json_dumps(summary))
    return 0


def tag_problem_families_command(
    dataset_path: Path,
    output_path: Path,
    summary_dir: Path | None,
) -> int:
    """CLI 命令：为数据集标注家族标签。

    Args:
        dataset_path: 数据集文件路径。
        output_path: 标注后的输出文件路径。
        summary_dir: 摘要输出目录路径，为 None 时不生成摘要。

    Returns:
        int: 成功返回 0。
    """
    summary = tag_problem_families(
        dataset_path=dataset_path,
        output_path=output_path,
        summary_dir=summary_dir,
    )
    print(json_dumps(summary))
    return 0


def prepare_positive_signal_candidate_command(
    tagged_dataset_path: Path,
    target_tag: str,
    output_dir: Path,
    boundary_tags: list[str],
    rule_assets_path: Path | None,
    signal_keys: list[str],
) -> int:
    """CLI 命令：为候选正信号标签准备离线摘要。"""
    summary = prepare_positive_signal_candidate(
        tagged_dataset_path=tagged_dataset_path,
        target_tag=target_tag,
        output_dir=output_dir,
        boundary_tags=boundary_tags,
        rule_assets_path=rule_assets_path,
        signal_keys=signal_keys,
    )
    print(json_dumps(summary))
    return 0


def json_dumps(payload: dict) -> str:
    """将字典序列化为格式化的 JSON 字符串。

    Args:
        payload: 需要序列化的字典。

    Returns:
        str: 格式化后的 JSON 字符串。
    """
    import json

    return json.dumps(payload, ensure_ascii=False, indent=2)


def build_parser() -> argparse.ArgumentParser:
    """构建 argparse 命令行解析器，注册所有子命令。

    Returns:
        argparse.ArgumentParser: 配置完成的命令行解析器实例。
    """
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
    complete.add_argument("--provider", default="deepseek")
    complete.add_argument("--model", default=None)
    complete.add_argument("--limit", type=int, default=None)
    complete.add_argument("--temperature", type=float, default=0.0)
    complete.add_argument("--max-tokens", type=int, default=256)

    analyze = subparsers.add_parser("analyze-errors", help="Analyze prediction rows from a baseline or API eval.")
    analyze.add_argument("--predictions-path", required=True)
    analyze.add_argument("--output-dir", required=True)

    attach = subparsers.add_parser(
        "attach-family-tags-to-predictions",
        help="Backfill family tags into an existing predictions file using a tagged dataset.",
    )
    attach.add_argument("--predictions-path", required=True)
    attach.add_argument("--tagged-dataset-path", required=True)
    attach.add_argument("--output-path", required=True)

    rule_assets = subparsers.add_parser(
        "build-offline-rule-assets",
        help="Build offline rule assets from a tagged dataset and optional tagged error summary.",
    )
    rule_assets.add_argument("--tagged-dataset-path", required=True)
    rule_assets.add_argument("--output-path", required=True)
    rule_assets.add_argument("--error-summary-path", default=None)
    rule_assets.add_argument("--report-path", default=None)

    attach_assets = subparsers.add_parser(
        "attach-offline-rule-assets",
        help="Attach offline rule-asset ids to rows that already have family tags.",
    )
    attach_assets.add_argument("--input-path", required=True)
    attach_assets.add_argument("--rule-assets-path", required=True)
    attach_assets.add_argument("--output-path", required=True)

    audit_assets = subparsers.add_parser(
        "audit-offline-rule-assets",
        help="Audit a prediction file through the offline rule-asset bundle.",
    )
    audit_assets.add_argument("--predictions-path", required=True)
    audit_assets.add_argument("--rule-assets-path", required=True)
    audit_assets.add_argument("--output-dir", required=True)

    consolidate_axes = subparsers.add_parser(
        "consolidate-offline-rule-axes",
        help="Deduplicate overlapping offline rule assets into canonical axes.",
    )
    consolidate_axes.add_argument("--predictions-path", required=True)
    consolidate_axes.add_argument("--audit-summary-path", required=True)
    consolidate_axes.add_argument("--output-dir", required=True)

    review_set = subparsers.add_parser(
        "build-offline-rule-review-set",
        help="Build a deduplicated review set from canonical offline rule axes.",
    )
    review_set.add_argument("--predictions-path", required=True)
    review_set.add_argument("--consolidation-summary-path", required=True)
    review_set.add_argument("--output-dir", required=True)

    compare = subparsers.add_parser("compare-candidates", help="Compare multiple candidate experiment runs.")
    compare.add_argument("--candidate-dir", action="append", dest="candidate_dirs", required=True)
    compare.add_argument("--output-dir", required=True)
    compare.add_argument("--baseline-dir", default=None)

    tag = subparsers.add_parser("tag-problem-families", help="Annotate a dataset with lightweight structural family tags.")
    tag.add_argument("--dataset-path", default="data/interim/public_all.jsonl")
    tag.add_argument("--output-path", required=True)
    tag.add_argument("--summary-dir", default=None)

    candidate = subparsers.add_parser(
        "prepare-positive-signal-candidate",
        help="Prepare an offline summary for a candidate structural positive signal.",
    )
    candidate.add_argument("--tagged-dataset-path", required=True)
    candidate.add_argument("--target-tag", required=True)
    candidate.add_argument("--output-dir", required=True)
    candidate.add_argument("--boundary-tag", action="append", dest="boundary_tags", default=[])
    candidate.add_argument("--rule-assets-path", default=None)
    candidate.add_argument("--signal-key", action="append", dest="signal_keys", default=[])

    subparsers.add_parser("show-error-taxonomy", help="Show the default error taxonomy.")
    subparsers.add_parser("show-family-tag-taxonomy", help="Show the structural family-tag taxonomy.")
    subparsers.add_parser("demo-metrics", help="Print a demo metrics object.")
    return parser


def main() -> int:
    """CLI 主入口，解析参数并分发到对应命令函数。

    Returns:
        int: 成功返回 0，失败返回 1。
    """
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
            provider=args.provider,
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
    if args.command == "attach-family-tags-to-predictions":
        return attach_family_tags_command(
            predictions_path=Path(args.predictions_path),
            tagged_dataset_path=Path(args.tagged_dataset_path),
            output_path=Path(args.output_path),
        )
    if args.command == "build-offline-rule-assets":
        return build_offline_rule_assets_command(
            tagged_dataset_path=Path(args.tagged_dataset_path),
            output_path=Path(args.output_path),
            error_summary_path=Path(args.error_summary_path) if args.error_summary_path else None,
            report_path=Path(args.report_path) if args.report_path else None,
        )
    if args.command == "attach-offline-rule-assets":
        return attach_offline_rule_assets_command(
            input_path=Path(args.input_path),
            rule_assets_path=Path(args.rule_assets_path),
            output_path=Path(args.output_path),
        )
    if args.command == "audit-offline-rule-assets":
        return audit_offline_rule_assets_command(
            predictions_path=Path(args.predictions_path),
            rule_assets_path=Path(args.rule_assets_path),
            output_dir=Path(args.output_dir),
        )
    if args.command == "consolidate-offline-rule-axes":
        return consolidate_offline_rule_axes_command(
            predictions_path=Path(args.predictions_path),
            audit_summary_path=Path(args.audit_summary_path),
            output_dir=Path(args.output_dir),
        )
    if args.command == "build-offline-rule-review-set":
        return build_offline_rule_review_set_command(
            predictions_path=Path(args.predictions_path),
            consolidation_summary_path=Path(args.consolidation_summary_path),
            output_dir=Path(args.output_dir),
        )
    if args.command == "compare-candidates":
        return compare_candidates_command(
            candidate_dirs=args.candidate_dirs,
            output_dir=Path(args.output_dir),
            baseline_dir=args.baseline_dir,
        )
    if args.command == "tag-problem-families":
        return tag_problem_families_command(
            dataset_path=Path(args.dataset_path),
            output_path=Path(args.output_path),
            summary_dir=Path(args.summary_dir) if args.summary_dir else None,
        )
    if args.command == "prepare-positive-signal-candidate":
        return prepare_positive_signal_candidate_command(
            tagged_dataset_path=Path(args.tagged_dataset_path),
            target_tag=args.target_tag,
            output_dir=Path(args.output_dir),
            boundary_tags=args.boundary_tags,
            rule_assets_path=Path(args.rule_assets_path) if args.rule_assets_path else None,
            signal_keys=args.signal_keys,
        )
    if args.command == "show-error-taxonomy":
        return show_error_taxonomy()
    if args.command == "show-family-tag-taxonomy":
        return show_family_tag_taxonomy()
    if args.command == "demo-metrics":
        return demo_metrics()
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
