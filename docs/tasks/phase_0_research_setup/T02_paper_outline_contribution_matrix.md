# T02 Paper Outline Contribution Matrix

## Task ID

`T02_paper_outline_contribution_matrix`

## Goal

把 `reports/paper/outline.md` 从高层 scaffold 细化为可执行的论文设计文档，并新增 contribution list 与 claim/evidence/status 矩阵，用来约束后续 corpus、taxonomy 和 screening 工作。

## Why Now

T01 已通过 review，研究目录和 seed config 已经落地。进入真实 corpus candidate register 之前，必须先明确论文想证明什么、哪些已有证据支持、哪些只是计划，否则后续 worker 容易为了“收集 prompt”而偏离研究主线。

## Allowed Files

Worker 只允许新增或修改以下文件：

```text
reports/paper/README.md
reports/paper/outline.md
reports/paper/contribution_list.md
reports/paper/claim_evidence_matrix.md
docs/07_handoff.md
```

如需要记录极短的 reviewer followup note，可在 `reports/paper/claim_evidence_matrix.md` 内完成，不新增其它治理文件。

## Forbidden Scope

本任务禁止：

- 修改 `src/`。
- 修改 `tests/`。
- 修改 `prompts/complete/` 或任何 prompt wording。
- 修改 `configs/research/`。
- 修改 `data/`、`artifacts/`。
- 下载外部资料或访问网络。
- 跑 API eval。
- 把未运行的实验写成结果。
- 把 released final evaluation subsets 写成赛时盲测。
- 把 T02 标记为完成。

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
reports/paper/outline.md
docs/项目工作历程与阶段性成果总结.md
docs/Stage1结果调研报告.md
```

可选读取：

```text
docs/Stage1科研继续推进调研报告.docx
docs/SAIR代数推理竞赛工程化实验计划.md
```

如果 docx 难以读取，不要阻塞任务；优先使用 `docs/02_experiment_plan.md` 和已有 markdown 报告。

## Expected Output

### 1. Refined outline

更新 `reports/paper/outline.md`，至少包含：

- working title
- one-paragraph abstract draft
- core claim
- RQ list
- contribution list summary
- section skeleton
- planned tables and figures
- evidence status
- not-yet-supported claims
- explicit post-release analysis caveat

必须保持 planning 口吻，不写成已有结果。

### 2. Contribution list

新增 `reports/paper/contribution_list.md`，至少包含：

- contribution id
- contribution statement
- source in local docs
- required evidence
- current status: `supported_by_existing_assets` / `planned_needs_data` / `unsupported_do_not_claim`
- nearest competing work or likely reviewer objection

贡献至少覆盖：

- prompt corpus
- prompt taxonomy
- unified evaluation protocol
- structural findings
- feature-aware textual distillation
- reproducibility / attribution package

### 3. Claim/evidence/status matrix

新增 `reports/paper/claim_evidence_matrix.md`，至少包含：

- claim id
- claim text
- linked RQ
- needed artifact
- current evidence
- missing evidence
- allowed wording now
- forbidden wording now

必须显式列出：

- `feature-aware textual distillation improves robustness` 当前不能作为结果 claim。
- `released final evaluation subsets` 只能作为 post-release analysis。
- taxonomy mapping from experiment plan section 6.2 to YAML fields 是后续前置条件。
- T01 review 中提到的 `compression_style` 和 `ce_search_depth` 缺口。

### 4. Handoff update

更新 `docs/07_handoff.md`：

- 标记 T02 worker 已执行但待 review。
- 记录改动文件。
- 说明不应直接进入 T03，需先 review T02。

## Verification

至少运行：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

并做文本检查：

```powershell
Select-String -Path reports/paper/outline.md -Pattern "post-release analysis|Not-Yet-Supported|claim"
Select-String -Path reports/paper/contribution_list.md -Pattern "supported_by_existing_assets|planned_needs_data|unsupported_do_not_claim"
Select-String -Path reports/paper/claim_evidence_matrix.md -Pattern "forbidden wording|released final evaluation subsets|compression_style|ce_search_depth"
```

## Docs to Update

- `docs/07_handoff.md`

不要修改 `docs/04_task_board.md` 的完成状态。该状态由 Captain 在 review 后更新。

## Reviewer Type

normal

## Worker Final Report Required Format

```text
Task: T02_paper_outline_contribution_matrix
Changed files:
- ...

Verification:
- command: ...
  result: pass/fail

Notes:
- ...

Risks / follow-up:
- ...
```
