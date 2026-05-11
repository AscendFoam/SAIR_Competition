# Feasibility Report

日期：2026-05-11

## 1. 问题定义

本项目研究 SAIR Stage1 公开 prompt 生态中的 textual distillation 现象。核心对象不是单个最高分 prompt，而是 prompt 结构如何影响：

- parse stability
- true/false recall tradeoff
- model transfer gap
- public split 到 released final evaluation subsets 的 robustness gap
- problem family 条件表现

## 2. 相关工作矩阵

| 类别 | 代表方向 | 与本项目关系 | 差异化要求 |
|---|---|---|---|
| Prompt ceiling | Less Is More | 直接相邻 | 必须超越“prompt 越长未必越好”，加入 corpus、taxonomy、provenance 和 post-release robustness |
| Prompt optimization | prompt search / prompt evolution | 方法背景 | 本项目第一阶段不做大规模搜索，优先做 feature-aware controlled variants |
| CoT distillation | rationale / trace distillation | 概念背景 | 本项目研究的是 prompt text 作为知识载体，不训练学生模型 |
| Formal reasoning eval | Lean / equational reasoning benchmarks | 任务背景 | 当前主线仍是 Stage1 prompt judge，不启动正式 Stage2 solver |
| Error taxonomy | family-conditioned error analysis | 本仓库已有资产 | 将 problem family tag 与 prompt feature tag 做交叉分析 |

## 3. 最像的 5 个已有工作

当前已知最相近工作类型：

1. `Less Is More` 类 prompt complexity ceiling 研究。
2. LLM prompt evolution / automatic prompt engineering。
3. Chain-of-thought distillation 与 rationale compression。
4. Formal mathematics benchmark evaluation。
5. Post-hoc leaderboard and public solution analyses。

需要后续在论文相关工作阶段补充正式引用和差异化表。

## 4. 可差异化点

本项目可成立的关键贡献：

1. 构建带 provenance 的 SAIR Stage1 public prompt corpus。
2. 提出 prompt feature taxonomy，用结构标签替代 anecdotal prompt comparison。
3. 用统一 pipeline 复算代表性 prompt 的跨模型、跨 split 和 released subsets 表现。
4. 把 prompt feature 与 problem family tag 交叉，分析结构族条件错误。
5. 验证 feature-aware distilled prompt 是否比单纯堆规则更稳。

## 5. MVP 实验

MVP 范围：

- `8-12` 个 prompt 候选进入 corpus。
- `3-5` 个 prompt 进入完整复算 shortlist。
- 至少一个 feature-aware pair 做 controlled ablation。
- 输出 corpus audit、taxonomy report、screening summary、full eval main table 和 paper outline。

## 6. 风险

| 风险 | 影响 | 缓解 |
|---|---|---|
| 与 Less Is More 重复 | 论文贡献变弱 | 把 corpus 和 taxonomy 作为核心贡献 |
| 后视镜泄漏 | 结论不可发表 | released subsets 统一标注后赛事实证，不用于 prompt selection reward |
| 公开 prompt 不足 | corpus 不够支撑统计 | 允许结构级编码，不强行收录不可合法存储原文 |
| API 成本过高 | 实验无法完成 | 严格 screening 到 shortlist |
| provider 混杂 | 结论不可解释 | run_config 记录 provider route、model、temperature、token cap |
| Stage2 分散主线 | Stage1 论文停滞 | Stage2 仅跟踪规则和资产映射 |

## 7. Go / No-Go 判断

Go，但采用窄启动：

- Phase 0 到 Phase 2 只做目录、schema、corpus、taxonomy。
- Phase 3 之后再决定 API 预算。
- 任何新方法都必须通过 `docs/06_eval_protocol.md` 的阶段化评测纪律。

