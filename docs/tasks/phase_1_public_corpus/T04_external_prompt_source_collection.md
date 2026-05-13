# T04 External Prompt Source Collection

## Task ID

`T04_external_prompt_source_collection`

## Goal

进入 Phase 1，核验 T03 candidate register 中 public placeholders 的来源、URL、作者/团队、license/ToS 和 storage eligibility，并解决 `data/*/prompt_corpus` governance files 的 git tracking strategy。

## Why Now

T03 已建立 11 个候选的 candidate register v0，但其中 2 个 public placeholders 仍缺少真实 provenance。Reviewer 还指出 `data/interim/prompt_corpus/` 和 `data/external/prompt_corpus/` 被 `.gitignore` 排除，关键研究状态可能无法提交。T04 必须先把 provenance 和可提交性做稳，再进入 T05 normalization。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
.gitignore
data/external/prompt_corpus/raw_index.example.jsonl
data/external/prompt_corpus/raw_index.jsonl
data/interim/prompt_corpus/candidate_register_v0.jsonl
data/interim/prompt_corpus/provenance_rules.md
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/research/corpus_audit/summary.md
docs/07_handoff.md
```

如决定不改 `.gitignore`，必须在 `docs/07_handoff.md` 和 `reports/research/corpus_audit/summary.md` 中明确列出需要 `git add -f` 的文件。

## Forbidden Scope

本任务禁止：

- 修改 `src/`。
- 修改 `tests/`。
- 修改 `prompts/complete/` 中任何 prompt wording。
- 修改 `configs/research/`。
- 修改 `artifacts/`。
- 跑 API eval。
- 复制外部 prompt 原文到仓库，除非来源 license/ToS 明确允许且只保存到任务允许文件。
- 把 external placeholders 伪装成 license-confirmed corpus entries。
- 把 normalized corpus 写成 completed。
- 把 T04 标记为完成。

## Inputs to Read

必须先读：

```text
README.md
AGENTS.md
docs/02_experiment_plan.md
docs/04_task_board.md
docs/05_decision_log.md
docs/06_eval_protocol.md
docs/07_handoff.md
docs/08_risks_and_open_questions.md
docs/review/T03_prompt_corpus_candidate_register_review.md
data/interim/prompt_corpus/candidate_register_v0.jsonl
data/interim/prompt_corpus/provenance_rules.md
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/research/corpus_audit/summary.md
.gitignore
```

## External Lookup Policy

This task may use web lookup only for provenance metadata:

- source URL
- author/team
- license or ToS note
- whether prompt text can be stored, linked, or only structure-coded

Do not download bulk data. Do not paste external prompt full text into the repository.

## Expected Output

### 1. Git tracking decision

Choose one:

1. Update `.gitignore` with a narrow allowlist for prompt corpus governance files, such as:

```text
!data/external/prompt_corpus/
!data/external/prompt_corpus/*.md
!data/external/prompt_corpus/*.jsonl
!data/interim/prompt_corpus/
!data/interim/prompt_corpus/*.md
!data/interim/prompt_corpus/*.json
!data/interim/prompt_corpus/*.jsonl
```

2. Keep `.gitignore` unchanged and document explicit `git add -f` paths.

Do not broadly unignore `data/raw`, all `data/interim`, or all `data/external`.

### 2. Raw index update

Create or update `data/external/prompt_corpus/raw_index.jsonl`.

Each record should include:

```json
{
  "source_id": "",
  "source_type": "official|contributor_network|github|paper|social",
  "source_url": "",
  "author_or_team": "",
  "retrieved_or_checked_on": "2026-05-13",
  "license_or_tos_note": "",
  "prompt_text_storage": "allowed|not_allowed|unknown|metadata_only|structure_only",
  "recommended_register_action": "promote_direct|keep_metadata_only|keep_structure_only|exclude",
  "notes": ""
}
```

If no reliable source can be verified for a placeholder, record that honestly and recommend `structure_only` or `exclude`.

### 3. Candidate register update

Update `data/interim/prompt_corpus/candidate_register_v0.jsonl` for public placeholders:

- fill source URL when verified
- fill author/team when known
- update license note
- update storage status and recompute eligibility
- keep prompt hash empty unless local text is legitimately stored

### 4. Manifest and audit update

Update:

- `data/interim/prompt_corpus/prompt_corpus_manifest.json`
- `reports/research/corpus_audit/summary.md`

They must report:

- candidate count
- verified external source count
- metadata-only count
- structure-only count
- excluded count
- git tracking strategy
- remaining missing metadata

### 5. Handoff update

Update `docs/07_handoff.md`:

- mark T04 worker executed but awaiting review
- record files changed
- record git tracking choice
- state that T05 must not proceed if tracking/provenance remains unresolved

## Verification

Run:

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

Validate JSON:

```powershell
python -m json.tool data/interim/prompt_corpus/prompt_corpus_manifest.json
```

Validate JSONL:

```powershell
Get-Content data/external/prompt_corpus/raw_index.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
Get-Content data/interim/prompt_corpus/candidate_register_v0.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
```

Check git tracking:

```powershell
git check-ignore -v data/interim/prompt_corpus/candidate_register_v0.jsonl
git check-ignore -v data/external/prompt_corpus/raw_index.jsonl
```

If files remain ignored by design, final report must list exact `git add -f` commands.

## Docs to Update

- `docs/07_handoff.md`

Do not modify `docs/04_task_board.md`; Captain updates task completion after review.

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T04_external_prompt_source_collection
Changed files:
- ...

Git tracking decision:
- allowlist / git-add-f / unresolved

External provenance summary:
- verified:
- metadata_only:
- structure_only:
- excluded:

Verification:
- command: ...
  result: pass/fail

Risks / follow-up:
- ...
```
