# SAIR 代数推理竞赛工程化实验计划

## 1. 文档定位

本文档用于把 SAIR `Mathematics Distillation Challenge - Equational Theories (Stage 1)` 按“工程项目”方式推进，目标不是写一份泛泛的参赛建议，而是产出一套可以直接执行的研发计划、实验框架、版本管理方式、评测协议和风险控制方案。

本文档基于以下本地材料整理：

- `docs/Doubao的总结与分析.md`
- `webpages/The Foundation for Science and AI Research (SAIR).html`

当两者冲突时，以本地网页快照中可核实的信息为准。

---

## 2. 已确认事实与关键修正

### 2.1 已确认事实

- 竞赛名称：`Mathematics Distillation Challenge - Equational Theories`
- 当前聚焦阶段：`Stage 1`
- Stage 1 截止时间：`2026-04-20 23:59 AoE`
- 对应北京时间：`2026-04-21 19:59 CST`
- Stage 1 排行榜发布时间：`2026-04-30` 或之前
- Stage 2 开始时间：`2026-05-01`
- 任务形式：给定 `Equation 1` 和 `Equation 2`，判断 `Equation 1 是否蕴含 Equation 2`
- Stage 1 输出目标：可解析的 `true/false` 答案
- 提交对象不是单纯“规则文本”，而是 `complete prompt`
- 网页原文说明：`complete prompt = prompt template + cheatsheet text`
- cheatsheet 上限：`10KB`
- 除了 `data/raw/prompt_templates.jsonl` 之外，官方还提供了若干 `cheatsheet_xxx.md` 样例文件
- 这些 `cheatsheet_xxx.md` 样例通常不只是“规则摘要”，而是同时包含任务 framing、占位符、推理步骤与输出契约的 prompt 风格样例
- 网页叙述部分出现过 `{ equation1 } / { equation2 }` 表述，而提交界面提示中出现过 `{{ equation1 }} / {{ equation2 }}`
- 因此 placeholder 语法必须以官方 playground 和提交界面实测为准
- 公开训练/开发题不是 1200，而是：
  - `normal: 1000`
  - `hard1: 69`
  - `hard2: 200`
  - 合计 `1269`
- 官方离线评测是 `no-tools setting`
- 官方离线评测明确不提供：
  - 浏览器访问
  - web search
  - 外部互联网检索
- 离线评测集与公开 `1269` 题不同
- 离线评测集真值分布平衡：`50% TRUE / 50% FALSE`
- 官方建议资源约束：
  - 平均成本 `<= USD 0.01 / problem`
  - 平均求解时间 `<= 10 min / problem`
- Stage 1 评测模型尚未最终确定
- 网页只给出候选家族示例：`OpenAI OSS`、`Llama`、`Gemini Flash`
- 最终评测模型列表最晚在 `2026-04-10` 前公布或由社区投票决定
- Stage 1 提交内容后续可能公开
- 比赛处于 `experimental phase`
- 规则、评分细节、评测流程可能调整

### 2.2 对现有总结的关键修正

以下内容不宜直接作为项目假设：

- “公开题量是 1200”不准确，当前快照显示是 `1269`
- “官方已经确定强模型/弱模型双轨评测”未在网页快照中得到确认
- “官方评测模型没有深度思考能力”未得到确认
- “只需要优化 cheatsheet”表述不完整，工程上应以 `complete prompt` 作为优化对象
- “官方 cheatsheet 样例可以直接当作本地主线 prompt 使用”也是不完整的理解；更合理的做法是先把它们视为官方 prompt 原型，再做 strict 适配
- “占用大算力是主线”不成立，Stage 1 更像是 `规则提炼 + prompt 工程 + 评测纪律`

### 2.3 直接影响实验设计的约束

- 不能依赖工具调用、检索、代理系统、多轮交互
- 不能依赖按题型切换不同 prompt
- 不能把高性能寄托在某一个尚未确认的官方模型版本上
- 不能把公开题集准确率当作唯一目标，否则极易过拟合
- 需要同时优化：
  - 规则内容
  - prompt 模板结构
  - 输出格式稳定性
  - 压缩后的信息密度

