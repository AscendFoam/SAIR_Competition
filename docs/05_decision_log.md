# Decision Log

本文件记录影响研究方向、架构或复现实验解释的关键决策。普通执行细节写入 `docs/07_handoff.md`。

## D001: Stage1 后续主线切换为 prompt textual distillation research

日期：2026-05-11

决策：

后续主线从“继续优化 Stage1 prompt 刷榜”切换为“基于公开 prompt 生态的 textual distillation 与鲁棒性研究”。

理由：

- Stage1 最终提交已收口。
- 仓库已有数据、评测、tagger 和 analysis 资产。
- 继续刷 prompt 容易陷入局部 wording 调参，科研价值低。
- corpus、taxonomy、统一复算和 robustness gap 更容易形成可发表贡献。

影响：

- `docs/02_experiment_plan.md` 作为研究基准。
- `docs/04_task_board.md` 以 Phase 0 到 Phase 7 组织任务。
- Stage2 只保留轻量规则跟踪和资产映射。

## D002: Released final evaluation subsets 只作为后赛事实证分析

日期：2026-05-11

决策：

任何 released final evaluation subsets 的使用必须标注为 `post-release analysis`，不得作为 prompt selection reward，不得包装成赛时盲测泛化。

理由：

- subsets 已公开，存在后视镜风险。
- 论文可信度依赖清晰区分 screening、recomputed benchmark 和 post-release analysis。

影响：

- `docs/06_eval_protocol.md` 明确三类评测。
- reviewer 必须检查是否有泄漏式叙事。

## D003: Prompt taxonomy 和 problem family tagger 分层维护

日期：2026-05-11

决策：

prompt taxonomy 描述 prompt 结构，family tagger 描述题目结构，两者不合并。

理由：

- 合并标签会让解释对象混乱。
- 真正的研究价值来自 prompt feature 和 problem family 的交叉分析。

影响：

- `configs/research/prompt_feature_taxonomy.yaml` 后续只定义 prompt 结构标签。
- family-conditioned metrics 在 analysis 层完成。

## D004: 默认单 worker 顺序执行

日期：2026-05-11

决策：

除非 Captain 拆出互不依赖且文件范围不重叠的任务，否则默认单 worker 顺序执行。

理由：

- 当前任务主要涉及治理文档、schema、目录和评测协议，状态强相关。
- 并行会增加文档状态冲突和 review 成本。

影响：

- `docs/04_task_board.md` 始终维护一个 Current Unique Task。

## D005: 接受 T01 review verdict 并进入 T02

日期：2026-05-12

决策：

`docs/review/T01_research_scaffold_review.md` verdict 为 `PASS`，Captain 接受该结论，标记 `T01_research_scaffold` 完成，并将 Current Unique Task 切换到 `T02_paper_outline_contribution_matrix`。

理由：

- Reviewer 未发现 blocking issue。
- T01 输出均为 scaffold/seed/example 状态，没有伪造 corpus 或实验完成事实。
- JSON/YAML 和 JSONL 示例已通过 reviewer 独立验证。
- 没有越界修改 `src/`、`tests/`、prompt wording 或历史 artifacts。

非阻塞事项处理：

- `repeats: "1-3"` 作为 example template 暂时接受，正式 runner config 在 T10 前收敛。
- `storage_policy` typo 放入 T03 清理范围。
- taxonomy 字段映射、`compression_style`、`ce_search_depth` 放入 T02/T07 后续约束。

## D006: T02 优先于 T03

日期：2026-05-12

决策：

下一任务先做 T02，而不是直接做 T03 corpus candidate register。

理由：

- T01 已创建 paper outline v0，但 outline 仍是高层 scaffold。
- 先建立 claim/evidence/status 矩阵，可以约束后续 corpus 收集和 taxonomy 标注服务于论文主张。
- T02 不需要网络和 API 成本，适合作为进入真实数据登记前的低风险收敛任务。
