# Risks and Open Questions

## Captain Update (2026-05-23, T12 Review)

- `T12_rerun_screening_with_alternate_low_cost_model` has been accepted as `PASS_WITH_WARNINGS`.
- T12 is complete, but it confirms the zero-survivor Stage A failure only across two DeepSeek models, not across providers.
- The Current Unique Task is now `T12b_run_screening_on_non_deepseek_provider`.
- Deferred T12 review warning `N1` is recorded below as a live risk.

## Captain Update (2026-05-18, T11 Review)

- `T11_run_screening_on_selected_prompt_candidates` has been accepted as `PASS_WITH_WARNINGS`.
- T11 is complete, but it produced a zero-survivor screening failure on `deepseek / deepseek-chat`.
- The Current Unique Task is now `T12_rerun_screening_with_alternate_low_cost_model`.
- Deferred T11 review warnings and the new model-specific screening-collapse risk are recorded below.

## T11 Follow-Ups

### R25: DeepSeek screening collapse blocks shortlist formation

Source:
- T11 execution result
- T11 review accepted by Captain

Risk:
- Two reviewed Stage A runs on DeepSeek routes now produced zero surviving prompts.
- P0 collapsed on parse success in both runs, and all 8 strict prompts collapsed on the all-false gate in both runs.
- Under the current frozen T10 shortlist rules, Milestone 3 cannot exit and downstream prompt selection remains blocked.

Mitigation:
- Do not write a shortlist-facing summary or advance to recomputed benchmark selection yet.
- Attempt one genuine non-DeepSeek Stage A rerun with all non-model settings frozen.
- If a non-DeepSeek route is not locally usable, escalate to a Captain redesign decision rather than silently relaxing thresholds.
- Preserve the two DeepSeek results as valid model-bias findings even if they do not support shortlist formation.

### R26: Screening metric naming drifts between raw artifacts and screening-facing reports

Source:
- T11 review `N1`
- T11 review `N3`

Risk:
- Raw `summary.json` artifacts expose `true_accuracy` / `false_accuracy`, while screening manifests and review logic use `true_recall` / `false_recall`.
- The values are semantically aligned here, but the naming drift can confuse downstream reporting and any future automation that expects one canonical metric key.

Mitigation:
- Treat the T11 manifest mapping as correct for current governance use.
- A later tooling/doc-hygiene task should add explicit alias wording or schema normalization so raw artifacts and screening summaries use one stable vocabulary.

### R27: Cross-provider generality is still unresolved after T12

Source:
- T12 review `N1`

Risk:
- T11 used `deepseek-chat` and T12 used `deepseek-v4-flash`, but both reviewed runs still used the DeepSeek provider.
- The near-identical all-false behavior may therefore be provider-specific rather than universal to Stage A or to the prompts themselves.
- If we redesign shortlist rules before obtaining one true cross-provider contrast, we risk overfitting protocol changes to one provider family.

Mitigation:
- Run one reviewed non-DeepSeek Stage A probe if a locally usable route exists.
- If no such route is available, document that limit explicitly and make any later protocol redesign conditional on that evidence gap.

## Captain Update (2026-05-18)

- T10 review verdict `PASS` has been accepted by Captain.
- `T10_build_screening_evaluation_matrix` is complete.
- Current Unique Task is now `T11_run_screening_on_selected_prompt_candidates`.
- Deferred review warnings from T10 are recorded below as doc-consistency / reporting-hygiene risks so they are not lost before T12.

## T10 Deferred Review Follow-Ups

### R22: Screening matrix wording may drift from authoritative prompt feature counts

Source:
- T10 review `N1`

Risk:
- `reports/research/screening/screening_matrix_v1.md` Section 8 distribution wording may not exactly match `data/interim/prompt_corpus/prompt_features_v1.jsonl`.
- This is not a screening-design blocker, but it can create reporting ambiguity in later summary writing.

Mitigation:
- Treat `prompt_features_v1.jsonl` as authoritative for any count/distribution claim.
- Clean the wording during later reporting/doc-hygiene work before paper-facing summaries are finalized.

### R23: Candidate registry narrative may drift from authoritative prompt feature counts

Source:
- T10 review `N2`

Risk:
- `reports/research/screening/screening_candidate_registry_v1.md` contains wording that may be inconsistent with the authoritative coded feature file.
- This can confuse later readers about why candidate coverage was selected.

Mitigation:
- Do not change candidate membership during T11.
- Reconcile narrative wording against `prompt_features_v1.jsonl` in a later reporting/doc-hygiene task.