---

## 3. 项目目标、非目标与成功标准

### 3.1 项目目标

本项目的最终交付不是“写出一份看起来聪明的 cheatsheet”，而是：

1. 产出一个可提交、可复现、可解释的 `complete prompt`
2. 建立一套能够持续迭代 prompt 的工程流水线
3. 在公开数据上形成可量化的效果提升
4. 在官方环境中保证解析成功、格式合规、风险可控
5. 为 Stage 2 保留可复用的知识资产和误差分析资产

### 3.2 非目标

以下方向不应成为 Stage 1 主线：

- 微调模型
- 训练私有模型权重
- 构建多轮 agent 工作流
- 为不同题人工切换不同版本 prompt
- 大规模依赖 GPU 做“模型训练型”竞赛方案
- 单纯追求在公开题集上刷分而不控制泛化风险

### 3.3 成功标准

#### 必须满足的硬标准

- 提交物合规
- cheatsheet 大小 `<= 10KB`
- 输出可以被稳定解析为 `true/false`
- placeholder 使用正确
- 本地评测流程可复现
- 每次实验都有版本号、配置、结果记录

#### 期望达到的效果标准

- 与最小基线 prompt 相比，公开数据 holdout 上出现稳定提升
- 不同 proxy 模型上的效果排名具有一致性，而不是只在单模型上有效
- 解析失败率接近 0
- 输出延迟与成本符合官方建议范围

#### 过程标准

- 每日实验有记录
- 每个版本都有明确“为什么要改”
- 每次改动都能在固定数据切分上验证
- 提交前至少保留 `2~3` 个可回滚版本

---

## 4. 整体策略：把比赛当成一个 Prompt R&D 项目

### 4.1 核心判断

这个比赛的最优工程对象应定义为：

`完整推理协议 = 模板结构 + 规则内容 + 输出契约 + 压缩策略 + 评测流程`

因此项目不应只围绕“写 cheatsheet”，而应围绕以下五层展开：

1. `Constraint Layer`
   - 竞赛规则、大小限制、输出规范、离线 no-tools 约束
2. `Math Layer`
   - 等式理论、law family、蕴含与非蕴含的核心模式
3. `Prompt Layer`
   - 指令顺序、规则排序、负例优先级、输出约束
4. `Evaluation Layer`
   - 数据切分、proxy 模型、指标体系、错误分析
5. `Release Layer`
   - 冻结版本、回滚版本、提交检查、证据留存

### 4.2 战略主线

建议采用“三阶段主线 + 两条侧线”的结构。

#### 主线 A：构建可靠基线

- 先做一个极简、可解析、可批量跑的 baseline
- 目标不是高分，而是建立实验闭环

#### 主线 B：提炼高信息密度规则库

- 从公开题集、4694 laws、蕴含图中提炼高频规律
- 把数学知识变成适合小模型/低成本模型读取的规则文本

#### 主线 C：优化 complete prompt 结构

- 把“什么规则放前面、如何组织、如何约束输出”当成核心实验变量

#### 侧线 D：建立误差分析资产

- 为每次错误建立标签和原因分类
- 累积出“什么题型容易错、为什么错、需要补哪类规则”

#### 侧线 E：为 Stage 2 保留结构化资产

- 保留反例思路、证明草稿、law family 分类
- 即便 Stage 1 不直接用，也不要浪费

#### 侧线 F：官方 prompt 原型的 strict 适配实验

- 将官方 `cheatsheet_balanced`、`cheatsheet_counterexample_first`、`cheatsheet_example_fast_filters` 视作三类“官方 prompt 原型”
- 不直接拿原文替换当前本地主线 prompt，而是提炼其结构特点，再改写成适合 `true/false` 首行稳定解析的 strict 版本
- 与现有主线分开编号、分开评测、分开记录，避免把“风格探索”与“主线稳态优化”混在一起
- 优先把这条线当作对照实验与灵感来源，而不是立即争夺主线

