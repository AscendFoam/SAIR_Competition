# T01 Research Scaffold

## Task ID

`T01_research_scaffold`

## Goal

创建 Phase 0 研究脚手架，让后续 corpus、taxonomy、screening 和 paper 工作有固定目录、机器可读 seed config 和可审计 manifest。

## Why Now

`docs/02_experiment_plan.md` 已明确研究主线。继续推进前必须先建立研究目录和 schema，否则 worker 容易把 corpus、实验结果、论文草稿和私有资产混在历史竞赛目录里。

## Allowed Files

Worker 只允许新增或修改以下文件和目录：

```text
configs/research/README.md
configs/research/corpus_sources.example.json
configs/research/prompt_feature_taxonomy.yaml
configs/research/evaluation_matrix.example.json

data/external/prompt_corpus/README.md
data/external/prompt_corpus/raw_index.example.jsonl
data/interim/prompt_corpus/README.md
data/interim/prompt_corpus/prompt_corpus_manifest.json

reports/research/README.md
reports/research/corpus_audit/summary.md
reports/research/taxonomy/README.md
reports/research/screening/README.md
reports/research/full_eval/README.md
reports/research/statistical_analysis/README.md
reports/research/figures/figure_notes.md

reports/paper/README.md
reports/paper/outline.md

docs/07_handoff.md
```

如确实需要补充 `.gitkeep` 或 README 来保留空目录，可以在上述目录内新增。

## Forbidden Scope

本任务禁止：

- 修改 `src/`。
- 修改 `tests/`。
- 修改 `prompts/complete/` 中任何 prompt wording。
- 修改或删除 `artifacts/candidates/`、`artifacts/final/` 历史结果。
- 下载外部数据或访问网络。
- 跑 API eval。
- 把 corpus、taxonomy、paper outline 写成已完成实验事实。
- 将 T01 标记为完成。

## Inputs to Read

必须先读：

```text
README.md
AGENTS.md
docs/02_experiment_plan.md
docs/03_architecture.md
docs/04_task_board.md
docs/06_eval_protocol.md
docs/07_handoff.md
docs/08_risks_and_open_questions.md
configs/README.md
data/README.md
reports/README.md
```

## Expected Output

### 1. Research config seed files

`configs/research/corpus_sources.example.json` 应包含第一批 source type 和候选来源占位，不需要真实抓取外部 prompt。

`configs/research/prompt_feature_taxonomy.yaml` 应覆盖 `docs/02_experiment_plan.md` 中的 taxonomy 大类：

- length features
- structural modules
- module order
- counterexample strategy
- TRUE strategy
- output stability
- provenance and public-work relation

`configs/research/evaluation_matrix.example.json` 应表达三阶段评测：

- screening
- recomputed benchmark
- post-release analysis

并包含 prompt set、dataset set、model/provider config、metrics 和 leakage notes 的字段。

### 2. Prompt corpus directories

`data/external/prompt_corpus/README.md` 说明 raw prompt index 和 raw prompt text 的边界。

`data/external/prompt_corpus/raw_index.example.jsonl` 至少给出 `2-3` 条示例记录，示例可使用本地 prompt 或 placeholder public source，但必须明确 `example_only: true`。

`data/interim/prompt_corpus/prompt_corpus_manifest.json` 应明确当前状态为 seed/scaffold，不得声称已经完成 `8-12` 个 prompt 收集。

### 3. Report scaffold

创建 `reports/research/` 下核心子目录 README 或 summary 草稿，说明每个目录用途。

`reports/research/corpus_audit/summary.md` 应是草稿模板，包含：

- corpus size
- source counts
- hash coverage
- missing metadata
- license/tos notes
- next actions

### 4. Paper outline v0

`reports/paper/outline.md` 应包含：

- working title
- core claim
- RQ list
- contribution list
- section skeleton
- planned figures
- current evidence status
- not-yet-supported claims

必须写清这是 outline，不是论文结果。

### 5. Handoff update

更新 `docs/07_handoff.md` 的 T01 状态说明，记录 worker 做了哪些文件，以及哪些仍待 review。不要把 T01 标记为最终完成。

## Verification

至少运行以下验证，并在 worker 最终报告中贴出结果摘要：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

验证 JSON 文件可解析：

```powershell
python -m json.tool configs/research/corpus_sources.example.json
python -m json.tool configs/research/evaluation_matrix.example.json
python -m json.tool data/interim/prompt_corpus/prompt_corpus_manifest.json
```

验证 JSONL 示例每行可解析：

```powershell
Get-Content data/external/prompt_corpus/raw_index.example.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
```

如果环境缺少 `python` 命令，使用仓库 README 推荐的 Conda Python，并在报告中说明。

## Docs to Update

- `docs/07_handoff.md`

不要修改 `docs/04_task_board.md` 的完成状态。该状态由 Captain 在 review 后更新。

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T01_research_scaffold
Changed files:
- ...

Verification:
- command: ...
  result: pass/fail

Notes:
- ...

Risks / follow-up:
- ...
```

