# 项目迁移交接 Prompt

以下内容可直接整体复制给另一台设备上的新 AI，作为本项目的接手提示词使用。

---

你现在接手的是一个 **SAIR 代数推理竞赛工程化实验仓库**。请不要把它当作“从零开始的新项目”，而要把它当作一个**已经推进到中后期、已有稳定主线与离线分析体系的竞赛工程**来继续工作。你的目标不是重新发明方法，而是在现有策略基础上继续稳健推进。

## 1. 项目简要背景

本项目对应 SAIR `Mathematics Distillation Challenge - Equational Theories (Stage 1)`。  
任务是：给定 `Equation 1` 和 `Equation 2`，判断 `Equation 1` 是否必然蕴含 `Equation 2`，输出可解析的 `true/false`。

这是一个**符号结构理解 + 代数推理 + prompt 工程**问题，不是普通问答任务。  
当前路线**不是微调模型，不是训练新模型**，而是：

- 利用官方公开数据做工程化评测
- 通过 prompt 迭代找到稳定主线
- 用 `family tagger` 给样本打结构标签
- 把高价值规律沉淀为 `offline rule assets`
- 通过 `canonical axes` 和 `review set` 做人工复核与更细切分
- 只在证据足够强时，才考虑把极少数规律以更隐式、更程序化的方式反馈给主线 prompt

## 2. 竞赛与工程上的关键事实

- 当前参考日期：`2026-04-14`
- Stage 1 截止时间：`2026-04-20 23:59 AoE`
- 对应北京时间：`2026-04-21 19:59 CST`
- 官方公开数据总量：`1269`
  - `normal = 1000`
  - `hard1 = 69`
  - `hard2 = 200`
- 当前固定切分：
  - `smoke = 64`
  - `dev = 824`
  - `holdout = 254`
  - `audit = 127`
- Stage 1 的提交对象是 `complete prompt`
- 官方约束里，`complete prompt = prompt template + cheatsheet text`
- `cheatsheet` 大小上限是 `10KB`
- 官方离线评测是 `no-tools setting`，不能依赖外部检索、浏览器、agent 工具链

请注意：本项目已经明确选择**工程化 prompt 路线**，而不是“在公开题上做训练型深度学习方案”。

## 3. 仓库结构总览

请优先理解以下目录：

- `docs/`
  - 项目背景、工程化实验计划、工作历程总结、理论备忘、下一周执行清单
- `data/raw/`
  - 官方原始数据与官方 cheatsheet 样例
- `data/interim/`
  - 标准化后的公开数据、registry、带标签数据
- `data/interim/splits/`
  - 固定切分后的 `smoke/dev/holdout/audit`
- `prompts/complete/`
  - 各版本完整 prompt
- `artifacts/candidates/`
  - 各版本 prompt 的实际评测结果
- `reports/experiments/`
  - prompt 对比、family tagger、offline assets、canonical axes、review set 等实验报告
- `src/sair_competition/`
  - 核心代码
- `tests/`
  - 单元测试

重点代码文件：

- `src/sair_competition/cli.py`
- `src/sair_competition/features/family_tagger.py`
- `src/sair_competition/analysis/error_report.py`
- `src/sair_competition/analysis/offline_rule_assets.py`
- `src/sair_competition/analysis/offline_rule_review.py`
- `src/sair_competition/eval/openai_compatible.py`

## 4. 你接手后必须优先阅读的文档

请按这个顺序读：

1. `docs/项目工作历程与阶段性成果总结.md`
   - 这是最重要的总览文档，包含从项目开始到现在的完整推进过程，以及最近一轮新增工作的详细解释。
2. `docs/SAIR代数推理竞赛工程化实验计划.md`
   - 这是项目最初的工程化总设计，帮助你理解为什么仓库被组织成现在这样。
3. `docs/下一周执行清单.md`
   - 这是阶段性执行计划，但要结合最新总结文档理解，不能机械照搬。
4. `docs/理论备忘.md`
   - 用于理解这个问题的算法视角、可判定性视角，以及为什么当前路线选择 prompt + 结构资产，而不是训练黑箱模型。
5. `README.md`
   - 看 CLI 使用与本地运行方法。

如果时间足够，再读：

- `reports/experiments/offline_rule_review_set_day2_v2/summary.md`
- `reports/experiments/offline_rule_review_set_day2_v2/oa_true_target_lhs_amplification_review_verdict.md`
- `reports/experiments/offline_rule_axis_day2_v2/summary.md`
- `reports/experiments/offline_rule_assets_day2_v2/report.md`

## 5. 当前项目现状

### 5.1 当前最好的 prompt 主线

当前稳态主分支是：

- `prompts/complete/P1.2.3_implicit_guardrail_v2.txt`

对应结果在：