---

## 5. 推荐工程目录结构

建议尽快把当前仓库从“资料夹”升级为“可研发仓库”。

```text
SAIR_Competition/
├─ data/
│  ├─ raw/
│  │  ├─ normal.*
│  │  ├─ hard1.*
│  │  ├─ hard2.*
│  │  ├─ equations.txt
│  │  └─ export_raw_implications.*
│  ├─ interim/
│  │  ├─ public_all.jsonl
│  │  ├─ metadata.jsonl
│  │  └─ splits/
│  └─ external/
├─ prompts/
│  ├─ templates/
│  ├─ cheatsheets/
│  ├─ complete/
│  └─ archive/
├─ configs/
│  ├─ models/
│  ├─ eval/
│  └─ prompts/
├─ src/
│  └─ sair_competition/
│     ├─ data/
│     ├─ parse/
│     ├─ features/
│     ├─ prompting/
│     ├─ eval/
│     └─ analysis/
├─ reports/
│  ├─ daily/
│  ├─ experiments/
│  └─ release/
├─ artifacts/
│  ├─ candidates/
│  ├─ final/
│  └─ backups/
└─ docs/
   ├─ Doubao的总结与分析.md
   └─ SAIR代数推理竞赛工程化实验计划.md
```

### 5.1 工程原则

- `data/raw` 永不手改
- `prompts/complete` 只保存可直接提交或可直接测试的完整 prompt
- `reports/experiments` 每个实验一份记录
- notebook 只做临时探索，不作为事实来源
- 版本决策以脚本化评测结果为准，不以“感觉”决策

---

## 6. 交付物定义

### 6.1 最终交付物

- `final_complete_prompt.txt`
- `final_cheatsheet.txt`
- `release_note.md`
- `final_eval_report.md`
- `submission_checklist.md`

### 6.2 中间交付物

- 数据标准化结果
- 固定切分文件
- baseline prompt
- 候选 prompt 版本库
- 错题分析表
- law family 规则表
- 压缩映射表

### 6.3 每个 prompt 版本必须附带的元数据

- 版本号，例如 `P0.1.0`
- 变更原因
- 使用的模板版本
- 使用的 cheatsheet 版本
- 字节大小
- 评测模型
- 评测数据切分
- 准确率
- TRUE/FALSE 分项表现
- normal/hard1/hard2 分项表现
- 解析失败率
- 单题平均耗时
- 备注与下一步假设

---

## 7. 数据与标注策略

### 7.1 数据资产优先级

优先级从高到低如下：

1. 官方公开 selected problems
2. `equations.txt` 中的 4694 laws
3. raw implication graph
4. 本地派生的 metadata
5. 强模型辅助生成的规则候选

### 7.2 数据切分原则

公开题集不能直接被当成“越刷越好”的训练靶子，必须冻结切分。

建议在拿到全部公开题后，立刻生成并固定四个切分：

- `smoke`
  - 用途：快速回归
  - 规模：`48~64` 题
- `dev`
  - 用途：主要调参
  - 规模：约 `70%`
- `holdout`
  - 用途：版本晋升
  - 规模：约 `20%`
- `audit`
  - 用途：最终冻结前只跑少量次数
  - 规模：约 `10%`

建议按以下维度做分层抽样：

- 数据来源：`normal / hard1 / hard2`
- 标签：`TRUE / FALSE`
- 表达式复杂度
- 变量个数
- 运算树深度

### 7.3 推荐的固定切分规模

如果公开题总量仍为 `1269`，建议如下：

- `smoke`: `64`
- `dev`: `824`
- `holdout`: `254`
- `audit`: `127`

也可以按来源近似分配：

- normal：`1000`
- hard1：`69`
- hard2：`200`

重点不是具体数字，而是：

- 切分一旦生成就冻结
- 所有实验在同一切分上比较
- `audit` 集在最后阶段才高频使用

### 7.4 元特征工程

