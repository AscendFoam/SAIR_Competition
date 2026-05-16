# Feasibility Report

日期：2026-05-12

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

## 8. Phase 0 可行性进展

`T01_research_scaffold` 已经通过 review，说明 Phase 0 的仓库脚手架可行：

- 研究目录、seed config、manifest 和 outline 已创建。
- JSON/YAML scaffold 可解析。
- 没有越界修改 `src/`、`tests/`、prompt wording 或历史 artifacts。

Phase 0 进展：

1. `T01`: research scaffold 已通过 review。
2. `T02`: paper outline、contribution list、claim/evidence/status matrix 已通过 review。
3. `T03`: candidate register v0 和 provenance rules 已通过 review。

Phase 0 exit criteria 基本满足：

- 研究目录和 seed config 已创建。
- paper claim/evidence guardrail 已建立。
- 第一批 `8-12` prompt 候选目标已达到，当前为 11 个候选。
- normalized corpus 仍未完成，进入 Phase 1 后处理。

Review 非阻塞事项会在后续任务吸收：taxonomy 字段映射在 T07 前完成，`repeats` 类型和 source storage typo 在后续 config 收敛时清理。

T02 review 非阻塞事项处理：

- `unsupported_do_not_claim` 未实际使用：deferred 到 T03/T21 前，在 rejected/unsupported claim 区域补充或在论文草稿阶段检查。
- C7 更像内部项目 justification：accepted，保留为 setup/motivation，不作为论文主贡献。
- `outline.md` 使用绝对 Windows 链接：deferred 到 T03 的 hygiene fix。

T03 review 非阻塞事项处理：

- `data/` prompt corpus 文件被 `.gitignore` 排除：deferred 到 T04 前置治理决策。
- `prompt_tokens_est` 全为 0：accepted for v0，deferred 到 taxonomy/corpus normalization 任务。
- external placeholders 缺少 URL、author、license：deferred 到 T04 主任务。
- `configs/research/corpus_sources.example.json` 的 typo 仍存在：accepted because T03 forbidden scope 不允许改，后续专门 config hygiene 时处理。

T04 review 非阻塞事项处理：

- `direct_recompute_count` 混合 eligibility 与 text-ready 语义：deferred 到 T05，必须拆成 eligible/text-ready。
- Contributor Network provenance 依赖 LinkedIn post：accepted as fragile host-level provenance，deferred 到 T05/T06 寻找稳定一手来源。
- 外部候选数量仍少：deferred 到 T05/T06，主动补 GitHub/paper candidates。
- `raw_index.example.jsonl` 与 `raw_index.jsonl` schema 不一致：deferred 到 T05。

T05 review 判断：

- `docs/review/T05_normalize_prompt_corpus_v1_review.md` verdict 为 `PASS`。
- `corpus_v1` 已满足 Phase 1 最小 corpus snapshot：11 条记录，9 条 text-ready，10 条 eligible，1 条 metadata-only，1 条 structure-only。
- `direct_recompute_count` 语义混合问题已通过 manifest 中的 `eligible_count` / `text_ready_count` / `mirrored_external_count` 拆分解决。
- `raw_index.example.jsonl` schema misalignment 已解决。

T05 review 非阻塞事项处理：

- `candidate_register_v0.jsonl` 未回填新字段：accepted；后续以下游 `corpus_v1.jsonl` 为 authoritative snapshot。
- missing metadata report 对 9 条本地记录逐条提示 `source_url` 缺失：accepted as verbose but correct；T06 可在 audit narrative 中聚合说明。
- `prompt_tokens_est` 全为 0：deferred 到 T07 前，避免长度分桶误读。
- GitHub MIT source 未镜像：accepted；如需要 external text-ready coverage，后续单开 provenance/import 任务。
- Contributor Network 稳定 prompt-level URL 仍缺：deferred 到 T06 风险说明。
