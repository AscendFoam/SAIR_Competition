# SAIR Stage1 数学蒸馏科研工程化实验方案

截至日期：2026-05-11

## 1. 文档定位

本文档是 `docs/SAIR代数推理竞赛工程化实验计划.md` 的后续科研版工程方案，用于指导 SAIR `Mathematics Distillation Challenge - Equational Theories` Stage1 收官之后的继续研究。

旧方案的核心目标是完成 Stage1 参赛提交；本方案的核心目标已经切换为：

> 把 Stage1 当成一个公开、可复现、可统计分析的 prompt textual distillation 自然实验平台，研究 prompt 作为“文本蒸馏载体”时的结构、复杂度、模块顺序、内容来源、模型依赖性与跨分布鲁棒性。

因此，接下来一段时间不应把主线理解为“继续改 prompt 刷榜”，也不应急着全面转向 Stage2 solver。当前主线仍然是 Stage1 后赛事实证科研，重点产出应是语料、taxonomy、评测、统计结论、小方法和论文雏形。Stage2 只作为远期衔接和低频规则跟踪，不作为当前主要工程投入。

本文档主要基于以下材料整理：

- `docs/SAIR代数推理竞赛工程化实验计划.md`
- `docs/项目工作历程与阶段性成果总结.md`
- `docs/Stage1结果调研报告.md`
- `docs/Stage1科研继续推进调研报告.docx`

其中研究方向与优先级以 `Stage1科研继续推进调研报告.docx` 为主；项目状态、已有代码资产与历史实验结论以 `项目工作历程与阶段性成果总结.md` 为准。

---

## 2. 总体判断与方向修正

### 2.1 当前项目状态

Stage1 参赛提交已经完成收口。最终提交版本为：

- `prompts/complete/P1.2.5_minimal_rule_missing_hard_composition.txt`
- release id: `RC1_P1_2_5_official_playground_20260420`
- size: `4059` bytes
- SHA256: `44c882227e88906ed393f4aa1a0dfdbbf17862d683c58fc7029054aa062000b5`

项目已经形成以下可复用工程资产：

- 官方公开数据标准化与固定切分链路
- `smoke/dev/holdout/audit` 数据拆分
- baseline runner 与 complete prompt API eval runner
- verdict parser、metrics、candidate comparison 工具
- `family_tagger`
- `offline rule assets`
- `canonical axes`
- `review set`
- `positive signal candidate` 准备链路
- `P1_2_3` 与 `P1_2_5` 的风险画像
- 官方 playground 小样本迁移记录

这些资产不是研究结束后的“附属品”，而是后续科研工作的起点。

### 2.2 必须避免的错误方向

后续工作不应继续沿用赛前心态。以下方向暂时不作为主线：

- 继续大规模手写新 prompt 分支
- 在已公开 final evaluation subsets 上包装“赛时泛化能力”
- 只写 Stage1 leaderboard 复盘
- 只做 qualitative prompt 案例摘录
- 直接跳到 Stage2 Lean solver 而放弃 Stage1 蒸馏研究
- 在没有稳定 GPU、训练脚本和清晰对照的情况下强行加入 7B fine-tuning
- 把 `P1_2_5` 的 wording 当作最终知识来源，而忽略其 false leakage 风险

当前最重要的方向修正是：

> 从“比赛提交优化”转向“公开 prompt 语料驱动的 textual distillation 与鲁棒性研究”。

### 2.3 新研究 framing

建议把研究问题定义为：

> 基于 SAIR Stage1 官方与社区公开数据，研究 prompt 作为文本蒸馏载体时，其结构复杂度、模块顺序、内容来源与目标模型、评测分布之间的关系；并提出一种提高跨模型与跨分布鲁棒性的 prompt-distillation 方法。

这个 framing 有三个优点：

1. 避免和已有 `Less Is More` 工作重复为“又跑了一批 prompt 变体”。
2. 把本项目已有工程链路转化为可发表的实验基础设施。
3. 允许同时产出论文、复现包、dashboard 和求职展示项目。

---

## 3. 科研目标、非目标与成功标准

### 3.1 科研目标

本阶段的核心目标不是提交一个更高分的 Stage1 prompt，而是产出一套可复现研究结果：

1. 构建一个带 provenance 的公开 prompt corpus。
2. 建立 Stage1 prompt feature taxonomy。
3. 用统一评测脚本复算代表性 prompt 的跨模型、跨 split、跨 released subset 表现。
4. 量化 prompt 结构、长度、模块顺序、输出契约与性能/鲁棒性的关系。
5. 提出并验证一个小而清晰的 textual distillation 方法。
6. 形成可投稿的经验研究论文初稿。
7. 保留后续 Stage2 或神经符号方法可继承的结构资产。

### 3.2 工程目标

工程上要把现有竞赛仓库升级为“科研实验仓库”：

- 数据、prompt corpus、taxonomy、实验结果、统计分析和论文图表分层存放。
- 所有实验都有版本、配置、输入文件、输出文件和摘要报告。
- 所有 prompt 都有来源、hash、许可/归因说明和结构标签。
- 所有结论都能追溯到固定数据版本和固定评测配置。
- 所有后赛事实验明确标注时间性，避免数据泄漏式叙事。

### 3.3 非目标

