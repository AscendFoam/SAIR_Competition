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

`T02_paper_outline_contribution_matrix`

任务包：

- `docs/tasks/phase_0_research_setup/T02_paper_outline_contribution_matrix.md`

状态：

- Ready for worker。
- 尚未执行。
- T01 已通过 review 并由 Captain 标记完成。

T01 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T01_research_scaffold_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T01。
- Non-blocking followups: T03 清理 `storage_policy` typo；T07 前补 taxonomy mapping、`compression_style` 和 `ce_search_depth` 决策；T10 前收敛 `repeats` schema。

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
docs/tasks/phase_0_research_setup/T02_paper_outline_contribution_matrix.md
```

## 4. Worker 执行边界

下一轮 worker 只做 T02：

- 细化 `reports/paper/outline.md`。
- 新增 contribution list 和 claim/evidence/status matrix。
- 从既有本地文档抽取研究贡献、证据来源和未支持 claim。
- 将 T01 review 中 taxonomy mapping 相关提醒写入 paper claim 约束。

不要做：

- 不改 `src/`。
- 不跑 API eval。
- 不改 prompt wording。
- 不下载外部数据。
- 不删除或重命名历史文档。
- 不标记任务完成。

## 5. Reviewer 重点

T02 reviewer 类型：normal。

重点检查：

- 是否把 paper claim 分成 supported / planned / unsupported。
- 是否从本地文档抽取 contribution，而不是凭空扩写。
- 是否避免把未运行实验写成结果。
- 是否保留 released subsets 的 `post-release analysis` 限定。
- 是否越界修改代码、prompt 或 artifacts。

## 6. 完成 T02 后 Captain 要做

如果 review 为 `PASS`：

1. 在 `docs/04_task_board.md` 勾选 `T02`。
2. 更新本文件的当前状态。
3. 将 Current Unique Task 切换为 `T03`，但不直接执行。

如果 `PASS_WITH_WARNINGS`：

1. 把 warning 分类为 accepted、deferred、rejected。
2. deferred 写入 `docs/08_risks_and_open_questions.md`。
3. 再决定是否进入下一任务。

如果 `BLOCK`：

1. 只派修 blocking issue 的小任务。
2. 同一任务最多自动复审一次。
3. 第二次仍 BLOCK 则停止交给用户裁决。

## 7. 当前未验证事项

- T02 尚未执行。
- corpus 真实记录尚未采集，manifest 仍为 `seed_scaffold_not_collected`。
- paper outline 仍缺少 claim/evidence/status 矩阵。
- screening / recomputed benchmark / post-release analysis 仍未开始执行。
- T03 之后的任务包尚未详细展开。
