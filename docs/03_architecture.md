# Architecture

日期：2026-05-12

## 1. 仓库定位

本仓库从 SAIR Stage1 参赛工程仓库升级为科研实验仓库。架构目标是让每个结论都能追溯到：

- prompt text 或 prompt feature summary
- prompt hash
- corpus manifest
- dataset split
- model/provider config
- parser 和 metrics 版本
- run output 和 summary report

## 2. 当前可复用资产

已有代码资产：

- `src/sair_competition/data/`: 公开数据标准化与 frozen splits。
- `src/sair_competition/eval/`: baseline runner、complete prompt runner、parser、metrics。
- `src/sair_competition/features/`: problem family tagger。
- `src/sair_competition/analysis/`: error report、family slice、offline rule assets、candidate comparison。
- `prompts/complete/`: 历史 prompt 候选，包括 `P1.2.3`、`P1.2.5` 和 `P2.0.*` official archetype strict adaptations。
- `data/interim/splits/`: `smoke/dev/holdout/audit` 及已标注派生 split。
- `artifacts/candidates/`: 历史候选实验输出。

## 3. 新研究层目录

目标目录：

```text
configs/research/
  corpus_sources.example.json
  prompt_feature_taxonomy.yaml
  evaluation_matrix.example.json

data/external/prompt_corpus/
  raw_index.jsonl
  raw_prompts/

data/interim/prompt_corpus/
  corpus_v1.jsonl
  prompt_features_v1.jsonl
  prompt_corpus_manifest.json

reports/research/
  corpus_audit/
  taxonomy/
  screening/
  full_eval/
  distillation_method/
  ablations/
  statistical_analysis/
  figures/

reports/paper/
  outline.md
  related_work.md
  draft.md
  reproducibility_statement.md

artifacts/research_runs/
  screening/
  official_model_eval/
  ablations/
```

这些目录已经由 `T01_research_scaffold` 创建，并在 `docs/review/T01_research_scaffold_review.md` 中通过 normal review。当前状态仍是 scaffold，不代表 corpus、taxonomy 或实验结果已经完成。

## 4. 数据流

```text
Public sources / local prompt files
  -> prompt corpus raw index
  -> normalized corpus_v1.jsonl
  -> prompt hash manifest
  -> prompt feature taxonomy
  -> screening evaluation matrix
  -> research runs
  -> metrics tables
  -> statistical analysis
  -> paper figures and claims
```

## 5. 核心模块边界

### Corpus Layer

职责：

- prompt 来源登记
- hash 和 byte/token 统计
- license / attribution note
- public / local / social / paper source 分级

不得做：

- 混入未公开私有 prompt
- 大段转载不可公开 prompt 到论文正文
- 删除原始来源信息

### Taxonomy Layer

职责：

- prompt feature schema
- 半人工标注
- 后续 extractor CLI
- self-audit report

不得做：

- 把 problem family tag 和 prompt taxonomy 混成一个标签体系
- 未复核就把自动标注当作事实

### Evaluation Layer

职责：

- screening
- recomputed benchmark
- post-release analysis
- run_config 和 raw output 管理

不得做：

- 在 released subsets 上调 prompt
- 混用不同 provider route 却放在同一主表里

### Analysis Layer

职责：

- true/false recall tradeoff
- robustness gap
- model transfer gap
- family-conditioned metrics
- statistical tests and figures

不得做：

- 只汇报最高 accuracy
- 忽略 parse failure 和 cost/time

## 6. 推荐新增 CLI

后续可按任务逐步新增：

- `collect-prompt-corpus`
- `hash-prompt-corpus`
- `extract-prompt-features`
- `audit-prompt-corpus`
- `build-research-eval-matrix`
- `summarize-research-runs`
- `fit-prompt-feature-models`
- `make-paper-figures`

这些不是当前已完成能力，必须等 worker 实现、测试和 review 后才能在 README 中写成可用命令。

