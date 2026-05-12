# T03 Prompt Corpus Candidate Register

## Task ID

`T03_prompt_corpus_candidate_register`

## Goal

建立第一批 prompt candidate register v0 和 provenance rules，明确哪些 prompt 可以直接进入后续 recompute，哪些只能做 metadata-only 或 structure-only 记录，并吸收 T01/T02 review 的轻量 hygiene followups。

## Why Now

T01 已完成研究脚手架，T02 已完成 paper claim/evidence guardrail。进入 Phase 1 正式 corpus cleaning 前，必须先把候选池、来源边界、许可/归因状态、存储策略和后赛事实验限制写清楚，避免后续 worker 把不可公开 prompt 或未核验外部材料直接混入 corpus。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
data/external/prompt_corpus/raw_index.example.jsonl
data/interim/prompt_corpus/candidate_register_v0.jsonl
data/interim/prompt_corpus/provenance_rules.md
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/research/corpus_audit/summary.md
reports/paper/outline.md
reports/paper/contribution_list.md
docs/07_handoff.md
```

允许读取但不修改：

```text
prompts/complete/
configs/research/
docs/review/
```

## Forbidden Scope

本任务禁止：

- 修改 `src/`。
- 修改 `tests/`。
- 修改 `prompts/complete/` 中任何 prompt wording。
- 修改 `configs/research/`，除非另开任务。
- 修改 `artifacts/`。
- 下载外部数据或访问网络。
- 复制外部 public prompt 原文到仓库。
- 跑 API eval。
- 把 candidate register 写成 completed corpus。
- 把 T03 标记为完成。

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
docs/review/T01_research_scaffold_review.md
docs/review/T02_paper_outline_contribution_matrix_review.md
configs/research/corpus_sources.example.json
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/paper/claim_evidence_matrix.md
```

需要检查本地 prompt 文件列表：

```text
prompts/complete/
```

## Expected Output

### 1. Candidate register v0

新增 `data/interim/prompt_corpus/candidate_register_v0.jsonl`，至少登记 `8-12` 个候选，其中应优先覆盖：

- `P1.2.3_implicit_guardrail_v2`
- `P1.2.5_minimal_rule_missing_hard_composition`
- `P2.0.0_official_balanced_strict_v0`
- `P2.0.1_official_counterexample_first_strict_v0`
- `P2.0.2_official_fast_filters_strict_v0`
- minimal / no-cheatsheet baseline 或 `P0` 类本地 baseline
- 其它本地历史 prompt，作为 local contrast candidates
- public prompt placeholders，只能 metadata-only 或 structure-only，不复制原文

每行至少包含：

```json
{
  "candidate_id": "",
  "source_type": "local|official|github|paper|contributor_network|social",
  "source_ref": "",
  "prompt_text_path": "",
  "prompt_sha256": "",
  "prompt_bytes": 0,
  "storage_status": "local_text_available|metadata_only|structure_only|excluded",
  "recompute_eligibility": "direct_recompute|needs_license_review|structure_only|exclude",
  "post_release_relation": "pre_release_design|post_release_analysis_only|unknown",
  "license_or_tos_note": "",
  "attribution_note": "",
  "candidate_role": "baseline|local_contrast|official_archetype|public_placeholder|distillation_future",
  "notes": ""
}
```

本地 prompt 的 hash 和 byte size 应从文件实际计算，不要手写猜测。

### 2. Provenance rules

新增 `data/interim/prompt_corpus/provenance_rules.md`，至少写清：

- source type 定义。
- storage eligibility。
- direct recompute eligibility。
- metadata-only 和 structure-only 记录条件。
- released final evaluation subsets 的 post-release 限定。
- attribution policy。
- public/private asset boundary。

### 3. Manifest update

更新 `data/interim/prompt_corpus/prompt_corpus_manifest.json`：

- status 仍不得写成 completed corpus。
- 记录 candidate register v0 的路径。
- 记录 candidate count、direct recompute count、structure-only count。
- 记录 hash coverage。
- 记录 next actions。

### 4. Corpus audit draft update

更新 `reports/research/corpus_audit/summary.md`：

- corpus size 仍按真实状态写。
- candidate register size 单独写。
- source counts。
- hash coverage。
- missing metadata。
- license/tos notes。
- next actions for T04。

### 5. T01/T02 review hygiene

在允许范围内处理：

- 修正 `reports/paper/outline.md` 中指向 `contribution_list.md` 的绝对 Windows 链接，改为相对链接。
- 在 `reports/paper/contribution_list.md` 增加一个 rejected/unsupported claim 或说明，使 `unsupported_do_not_claim` 状态实际出现。
- `raw_index.example.jsonl` 或 T03 新规则中处理 T01 review 提到的 `storage_policy` typo，不必修改 `configs/research/`。

### 6. Handoff update

更新 `docs/07_handoff.md`：

- 标记 T03 worker 已执行但待 review。
- 记录改动文件。
- 说明不能直接进入 T04，需先 review T03。

## Verification

至少运行：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

验证 JSON 文件可解析：

```powershell
python -m json.tool data/interim/prompt_corpus/prompt_corpus_manifest.json
```

验证 JSONL 每行可解析：

```powershell
Get-Content data/interim/prompt_corpus/candidate_register_v0.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
Get-Content data/external/prompt_corpus/raw_index.example.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
```

检查关键字段：

```powershell
Select-String -Path data/interim/prompt_corpus/provenance_rules.md -Pattern "structure-only|metadata-only|direct recompute|post-release"
Select-String -Path reports/paper/contribution_list.md -Pattern "unsupported_do_not_claim"
Select-String -Path reports/paper/outline.md -Pattern "D:/Codes"
```

最后一个命令应无匹配；如果仍有匹配，需要说明原因。

## Docs to Update

- `docs/07_handoff.md`

不要修改 `docs/04_task_board.md` 的完成状态。该状态由 Captain 在 review 后更新。

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T03_prompt_corpus_candidate_register
Changed files:
- ...

Verification:
- command: ...
  result: pass/fail

Candidate register summary:
- total candidates:
- direct_recompute:
- metadata_only:
- structure_only:
- excluded:

Risks / follow-up:
- ...
```
