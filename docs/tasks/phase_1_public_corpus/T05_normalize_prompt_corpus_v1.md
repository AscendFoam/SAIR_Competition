# T05 Normalize Prompt Corpus v1

## Task ID

`T05_normalize_prompt_corpus_v1`

## Goal

将 `candidate_register_v0.jsonl` 规范化为第一版 `corpus_v1.jsonl`，生成 duplicate report 和 missing metadata report，并拆清 `eligible`、`text_ready`、`mirrored_external` 等计数，避免后续 eval 或 taxonomy worker 误读候选状态。

## Why Now

T04 已通过 review，外部 provenance v0 和 git tracking strategy 已落地。现在仍缺 normalized corpus snapshot：manifest 的 `corpus_size` 仍为 0，且 `direct_recompute_count` 混合了“许可上可重算”和“本地已有文本可直接跑”的语义。T05 必须把 corpus 状态规范化后，才能进入 T06 audit 或后续 taxonomy / screening。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
data/external/prompt_corpus/raw_index.example.jsonl
data/external/prompt_corpus/raw_index.jsonl
data/external/prompt_corpus/raw_prompts/
data/interim/prompt_corpus/candidate_register_v0.jsonl
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/duplicate_report_v1.json
data/interim/prompt_corpus/missing_metadata_report_v1.json
data/interim/prompt_corpus/prompt_corpus_manifest.json
data/interim/prompt_corpus/provenance_rules.md
reports/research/corpus_audit/summary.md
docs/07_handoff.md
```

If external prompt text is mirrored, it must only go under:

```text
data/external/prompt_corpus/raw_prompts/
```

and only when license/ToS permits it.

## Forbidden Scope

本任务禁止：

- 修改 `src/`。
- 修改 `tests/`。
- 修改 `prompts/complete/` 中任何 prompt wording。
- 修改 `configs/research/`。
- 修改 `artifacts/`。
- 跑 API eval。
- 使用 released final evaluation subsets 做任何 prompt selection。
- 复制 license/ToS 不清楚的外部 prompt 原文。
- 把 Contributor Network host-level placeholder 提升为 direct eval。
- 把 normalized corpus 写成 complete public ecosystem coverage。
- 把 T05 标记为完成。

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
docs/review/T04_external_prompt_source_collection_review.md
data/external/prompt_corpus/raw_index.jsonl
data/interim/prompt_corpus/candidate_register_v0.jsonl
data/interim/prompt_corpus/provenance_rules.md
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/research/corpus_audit/summary.md
```

## Expected Output

### 1. Corpus v1

新增 `data/interim/prompt_corpus/corpus_v1.jsonl`。

Each record must include at least:

```json
{
  "prompt_id": "",
  "candidate_id": "",
  "source_type": "",
  "source_url": "",
  "author_or_team": "",
  "prompt_text_path": "",
  "prompt_sha256": "",
  "prompt_bytes": 0,
  "prompt_tokens_est": 0,
  "text_ready": true,
  "eligible_for_recompute": true,
  "storage_status": "",
  "license_or_tos_note": "",
  "attribution_note": "",
  "post_release_relation": "",
  "corpus_inclusion_status": "included_text_ready|included_metadata_only|included_structure_only|excluded",
  "notes": ""
}
```

Rules:

- Local prompt records with valid paths/hash may be `included_text_ready`.
- GitHub MIT source may be imported only if the worker can preserve source URL, file path, license note, author/team, hash and attribution.
- If GitHub prompt is not mirrored, keep it metadata-only and do not mark `text_ready: true`.
- Contributor Network host-level source stays structure-only unless a stable prompt-level page and storage terms are verified.

### 2. Duplicate report

新增 `data/interim/prompt_corpus/duplicate_report_v1.json`:

- duplicate by SHA256
- duplicate by normalized source URL
- duplicate by candidate_id / prompt_id
- action notes

### 3. Missing metadata report

新增 `data/interim/prompt_corpus/missing_metadata_report_v1.json`:

- missing source URL
- missing author/team
- missing license note
- missing prompt hash
- missing local text
- unresolved storage eligibility
- recommended next action per record

### 4. Manifest update

更新 `prompt_corpus_manifest.json`，必须拆分：

- `candidate_count`
- `corpus_v1_record_count`
- `eligible_count`
- `text_ready_count`
- `mirrored_external_count`
- `metadata_only_count`
- `structure_only_count`
- `excluded_count`
- `hash_coverage`
- `duplicate_report_path`
- `missing_metadata_report_path`

Do not leave ambiguous `direct_recompute_count` as the only headline count.

### 5. Raw index example schema alignment

更新 `data/external/prompt_corpus/raw_index.example.jsonl`，让 example schema 与 `raw_index.jsonl` 的 T04 schema 对齐，或明确在文件内用 `schema_note` 说明两者差异。

### 6. Corpus audit update

更新 `reports/research/corpus_audit/summary.md`:

- corpus v1 size
- text-ready count
- eligible count
- mirrored external count
- missing metadata summary
- duplicate summary
- remaining risks for T06

### 7. Handoff update

更新 `docs/07_handoff.md`:

- 标记 T05 worker 已执行但待 review。
- 记录 changed files。
- 记录是否 mirrored GitHub prompt text。
- 说明不能直接进入 T06，需先 review T05。

## Verification

Run:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

Validate JSON:

```powershell
python -m json.tool data/interim/prompt_corpus/prompt_corpus_manifest.json
python -m json.tool data/interim/prompt_corpus/duplicate_report_v1.json
python -m json.tool data/interim/prompt_corpus/missing_metadata_report_v1.json
```

Validate JSONL:

```powershell
Get-Content data/interim/prompt_corpus/corpus_v1.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
Get-Content data/external/prompt_corpus/raw_index.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
Get-Content data/external/prompt_corpus/raw_index.example.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
```

Check count semantics:

```powershell
Select-String -Path data/interim/prompt_corpus/prompt_corpus_manifest.json -Pattern "eligible_count|text_ready_count|mirrored_external_count"
Select-String -Path reports/research/corpus_audit/summary.md -Pattern "text-ready|eligible|missing metadata|duplicate"
```

If external prompt text is mirrored, verify hash:

```powershell
Get-FileHash data/external/prompt_corpus/raw_prompts/* -Algorithm SHA256
```

## Docs to Update

- `docs/07_handoff.md`

Do not modify `docs/04_task_board.md`; Captain updates task completion after review.

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T05_normalize_prompt_corpus_v1
Changed files:
- ...

Mirrored external prompt text:
- yes/no
- source:

Corpus summary:
- corpus_v1_record_count:
- eligible_count:
- text_ready_count:
- mirrored_external_count:
- metadata_only_count:
- structure_only_count:
- excluded_count:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