每道题建议额外生成以下 metadata，用于错误分析：

- `num_vars`
- `num_ops_eq1`
- `num_ops_eq2`
- `tree_depth_eq1`
- `tree_depth_eq2`
- `has_repeated_var_pattern`
- `canonical_law_family`
- `is_known_high_outdegree_law`
- `source_split`
- `label`

这些特征不是为了训练模型，而是为了让错误分析可结构化。

---

## 8. Prompt 作为核心实验对象的拆解方式

### 8.1 版本拆解

不要只存一份“最终 prompt”，而是拆成三个层次：

1. `Template`
   - 固定框架
   - placeholder
   - 输出格式要求
   - 推理步骤骨架
2. `Cheatsheet`
   - 规则主体
   - 正例规则
   - 反例规则
   - 优先级排序
3. `Complete Prompt`
   - 实际喂给模型的组合结果

### 8.2 需要被显式实验的维度

#### A. 输出契约

- 输出 `true/false` 还是 `True/False`
- 是否允许句号、换行、解释
- 是否要求“只输出一个词”

这不是细节问题，而是提交风险问题。

#### B. 模板结构

- 指令优先
- 规则优先
- 先给判断标准再给规则
- 先给负例过滤再给正例归纳

#### C. 规则组织方式

- 按 law family 分组
- 按推理优先级排序
- 按“先排除 FALSE，再确认 TRUE”排序
- 按高频到低频排序

#### D. 表达形式

- 自然语言
- 半形式化规则
- 极致压缩符号化表达

#### E. 示例使用

- 零样本
- 单个极短示例
- 两三个短示例

在 10KB 限制下，示例是否值得占空间必须被实验验证。

#### F. 推理控制语句

- 直接判断
- 使用固定检查表
- 要求先做代换/重写，再输出
- 是否加入“先尝试寻找反例信号”的步骤

### 8.3 建议的候选 prompt 家族

至少同时推进以下四类候选：

#### Family A：Contract-First Minimal

特点：

- 极短
- 强输出约束
- 少量关键规则

用途：

- 作为稳健基线
- 测试“小 prompt 是否反而更适合低成本模型”

#### Family B：Checklist-First

特点：

- 给模型一个固定判断顺序
- 规则数量中等
- 强调过程稳定性

用途：

- 提升解析稳定性
- 降低模型自由发挥

#### Family C：Rule-Library Heavy

特点：

- 规则密度高
- 重视 law family 覆盖
- 更像压缩知识库

用途：

- 测试“高覆盖率”策略是否有效

#### Family D：Hybrid with False Filters

特点：

- 前面先放非蕴含快速排除规则
- 后面再放正例重写规则

用途：

- 因官方评测 TRUE/FALSE 平衡，FALSE 识别能力非常关键

---

## 9. 基线设计

### 9.1 为什么必须先做基线

没有 baseline，就无法回答下面这些问题：

- 你的规则到底有没有贡献
- 提升来自规则，还是来自模板
- 提升是真提升，还是切分波动
- 大 prompt 真的比小 prompt 好吗

### 9.2 基线清单

建议至少建立以下四个基线：

#### B0：极简格式基线

- 只包含任务说明
- 只包含输出约束
- 不包含规则库

用途：

- 测裸 prompt 能力

#### B1：最小数学规则基线

- 加入最基础的判断定义
- 加入极少量通用规则

用途：

- 衡量“只加一点规则”的收益

#### B2：Doubao 风格规则基线

- 从现有总结里抽取一版压缩规则

用途：

- 作为从现有材料出发的参考起点

#### B3：高频 law family 基线

- 从公开题集中最常见或最关键的 law family 抽取

用途：

- 作为真正的工程主基线

### 9.3 晋升标准

一个新版本只有在满足以下条件时才可晋升：

- 相对上一版本在 `holdout` 上提升 `>= 2` 个百分点
- 或解析失败率显著下降
- 或在 hard 子集上出现明确提升且总体不退化

