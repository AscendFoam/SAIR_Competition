# T09 Taxonomy Self-Audit and Conflict Resolution

## Task ID

`T09_taxonomy_self_audit_and_conflict_resolution`

## Goal

对 T07 人工 taxonomy 与 T08 extractor skeleton 的一致性、边界案例和字段冲突做自审，产出 taxonomy self-audit 报告与 conflict resolution note，作为 Milestone 2 的收口任务。

本任务不是泛泛总结。它必须对已知分歧做实质 adjudication，并给出后续 T10/T19 可直接引用的字段使用规则。

## Why Now

Milestone 2 不是“写出一些 feature 字段”就算结束。要进入 T10 screening，必须先回答：

- manual taxonomy 是否稳定
- extractor 输出是否没有明显跑偏
- 哪些字段现在可信，哪些字段仍需人工 override

T09 负责把这些问题集中收口。

T08 review 已经明确指出至少三类必须处理的问题：

- P2.0.2 `counterexample_requirement` 的 manual vs extractor 分歧；
- `rule_or_heuristic_block` 对 `override` 关键词的 fragile heuristic；
- 低方差字段与 extractor-stability vs manual-alignment 的叙事边界。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/taxonomy/README.md
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
reports/research/taxonomy/extractor_v1_notes.md
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
docs/review/T07_manual_taxonomy_coding_v1_review.md
docs/review/T08_prompt_feature_extractor_skeleton_review.md
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
reports/research/taxonomy/extractor_v1_notes.md
src/sair_competition/analysis/prompt_features.py
tests/test_prompt_feature_extractor.py
```

## Expected Output

### 1. `self_audit_v1.md`

必须至少包含：

- sample coverage
- manual coding pool vs extractor coverage
- field variance note
- manual vs extractor mismatch table
- 哪些字段可直接进入 T10/T19
- 哪些字段只能说明性使用
- 哪些字段仍需人工 override
- 不能支持的 claim

### 2. `conflict_resolution_v1.md`

必须至少对以下问题给出明确 adjudication：

- P2.0.2 `counterexample_requirement` authoritative 值保留什么，以及理由
- `rule_or_heuristic_block` 的 `override` fragile heuristic 当前是否接受
- 低方差字段是保留、降权、还是只做说明性标签
- “extractor 行为稳定性”与“manual coding 一致性主张”在报告中如何区分

### 3. `prompt_features_v1.jsonl` 最小修正规则

如确有必要，可对 `prompt_features_v1.jsonl` 做最小修正，但必须满足：

- 只改有明确 adjudication 支撑的字段
- 在 `conflict_resolution_v1.md` 中逐条说明
- 不得静默改动

### 4. `extractor_v1_notes.md` 同步

如果 T09 的 adjudication 改变了 extractor 的解释边界、已知分歧说明或低方差字段策略，应同步更新：

```text
reports/research/taxonomy/extractor_v1_notes.md
```

## Verification

至少运行：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

以及任何与 T08 extractor 对照相关的 focused consistency check。

建议至少补一条：

```powershell
python -m pytest tests/test_prompt_feature_extractor.py -q
```

如果修改了 `prompt_features_v1.jsonl`，还应验证：

```powershell
Get-Content data/interim/prompt_corpus/prompt_features_v1.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
```

## Docs to Update

- `reports/research/taxonomy/README.md`
- `reports/research/taxonomy/extractor_v1_notes.md`
- `reports/research/taxonomy/self_audit_v1.md`
- `reports/research/taxonomy/conflict_resolution_v1.md`
- `docs/07_handoff.md`

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T09_taxonomy_self_audit_and_conflict_resolution
Changed files:
- ...

Adjudication summary:
- P2.0.2 counterexample_requirement:
- low-variance fields policy:
- extractor/manual boundary:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