近期不追求：

- Stage2 正式 solver 主线开发。
- Lean 4 证明搜索系统。
- 大规模模型微调。
- 自动 prompt evolution 的大规模搜索。
- 覆盖所有社交媒体自述结果。
- 重新制造一个数学 benchmark。
- 把公开 final evaluation subsets 当作私有盲测集使用。

### 3.4 成功标准

#### 必须达到

- 形成可复现的 prompt corpus schema。
- 至少整理 `8-12` 个代表性公开/本地 prompt 候选。
- 完成 prompt taxonomy v1。
- 能用统一评测入口跑通小样本筛选实验。
- 实验报告包含 accuracy、strict F1、parse success rate、True/False recall、cost/time、repeat consistency 或等价稳定性指标。
- released final evaluation subsets 的使用在报告中明确标注为后赛事实证分析。

#### 期望达到

- 在 `3-5` 个代表性 prompt 上完成官方三模型或近似官方配置的完整评测。
- 形成一组可统计支持的结构结论，例如长度-性能非单调性、trivial-first/CE-first 顺序效应、strict formatting 对 parse rate 的影响。
- 提出一个 distilled prompt 方法，在 robustness gap 或 parse stability 上优于手工 baseline。
- 形成 workshop/TMLR 风格论文初稿。

#### 冲刺目标

- 建立轻量 dashboard 或 notebook 报告系统。
- 实现 prompt lint / robustness analyzer 原型。
- 把 corpus、taxonomy 和评测结果整理成可公开的复现包。
- 在方法足够清楚时，准备 AAAI/NeurIPS E&D 风格升级版。

---

## 4. 研究假设与核心问题

### 4.1 主假设

本项目要验证的不是“某个 prompt 是否最高分”，而是以下更一般的问题：

1. Prompt 作为文本蒸馏载体，存在可量化的结构-性能关系。
2. 更长、更复杂的 prompt 不一定更好，且可能导致认知过载、parse instability 或模型特异脆弱性。
3. 模块顺序会影响模型注意力和最终 verdict，尤其是 `trivial-first` 与 `counterexample-first` 的差异。
4. 强 false-filter 与 true-recall 之间存在跨分布 tradeoff。
5. 对公开数据局部最优的 prompt，可能在 released evaluation subsets 上出现明显 robustness gap。
6. 将公开 prompt 共性与错误模式做结构化蒸馏，可能比继续堆 wording 更稳。

### 4.2 研究问题

建议把论文和工程实验围绕以下 RQ 展开：

- `RQ1`: Stage1 公开 prompt 生态中有哪些可重复出现的结构模块？
- `RQ2`: Prompt 长度、模块顺序、输出契约、counterexample 使用方式与性能指标有什么统计关系？
- `RQ3`: 哪些 prompt 结构在模型间迁移稳定，哪些结构具有明显 model-specific bias？
- `RQ4`: public split 到 released evaluation subsets 的掉点主要来自哪些结构与分布偏移？
- `RQ5`: 基于公开 prompt corpus 和错误模式的 textual distillation，能否降低 robustness gap 或提升 parse/recall 稳定性？
- `RQ6`: Stage1 文本蒸馏的边界在哪里，它与传统 model distillation、CoT distillation、feedback-driven distillation 有什么关系？

### 4.3 应避免的伪问题

以下问题不够好，不建议作为论文主问题：

- 谁在 Stage1 排名最高？
- 哪个 prompt 案例最有趣？
- 我们能不能把本地 smoke 再提高 2 个点？
- 是否能用更长 cheatsheet 记住更多规则？
- 能否把 `P1_2_5` 再改一版？

这些问题可以作为背景或附录，但不能承担主贡献。

---

## 5. 数据资产与语料工程

### 5.1 数据源分级

后续数据源按可信度分为四层。

#### Tier 1：官方公开资源

优先级最高，作为论文主分析基础：

- 官方 Stage1 overview / evaluation setup
- 官方 selected problems
- 官方 benchmark dataset
- 官方 judge repository
- released final evaluation subsets
- 官方可索引 Contributor Network 页面

#### Tier 2：公开 GitHub 复现仓库

可进入主语料，但必须记录 provenance：

- 公开 prompt 文件
- 公开实验脚本
- 公开结果表
- 公开 commit hash
- license / terms note

#### Tier 3：公开论文与报告

用于 taxonomy、对照实验与动机：

- `Less Is More: Cognitive Load and the Single-Prompt Ceiling in LLM Mathematical Reasoning`
- 公开 Stage1 分析报告
- 相关 textual distillation / CoT distillation / prompt evolution 文献

#### Tier 4：社交媒体与自述结果

只作为补充案例，不作为主统计结论依据：

- X / Mastodon / Hacker News / Discord / Zulip 片段
- 个人博客
- 未提供 prompt 全文或评测配置的结果截图

### 5.2 Corpus schema

建议新增 `data/external/prompt_corpus/` 和 `data/interim/prompt_corpus/`，并使用如下 schema：

