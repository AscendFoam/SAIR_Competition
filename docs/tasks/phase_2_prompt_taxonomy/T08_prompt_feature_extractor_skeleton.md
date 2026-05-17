# T08 Prompt Feature Extractor Skeleton

## Task ID

`T08_prompt_feature_extractor_skeleton`

## Goal

基于 T07 的人工 taxonomy v1，实现一个最小可验证的 prompt feature extractor skeleton 与测试，支持从 local text-ready prompt 生成与人工编码同 schema 的结构化特征输出。

本任务只做 skeleton：重点是 schema alignment、解析入口、基础规则和测试，不追求一次性覆盖所有 taxonomy 细节。

同时，本任务必须顺手收口 T07 review 的一个明确非阻塞问题：

- 统一 token estimate 文档口径，解决 `floor(bytes/4)` 与 `round(bytes/4)` 描述不一致。

## Why Now

T07 之后应当已经有：

- `prompt_features_v1.jsonl`
- taxonomy v1 report
- mapping note
- reviewable 的 length-bucket / token-estimate 口径

没有这些人工基线，就不应该直接写 extractor。T08 的职责是把手工 taxonomy 变成后续可重复运行的代码骨架，为 T09 自审和 T10 screening 提供可复用输入。

此外，T07 reviewer 已明确提醒两个设计约束，T08 必须吸收：

- token estimate 口径要统一；
- 低方差字段可以保留，但不能在 extractor 设计或说明中被误写成高信息量特征。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
src/sair_competition/analysis/
src/sair_competition/cli.py
tests/
configs/research/prompt_feature_taxonomy.yaml
reports/research/taxonomy/README.md
reports/research/taxonomy/extractor_v1_notes.md
reports/research/taxonomy/taxonomy_v1.md
docs/07_handoff.md
```

## Forbidden Scope

本任务禁止：

- 修改 `prompts/complete/` 中任何 prompt wording。
- 修改 corpus provenance files 或把 external records 提升为 text-ready。
- 修改 `data/interim/prompt_corpus/corpus_v1.jsonl` 或 `prompt_features_v1.jsonl` 中的人工标注值，除非你发现明确 bug；如发现 bug，不在本任务静默修，转交 T09 或单开修复任务。
- 跑 API eval、screening eval 或 released subset analysis。
- 把 extractor coverage 写成“已替代人工标注”。
- 让低方差字段成为 extractor 成功标准的主要论据。
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
docs/review/T07_manual_taxonomy_coding_v1_review.md
docs/tasks/phase_2_prompt_taxonomy/T07_manual_taxonomy_coding_v1.md
configs/research/prompt_feature_taxonomy.yaml
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
```

## Expected Output

### 1. 最小 extractor 入口

必须提供一个明确入口，可对 text-ready local prompt 产出结构化 features。

要求：

- 输入必须基于 local text-ready prompt text。
- 输出字段必须是 `prompt_features_v1.jsonl` schema 的子集或等结构兼容集。
- 至少覆盖一组高价值、可规则化、在 9 条样本上有区分度的字段。

建议优先覆盖：

- `prompt_bytes_bucket`
- `prompt_tokens_est_bucket`
- `verdict_contract`
- `rule_or_heuristic_block`
- `opening_strategy`
- `counterexample_requirement`
- `explicit_final_token`

低方差字段如 `examples_block`、`finite_model_search_hint`、`identity_or_invariant_guidance` 可以保留在 schema 中，但不要求本轮作为 extractor 的主覆盖目标。

### 2. Focused tests

至少一组 focused tests，必须验证：

- extractor 输出可解析；
- 输出字段名与 schema 对齐；
- 至少几个核心字段在代表性 prompt 上与人工标注一致；
- metadata-only / structure-only records 不会被误当作 extractor 输入。

测试不要求覆盖全部 27 个字段，也不要求做端到端大矩阵。

### 3. Extractor note

新增：

```text
reports/research/taxonomy/extractor_v1_notes.md
```

必须写清：

- 哪些字段已规则化支持；
- 哪些字段仍依赖人工复核；
- 哪些字段因低方差或规则脆弱而只保留占位；
- extractor 输出不能替代 T09 self-audit。

### 4. Token estimate 口径统一

本任务必须统一 token estimate 文档口径。

允许修改：

```text
reports/research/taxonomy/taxonomy_v1.md
```

要求：

- 明确当前使用 `floor(bytes/4)` 还是 `round(bytes/4)`。
- 文档口径必须与现有数据一致，或明确说明为何改动并如何影响 bucket。
- 不要把该启发式写成 tokenizer 精确计数。

### 5. Scope honesty

必须明确说明：

- 这是 extractor skeleton，不是 full automation。
- manual taxonomy 仍是 authoritative reference。
- T09 仍需处理单编码者 bias、低方差字段和边界案例。

## Verification

至少运行：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

以及与新增 extractor/tests 对应的 focused tests。

建议补充：

```powershell
python -m pytest <focused_test_paths> -q
```

如果存在新的 CLI 入口，还应补一条最小 smoke command，并在最终报告里写清输出位置或返回结构。

## Docs to Update

- `reports/research/taxonomy/README.md`
- `reports/research/taxonomy/extractor_v1_notes.md`
- `reports/research/taxonomy/taxonomy_v1.md`
- `docs/07_handoff.md`

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T08_prompt_feature_extractor_skeleton
Changed files:
- ...

Extractor coverage:
- supported fields:
- unsupported/manual-only fields:
- token estimate wording fixed as:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