## 7. T01 Review Followups

T01 review 没有 blocking issue。以下架构层事项进入后续任务：

- `configs/research/evaluation_matrix.example.json` 中 `repeats: "1-3"` 是模板表达，正式 runner config schema 必须落成整数或显式 repeat list。
- `configs/research/prompt_feature_taxonomy.yaml` 与 `docs/02_experiment_plan.md` 第 6.2 节字段存在抽象层级差异，Phase 2 前需要写 mapping note。
- taxonomy seed 缺少 `compression_style` 和 `ce_search_depth`，Phase 2 manual coding 前决定是否加入。

## 8. T02 Review Followups

T02 review 没有 blocking issue。paper layer 现在有：

- `reports/paper/outline.md`
- `reports/paper/contribution_list.md`
- `reports/paper/claim_evidence_matrix.md`

后续注意：

- `reports/paper/outline.md` 中绝对 Windows 链接需要在 T03 或 standalone hygiene fix 中改成相对链接。
- `C7` 只能作为 setup/motivation，不应进入论文主贡献列表的最终版本。
- `unsupported_do_not_claim` 状态目前只出现在任务验证层面，后续需要至少保留一个 rejected/unsupported claim，避免 claim 分类形同虚设。

## 9. T03 Review Followups

T03 review 没有 blocking issue。corpus layer 现在有：

- `data/interim/prompt_corpus/candidate_register_v0.jsonl`
- `data/interim/prompt_corpus/provenance_rules.md`
- `data/interim/prompt_corpus/prompt_corpus_manifest.json`
- `data/external/prompt_corpus/raw_index.example.jsonl`

后续注意：

- `.gitignore` 当前排除 `data/interim/*` 和 `data/external/*`，所以 prompt corpus governance files on disk 可能不会进入普通 git add。T04 前必须决定 force-add 还是调整 `.gitignore` allowlist。
- `prompt_tokens_est` 仍未计算，当前只能用 `prompt_bytes` 做 v0 size signal。
- public placeholders 仍缺少 source URL、author/team 和 license confirmation，T04 需要补齐或降级为 structure-only / excluded。

## 10. T04 Review Followups

T04 review 没有 blocking issue。corpus governance files 现在通过 `.gitignore` 窄 allowlist 可被 git 跟踪。

后续注意：

- Manifest 中 `direct_recompute_count=10` 当前表达 eligibility，不等价于 text is locally available。T05 必须拆分 `eligible_count` 与 `text_ready_count`。
- GitHub external source 已验证 MIT license，但原文未镜像；T05 需要决定是否导入具体 prompt 文件或继续 metadata-only。
- Contributor Network source 仍是 LinkedIn host-level provenance，T05/T06 应寻找更稳定的一手 URL，否则保持 structure-only。
- `raw_index.example.jsonl` 仍是旧 schema 示例，T05 可统一 example schema。

## 11. T05 Corpus v1 Status

T05 review 没有 blocking issue。corpus layer 现在有规范化 snapshot：

- `data/interim/prompt_corpus/corpus_v1.jsonl`
- `data/interim/prompt_corpus/duplicate_report_v1.json`
- `data/interim/prompt_corpus/missing_metadata_report_v1.json`

当前架构约束：

- `corpus_v1.jsonl` 是后续 taxonomy / screening 的 authoritative corpus snapshot；`candidate_register_v0.jsonl` 保留为 provenance input，不要求 schema 与 corpus v1 完全一致。
- 只有 `corpus_inclusion_status=included_text_ready` 且有 hash/path 的记录可进入本地直接复算。
- `included_metadata_only` 可用于 provenance、audit 和可能的未来 import 决策，但不能直接进入 eval。
- `included_structure_only` 只能用于结构级讨论或风险记录，不能进入 eval。
- T06 需要把上述边界写成 public/private asset boundary note，避免 release manifest 或后续 worker 误读。