- `artifacts/candidates/P1_2_3_implicit_guardrail_v2/summary.json`

当前关键指标（在 `smoke` 固定切分上）：

- `accuracy = 0.546875`
- `balanced accuracy = 0.5371`
- `parse success = 1.0`
- `true_accuracy = 0.2258`
- `false_accuracy = 0.8485`

这条主线的意义不是“已经分最高”，而是：

- 它没有退化成全 `true`
- 也没有退化成全 `false`
- 输出稳定、格式可靠、便于继续迭代

请注意：**当前不应轻易推翻或重写这条主线。**

### 5.2 当前高召回挖掘支线

另一个重要分支是：

- `prompts/complete/P1.2.5_minimal_rule_missing_hard_composition.txt`

它的意义不是作为主线，而是作为**高召回挖掘支线**。  
它曾经在 `smoke` 上取得更高的召回与更高的 balanced accuracy，但同时带来了明显假阳性，因此：

- 可以用来挖“哪些真例结构被翻正了”
- 不应直接继承其 wording 回到主线

简言之：`P1_2_3` 是稳态主线，`P1_2_5` 是挖掘支线。

### 5.3 当前离线结构资产链路已经成型

目前项目已经完成这样一条闭环：

- `family tagger`
- `offline rule assets`
- `canonical axes`
- `deduplicated review set`
- `人工复核`
- `子型细切`
- `回写代码`

当前最新版本是 `day2_v2`，核心结果如下：

- `reports/experiments/offline_rule_assets_day2_v2/report.json`
  - `asset_count = 13`
- `reports/experiments/offline_rule_axis_day2_v2/summary.json`
  - `canonical_axis_count = 7`
- `reports/experiments/offline_rule_review_set_day2_v2/summary.json`
  - `review_row_count = 13`
  - `review_axis_count = 6`

这说明项目已经不只是“打标签做统计”，而是已经进入了“把结构规律沉淀成资产，并为后续更隐式利用做准备”的阶段。

## 6. 当前最关键的最近进展

最近最重要的一次推进，是对：

- `OA_TRUE_TARGET_LHS_AMPLIFICATION`

做了更细的子型拆分，并已经真正落到代码与产物里。

### 当前结论

保留父轴：

- `OA_TRUE_TARGET_LHS_AMPLIFICATION`

但新增两个子型：

- `TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR`
- `TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR`

对应的离线资产：

- `OA_TRUE_TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR`
- `OA_TRUE_TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR`

### 当前策略

- `MULTI_ANCHOR`
  - 对应 `2` 条高置信 `smoke` 真例：`normal_0040`、`normal_0489`
  - 已提升为 `prepare_programmatic_positive_signal` 候选
- `SINGLE_ANCHOR`
  - 对应 `1` 条边界真例：`normal_0920`
  - 暂时只保留为观察子型，不和 `MULTI_ANCHOR` 同强度推进

### 这件事为什么重要

它说明项目已经开始做到：

- 不把一个宽轴粗暴整体推进
- 而是先继续细切，再区分“高置信可推进子型”和“边界观察子型”

这正是当前工程路线的核心方法论。

## 7. 已经验证过的重要结论

请不要重复踩这些坑：

1. **强 false-filter 路线容易让模型退化成几乎全 `false`。**
   - `P1.2.1 / P1.4.0 / P1.4.1 / P1.4.2` 都说明了这一点。

2. **官方 cheatsheet 样例直接 strict 化后，在当前 DeepSeek 上会退化成几乎全 `false`。**
   - `P2.0.0 / P2.0.1 / P2.0.2` 都是这样。
   - 因此官方原型目前只能作为 prompt 风格参考，不应直接并回主线。

3. **当前最稳的方向不是继续堆 wording，而是继续做离线结构资产。**

4. **宽标签经常真假混合，必须先细切。**
   - `TARGET_SHARED_LHS_AND_NEW_VARS` 和 `TARGET_LHS_AMPLIFICATION` 都已经证明了这一点。

## 8. 当前最推荐的下一步工作

请按照下面优先级继续推进：

### 第一优先级

把最新 `family_tagger` 拿到更大的固定切分上验证泛化性，优先 `dev`。

目标：

- 检查新子型是否只在 `smoke` 上成立
- 统计样本数、`true/false` 分布、与主线漏判的关系

重点关注：

- `TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR`
- `TARGET_LHS_AMPLIFICATION_SINGLE_ANCHOR`
- `TARGET_SHARED_LHS_AND_NEW_VARS_*` 子型

### 第二优先级

继续完成剩余高价值主轴的人工复核与细切，优先：

- `OA_TRUE_TARGET_SHARED_NEW_VARS_SINGLETON_SOURCE`
- `OA_TRUE_SINGLETON_WITH_TARGET_SHARED_LHS`
- `OA_TRUE_DISJOINT_BINARY_BINARY`

