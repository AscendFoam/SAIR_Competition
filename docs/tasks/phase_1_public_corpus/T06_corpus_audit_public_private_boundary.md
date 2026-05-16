# T06 Corpus Audit and Public/Private Boundary

## Task ID

`T06_corpus_audit_public_private_boundary`

## Goal

基于 T05 已通过 review 的 `corpus_v1`，写清 corpus audit 和 public/private asset boundary，给后续 T07 taxonomy 与 T10 screening 一个不会误用语料的边界说明。

本任务不新增 prompt，不镜像外部 prompt，不跑评测，只把当前 11 条 corpus v1 记录的公开性、可复算性、发布边界和下游使用规则整理成可审计文档。

## Why Now

T05 已完成 normalized corpus snapshot：

- 11 records total
- 9 text-ready local records
- 10 eligible records
- 1 GitHub MIT metadata-only record
- 1 Contributor Network structure-only record
- 0 mirrored external records
- 0 duplicate records

进入 taxonomy 或 screening 前，需要把这些状态转成明确的使用规则，否则下游 worker 可能把 metadata-only / structure-only 记录误当作可直接复算 prompt。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
reports/research/corpus_audit/summary.md
reports/research/corpus_audit/public_private_boundary.md
data/interim/prompt_corpus/prompt_corpus_manifest.json
data/interim/prompt_corpus/provenance_rules.md
docs/07_handoff.md
```

## Forbidden Scope

本任务禁止：

- 修改 `src/`。
- 修改 `tests/`。
- 修改 `prompts/complete/` 中任何 prompt wording。
- 修改 `configs/research/`。
- 修改 `artifacts/`。
- 修改 `data/external/prompt_corpus/raw_index.jsonl` 或 `raw_index.example.jsonl`。
- 修改 `data/interim/prompt_corpus/corpus_v1.jsonl`、`duplicate_report_v1.json`、`missing_metadata_report_v1.json`。
- 下载、复制、镜像或粘贴任何外部 prompt 原文。
- 跑 API eval、screening eval 或 released subset analysis。
- 把 GitHub metadata-only record 提升为 text-ready。
- 把 Contributor Network structure-only record 提升为 eligible/text-ready。
- 把 corpus v1 写成完整 public ecosystem coverage。
- 修改 `docs/04_task_board.md` 或把 T06 标记为完成。

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
docs/review/T05_normalize_prompt_corpus_v1_review.md
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/duplicate_report_v1.json
data/interim/prompt_corpus/missing_metadata_report_v1.json
data/interim/prompt_corpus/prompt_corpus_manifest.json
data/interim/prompt_corpus/provenance_rules.md
reports/research/corpus_audit/summary.md
```

## Expected Output

### 1. Public/private asset boundary note

新增：

```text
reports/research/corpus_audit/public_private_boundary.md
```

必须至少包含：

- Corpus snapshot and status: `post-release analysis` research corpus, not complete public ecosystem coverage.
- Asset classes:
  - repository-local text-ready records
  - GitHub MIT metadata-only record
  - Contributor Network structure-only record
  - excluded/not-for-release records
- For each class:
  - whether full text is stored locally
  - whether hash/path exists
  - whether it can enter T07 taxonomy
  - whether it can enter T10 screening
  - whether it can enter public release package
  - what attribution or limitation note is required
- Explicit rule: only text-ready records with local path and SHA256 can enter direct recompute.
- Explicit rule: metadata-only and structure-only records cannot enter eval until a later reviewed task changes their status.
- Explicit rule: released final evaluation subsets are not prompt sources and remain only `post-release analysis` assets.

### 2. Corpus audit summary update

更新：

```text
reports/research/corpus_audit/summary.md
```

要求：

- Keep T05 counts intact.
- Mention T05 review verdict: `PASS`.
- Make `corpus_v1.jsonl` the authoritative snapshot for downstream tasks.
- Aggregate the 9 local `missing source_url` records as policy-exempt rather than making them look equally actionable.
- List the two actionable external gaps separately:
  - GitHub MIT source: eligible but not mirrored, no local path/hash.
  - Contributor Network source: host-level provenance only, no stable prompt-level URL.
- State that token estimates are still unavailable and must not support length-bucket claims yet.

### 3. Manifest/provenance note updates if needed

If useful, update:

```text
data/interim/prompt_corpus/prompt_corpus_manifest.json
data/interim/prompt_corpus/provenance_rules.md
```

Only allowed changes:

- Add or clarify downstream-use notes.
- Add reference to `reports/research/corpus_audit/public_private_boundary.md`.
- Do not change counts unless you find an internal inconsistency; if you do, document it in handoff and do not silently reinterpret the corpus.

### 4. Handoff update

更新：

```text
docs/07_handoff.md
```

要求：

- 标记 T06 worker 已执行但待 review。
- 记录 changed files。
- 记录 no external prompt text mirrored。
- 记录 T07/T10 gating rule: only text-ready + hash records may enter direct recompute.
- 说明不能直接进入 T07，需先 review T06。

## Verification

Run:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

Validate JSON if manifest is changed:

```powershell
python -m json.tool data/interim/prompt_corpus/prompt_corpus_manifest.json
```

Validate boundary references:

```powershell
Select-String -Path reports/research/corpus_audit/public_private_boundary.md -Pattern "text-ready|metadata-only|structure-only|post-release analysis|direct recompute"
Select-String -Path reports/research/corpus_audit/summary.md -Pattern "T05 review|authoritative|policy-exempt|token"
```

Scope check:

```powershell
git diff --name-only
```

The diff must only include allowed files plus pre-existing unrelated user changes. Do not revert unrelated changes.

## Docs to Update

- `reports/research/corpus_audit/summary.md`
- `reports/research/corpus_audit/public_private_boundary.md`
- `docs/07_handoff.md`
- optional: `data/interim/prompt_corpus/prompt_corpus_manifest.json`
- optional: `data/interim/prompt_corpus/provenance_rules.md`

Do not modify `docs/04_task_board.md`; Captain updates task completion after review.

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T06_corpus_audit_public_private_boundary
Changed files:
- ...

External prompt text mirrored:
- no

Boundary summary:
- text-ready records:
- metadata-only records:
- structure-only records:
- eval-eligible records:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
