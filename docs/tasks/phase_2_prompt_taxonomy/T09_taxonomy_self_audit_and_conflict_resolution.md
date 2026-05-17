# T09 Taxonomy Self-Audit and Conflict Resolution

## Task ID

`T09_taxonomy_self_audit_and_conflict_resolution`

## Goal

对 T07 人工 taxonomy 与 T08 extractor skeleton 的一致性、边界案例和字段冲突做自审，产出 taxonomy self-audit 报告与 conflict resolution note，作为 Milestone 2 的收口任务。

## Why Now

Milestone 2 不是“写出一些 feature 字段”就算结束。要进入 T10 screening，必须先回答：

- manual taxonomy 是否稳定
- extractor 输出是否没有明显跑偏
- 哪些字段现在可信，哪些字段仍需人工 override

T09 负责把这些问题集中收口。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/taxonomy/README.md
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
reports/research/taxonomy/self_audit_v1.md
reports/research/taxonomy/conflict_resolution_v1.md
docs/07_handoff.md
```

## Forbidden Scope

本任务禁止：

- 修改 `src/` 与 `tests/`，除非 Captain 之后单独开修复任务。
- 修改 `prompts/complete/`。
- 跑 API eval。
- 越过 T06 boundary gate 给非 text-ready records 做 full-text coding。
- 修改 `docs/04_task_board.md` 或把 T09 标记为完成。

## Inputs to Read

必须先读：

```text
README.md
AGENTS.md
docs/02_experiment_plan.md
docs/04_task_board.md
docs/06_eval_protocol.md
docs/07_handoff.md
docs/08_risks_and_open_questions.md
docs/tasks/phase_2_prompt_taxonomy/T07_manual_taxonomy_coding_v1.md
docs/tasks/phase_2_prompt_taxonomy/T08_prompt_feature_extractor_skeleton.md
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
reports/research/taxonomy/extractor_v1_notes.md
```

## Expected Output

- `self_audit_v1.md`: 写清 sample coverage、字段稳定性、manual vs extractor mismatch、不能支持的 claim。
- `conflict_resolution_v1.md`: 写清字段冲突、边界案例、保留争议和最终 adjudication rule。
- 如确有必要，可对 `prompt_features_v1.jsonl` 做最小修正，但必须在报告中逐条解释。

## Verification

至少运行：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

以及任何与 T08 extractor 对照相关的 focused consistency check。

## Docs to Update

- `reports/research/taxonomy/README.md`
- `reports/research/taxonomy/self_audit_v1.md`
- `reports/research/taxonomy/conflict_resolution_v1.md`
- `docs/07_handoff.md`

## Reviewer Type

normal