```json
{
  "prompt_id": "public_an45c_reconstructed_v1",
  "source_type": "official|contributor_network|github|paper|local|social",
  "source_url": "",
  "source_ref": "",
  "author_or_team": "",
  "timestamp": "",
  "license_or_tos_note": "",
  "prompt_text_path": "",
  "prompt_sha256": "",
  "prompt_bytes": 0,
  "prompt_tokens_est": 0,
  "complete_or_cheatsheet": "complete_prompt|cheatsheet|template|unknown",
  "reported_model": "",
  "reported_split": "",
  "reported_metrics": {},
  "official_or_self_reported": "official|self_reported|recomputed|unknown",
  "builds_on_public_work": [],
  "visibility_note": "",
  "post_release_use_allowed": true
}
```

### 5.3 Prompt text 存储原则

公开 prompt 文本可以在本地研究仓库存储，但必须遵守以下原则：

- 不把未公开的竞赛私有 prompt 混入公开 corpus。
- 每份 prompt 保留原始来源、hash、抓取日期。
- 论文正文不大段转载 prompt 全文，只使用短摘录、结构标签和 feature summary。
- 任何由本项目改写的 distilled prompt 都记录依赖来源。
- 对 Contributor Network 来源保留 contributor attribution。

### 5.4 推荐目录调整

建议新增以下目录：

```text
SAIR_Competition/
├─ data/
│  ├─ external/
│  │  └─ prompt_corpus/
│  │     ├─ raw_index.jsonl
│  │     └─ raw_prompts/
│  └─ interim/
│     └─ prompt_corpus/
│        ├─ corpus_v1.jsonl
│        ├─ prompt_features_v1.jsonl
│        └─ prompt_corpus_manifest.json
├─ configs/
│  ├─ research/
│  │  ├─ corpus_sources.example.json
│  │  ├─ prompt_feature_taxonomy.yaml
│  │  └─ evaluation_matrix.example.json
├─ reports/
│  ├─ research/
│  │  ├─ corpus_audit/
│  │  ├─ taxonomy/
│  │  ├─ statistical_analysis/
│  │  └─ figures/
│  └─ paper/
│     ├─ outline.md
│     ├─ related_work.md
│     └─ draft.md
└─ artifacts/
   └─ research_runs/
      ├─ screening/
      ├─ official_model_eval/
      └─ ablations/
```

现有 `reports/experiments/` 仍保留用于具体实验；`reports/research/` 用于跨实验综合分析。

---

## 6. Prompt Feature Taxonomy

### 6.1 Taxonomy 的作用

Taxonomy 是本科研阶段的核心资产。没有 taxonomy，项目只能做“案例总结”；有了 taxonomy，才能做统计建模和结构效应分析。

每个 prompt 至少要编码以下类别：

1. 长度与密度
2. 模块组成
3. 模块顺序
4. 输出契约
5. 推理控制方式
6. 反例策略
7. TRUE 证明策略
8. hallucination guardrail
9. examples / demonstrations
10. 与已有 public work 的关系

### 6.2 建议 feature 字段

#### 长度特征

- `prompt_bytes`
- `prompt_tokens_est`
- `near_10kb_cap`
- `length_bucket`: `short / medium / long / near_cap`
- `compression_style`: `natural_language / symbolic / hybrid`

#### 结构模块

- `has_task_framing`
- `has_magma_reset`
- `has_no_hidden_axioms_warning`
- `has_verdict_first_contract`
- `has_strict_final_answer_contract`
- `has_stepwise_checklist`
- `has_decision_tree`
- `has_ce_lookup_or_table`
- `has_trivial_magma_rule`
- `has_false_filters`
- `has_true_positive_rules`
- `has_examples`
- `has_confidence_or_uncertainty_language`

#### 模块顺序

- `first_substantive_module`: `trivial_first / ce_first / format_first / axiom_reset_first / examples_first / other`
- `ce_before_true_rules`
- `true_rules_before_ce`
- `format_contract_position`: `front / middle / end / repeated`
- `guardrail_position`: `front / after_rules / final`

#### 反例策略

- `counterexample_mode`: `none / conceptual / finite_magma_table / lookup / search_instruction`
- `ce_search_depth`: `implicit / shallow / explicit_multi_step`
- `false_default_when_uncertain`
- `true_default_when_no_ce`

#### TRUE 策略

- `true_mode`: `rewrite / substitution / structural_family / trivial_magma / positive_signal / weak_heuristic`
- `has_law_family_rules`
- `has_shared_lhs_rules`
- `has_new_vars_rules`
- `has_target_amplification_rules`
- `has_singleton_collapse_rules`

#### 输出稳定性

- `allows_reasoning_text`
- `requires_single_word_output`
- `requires_final_line`
- `case_contract`: `lowercase / uppercase / either`
- `parse_risk`: `low / medium / high`

### 6.3 标注策略

先采用半人工标注，不急着完全自动化：

1. 对 `8-12` 个候选 prompt 手工标注 taxonomy v0。
2. 基于人工结果写规则化 feature extractor。
3. 用 extractor 生成 taxonomy v1。
4. 人工复核冲突样本。
5. 在论文中报告 inter-annotator 或 self-audit 一致性。

### 6.4 与现有 family tagger 的关系

Prompt taxonomy 和 problem family tagger 是两类不同标签：

- `prompt taxonomy`: 描述 prompt 本身的结构。
- `family_tagger`: 描述题目的代数结构族。

真正有研究价值的是二者交叉：