如果新版本只在 `dev` 集提升而 `holdout` 不提升，不晋升。

---

## 10. 规则提炼路线

### 10.1 规则来源不应只有一种

建议同时从四条路径抽规则：

1. 从 4694 laws 抽“高层结构规律”
2. 从公开题错题里抽“判别性规则”
3. 从 implication graph 抽“中心节点/高出度规律”
4. 从强模型辅助分析中抽“候选描述”，再由人审校

### 10.2 规则库建议结构

把规则拆成四类：

#### I. 定义与总原则

- 蕴含定义
- 何时可判 TRUE
- 何时只要找到一个反例方向就应判 FALSE

#### II. 正向重写规则

- 代换
- 结构重写
- 已知 law family 导出的常见后果

#### III. 负向排除规则

- 常见不蕴含模式
- 变量约束不匹配
- 结构强度不足
- 仅有弱律无法推出强律

#### IV. 决策顺序规则

- 先检查显式相同/重命名等价
- 再检查是否存在直接重写链
- 再检查高频非蕴含模式
- 最后才做复杂组合推断

### 10.3 规则审核原则

所有写进 cheatsheet 的规则必须满足：

- 不是某一道题的硬编码答案
- 尽量可泛化到一类题
- 能说明适用条件
- 不与已有规则冲突

建议建立一个 `rule registry` 表，字段包括：

- `rule_id`
- `rule_text`
- `rule_type`
- `source`
- `confidence`
- `support_examples`
- `failure_examples`
- `status`

### 10.4 强模型的正确使用方式

强模型可以用，但位置要放对：

- 用于总结 law family
- 用于生成规则候选草稿
- 用于帮助解释错误模式
- 不应用于替代验证
- 不应用于决定最终版本是否有效

原则是：

`强模型负责启发，固定切分评测负责裁决`

---

## 11. 评测协议

### 11.1 本地评测必须模拟官方核心约束

本地评测要尽量贴近官方：

- 单轮
- 无工具
- 同一份 complete prompt 跑整套题
- 输出只允许目标格式

### 11.2 proxy 模型策略

由于官方模型在 `2026-04-10` 前未最终确定，建议用“模型家族覆盖”而不是单模型押注。

建议至少维护三类 proxy：

#### Proxy 1：低成本开源/开源风格

用途：

- 模拟官方“低成本、可大规模跑”的约束
- 观察规则文本对相对朴素模型是否友好

#### Proxy 2：商业低成本模型

用途：

- 测试模板在实用商用模型上的稳定性

#### Proxy 3：强模型教师

用途：

- 发现边界情况
- 不作为最终选择唯一依据

### 11.3 评测维度

每次评测至少输出以下指标：

- overall accuracy
- TRUE accuracy
- FALSE accuracy
- normal accuracy
- hard1 accuracy
- hard2 accuracy
- parse success rate
- average latency
- estimated cost

### 11.4 结论判定纪律

不要仅凭 overall accuracy 决策。

需要同时看：

- FALSE 是否明显崩溃
- hard 子集是否退化
- 解析稳定性是否下降
- 不同模型上的排名是否一致

### 11.5 playground 的使用原则

官方 playground 只做三类事：

1. 验证 placeholder 与输出格式是否兼容
2. 验证 complete prompt 在官方界面是否能正确运行
3. 提交前做最终 dry run

不建议把 playground 当高频调参平台。

原因：

- 容易形成不可复现的人工调参
- 成本高
- 结果记录难以沉淀

---

## 12. 错误分析方法

### 12.1 错误标签体系

建议每道错题至少打一个主标签：

- `FORMAT`
  - 输出不可解析
- `RULE_MISSING`
  - 缺少某类规则
- `RULE_CONFLICT`
  - 规则互相打架
- `PROMPT_AMBIGUOUS`
  - 模板表述让模型误解
- `FALSE_FILTER_WEAK`
  - 非蕴含排除不够强
- `OVERCOMPRESSION`
  - 压缩过度导致规则不可读
- `MODEL_SPECIFIC`
  - 某类模型理解方式特殊
