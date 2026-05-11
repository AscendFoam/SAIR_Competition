# SAIR Competition Agent Guide

本仓库当前主线是 SAIR Stage1 后赛事实证科研，不再默认以刷榜或 Stage2 solver 为目标。所有 agent 必须先读：

- `README.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Roles

### Captain

Captain 负责项目拆解、任务调度、结果整合和治理文档更新。

每轮必须明确：

1. 当前唯一任务。
2. 为什么现在做它。
3. Worker 任务包。
4. 允许修改的文件范围。
5. 禁止做的事。
6. 验证命令或验收标准。
7. 完成后需要更新的治理文件。

Captain 不直接进行大规模实现，不把计划写成已完成事实。

### Worker

Worker 只执行 Captain 指定的一个任务。

规则：

1. 只改任务包 `Allowed files`。
2. 不做 `Forbidden scope`。
3. 不自动领取下一任务。
4. 完成后运行 `Verification`。
5. 汇报改动、验证结果和剩余风险。
6. 不直接把任务标记为完成，任务完成状态由 Captain 在 review 后更新。

### Reviewer

Reviewer 默认只读审查，不改文件。

重点检查：

1. 是否真的完成任务目标。
2. 是否存在伪实现、mock、stub、hardcode。
3. 是否缺少测试或验证。
4. 是否越界修改。
5. 是否破坏已有功能。
6. 文档是否把计划写成事实。

输出 verdict：`PASS`、`PASS_WITH_WARNINGS` 或 `BLOCK`。

## Project Discipline

- 仓库文件是主状态，聊天 session 不是主状态。
- 每轮只推进一个 Current Unique Task。
- 不让多个 worker 同时修改同一批文件。
- 后赛事实验必须标注 `post-release analysis`，不能包装成赛时盲测。
- 不把未公开 prompt、API raw outputs、私有数据或敏感配置写入公开复现包。
- 研究结论必须能追溯到 prompt hash、数据版本、run config 和评测协议。

## Current Research Direction

本阶段研究问题是：

> 基于 SAIR Stage1 公开 prompt 生态，构建 provenance-aware prompt corpus 与 prompt feature taxonomy，量化 prompt 结构、模型和分布偏移之间的关系，并验证 feature-aware textual distillation 是否能改善鲁棒性。

近期非目标：

- 不继续大规模手写 prompt 刷榜。
- 不把 released final evaluation subsets 当作私有盲测。
- 不启动正式 Stage2 Lean solver 主线。
- 不做大规模模型微调。

## Task Package Location

所有 worker 任务包放在：

```text
docs/tasks/<milestone_name>/<TaskID>_<short_name>.md
```

当前任务板由 `docs/04_task_board.md` 维护。

