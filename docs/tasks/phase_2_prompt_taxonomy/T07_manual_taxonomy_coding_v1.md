# T07 Manual Taxonomy Coding v1

## Task ID

`T07_manual_taxonomy_coding_v1`

## Goal

对第一批 9 条 text-ready local prompt 做人工 taxonomy 编码，生成 `prompt_features_v1.jsonl`、taxonomy v1 报告和 plan-to-schema mapping note，并补足 reviewable 的 `prompt_tokens_est` / length-bucket 口径。

本任务的重点是把 T06 已确认的 corpus 边界转成可供 T08 extractor skeleton 和 T10 screening 复用的结构化输入，而不是实现 extractor，更不是开始评测。

## Why Now

Milestone 1 已以 `Conditional` gate 关闭，允许进入 Milestone 2，但条件很明确：

- 只能使用 `corpus_v1.jsonl` 作为 authoritative snapshot。
- 只能对 9 条 text-ready local records 做 full-text coding。
- `prompt_tokens_est` 仍为 `0`，长度相关特征还不能安全用于后续分析。

T07 是后续 T08/T10 的前置：没有稳定的人工 taxonomy，就不该写 extractor skeleton，也不该开始 screening matrix。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_features_v1.jsonl
configs/research/prompt_feature_taxonomy.yaml
reports/research/taxonomy/README.md
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
docs/07_handoff.md
```

## Forbidden Scope

本任务禁止：

- 修改 `src/`。
- 修改 `tests/`。
- 修改 `prompts/complete/` 中任何 prompt wording。
- 修改 `artifacts/`。
- 跑 API eval、screening eval 或 released subset analysis。
- 下载、复制、镜像或粘贴任何外部 prompt 原文。
- 把 GitHub metadata-only record 或 Contributor Network structure-only record 提升为 full-text coded。
- 把 taxonomy seed scaffold 伪写成 extractor 已完成。
- 修改 `docs/04_task_board.md` 或把 T07 标记为完成。

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
configs/research/prompt_feature_taxonomy.yaml
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/research/corpus_audit/summary.md
reports/research/corpus_audit/public_private_boundary.md
reports/research/taxonomy/README.md
```

## Expected Output

### 1. `prompt_features_v1.jsonl`

新增：

```text
data/interim/prompt_corpus/prompt_features_v1.jsonl
```

要求：

- 只包含 9 条 `included_text_ready` local records。
- 每条记录必须能回链到 `prompt_id` / `candidate_id`。
- 记录 taxonomy field values、manual coding note、coder note、length-bucket choice。
- 不要把 GitHub metadata-only 或 Contributor Network structure-only 记录写成 full-text coded rows。

### 2. `corpus_v1.jsonl` token estimate backfill

允许为 9 条 text-ready local records 回填：

- `prompt_tokens_est`
- 如需要，可补充简短 note 字段说明估算方法

要求：

- 估算方法必须 reviewable。
- 不要伪称为精确 tokenizer count，除非你真的在本任务 allowed scope 内明确使用并记录了 tokenizer 方法。
- 对 2 条非 text-ready external records 不要求补齐 token estimate。

### 3. taxonomy report

新增：

```text
reports/research/taxonomy/taxonomy_v1.md
reports/research/taxonomy/taxonomy_mapping_note.md
```

其中必须写清：

- 本轮 full-text coding pool 为什么只有 9 条 text-ready local records。
- experiment plan 第 6.2 节字段与 `prompt_feature_taxonomy.yaml` 当前字段如何对应。
- 哪些字段直接采用 seed scaffold，哪些字段需补充、收紧或保留为后续扩展。
- length bucket、`compression_style`、`ce_search_depth` 的当前处理方式。
- 哪些 feature 现在能支持，哪些仍只是 planning placeholder。

### 4. taxonomy seed update if needed

允许更新：

```text
configs/research/prompt_feature_taxonomy.yaml
```

但只允许：

- 把 seed scaffold 调整成更适合 manual coding 的 v1 字段集合。
- 加入 reviewer 已长期 deferred 的 `compression_style` / `ce_search_depth`，如果你认为它们在 9 条样本上可稳定编码。
- 修正文档级字段描述或 allowed_values。

不要：

- 引入 extractor-specific implementation detail。
- 把无法稳定编码的字段伪装成已解决。

### 5. Handoff update

更新：

```text
docs/07_handoff.md
```

要求：

- 标记 T07 worker 已执行但待 review。
- 记录 coding pool size、非 text-ready exclusion、token estimate handling。
- 说明 T08 还未执行，T10 更未开始。

## Verification

Run:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

Validate JSONL:

```powershell
Get-Content data/interim/prompt_corpus/prompt_features_v1.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
Get-Content data/interim/prompt_corpus/corpus_v1.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
```

Basic consistency checks:

```powershell
Select-String -Path reports/research/taxonomy/taxonomy_v1.md -Pattern "text-ready|metadata-only|structure-only|compression_style|ce_search_depth|length"
Select-String -Path reports/research/taxonomy/taxonomy_mapping_note.md -Pattern "6.2|mapping|seed|bucket"
```

Optional count sanity check:

```powershell
(Get-Content data/interim/prompt_corpus/prompt_features_v1.jsonl).Count
```

Expected: `9`

## Docs to Update

- `reports/research/taxonomy/README.md`
- `reports/research/taxonomy/taxonomy_v1.md`
- `reports/research/taxonomy/taxonomy_mapping_note.md`
- `docs/07_handoff.md`
- optional: `configs/research/prompt_feature_taxonomy.yaml`
- optional: `data/interim/prompt_corpus/corpus_v1.jsonl`

Do not modify `docs/04_task_board.md`; Captain updates task completion after review.

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T07_manual_taxonomy_coding_v1
Changed files:
- ...

Coding summary:
- coded records:
- excluded non-text-ready records:
- token estimate method:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
