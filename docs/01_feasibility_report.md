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

T06 review 判断：

- `docs/review/T06_corpus_audit_public_private_boundary_review.md` verdict 为 `PASS`。
- public/private asset boundary 已把 9 条 text-ready local records、1 条 metadata-only GitHub record、1 条 structure-only Contributor Network record 的下游使用规则写清。
- `corpus_v1.jsonl` 已被明确为 T07/T10 的 authoritative snapshot，metadata-only / structure-only 记录不会误入 eval。

Milestone 1 review 判断：

- `docs/review/M1_review.md` gate 为 `Conditional`。
- 当前 Milestone 1 功能目标已完成：candidate register、provenance cleaning、corpus v1、duplicate report、missing metadata report、boundary note 均已落地并通过 task review。
- `validate-layout`、manifest JSON 和 `corpus_v1.jsonl` 解析在当前仓库可通过，但 clean-environment reproducibility 仍是部分成立，因为外部 mirror/import 故意未做、taxonomy/eval 产物尚不存在。

进入 Milestone 2 的前置条件已满足，但必须保留三个现实约束：

- T07 只能对 9 条 text-ready local records 做 full-text coding。
- `prompt_tokens_est` 仍需在 T07 中补足或给出 reviewable 估算规则。
- GitHub MIT source mirror decision 与 Contributor Network stable URL 仍是 deferred provenance work，不应偷渡进 taxonomy 或 screening。

T07 review 判断：

- `docs/review/T07_manual_taxonomy_coding_v1_review.md` verdict 为 `PASS`。
- 第一批 9 条 text-ready local records 的 manual taxonomy 已落地，`prompt_features_v1.jsonl` 可作为 extractor skeleton 的人工基线。
- `compression_style` 与 `ce_search_depth` 已从长期 deferred 状态转为已编码字段。

T07 review 非阻塞事项处理：

- token estimate 公式文档 `floor` vs `round` 不一致：deferred 到 T08 收口。
- 低方差字段对 extractor/statistical use 的影响：accepted as known limitation；T08/T09 继续控制，不在当前阶段删除字段。
- P1.2.3 bucket boundary sensitivity：accepted；保留边界注释，不在当前阶段强行改 bucket 规则。

T08 review 判断：

- `docs/review/T08_prompt_feature_extractor_skeleton_review.md` verdict 为 `PASS`。
- 已建立 skeleton extractor、CLI 入口与 focused tests，足以支撑 T09 自审和后续 screening 准备。
- token estimate 口径已经统一为 `round(bytes/4)`，T07 留下的文档漂移已解决。

T08 review 非阻塞事项处理：

- P2.0.2 `counterexample_requirement` 的 manual vs extractor 分歧：deferred 到 T09 adjudication。
- `rule_or_heuristic_block` 的 saturated/extended 区分依赖 `override` 关键词：deferred 到 T09/后续 corpus expansion 复核。
- 低方差字段与 extractor-stability vs manual-alignment 的解释边界：deferred 到 T09 明确写成自审结论。

T09 review 判断：

- `docs/review/T09_taxonomy_self_audit_and_conflict_resolution_review.md` verdict 为 `PASS`。
- T09 已完成自审与冲突裁决，唯一数据修正是 P2.0.2 `counterexample_requirement: optional -> absent`。
- 自审后 7 个 rule-ized 字段在 9 条 prompt 上达到 63/63 一致；manual coding 与 extractor 的关系被明确收口为“manual authoritative, extractor supporting cross-check”。

T09 review warning 处理：

- `.claude/settings.json` 工具权限噪音：accepted，不纳入研究提交。
- 低方差字段在 `self_audit_v1.md` 与 `conflict_resolution_v1.md` 的分组口径不完全一致：deferred 到后续文档 hygiene 或 screening 总结阶段统一，不阻塞 T10。
- `self_audit_v1.md` 末尾 “Recommendations for T09 Adjudication Input” 标题语气仍像预审建议：deferred，后续如开文档润色任务再清。

进入 Milestone 3 的前置条件现在成立，但仍保留三个执行约束：

- T10 只能使用 9 条 text-ready local records 作为 screening 候选池。
- T10/T19 不得把 10 个低方差字段作为独立统计变量。
- screening matrix 必须以 T09 的 field usage classification 为准，manual coding 为权威引用，extractor 只做交叉验证。
## Captain Status Update (2026-05-18)

- Feasibility remains confirmed for the Stage1 research line.
- The Stage A screening design gate is now review-backed through T10.
- The next critical-path task is `T11_run_screening_on_selected_prompt_candidates`.
