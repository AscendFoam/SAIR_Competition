# Handoff

日期：2026-05-11

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

`T01_research_scaffold`

任务包：

- `docs/tasks/phase_0_research_setup/T01_research_scaffold.md`

状态：

- Ready for worker。
- 尚未执行。
- 尚未 review。

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
docs/tasks/phase_0_research_setup/T01_research_scaffold.md
```

## 4. Worker 执行边界

下一轮 worker 只做 T01：

- 创建研究目录。
- 写 seed configs。
- 写 prompt corpus manifest。
- 写 paper outline v0。
- 运行任务包里的验证。

不要做：

- 不改 `src/`。
- 不跑 API eval。
- 不改 prompt wording。
- 不下载外部数据。
- 不删除或重命名历史文档。
- 不标记任务完成。

## 5. Reviewer 重点

T01 reviewer 类型：normal。

重点检查：

- JSON 文件是否可解析。
- YAML 是否为人类可读且字段覆盖 `docs/02_experiment_plan.md` 的 taxonomy。
- manifest 是否明确当前 corpus 为空或 seed 状态，不能伪称已收集完。
- paper outline 是否写成计划，不写成已有实验结果。
- 是否越界修改 `src/`、prompt 或历史 artifacts。

## 6. 完成 T01 后 Captain 要做

如果 review 为 `PASS`：

1. 在 `docs/04_task_board.md` 勾选 `T01`。
2. 更新本文件的当前状态。
3. 在 `docs/05_decision_log.md` 记录任何关键 schema 决策。
4. 将 Current Unique Task 切换为 `T02` 或 `T03`，但不直接执行。

如果 `PASS_WITH_WARNINGS`：

1. 把 warning 分类为 accepted、deferred、rejected。
2. deferred 写入 `docs/08_risks_and_open_questions.md`。
3. 再决定是否进入下一任务。

如果 `BLOCK`：

1. 只派修 blocking issue 的小任务。
2. 同一任务最多自动复审一次。
3. 第二次仍 BLOCK 则停止交给用户裁决。

## 7. 当前未验证事项

- 新研究目录尚未创建。
- corpus schema 尚未落地到机器可读配置。
- paper outline v0 尚未创建。
- T01 之后的任务包尚未详细展开。