- `HARD_COMPOSITION`
  - 多规则组合场景失败

### 12.2 每次实验后的固定动作

每次完整评测后都做以下动作：

1. 抽取全部错题
2. 统计错题标签分布
3. 找出 top 3 错误簇
4. 只围绕 top 3 错误簇改 prompt
5. 记录“这次改动对应哪一类错误”

禁止无目的大改。

### 12.3 误差修复优先级

优先级建议如下：

1. 解析失败
2. placeholder 兼容问题
3. 大类 FALSE 误判
4. 高频 law family 缺失
5. hard 边缘场景
6. 纯粹的措辞润色

---

## 13. 时间计划与里程碑

以下时间计划按当前日期 `2026-03-21` 制定。

### Phase 0：项目初始化与规则核验

时间：`2026-03-21 ~ 2026-03-23`

目标：

- 建立工程目录
- 下载和固化官方公开数据
- 核实 placeholder、输出格式、大小规则
- 形成 baseline 流水线

交付物：

- 冻结的数据清单
- baseline prompt `B0/B1`
- 初版切分文件
- 首次 smoke 结果

退出条件：

- 能从命令行一键完成一次小规模评测

### Phase 1：基线建立与错误分类

时间：`2026-03-24 ~ 2026-03-29`

目标：

- 建立 `B0~B3`
- 完成第一轮对比
- 建立错误标签体系

交付物：

- baseline report v1
- error taxonomy v1
- rule registry v1

退出条件：

- 至少明确 2 个有效改进方向

### Phase 2：Prompt 家族并行探索

时间：`2026-03-30 ~ 2026-04-05`

目标：

- 并行推进 `Family A/B/C/D`
- 找到在不同 proxy 模型上都相对稳健的方向

交付物：

- prompt families 对比报告
- 候选版本 shortlist

退出条件：

- 至少保留 2 个有竞争力的结构方向

### Phase 3：规则强化与跨模型稳健性

时间：`2026-04-06 ~ 2026-04-10`

目标：

- 重点优化 FALSE 识别与 hard 集
- 关注官方在 `2026-04-10` 前公布的评测模型信息

交付物：

- robustness report
- 规则库 v2

退出条件：

- 根据官方模型家族信息更新 proxy 组合

### Phase 4：架构冻结与压缩优化

时间：`2026-04-11 ~ 2026-04-16`

目标：

- 冻结 prompt 大结构
- 只做规则排序、压缩、少量措辞修复

交付物：

- `P1.x` 候选版本
- 压缩前后对照表
- 解析稳定性报告

退出条件：

- shortlist 收敛到 `2~3` 个版本

### Phase 5：官方环境 dry run 与发布准备

时间：`2026-04-17 ~ 2026-04-19`

目标：

- 在官方 playground 验证最终候选
- 完成提交检查

交付物：

- release candidate
- submission checklist
- rollback 版本备份

退出条件：

- 已确认主版本与备用版本

### Phase 6：最终提交窗口

时间：`2026-04-20 ~ 2026-04-21 19:59 CST`

目标：

- 正式提交
- 保留证据
- 锁定版本

交付物：

- 正式提交截图
- 最终 release note
- 最终归档

---

## 14. 未来 72 小时具体执行清单

如果现在立刻开工，建议只做以下事情，不要一开始就陷入大规模 prompt 打磨。

### Day 1

- 初始化仓库结构
- 下载官方公开数据与 laws 文件
- 写数据读取脚本
- 确认 placeholder 语法
- 建立 `B0`

### Day 2

- 建立固定切分
- 写批量评测脚本
- 建立统一结果格式
- 跑第一轮 smoke

### Day 3

- 建立 `B1/B2/B3`
- 形成第一份 baseline 对比报告
- 建立错题标签体系

这三天的目标不是高分，而是“建立正确的研发地基”。

---

## 15. 技术栈建议

### 15.1 必选技术栈