- 某类 prompt 结构是否特别擅长 `TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR`？
- CE-first prompt 是否在 false-heavy split 上表现更好，但在 true-heavy 子型上漏判？
- strict formatting 是否对所有 problem family 都提升 parse rate？
- `P1_2_5` 的高 true recall 是否集中来自少数结构族？

这部分可以成为论文的亮点。

---

## 7. 评测协议

### 7.1 原则

后续实验必须明确区分三类评测：

1. `screening`: 小样本筛选，用于淘汰明显差的 prompt。
2. `recomputed benchmark`: 统一配置下的复算，用于论文主结果。
3. `post-release analysis`: 在已公开 final evaluation subsets 上做后赛事实证分析。

不能把第三类包装成赛时未知盲测结果。

### 7.2 数据切分

继续保留当前仓库已有切分：

- `smoke`: 快速回归与格式检查。
- `dev`: 主要开发与 taxonomy 交叉分析。
- `holdout`: 本地稳定性检查。
- `audit`: 人工审阅与边界案例。

新增研究使用的公开 released subsets：

- `evaluation_normal`
- `evaluation_hard`
- `evaluation_extra_hard`
- `evaluation_order5`

这些 released subsets 在论文中统一称为 `released final evaluation subsets`，并明确写作后赛事实证分析。

### 7.3 Prompt 候选集合

第一轮建议只选 `8-12` 个 prompt：

1. `P1_2_3_implicit_guardrail_v2`: 本地稳态保守主线。
2. `P1_2_5_minimal_rule_missing_hard_composition`: Stage1 RC1 高召回提交分支。
3. `P2_0_0_official_balanced_strict_v0`: 官方 balanced 原型 strict 适配。
4. `P2_0_1_official_counterexample_first_strict_v0`: CE-first strict 适配。
5. `P2_0_2_official_fast_filters_strict_v0`: fast-filter strict 适配。
6. `AN38` 或可合法复现的 CE-first public prompt。
7. `AN45c` 或可合法复现的 trivial-first public prompt。
8. 无 cheatsheet / minimal prompt baseline。
9. 人工 distilled prompt v0。
10. LLM-assisted distilled prompt v0。
11. feature-aware distilled prompt v0。
12. 可选 public contributor prompt。

说明：上述 `P2_0_*` 是本仓库历史上的 prompt 版本编号，表示官方 archetype strict adaptation 分支，不代表当前工作已经切换到 Stage2 solver 主线。

如果 prompt 原文不可合法存储或复现，则只做结构级编码，不纳入直接复算。

### 7.4 模型与 provider

优先按官方 Stage1 三模型复现：

- `gpt-oss-120b`
- `llama-3-3-70b-instruct`
- `gemma-4-31b-it`

如果官方 route 或 API 条件不可直接复现，则记录替代模型与差异：

- provider name
- model name
- route
- temperature
- seed
- max tokens
- reasoning mode
- timestamp
- judge commit

任何跨 provider 结论都必须注明 provider 差异可能是混杂因素。

### 7.5 三阶段评测设计

#### Stage A：小样本筛选

目标：

- 检查 parse stability。
- 初步观察 true/false tradeoff。
- 过滤明显不值得全量评测的候选。

建议配置：

- prompt 数量：`8-12`
- 数据：`hard1/hard2/hard3` 分层子样本 + 当前 `smoke`
- 模型：先用 `1` 个低成本 proxy 或当前可用 API
- repeats：`1`

进入下一阶段条件：

- parse success rate 接近 `1.0`
- 没有全 true / 全 false 塌缩
- 至少代表一种有研究意义的结构类型

#### Stage B：代表性 prompt 完整评测

目标：

- 形成论文主表。
- 比较结构、模型、split 的稳定性。

建议配置：

- prompt 数量：`3-5`
- 模型：官方三模型或最接近三模型组合
- 数据：released subsets + 本地固定切分
- repeats：`1-3`，根据预算决定

必须输出：

- predictions.jsonl
- raw_outputs.jsonl 或等价缓存
- summary.json
- metrics.csv
- run_config.json
- prompt hash manifest

#### Stage C：消融与鲁棒性

目标：

- 验证结构因素，而不是只报最终分。

建议消融：

- `short / medium / near-cap`
- `trivial-first / CE-first`
- `strict formatting / relaxed formatting`
- `with examples / no examples`
- `false-filter heavy / balanced / true-recall oriented`
- `universal prompt / model-specific prompt`

### 7.6 指标体系

必须包含官方一致指标：

- `accuracy`
- `strict_f1`
- `parse_success_rate`
- `true_recall`
- `false_recall`
- `avg_time_secs`
- `avg_cost_usd`
- `repeat_consistency`

本项目新增指标：

- `prompt_bytes`
- `prompt_tokens_est`
- `balanced_accuracy`
- `robustness_gap`: public/dev 到 released subsets 的掉点
- `model_transfer_gap`: 最优模型与最差模型之间差距
- `format_failure_rate`
- `family_conditional_accuracy`
- `family_conditional_recall`

### 7.7 结论判定纪律

任何 prompt 方法只有在满足以下条件时，才可作为论文方法结论：

- 不只在单一模型提升。
- 不只在单一 split 提升。
- 不以 parse failure 或输出格式异常换取表面分数。
- 不在 released subsets 上调参后宣称盲测泛化。
- 能说明 true/false tradeoff。
- 能报告成本与延迟。