### R24: Indirect self-audit references reduce report traceability

Source:
- T10 review `N4`

Risk:
- Some wording in `screening_matrix_v1.md` references prior self-audit/conflict-resolution evidence too indirectly.
- This is a traceability and readability issue, not an execution blocker.

Mitigation:
- Later reporting/doc-hygiene work should replace indirect phrases with direct citations or direct statements.
- T11 should proceed without redesigning T10 artifacts.

日期：2026-05-17

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

Status:

- T04 已采用 `.gitignore` 窄 allowlist，风险降级为 monitor。

### R14: `direct_recompute` 与 `text_ready` 语义混淆

信号：

- Manifest 中 `direct_recompute_count` 包含已许可但尚未本地镜像的 external source。
- 下游 worker 误以为所有 direct-recompute candidates 都有本地 prompt text 和 hash。

应对：

- T05 manifest 必须拆分 `eligible_count`、`text_ready_count`、`mirrored_external_count`。
- eval 只能使用 text-ready 且 hash 覆盖的 prompt。

Status:

- T05 已拆分 `eligible_count=10`、`text_ready_count=9`、`mirrored_external_count=0`，风险降级为 monitor。
- T06 已把该边界写入 public/private asset boundary，风险降级为 monitor。

### R15: 外部 provenance anchor 不稳定

信号：

- Contributor Network 只用 LinkedIn post 作为 host-level anchor。
- source URL 可能失效或不能指向具体 prompt。

应对：

- T05/T06 尝试寻找稳定 first-party URL。
- 未找到前保持 structure-only，不进入 direct recompute。

Status:

- T06 未解除该风险；Contributor Network 仍只有 host-level provenance。
- 继续 deferred 到后续 provenance/import 任务或论文 limitation。

### R16: `corpus_v1` 与 `candidate_register_v0` schema drift

信号：

- 下游 worker 从 `candidate_register_v0.jsonl` 读取旧字段，而不是从 `corpus_v1.jsonl` 读取 `text_ready`、`eligible_for_recompute` 和 `corpus_inclusion_status`。
- 任务报告把 candidate register 当成 eval-ready corpus。

应对：

- T06 boundary note 必须声明 `corpus_v1.jsonl` 是 authoritative corpus snapshot。
- T07/T10 任务包必须把 `corpus_v1.jsonl` 列为输入，而不是直接从 candidate register 决定 eval eligibility。

Status:

- T06 已把 `corpus_v1.jsonl` 写成 authoritative snapshot。
- T07/T10 仍需在任务包和 review 中持续执行业务约束，风险降级为 monitor。

### R17: Missing metadata report verbosity hides actionable external gaps

信号：

- 9 条本地记录缺 `source_url` 的 info 级提示淹没了 2 条外部记录缺 hash/path 的 actionable issue。

应对：

- T06 corpus audit narrative 中聚合本地 source_url policy-exempt 缺失。
- 单独列出 GitHub metadata-only 和 Contributor Network structure-only 两个 actionable external gaps。

Status:

- T06 已完成 narrative 聚合和 actionable gap 拆分，风险降级为 monitor。

### R18: Milestone 1 clean-environment reproducibility 被高估

信号：

- 文档把当前 Phase 1 状态写成“可从干净环境完整重建 public corpus”。
- 忽略 GitHub metadata-only 未镜像、Contributor Network 未解析 prompt-level URL 的事实。

应对：

- Milestone 1 review 明确保持 `Conditional`，而不是 `Allow`。
- T07/T10/T21 继续把当前状态描述为“review-backed local research snapshot”，不是外部 source 全量可重建包。

### R19: token estimate 口径漂移

信号：

- taxonomy report 写 `floor(prompt_bytes / 4)`，而实际回填数据使用 `round(prompt_bytes / 4)`。
- 下游 extractor、screening 或 paper draft 继承了不一致的口径。

应对：

- T08 统一 token estimate 文档与实现口径。
- 在统一前，长度相关结论只允许写成 heuristic，不允许写成精确 tokenizer count。

Status:

- T08 已统一为 `round(bytes/4)`，风险降级为 monitor。

### R20: 低方差 taxonomy 字段被误当成高信息特征

信号：

- `ce_search_depth`、`finite_model_search_hint`、`examples_block`、`identity_or_invariant_guidance` 等字段在当前 9 条样本上几乎无方差。
- T08/T10/T19 把这些字段直接当作重要建模信号。

