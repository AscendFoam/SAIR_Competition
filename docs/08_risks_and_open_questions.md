# Risks and Open Questions

日期：2026-05-12

## Active Risks

### R1: 研究退化成比赛复盘

信号：

- 文档主要讨论排名和最高分。
- 图表只展示 leaderboard。
- 没有 taxonomy、统计检验或方法。

应对：

- 每个实验绑定 RQ。
- 每张图必须回答结构、模型或鲁棒性问题。
- paper title 和摘要避免写成 Stage1 summary。

### R2: 与 Less Is More 重复

信号：

- 只复现 prompt 长度和 ceiling。
- 没有 public corpus、taxonomy、provenance 或 post-release robustness。

应对：

- 把 corpus construction 和 prompt feature taxonomy 作为核心贡献。
- 相关工作阶段正式写差异化矩阵。

### R3: 后视镜风险

信号：

- 在 released subsets 上选择或调 prompt。
- 把 released subsets 叙述为私有盲测。

应对：

- 统一标注 `post-release analysis`。
- prompt selection 只使用 screening 和本地固定 split。
- Reviewer 必须审查叙事是否泄漏。

### R4: 公开语料选择偏差

信号：

- 只分析公开 prompt，却推断全部参赛者。
- 社交媒体 self-report 被放进主统计表。

应对：

- source type 分为 official、github、paper、local、social 等。
- 主结论限定在公开可复现语料。
- limitations 明确写选择偏差。

### R5: API 预算失控

信号：

- 太多 prompt 直接进入完整评测。
- repeats 过早增加。

应对：

- 严格执行 Stage A 到 Stage B 到 Stage C。
- 只有 shortlist 进入完整评测。

### R6: Model/provider 混杂

信号：

- 同一模型名不同 route。
- temperature、token cap、reasoning mode 混在同一主表里。

应对：

- `run_config.json` 必须记录 provider route。
- 混杂时分表或降低结论强度。

### R7: Prompt 原文版权和归因

信号：

- 大段转载 public prompt。
- 没有 license、source、hash 或 attribution。

应对：

- corpus 保存来源和 hash。
- 论文只用短摘录、结构标签和 summary。
- 不可合法存储的 prompt 只做结构级编码。

### R8: 方法贡献过弱

信号：

- 只有分析，没有 distilled prompt 方法或 controlled ablation。

应对：

- Phase 5 至少完成 human 或 feature-aware distilled prompt。
- 优先 feature-aware controlled variants。

### R9: 过早投入 Stage2

信号：

- Stage1 paper 尚未闭环，开始写 Lean solver。

应对：

- Stage2 只做规则跟踪和资产映射。
- Phase 7 后再决定是否切换主线。

### R10: 私有资产泄漏

信号：

- 未公开 prompt、API raw outputs、`.env` 或私有数据进入 release manifest。

应对：

- 公开复现包只放可公开 prompt、代码、结构标签和摘要结果。
- raw outputs 单独本地归档。

### R11: Seed taxonomy 与实验计划字段漂移

信号：

- `configs/research/prompt_feature_taxonomy.yaml` 的字段名与 `docs/02_experiment_plan.md` 第 6.2 节无法对应。
- 后续 annotator 不知道 `compression_style`、`ce_search_depth` 等字段是否应标注。

应对：

- T02 在 paper claim/evidence matrix 中记录 taxonomy mapping 是未完成前置条件。
- T07 前写明 experiment-plan feature 到 YAML field 的 mapping。
- 若字段保留差异，必须在 taxonomy report 中解释。

### R12: Paper contribution 与内部项目 justification 混淆

信号：

- `C7` 这类“工程资产足以支撑后续科研”的内容被写成论文主贡献。
- contribution list 没有任何 rejected 或 unsupported claim，导致 guardrail 只剩形式。

应对：

- C7 只作为 setup/motivation，不进入最终 paper main contributions。
- T03 或 T21 前补一个 `unsupported_do_not_claim` 或 rejected-claim 区域。
- 论文草稿阶段检查 contribution list 与 claim evidence matrix 是否一致。

### R13: Prompt corpus governance files 被 gitignore 排除

信号：

- `data/interim/prompt_corpus/*` 和 `data/external/prompt_corpus/*` 在本地存在，但普通 `git add` 不会纳入提交。
- 后续 worker 以为 corpus register 已版本化，但切换环境后文件丢失。

应对：

- T04 前决定 force-add 具体 governance files，或调整 `.gitignore` allowlist。
- 不允许把 raw private data 一起放开，只 allowlist prompt corpus governance files。
- 提交前检查 `git status --ignored` 或明确列出需 `git add -f` 的路径。

## Open Questions

1. 官方三模型 route 是否仍可复现，若不可复现，采用哪些近似 provider 和模型？
2. public contributor prompt 的可合法存储范围是什么，只存 hash 和 feature summary 是否足够？
3. 第一轮 `8-12` 个 prompt 候选中，哪些 public prompt 可进入直接复算？
4. token 估算是否需要引入 tokenizer，还是 Phase 1 先用 byte size 和 rough estimate？
5. prompt feature extractor 是先规则化，还是先保留人工 JSONL 标注？
6. full eval 的 repeats 预算是多少？
7. paper 目标先按 workshop、TMLR 还是技术报告组织？
8. 是否需要同步到 `qcy_project_hub`，以及当前证据等级应记为 L2 还是 L3 候选？
9. `repeats` 在正式 eval config 中应使用整数、整数列表，还是单独 schema 字段？
10. `compression_style` 与 `ce_search_depth` 是否进入 TAX_V1，还是只进入人工 audit note？
11. T03 candidate register 中，哪些本地 prompt 可直接进入 recompute，哪些只能作为 historical/local contrast？
12. T02 的 `unsupported_do_not_claim` 状态是通过新增 rejected claim 解决，还是在 T21 paper draft 时解决？
13. `data/interim/prompt_corpus/` 和 `data/external/prompt_corpus/` 应使用 `.gitignore` allowlist 还是 `git add -f` 管理？
14. public placeholders 在 T04 后如果仍无 license confirmation，应降级为 structure-only 还是 excluded？
15. 是否在 T05 引入 tokenizer，还是继续使用 byte size 到 Phase 2？

## Deferred Items

- Stage2 Lean solver 预研。
- 大规模 prompt evolution。
- 大规模模型微调。
- dashboard 或 prompt lint 产品化。
- T01 review 非阻塞事项：`storage_policy` typo、taxonomy mapping、`compression_style`、`ce_search_depth`、正式 eval `repeats` schema。
- T02 review 非阻塞事项：`outline.md` 绝对路径链接、C7 主贡献边界、`unsupported_do_not_claim` 示例缺失。
- T03 review 非阻塞事项：prompt corpus data files git tracking、`prompt_tokens_est`、external placeholder provenance、`configs/research` typo cleanup。
