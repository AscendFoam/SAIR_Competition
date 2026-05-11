# Architecture

日期：2026-05-11

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

这些目录由 `T01_research_scaffold` 创建，不在 Captain 初始化文档任务中伪造为已完成。

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