应对：

- T08 extractor note 和 T09 self-audit 必须显式列出低方差字段。
- 统计分析前先检查字段方差和可解释性，不让低方差字段主导结论。

Status:

- T09 已明确 10 个低方差字段“保留 schema、排除统计模型、仅作说明性标签”的策略。
- 风险从未识别设计风险降级为执行风险 monitor；T10/T19 仍需在 matrix 与 analysis 中持续遵守。

### R21: manual taxonomy 与 extractor 结果的局部分歧被忽略

信号：

- 已知 extractor 与 manual coding 至少在 P2.0.2 `counterexample_requirement` 上不一致。
- T10/T19 直接消费 extractor 输出，却没有先做 adjudication。

应对：

- T09 必须给出 manual vs extractor mismatch 表和 adjudication rule。
- 在 T09 之前，不把 extractor 输出写成 authoritative feature truth。

Status:

- T09 已完成 P2.0.2 `counterexample_requirement` adjudication，并把 authoritative 值收敛为 `absent`。
- 当前风险降级为 monitor：后续若 corpus 扩展或 extractor 覆盖范围扩大，需要重新审视新的 mismatch。

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
13. `data/interim/prompt_corpus/` 和 `data/external/prompt_corpus/` 应使用 `.gitignore` allowlist 还是 `git add -f` 管理？已在 T04 选择 `.gitignore` narrow allowlist，后续 monitor。
14. public placeholders 在 T04 后如果仍无 license confirmation，应降级为 structure-only 还是 excluded？
15. 是否在 T05 引入 tokenizer，还是继续使用 byte size 到 Phase 2？T05 未引入 tokenizer；T07 前需要重新决定。
16. GitHub MIT source 是否在 T05 镜像具体 prompt 文件，还是只记录 reproducible URL 到 T06？T05 未镜像，保持 metadata-only；未来若需要 external text-ready coverage，单开任务。
17. `raw_index.example.jsonl` 是否应完全改成 T04 schema，还是保留旧 corpus schema 示例？T05 已改成 T04 schema。
18. T06 是否能找到 Contributor Network 的稳定 prompt-level URL，若找不到是否维持 structure-only 到 paper limitation？
19. T07 对 `prompt_tokens_est` 采用什么 reviewable 估算口径，才能既支持 length bucket 又不伪称 tokenizer 精度？
20. T08 应统一使用 `round(bytes/4)` 还是改回 `floor(bytes/4)`，以及是否需要保留 bucket boundary note 解释历史差异？
21. T09 两份文档里 low-variance / moderate-variance 的分组口径是否需要在后续 doc hygiene 中统一成一套固定写法？

## Deferred Items

- Stage2 Lean solver 预研。
- 大规模 prompt evolution。
- 大规模模型微调。
- dashboard 或 prompt lint 产品化。
- T01 review 非阻塞事项：`storage_policy` typo、taxonomy mapping、`compression_style`、`ce_search_depth`、正式 eval `repeats` schema。
- T02 review 非阻塞事项：`outline.md` 绝对路径链接、C7 主贡献边界、`unsupported_do_not_claim` 示例缺失。
- T03 review 非阻塞事项：prompt corpus data files git tracking、`prompt_tokens_est`、external placeholder provenance、`configs/research` typo cleanup。
- T04 review 非阻塞事项：eligible vs text-ready count split、LinkedIn provenance fragility、more external candidates、raw index example schema alignment。
- T05 review 非阻塞事项：candidate register/corpus v1 schema drift、missing metadata report verbosity、`prompt_tokens_est`、GitHub MIT mirror decision、Contributor Network stable URL。
- T06 review 非阻塞事项：handoff `eval-ready now` vs manifest `eligible_count` wording distinction、manifest `records_present` includes report path、`prompt_tokens_est`、GitHub MIT mirror decision、Contributor Network stable URL。
- T07 review 非阻塞事项：token estimate formula wording mismatch、low-variance taxonomy fields、P1.2.3 bucket boundary sensitivity。
- T08 review 非阻塞事项：P2.0.2 `counterexample_requirement` mismatch、`rule_or_heuristic_block` fragile heuristic、low-variance fields、extractor-stability vs manual-alignment boundary、`.claude/settings.json` tool-permission noise。
- T09 review 非阻塞事项：low-variance field grouping wording drift across T09 docs、`self_audit_v1.md` Section 7 标题语气仍像预审输入、`.claude/settings.json` tool-permission noise。
