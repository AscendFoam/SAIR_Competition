# T08 Prompt Feature Extractor Skeleton

## Task ID

`T08_prompt_feature_extractor_skeleton`

## Goal

基于 T07 的人工 taxonomy v1，实现一个最小可验证的 prompt feature extractor skeleton 与测试，支持从 local text-ready prompt 生成与人工编码同 schema 的结构化特征输出。

本任务只做 skeleton：重点是 schema alignment、解析入口、基础规则和测试，不追求一次性覆盖所有 taxonomy 细节。

## Why Now

T07 之后应当已经有：

- `prompt_features_v1.jsonl`
- taxonomy v1 report
- mapping note
- reviewable 的 length-bucket / token-estimate 口径

没有这些人工基线，就不应该直接写 extractor。T08 的职责是把手工 taxonomy 变成后续可重复运行的代码骨架，为 T09 自审和 T10 screening 提供可复用输入。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
src/sair_competition/analysis/
src/sair_competition/cli.py
tests/
configs/research/prompt_feature_taxonomy.yaml
reports/research/taxonomy/README.md
reports/research/taxonomy/extractor_v1_notes.md
docs/07_handoff.md
```

## Forbidden Scope

本任务禁止：

- 修改 `prompts/complete/` 中任何 prompt wording。
- 修改 corpus provenance files 或把 external records 提升为 text-ready。
- 跑 API eval、screening eval 或 released subset analysis。
- 把 extractor coverage 写成“已替代人工标注”。
- 修改 `docs/04_task_board.md` 或把 T08 标记为完成。

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
docs/review/T06_corpus_audit_public_private_boundary_review.md
docs/review/M1_review.md
docs/tasks/phase_2_prompt_taxonomy/T07_manual_taxonomy_coding_v1.md
configs/research/prompt_feature_taxonomy.yaml
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
```

## Expected Output

- 一个最小 extractor 入口，可对 text-ready local prompt 产出结构化 features。
- 至少一组 focused tests，验证 schema shape 与几个核心字段。
- `extractor_v1_notes.md` 写清哪些字段是规则化支持、哪些仍需人工复核。
- 不要求自动覆盖全部 taxonomy 字段。

## Verification

至少运行：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

以及与新增 extractor/tests 对应的 focused tests。

## Docs to Update

- `reports/research/taxonomy/README.md`
- `reports/research/taxonomy/extractor_v1_notes.md`
- `docs/07_handoff.md`

## Reviewer Type

normal
