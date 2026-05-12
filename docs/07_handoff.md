# Handoff

日期：2026-05-12

## 1. 当前项目状态

项目已从 Stage1 参赛收口切换到 Stage1 后赛事实证科研。核心基准文档是：

- `docs/02_experiment_plan.md`
- `docs/reference/AI_coding_workflow.md`

当前治理文档已初始化：

- `AGENTS.md`
- `CLAUDE.md`
- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## 2. Current Unique Task

`T03_prompt_corpus_candidate_register`

任务包：

- `docs/tasks/phase_0_research_setup/T03_prompt_corpus_candidate_register.md`

状态：

- Ready for worker。
- 尚未执行。
- T01、T02 已通过 review 并由 Captain 标记完成。

T01 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T01_research_scaffold_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T01。
- Non-blocking followups: T03 清理 `storage_policy` typo；T07 前补 taxonomy mapping、`compression_style` 和 `ce_search_depth` 决策；T10 前收敛 `repeats` schema。

T02 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T02_paper_outline_contribution_matrix_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T02。
- Non-blocking followups: T03 修正 `outline.md` 绝对路径链接；T03/T21 前补 rejected/unsupported claim；C7 只保留为 setup/motivation。

## 3. 下一位 Worker 需要先读

```text
README.md
AGENTS.md
docs/02_experiment_plan.md
docs/03_architecture.md
docs/04_task_board.md
docs/06_eval_protocol.md
docs/07_handoff.md
docs/08_risks_and_open_questions.md
docs/tasks/phase_0_research_setup/T03_prompt_corpus_candidate_register.md
```

## 4. Worker 执行边界

下一轮 worker 只做 T03：

- 建立第一批 prompt candidate register v0。
- 写明 provenance rules、storage eligibility、recompute eligibility 和 structure-only 记录条件。
- 清理 T01/T02 review 中指定的轻量 hygiene 项。
- 更新 handoff 为 T03 已执行待 review。

不要做：

- 不改 `src/`。
- 不跑 API eval。
- 不改 prompt wording。
- 不下载外部数据。
- 不删除或重命名历史文档。
- 不标记任务完成。

## 5. Reviewer 重点

T03 reviewer 类型：normal。

重点检查：

- 是否登记了第一批本地 prompt 候选，但没有复制不可公开外部 prompt。
- 是否区分 direct-recompute、metadata-only、structure-only 和 excluded。
- 是否保留 prompt hash / path / source / license note / post-release note 字段。
- 是否避免下载外部数据或跑 API。
- 是否只做 allowed files。

## 6. 完成 T03 后 Captain 要做

如果 review 为 `PASS`：

1. 在 `docs/04_task_board.md` 勾选 `T03`。
2. 更新本文件的当前状态。
3. 判断 Phase 0 exit criteria 是否满足。
4. 推荐进入 `T04`，但不直接执行。

如果 `PASS_WITH_WARNINGS`：

1. 把 warning 分类为 accepted、deferred、rejected。
2. deferred 写入 `docs/08_risks_and_open_questions.md`。
3. 再决定是否进入下一任务。

如果 `BLOCK`：

1. 只派修 blocking issue 的小任务。
2. 同一任务最多自动复审一次。
3. 第二次仍 BLOCK 则停止交给用户裁决。

## 7. 当前未验证事项

- T03 尚未执行。
- corpus 真实记录尚未采集，manifest 仍为 `seed_scaffold_not_collected`。
- prompt candidate register v0 尚未建立。
- screening / recomputed benchmark / post-release analysis 仍未开始执行。
- T04 之后的任务包尚未详细展开。