---

## 8. Textual Distillation 方法路线

### 8.1 为什么需要方法而不只是分析

如果项目只做 corpus 和统计分析，可以成为强技术报告或 workshop paper；但若想冲 TMLR 或 AAAI 风格论文，需要至少补一项“小而硬”的方法贡献。

方法不需要复杂，但必须清楚：

- 输入是什么。
- 输出是什么。
- 与 baseline 的差异是什么。
- 为什么可能更稳。
- 用什么评测证明它更稳。

### 8.2 Method Family A：人工 distilled prompt

输入：

- top public prompt 的结构共性
- `P1_2_3` 与 `P1_2_5` 的风险画像
- offline rule assets
- high-priority review axes

过程：

1. 抽取共同模块。
2. 去掉题目级硬编码和过强 false default。
3. 保留 strict output contract。
4. 将规则分为 axiom reset、quick true signals、false filters、decision fallback。
5. 控制长度在 `2-4KB`。

输出：

- `D1.0_human_distilled_balanced.txt`

主要用途：

- 作为研究方法的强可解释 baseline。

### 8.3 Method Family B：LLM-assisted distilled prompt

输入：

- 公开 prompt feature summary
- 常见错误模式
- problem family 标签统计
- 不能直接大段复制的归因约束

过程：

1. 强模型只看结构摘要和短摘录，不直接拼接 prompt 全文。
2. 生成 `3` 个候选 distilled prompt。
3. 用 taxonomy 检查它们的结构差异。
4. 只用 screening split 做初筛。
5. 选 `1` 个进入完整评测。

输出：

- `D1.1_llm_assisted_distilled.txt`

注意：

- 强模型生成的规则必须人工审查。
- 不能让强模型把 released subset 的答案模式写进 prompt。

### 8.4 Method Family C：Feature-aware distilled prompt

这是最适合论文的主方法候选。

核心思想：

> 不追求生成最强 prompt，而是显式控制 prompt feature，只改变一个关键因素，验证结构对鲁棒性的影响。

建议做三组：

1. `trivial-first` vs `CE-first`
2. `strict verdict-first` vs `relaxed reasoning-first`
3. `short balanced` vs `long rule-heavy`

每组只改变目标 feature，其余尽量固定。

输出：

- `D2.0_feature_trivial_first.txt`
- `D2.1_feature_ce_first.txt`
- `D2.2_feature_strict_format.txt`
- `D2.3_feature_relaxed_format.txt`
- `D2.4_feature_short_balanced.txt`
- `D2.5_feature_long_rule_heavy.txt`

论文价值：

- 可以从“哪个 prompt 高”转成“哪个结构因素有效”。

### 8.5 可选 Method Family D：小规模 prompt evolution

不作为第一优先级。只有在 A/B/C 完成后再考虑。

限制：

- 候选数不超过 `20`
- 每轮只在 screening split 上跑
- 不允许把 released subsets 用作 evolution reward
- 最终仍需用 taxonomy 解释演化结果

---

## 9. 统计分析方案

### 9.1 描述统计

先做以下基础图表：

- prompt 长度分布
- feature 频率分布
- 模块顺序分布
- 不同 prompt family 的 true/false recall 分布
- parse success rate 分布
- cost/time 分布

### 9.2 关联分析

建议做：

- prompt length 与 accuracy / robustness gap 的 Spearman correlation
- prompt length 与 parse success 的 Spearman correlation
- LOESS 曲线展示长度-性能非单调关系
- `trivial-first` 与 `CE-first` 的 balanced accuracy 差异
- strict formatting 与 parse success 的差异
- false-filter heavy 与 true recall 的 tradeoff

### 9.3 配对检验

同一题、同一模型、不同 prompt 的比较应尽量用配对检验：

- McNemar test
- bootstrap paired confidence interval
- permutation test

### 9.4 分布差异

public split 与 released subsets 的比较：

- label distribution
- source distribution
- expression depth
- operation count
- variable count
- family tag distribution
- Cliff's delta / rank-biserial correlation

### 9.5 回归模型

如果数据量足够，做题目级解释模型：

```text
correct ~ prompt_features + prompt_length + model + split + reasoning_mode
          + prompt_features:model
          + prompt_features:split
          + (1 | problem_id)
          + (1 | prompt_id)
```

可选模型：

- mixed-effect logistic regression
- cluster-robust logistic regression
- Bayesian hierarchical logistic regression

报告：

- odds ratio
- 95% CI
- p-value 或 posterior interval
- marginal effects

### 9.6 必须控制的混杂因素

至少写入实验配置和论文威胁章节：

- model architecture
- provider route
- reasoning mode
- token cap
- seed
- temperature
- parseability
- split label distribution
- post-release contamination
- prompt provenance / selection bias

---

## 10. 与现有 Stage1 资产的衔接

### 10.1 `P1_2_3` 的科研角色

`P1_2_3` 不再是提交主线，但仍是关键研究对象：

- 代表 false 侧强、true 侧保守的稳态 prompt。
- 适合作为 guardrail-heavy baseline。
- 可用于分析过度保守 prompt 的 true leakage。
- 可和 `P1_2_5` 构成风险画像对照。