### 第三优先级

围绕 `OA_TRUE_TARGET_LHS_AMPLIFICATION_MULTI_ANCHOR` 做真正的“程序化正信号候选”准备，但**不要立刻改主 prompt wording**。  
先做离线准备，例如：

- 更明确的触发条件
- 命中样本清单
- 边界样本清单
- 与其他正向资产的重叠关系

### 第四优先级

只有在更大切分验证通过后，才考虑是否值得对：

- `P1.2.3_implicit_guardrail_v2`

做一次**极小幅度**轻注入实验。

前提必须同时满足：

- 至少 `1~2` 个新子型在更大切分上仍然稳定
- 与主线主要漏判显著相关
- 能用非常短、非常弱、非常隐式的方式表达
- 不会重新引入强 false-filter 或强决策层

## 9. 推荐你接手后的具体动作顺序

1. 先阅读第 4 节提到的 5 份核心文档
2. 再确认当前最新产物：
   - `reports/experiments/offline_rule_assets_day2_v2/`
   - `reports/experiments/offline_rule_axis_day2_v2/`
   - `reports/experiments/offline_rule_review_set_day2_v2/`
3. 检查 `src/sair_competition/features/family_tagger.py` 中当前已实现的最新子型
4. 运行一次最新 tagger 到更大切分
5. 输出一份新的“标签泛化性验证摘要”
6. 再决定是否继续做剩余 review 轴的细切

## 10. 本地运行与环境说明

默认使用环境：

- `conda` 环境名：`generic`

通常需要：

```powershell
$env:PYTHONPATH='src'
```

关键命令示例：

```powershell
python -m sair_competition.cli tag-problem-families `
  --dataset-path data/interim/splits/dev.jsonl `
  --output-path data/interim/splits/dev_tagged_tmp.jsonl `
  --summary-dir reports/experiments/dev_family_tags_tmp
```

```powershell
python -m sair_competition.cli attach-family-tags-to-predictions `
  --predictions-path artifacts/candidates/P1_2_3_implicit_guardrail_v2/predictions.jsonl `
  --tagged-dataset-path data/interim/splits/smoke_tagged_day2_v2.jsonl `
  --output-path artifacts/candidates/P1_2_3_implicit_guardrail_v2_tagged_day2_v2/predictions.jsonl
```

```powershell
python -m sair_competition.cli analyze-errors `
  --predictions-path artifacts/candidates/P1_2_3_implicit_guardrail_v2_tagged_day2_v2/predictions.jsonl `
  --output-dir artifacts/candidates/P1_2_3_implicit_guardrail_v2_tagged_day2_v2_analysis
```

pytest 方面可以尝试使用：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_pytest.ps1 tests/test_offline_rule_review.py -q
```

因为过去是 Windows 环境下，裸 `pytest` 可能会受到外部插件加载和临时目录权限问题影响。

## 11. 私有信息与协作约束

这是竞赛项目，请注意：

- 不要建议把 `data/raw/`、`.env`、`prompts/complete/`、`reports/experiments/`、`artifacts/candidates/` 中的私有内容公开上传到 GitHub
- 不要输出或记录 `.env` 里的真实密钥
- 不要默认认为项目目标是“重新训练一个模型”
- 不要轻易推翻当前主线 `P1_2_3`
- 不要因为某个子型在 `smoke` 上看起来不错，就立刻把它写回主 prompt

## 12. 你在接手后应该追求的目标

短期目标：

- 验证最新结构子型在更大切分上的泛化性
- 完成剩余关键 review 轴的细切
- 继续把高价值规律沉淀为更稳的离线资产

中期目标：

- 形成 `1~2` 个真正稳定、可程序化利用的高置信正向子型
- 在不破坏主线稳定性的前提下，尝试一次极小幅度轻注入实验

最终目标：

- 在保持 `parse success = 1.0` 和整体稳定性的前提下，进一步提高主线对高价值真例结构族的覆盖率
- 交付一个合规、可复现、可解释的 `complete prompt`

## 13. 你接手后第一条回复建议

当你看完以上信息并读取核心文档后，建议你先输出一份简短接手确认，内容包括：

- 你对当前项目状态的理解
- 你认为最关键的 3 个事实
- 你准备先执行的下一步工作
- 你暂时不会做的事

请以“尊重现有策略、优先延续当前工程路线”为原则继续推进，而不是重新开一个完全不同的方法分支。

---

如果你已经理解以上内容，请从阅读以下文件开始：

1. `docs/项目工作历程与阶段性成果总结.md`
2. `docs/SAIR代数推理竞赛工程化实验计划.md`
3. `docs/下一周执行清单.md`
4. `docs/理论备忘.md`
5. `reports/experiments/offline_rule_review_set_day2_v2/summary.md`