- `Python 3.11+`
- `uv` 或 `poetry`
- `pandas` 或 `polars`
- `pydantic`
- `typer`
- `jinja2`
- `pytest`
- `rich`
- `orjson`

### 15.2 强烈建议加入的组件

- `duckdb`
  - 适合做实验结果查询
- `networkx`
  - 适合做 implication graph 分析
- `matplotlib` / `seaborn`
  - 适合做错误分布图
- `litellm` 或自定义 provider adapter
  - 统一不同模型 API 接口

### 15.3 可选组件

- `lark`
  - 若需要自己解析等式语法树
- `sympy`
  - 仅在你确定要复用表达式树工具时考虑

注意：

Stage 1 主体不是符号求解项目，因此不要过早把大量时间投进重型形式系统。

### 15.4 基础脚本清单

建议优先实现以下脚本：

- `prepare_public_data`
- `build_metadata`
- `make_splits`
- `build_complete_prompt`
- `run_eval`
- `summarize_eval`
- `analyze_errors`
- `check_submission_ready`

---

## 16. 算力、预算与资源建议

### 16.1 核心判断

Stage 1 的瓶颈不是训练算力，而是：

- 规则提炼质量
- prompt 结构设计
- 实验纪律
- 误差分析质量

### 16.2 硬件建议

#### 最小可行配置

- 无 GPU 也可推进
- 一台稳定的开发机
- 能访问 API 或使用官方 playground

#### 标准配置

- 一台本地开发机
- 可选云端低成本模型 API
- 可选一张消费级 GPU 用于跑开源小模型代理评测

#### 强化配置

- 1 张 24GB 级别消费卡或等价云实例
- 仅用于补充开源 proxy 评测，不是必要条件

### 16.3 预算档位建议

#### 低预算

- 目标：建立闭环，少量官方环境验证
- 适用：单人、初期

#### 中预算

- 目标：多轮 proxy 批量评测 + 强模型辅助分析
- 适用：想做稳定迭代的标准方案

#### 高预算

- 目标：高频多模型 sweep
- 适用：团队化推进

不建议一开始就上高预算，因为前期最重要的是把实验框架搭对。

---

## 17. 团队分工建议

### 17.1 单人方案

单人时建议切换三种“角色帽子”：

- `Research Lead`
  - 决定实验方向
- `Eval Engineer`
  - 保证脚本、切分、指标稳定
- `Release Owner`
  - 负责提交、回滚、证据保留

不要让“写 prompt 的自己”和“评估 prompt 的自己”完全混在一起。

### 17.2 两人方案

- 角色 1：数学规则与错误分析
- 角色 2：工程评测与版本管理

### 17.3 三人方案

- 角色 1：Prompt / 规则负责人
- 角色 2：评测工程负责人
- 角色 3：项目管理 / 风险与提交负责人

### 17.4 决策机制

建议明确：

- 谁能改 `main` 候选 prompt
- 谁批准版本晋升
- 谁负责最终提交

避免“大家都在改 prompt，但没人知道哪版有效”。

---

## 18. 风险清单与应对策略

### R1：官方规则变动

信号：

- 官方页面更新
- Zulip 通知

应对：

- 每周至少一次规则同步
- 关键规则变动当天更新文档和 checklist

### R2：评测模型公布较晚，导致押错方向

信号：

- `2026-04-10` 前后官方公布模型家族

应对：

- 前期用多家族 proxy
- 不在单模型上过拟合

### R3：把 cheatsheet 当唯一优化对象，忽略模板

信号：

- 规则内容看起来不错，但官方界面表现差

应对：

- 所有实验都保存 complete prompt
- 模板与规则分开版本化

### R3.1：误把官方样例 prompt 当作可直接部署的本地 strict prompt

信号：

- 引入官方样例后，输出突然变长，出现 `REASONING`、`PROOF`、`COUNTEREXAMPLE`
- 解析成功率下降，或 DeepSeek 在 smoke 集上出现新的格式性不稳定

应对：