### 10.2 `P1_2_5` 的科研角色

`P1_2_5` 是最终提交版本，也是高召回研究对象：

- 代表 true recall 更高但 false leakage 更强的 prompt。
- 适合做 true-positive signal mining。
- 不应直接把 wording 视为最终规则。
- 应结合 problem family 标签分析它救回了哪些结构族。

### 10.3 Offline rule assets 的科研角色

现有 offline assets 可以升级为论文中的结构解释工具：

- 用于解释 prompt 错误分布。
- 用于建立 family-conditioned metrics。
- 用于生成 distilled prompt 的规则候选。
- 用于判断哪些结构族适合 prompt 文本表达，哪些更适合 programmatic signal。

优先继续推进的轴：

- `TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR`
- `TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR`
- `TARGET_SHARED_LHS_AND_NEW_VARS`
- `OA_TRUE_TARGET_SHARED_NEW_VARS_SINGLETON_SOURCE`
- `OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS`
- `OA_TRUE_DISJOINT_BINARY_BINARY`

### 10.4 现有 CLI 的复用

继续复用：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
python -m sair_competition.cli tag-problem-families --dataset-path data/interim/splits/dev.jsonl --output-path data/interim/splits/dev_tagged.jsonl --summary-dir reports/experiments/dev_family_tags
python -m sair_competition.cli run-complete-prompt-eval --dataset-path data/interim/splits/smoke.jsonl --prompt-path prompts/complete/<candidate>.txt --output-dir artifacts/candidates/<run_id> --dotenv-path .env --model <model> --temperature 0 --max-tokens 256
python -m sair_competition.cli analyze-errors --predictions-path artifacts/candidates/<run_id>/predictions.jsonl --output-dir artifacts/candidates/<run_id>_analysis
python -m sair_competition.cli compare-candidates --candidate-dir artifacts/candidates/<run_a> --candidate-dir artifacts/candidates/<run_b> --output-dir reports/experiments/<comparison_id>
```

需要新增的 CLI 或脚本：

- `collect-prompt-corpus`
- `hash-prompt-corpus`
- `extract-prompt-features`
- `audit-prompt-corpus`
- `build-research-eval-matrix`
- `summarize-research-runs`
- `fit-prompt-feature-models`
- `make-paper-figures`

---

## 11. 目录与版本命名规范

### 11.1 研究版本命名

建议使用独立于参赛 prompt 的命名：

- corpus: `CORPUS_V1`, `CORPUS_V2`
- taxonomy: `TAX_V1`, `TAX_V2`
- distilled prompt: `D1.0`, `D1.1`, `D2.0`
- evaluation run: `RUN_YYYYMMDD_<prompt>_<model>_<split>`
- statistical analysis: `STAT_V1`, `STAT_V2`
- paper draft: `PAPER_D0`, `PAPER_D1`

### 11.2 实验记录模板

每个研究实验记录：

```text
Experiment ID:
Date:
Research question:
Prompt set:
Prompt feature version:
Dataset version:
Model/provider config:
Judge/parser version:
Hypothesis:
Metrics:
Main result:
Robustness result:
Family-conditioned result:
Decision:
Threats:
Next action:
```

### 11.3 Prompt corpus manifest

每次 corpus 更新必须生成：

- corpus size
- source counts
- prompt hash list
- license/tos audit
- duplicate report
- missing metadata report
- feature extraction summary

---

## 12. 里程碑计划

以下按 6-10 周单人主线安排，起点为 `2026-05-12`。日期可根据实际 API 预算与数据可得性调整。

### Phase 0：研究重定位与仓库准备

时间：`2026-05-12 ~ 2026-05-14`

目标：

- 冻结本文档作为后续执行基准。
- 建立 research 目录。
- 明确哪些旧竞赛资产可用于科研，哪些只做私有归档。
- 写出 paper outline v0。

交付物：

- `docs/02_experiment_plan.md`
- `reports/paper/outline.md`
- `configs/research/prompt_feature_taxonomy.yaml`
- `data/interim/prompt_corpus/prompt_corpus_manifest.json`

退出条件：

- 后续任务不再以“继续 Stage2”或“继续冲榜”作为默认主线。

### Phase 1：公开语料与 provenance 清洗

时间：`2026-05-15 ~ 2026-05-25`

目标：

- 收集官方、Contributor Network、GitHub、论文中可用 prompt。
- 建立 corpus schema。
- 完成 hash、来源、日期、许可说明记录。

交付物：

- `data/external/prompt_corpus/raw_index.jsonl`
- `data/interim/prompt_corpus/corpus_v1.jsonl`
- `reports/research/corpus_audit/summary.md`

退出条件：

- 至少 `8-12` 个可分析 prompt 进入 corpus。

### Phase 2：Prompt taxonomy v1

时间：`2026-05-26 ~ 2026-06-01`

目标：

- 手工标注代表性 prompt。
- 定义 feature taxonomy。
- 建立自动/半自动 feature extractor。

交付物：

- `configs/research/prompt_feature_taxonomy.yaml`
- `data/interim/prompt_corpus/prompt_features_v1.jsonl`
- `reports/research/taxonomy/taxonomy_v1.md`

退出条件：

- 每个候选 prompt 都有结构标签。

### Phase 3：小样本筛选实验

时间：`2026-06-02 ~ 2026-06-11`

目标：

- 对 `8-12` 个候选 prompt 做 screening。
- 过滤 parse 不稳、塌缩或不可复现候选。
- 选出 `3-5` 个进入完整评测。

交付物：

- `artifacts/research_runs/screening/*`
- `reports/research/screening/summary.md`
- `reports/research/screening/shortlist.md`

退出条件：

- shortlist 明确，并说明每个 prompt 代表的结构类型。

### Phase 4：完整评测与复算

时间：`2026-06-12 ~ 2026-06-24`

目标：

- 在官方三模型或近似配置上评测 shortlist。
- 覆盖本地固定切分与 released final evaluation subsets。
- 保存 raw outputs、run configs 和 metrics。

交付物：

- `artifacts/research_runs/official_model_eval/*`
- `reports/research/full_eval/main_table.csv`
- `reports/research/full_eval/summary.md`

退出条件：

- 能回答每个 prompt 的 model transfer gap 与 robustness gap。

### Phase 5：消融与 textual distillation 方法验证

时间：`2026-06-25 ~ 2026-07-05`

目标：

- 实现 human / LLM-assisted / feature-aware distilled prompt。
- 做关键结构消融。
- 验证方法是否改善鲁棒性或可解析性。

交付物：

- `prompts/complete/D*.txt`
- `reports/research/distillation_method/summary.md`
- `reports/research/ablations/summary.md`

退出条件：

- 至少一个 distilled prompt 方法有清楚的正结果或负结果。

### Phase 6：统计建模与图表

时间：`2026-07-06 ~ 2026-07-15`

目标：

- 完成描述统计、关联分析、配对检验、回归建模。
- 生成论文图表。

交付物：

- `reports/research/statistical_analysis/stat_v1.md`
- `reports/research/figures/*.png`
- `reports/research/figures/figure_notes.md`

退出条件：

- 每张图都能支持一个明确论文论点。

### Phase 7：论文初稿与复现包

时间：`2026-07-16 ~ 2026-07-31`

目标：

- 完成 workshop/TMLR 风格论文初稿。
- 整理复现脚本与结果 manifest。
- 明确是否升级为 AAAI/NeurIPS E&D 风格版本。

交付物：

- `reports/paper/draft.md`
- `reports/paper/related_work.md`
- `reports/paper/reproducibility_statement.md`
- `reports/research/release_manifest.md`

退出条件：

- 论文主贡献、实验表、图和威胁分析完整。

---

## 13. Stage2 衔接策略

### 13.1 当前不把 Stage2 作为主线

虽然 Stage2 已经是竞赛后续方向，但当前项目不应马上切换到 Stage2 solver。原因：

- Stage1 蒸馏科研已经有清晰数据、工程和发表路径。
- Stage2 需要 Lean 4、反例构造、概率校准和 solver 工程，复杂度显著更高。
- 如果现在切换，Stage1 已有资产容易停留在“参赛归档”而无法转化为论文。

### 13.2 Stage2 只做三类轻量工作

近期只做：

1. 规则跟踪：记录 Stage2 官方规则、证书格式、judge 更新。
2. 资产映射：标记哪些 Stage1 family tags 可能转成 Stage2 programmatic signal。
3. 最小预研：阅读 Lean / finite magma counterexample 相关接口，不开发正式 solver。

### 13.3 Stage2 启动条件

只有当以下条件满足时，再启动 Stage2 主线：

- Stage1 corpus/taxonomy/full eval 已完成。
- textual distillation 方法已有正负结论。
- paper draft 至少完成 v0。
- Stage2 规则、数据和 judge 已稳定。
- 明确有足够时间投入 Lean/counterexample 工程。

---

## 14. 风险清单与应对策略

### R1：研究问题退化成比赛复盘

信号：

- 文档主要在讲谁排名高。
- 图表只展示 leaderboard。
- 没有 taxonomy、统计检验或方法。

应对：

- 每个实验必须对应 RQ。
- 每个图必须回答结构-鲁棒性问题。
- 论文标题避免使用“Stage1 Summary”。

### R2：与 `Less Is More` 重复

信号：

- 只是在复现 prompt 变体和 ceiling 现象。
- 没有公开 prompt corpus、社区生态、统计建模或新方法。

应对：

- 把 corpus construction 和 feature taxonomy 作为核心贡献。
- 明确比较本项目与该论文的差异。
- 聚焦 public prompt ecosystem 与 post-release robustness。

### R3：后视镜风险

信号：

- 在 released final evaluation subsets 上调 prompt。
- 把 released subsets 当作私有盲测。

应对：

- 报告中统一标注 `post-release analysis`。
- prompt 方法选择不使用 released subsets 作为 reward。
- released subsets 只用于最终鲁棒性分析。

### R4：公开语料选择偏差

信号：

- 只分析公开提交，却推断所有参赛者。
- 社交媒体 self-report 进入主统计表。

应对：

- 区分 official、community-visible、self-reported。
- 主结论限定在公开可复现语料。
- 对选择偏差写入 limitations。

### R5：API 预算失控

信号：

- 太多 prompt 同时全量跑。
- repeats 过早增加。

应对：

- 严格三阶段评测。
- screening 先淘汰。
- 只对 shortlist 做完整评测。

### R6：模型/provider 混杂

信号：

- 同一模型名不同 route。
- 不同 token cap 混在一个表里。

应对：

- run_config 必须记录 provider route。
- 不同 route 分表或作为模型变量。
- 任何跨 provider 结论降低措辞强度。

### R7：Prompt 原文版权和归因问题

信号：

- 论文大段粘贴 prompt。
- 没有记录来源和 license。

应对：

- 原文在本地 corpus 保存 hash 与 source。
- 论文只用短摘录、结构标签和 summary。
- 每个 public prompt 保留 attribution。

### R8：方法贡献过弱

信号：

- 只有分析，没有新 prompt distillation 方法。

应对：

- 至少完成 human / LLM-assisted / feature-aware 三类方法之一。
- 优先做 feature-aware，因为最容易形成因果式消融。

### R9：过早投入 Stage2

信号：

- Stage1 论文还没开始，已经在写 Lean solver。

应对：

- Stage2 只保留轻量追踪。
- 以 Phase 7 作为是否切换条件。

### R10：仓库私有资产泄漏

信号：

- `data/raw`、`prompts/complete`、`artifacts/final` 被误提交。

应对：

- 继续遵守 `.gitignore`。
- 公开复现包只放可公开 prompt、代码、结构标签和摘要结果。
- 私有竞赛 prompt 与 API raw outputs 单独归档。

---

## 15. 论文与产品化交付

### 15.1 论文主张建议

建议论文主张写成：

> We study prompt-based textual distillation for formal equational reasoning through the public SAIR Stage1 ecosystem. We construct a provenance-aware prompt corpus, introduce a feature taxonomy for cheatsheet-style prompts, quantify how prompt structure interacts with model and distribution shift, and evaluate a feature-aware distilled prompt method for robustness.

中文表述：

> 本文基于 SAIR Stage1 公开 prompt 生态，构建带来源追踪的 prompt corpus 与结构 taxonomy，量化 prompt 结构在形式代数推理中的跨模型、跨分布鲁棒性，并验证一种 feature-aware textual distillation 方法。

### 15.2 推荐论文结构

```text
1. Introduction
2. Background: SAIR Stage1 and Prompt Textual Distillation
3. Public Prompt Corpus and Feature Taxonomy
4. Experimental Setup
5. Structural Findings
6. Feature-aware Textual Distillation
7. Robustness and Failure Analysis
8. Related Work
9. Limitations, Ethics, and Attribution
10. Conclusion
```

### 15.3 推荐图表

至少制作：

1. Prompt length vs performance scatter with LOESS。
2. True recall vs False recall tradeoff plot。
3. Accuracy-cost-latency Pareto plot。
4. Prompt feature × model heatmap。
5. Public split vs released subset robustness matrix。
6. Family-conditioned error heatmap。
7. `P1_2_3` vs `P1_2_5` risk profile comparison。

### 15.4 工具/Demo

建议做一个轻量工具，而不是大型产品：

#### Prompt lint / robustness analyzer

输入：

- prompt text

输出：

- byte size
- feature taxonomy
- parse risk
- length bucket
- suspected bias: true-leaning / false-leaning / balanced
- recommended eval matrix

#### Evaluation dashboard

输入：

- metrics csv
- prompt features jsonl

输出：

- prompt × model × split 表
- recall tradeoff
- robustness gap
- cost/time

---

## 16. 下一步 72 小时执行清单

### Day 1

- 冻结 `docs/02_experiment_plan.md`。
- 创建 `configs/research/`、`reports/research/`、`reports/paper/`。
- 写 `reports/paper/outline.md`。
- 从 docx 报告中抽取 RQ 与 contribution list。

### Day 2

- 定义 `prompt_corpus` schema。
- 建立 `corpus_sources.example.json`。
- 人工列出第一批 `8-12` 个 prompt 候选。
- 给 `P1_2_3`、`P1_2_5`、官方 strict archetypes 做 taxonomy 手工标注。

### Day 3

- 写 taxonomy v0。
- 设计 screening eval matrix。
- 选定第一批 screening split。
- 生成第一份 `reports/research/corpus_audit/summary.md` 草稿。

这三天的目标不是跑分，而是完成研究问题和数据结构落地。

---

## 17. 最终建议

接下来最稳的推进方式是：

1. 先把 Stage1 研究对象从“我的参赛 prompt”改成“公开 prompt textual distillation 生态”。
2. 先做 corpus 和 taxonomy，不先追求新 prompt 分数。
3. 先做 staged evaluation，不做全量 brute force。
4. 先研究 robustness gap，不只看最高 accuracy。
5. 先提出一个小而可控的 feature-aware distillation 方法，不急着做大规模自动演化。
6. Stage2 先监控和映射资产，等 Stage1 科研闭环完成后再进入。

如果严格按本文档推进，本项目的交付将不再只是一次 Stage1 参赛记录，而会转化为一套可发表、可复现、可展示的研究系统：

- 一个公开 prompt corpus
- 一个 prompt feature taxonomy
- 一套统一评测与鲁棒性分析协议
- 一组关于 textual distillation 边界的实证结论
- 一个小型 distilled prompt 方法
- 一篇 workshop/TMLR 起步、可升级到更高 venue 的论文
