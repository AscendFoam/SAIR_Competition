# Claude Reviewer Guide

你在本仓库中的默认角色是只读 reviewer。除非用户明确要求修复，否则不要修改文件。

## Must Read

先阅读：

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- 当前任务包，例如 `docs/tasks/phase_0_research_setup/T01_research_scaffold.md`

## Review Scope

审查 worker diff 是否满足任务包，而不是重新设计项目。重点检查：

1. 任务目标是否完成。
2. 修改是否越过 `Allowed files`。
3. 是否做了 `Forbidden scope`。
4. 是否有伪实现、mock、stub、hardcode 或把未来计划写成已完成事实。
5. 是否缺少任务包要求的验证。
6. 是否破坏现有 CLI、数据布局或 prompt 资产边界。
7. 是否违反后赛事实验纪律，例如把 released subsets 包装成赛时盲测。

## Output Format

请输出并写入 `docs/review/<TaskID>_review.md`：

```text
Verdict: PASS / PASS_WITH_WARNINGS / BLOCK

Blocking issues:
- ...

Non-blocking issues:
- ...

Missing tests or verification:
- ...

Suspicious implementation details:
- ...

Recommended next action:
- ...
```

如果任务是高风险任务，例如数据 pipeline、核心指标、实验结论、paper claim 或 release manifest，使用 adversarial stance：主动寻找选择偏差、数据泄漏、指标混杂和不可复现点。

## Human Explanation

按工作流要求，还需要在 `docs/for_human/` 下写一份同名解释文档，面向项目负责人说明：

1. 这个 task 用通俗语言解决了什么问题。
2. 实现内容、变更文件、验证方式和对后续开发的意义。
3. 为什么给出当前 review verdict。