- 官方样例只作为“结构参考”，不直接进入主线
- 先做 strict 改写版，再进入固定切分评测
- 在实验记录中显式区分“官方原型复刻”与“主线 prompt 迭代”

### R4：公开题过拟合

信号：

- dev 集持续涨，holdout 不涨

应对：

- 冻结切分
- `audit` 集少用
- 只接受 holdout 有提升的版本

### R5：解析失败或 placeholder 错误

信号：

- 输出带解释
- placeholder 未替换

应对：

- 建立自动 parser 测试
- 尽早用 playground 验证
- 把 placeholder 兼容性测试列为 Day 1 阻塞项

### R6：压缩过度，规则不可读

信号：

- 小模型准确率下降
- 某些规则在不同模型下理解不一致

应对：

- 为压缩版保留原始可读版
- 只在结构冻结后做重压缩

### R7：FALSE 识别长期偏弱

信号：

- TRUE accuracy 高，FALSE accuracy 低

应对：

- 单独建设 false-filter 规则簇
- 把 FALSE 作为单独优化目标

### R8：强模型生成的规则存在幻觉

信号：

- 写出来的规则听起来合理，但无法在数据上复现

应对：

- 强模型只做候选，不做真理源
- 任何规则入库前必须过样例验证

### R9：时间滑坡

信号：

- 截止前一周还在大改结构

应对：

- `2026-04-11` 后冻结大结构
- 后期只允许局部改动

### R10：单人连续作战导致实验记录失控

信号：

- 不知道哪一版是最好的

应对：

- 每日实验表
- 每版 release note
- 候选 prompt 统一命名

---

## 19. 提交前检查清单

提交前必须逐项确认：

- 团队成员资格合规
- 本次提交版本号已冻结
- 已保留主版本和备用版本
- cheatsheet 字节数 `<= 10KB`
- complete prompt 已在官方环境试跑
- placeholder 语法正确
- 输出只包含目标布尔值
- 不含依赖外部工具的指令
- 不含题目级硬编码答案
- 已记录本地最终评测结果
- 已截图保存提交证据

---

## 20. 建议的版本命名规则

建议采用如下命名：

- 模板：`T1.0`, `T1.1`
- cheatsheet：`C1.0`, `C1.1`
- complete prompt：`P1.0.0 = T1.0 + C1.0`

例如：

- `P0.1.0`
  - 第一版原型
- `P0.3.2`
  - 第三轮探索后的第二次局部修补
- `P1.0.0-rc1`
  - 第一版发布候选
- `P1.0.0-final`
  - 最终提交版

---

## 21. 建议的实验日志模板

每次实验建议记录：

```text
Experiment ID:
Date:
Goal:
Hypothesis:
Base version:
Change summary:
Models:
Data split:
Metrics:
Main errors:
Decision:
Next action:
```

长期看，实验日志和 prompt 本身一样重要。

---

## 22. 最终建议：如何理解这场比赛的最优打法

这场比赛最像的不是“数学竞赛”本身，也不是“训练大模型”，而是：

`受强约束的知识压缩与提示协议设计`

因此最佳推进方式应当是：

1. 先搭建工程闭环，而不是先追高分
2. 先建立 baseline，而不是直接写终版规则
3. 以 complete prompt 为优化对象，而不是只盯 cheatsheet
4. 以固定切分评测为裁决标准，而不是凭直觉修改
5. 重点建设 FALSE 识别、解析稳定性、压缩质量
6. 把官方样例 prompt 视为高价值参考原型，但只通过受控支线做 strict 蒸馏与适配
7. 在 `2026-04-10` 官方模型公布后做一次方向校正
8. 在 `2026-04-11` 后冻结大结构，避免最后一周失控

如果严格按本文档推进，最终你得到的不只是一个提交物，而是一套：

- 可复现的 prompt 研发流程
- 可回滚的版本体系
- 可解释的规则资产
- 可直接衔接 Stage 2 的知识沉淀

这会比“随手写一份 cheatsheet 然后不断试”更稳，也更接近工程化竞赛的正确打法。
