# T10 Build Screening Evaluation Matrix

## Task ID

`T10_build_screening_evaluation_matrix`

## Goal

把现有 screening seed template、T06 corpus boundary 和 T09 taxonomy adjudication 收敛成一个正式、可执行、可 review 的 Stage A screening evaluation matrix。

本任务只做 matrix 设计与配套说明，不运行 screening，不产出模型预测，不提前做 shortlist 结论。

## Why Now

T09 已经完成两个关键前置：

- manual taxonomy 与 extractor skeleton 的已知分歧已裁决；
- 哪些字段可直接进入 screening / T19，哪些字段只能 descriptive-only，已经写成明确规则。

如果不先冻结 screening matrix，T11 很容易一边跑实验一边改候选池、字段维度和 run config，最终让 review 难以判断哪些结论来自 protocol，哪些只是临时调度。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
configs/research/evaluation_matrix.example.json
configs/research/README.md
reports/research/screening/README.md
reports/research/screening/screening_matrix_v1.md
reports/research/screening/screening_candidate_registry_v1.md
reports/research/screening/screening_shortlist_rules_v1.md
docs/07_handoff.md
```

如需新增一个 machine-readable screening matrix 文件，也只允许放在：

```text
configs/research/
reports/research/screening/
```

## Forbidden Scope

本任务禁止：

- 修改 `src/`、`tests/`、`prompts/complete/`。
- 修改 `data/interim/prompt_corpus/corpus_v1.jsonl` 或 `prompt_features_v1.jsonl`。
- 跑 API eval、screening execution、released subset analysis。
- 生成 `predictions.jsonl`、`raw_outputs.jsonl` 或任何真实 run artifact。
- 把 metadata-only / structure-only records 提升为 screening 候选。
- 让 low-variance fields 成为主筛选维度。
- 修改 `docs/04_task_board.md` 或把 T10 标记为完成。

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
docs/review/T09_taxonomy_self_audit_and_conflict_resolution_review.md
docs/review/M1_review.md
configs/research/evaluation_matrix.example.json
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
reports/research/corpus_audit/public_private_boundary.md
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/extractor_v1_notes.md
reports/research/taxonomy/self_audit_v1.md
reports/research/taxonomy/conflict_resolution_v1.md
reports/research/screening/README.md
```

## Required Decisions

T10 必须明确回答以下问题：

1. 当前 screening 候选池到底是哪几条 prompt，哪些 record 明确不在池内。
2. screening matrix 中哪些字段可作为分层/比较维度。
3. 哪些字段只能 descriptive-only，不能作为 shortlist 决策主依据。
4. screening 用哪些 split，是否需要 hard slice sample。
5. screening 的 model/provider config 如何先写成可执行模板。
6. `repeats` 如何从 seed template 收敛为正式字段。
7. 进入 T11 的 shortlist / 淘汰标准是什么。

## Expected Output

### 1. Screening matrix 文档

新增：

```text
reports/research/screening/screening_matrix_v1.md
```

必须至少包含：

- scope and non-scope
- candidate pool definition
- allowed dataset splits
- model/provider config template
- required run artifacts
- required metrics
- screening pass/fail gates
- collapse checks
- taxonomy field usage rules

### 2. Candidate registry

新增：

```text
reports/research/screening/screening_candidate_registry_v1.md
```

必须至少列出：

- 9 条 text-ready local prompts 中哪些进入第一轮 screening
- 每个候选的来源类别、taxonomy family、长度 bucket、主要结构标签
- 是否为 core candidate / contrast candidate / deferred candidate
- 为什么 GitHub metadata-only 和 Contributor Network structure-only 不在当前候选池

### 3. Shortlist rules

新增：

```text
reports/research/screening/screening_shortlist_rules_v1.md
```

必须写清：

- 淘汰条件
- 入围条件
- parse collapse / all-true / all-false collapse 的处理
- 若多个 prompt 同结构同表现，如何做去冗余
- 进入 T11 之后允许保留多少候选（目标仍为 `3-5`）

### 4. Config 收敛

更新：

```text
configs/research/evaluation_matrix.example.json
configs/research/README.md
```

要求：

- 明确 screening phase 的 prompt set、dataset set、model/provider config、`repeats`
- 不再把 T10 该决定的内容留成模糊 placeholder
- 允许保留 provider_route 为 `to_fill`，但字段结构必须稳定
- `repeats` 不能继续使用 `"1-3"` 这种说明性字符串来表达 screening phase

### 5. README / handoff 同步

更新：

```text
reports/research/screening/README.md
docs/07_handoff.md
```

要求：

- screening README 要反映 “matrix defined, execution not started”
- handoff 要让下一位 worker 能直接接到 T11

## Field Usage Rules That Must Be Preserved

T10 必须显式继承 T09 结论：

- 可直接用于 screening / later analysis planning 的字段，以 `self_audit_v1.md` Section 4.1 为主。
- descriptive-only fields 不得作为 shortlist 主依据。
- 10 个 low-variance fields 必须保留在 schema/registry 中，但不得成为 screening matrix 主维度或统计变量。
- manual coding 是 authoritative taxonomy truth；extractor 只作 cross-check。

## Verification

至少运行：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

以及：

```powershell
python -m json.tool configs/research/evaluation_matrix.example.json > $null
```

如果新增 machine-readable matrix 文件，也要补一条对应解析校验命令，并在最终报告中写清结果。

## Docs to Update

- `configs/research/evaluation_matrix.example.json`
- `configs/research/README.md`
- `reports/research/screening/README.md`
- `reports/research/screening/screening_matrix_v1.md`
- `reports/research/screening/screening_candidate_registry_v1.md`
- `reports/research/screening/screening_shortlist_rules_v1.md`
- `docs/07_handoff.md`

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T10_build_screening_evaluation_matrix
Changed files:
- ...

Matrix decisions:
- candidate pool:
- allowed screening fields:
- descriptive-only fields:
- repeats / config decision:
- shortlist gate:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
