# Rank 274 Cheatsheet Performance Analysis

日期：2026-05-12

## 1. 文档目的

本文档分析你在公开榜单中的记录：

- team: `AscendFoam`
- rank: `274`
- cheatsheet size: `3.91 KB`
- avg accuracy: `51.6%`
- avg F1: `31.3%`
- parse success: `100.0%`
- avg cost: `$0.00009`

并回答四个问题：

1. 为什么你的 cheatsheet 表现不够好，但平均成本极低。
2. 为什么有些几乎空白的 cheatsheet 反而能比你更好。
3. 为什么有些 `9 KB` 左右的 cheatsheet 仍然会比你差。
4. 为什么榜首方案表现明显更强，它和你的 `P1.2.5` 到底差在哪。

本文依据四类材料：

- [docs/statistics_table.jsonl](docs/statistics_table.jsonl)
- [relative_papers/Less is more.md](relative_papers/Less%20is%20more.md)
- [docs/项目工作历程与阶段性成果总结.md](docs/%E9%A1%B9%E7%9B%AE%E5%B7%A5%E4%BD%9C%E5%8E%86%E7%A8%8B%E4%B8%8E%E9%98%B6%E6%AE%B5%E6%80%A7%E6%88%90%E6%9E%9C%E6%80%BB%E7%BB%93.md)
- 你补充的两张 leaderboard 截图，以及你提供的榜首 cheatsheet 文本

需要说明：

- `statistics_table.jsonl` 给的是榜单聚合指标，不含逐题预测，因此关于“为什么错”的一部分结论来自 prompt 结构分析和你本地实验记录。
- 你在仓库中的 `P1.2.5` 工作副本与最终冻结件一致，因此这里把 [prompts/complete/P1.2.5_minimal_rule_missing_hard_composition.txt](prompts/complete/P1.2.5_minimal_rule_missing_hard_composition.txt) 视为你的官方提交近似代表。

## 2. 先给出结论

最核心的结论有四条：

1. 你的 `P1.2.5` 不是“太长所以变差”，而是“用 3.9KB 自然语言启发式，把模型推到了一个很便宜、很快、但判别边界很脆弱的决策模式”。
2. 你的低成本主要不是因为“你比别人更高效地完成了同样的推理”，而是因为你要求模型只输出一个 token，并允许它在很浅的启发式层面就提前收敛，不必外显解析、规则轨迹或反例说明。
3. 几乎空白的 cheatsheet 有时更好，不是因为“空白本身神奇”，而是因为在这类任务里，额外提示如果不能提供稳定、可执行、可校验的结构特征，反而会干扰模型已有的内部先验；`Less is more` 的主张和你的榜单数据都支持这一点。
4. 榜首方案的强，不在于它“更长”，而在于它把 prompt 从“自然语言劝导”变成了“显式解析 + 特征提取 + 顺序规则 + 仿射探针 + 回退决策树”的准分类器。它的每一段字节都更像判别程序，而你的很多字节更像原则说明。

一句话概括：

> 你的 prompt 更像“让模型凭印象做一个受约束的快速判断”，榜首 prompt 更像“逼模型先把式子结构化，再按一个手工设计的判别器执行”。

## 3. 你的榜单记录到底处在什么位置

### 3.1 全榜中的相对位置

从 `docs/statistics_table.jsonl` 看，你这条记录有两个很显眼的特征：

- 成本极低：`$0.00009`，在 `312` 条记录里大约是第 `2` 便宜。
- 表现偏低：`51.6% accuracy / 31.3% F1`，大约只处在全榜 `12.5%` 分位附近。

换句话说：

- 你的成本几乎是全榜最低档。
- 你的精度和 F1 也几乎是全榜最低档。

这意味着你的方案不是“低成本下保持了不错性能”，而更像是“用极低成本换来了明显不够强的判别能力”。

### 3.2 和同尺寸 cheatsheet 的对比

把 `3.5 KB ~ 4.5 KB` 视作你的近邻区间：

- 该区间共 `36` 条记录
- 平均 accuracy: `54.78%`
- 平均 F1: `45.22%`
- 平均 cost: `$0.00045`

而你的记录是：

- accuracy: `51.6%`
- F1: `31.3%`
- cost: `$0.00009`

也就是：

- 你比同尺寸组平均低约 `3.2` 个 accuracy 点
- 你比同尺寸组平均低约 `13.9` 个 F1 点
- 但你的成本只有同尺寸组平均的大约 `1/5`

这说明：

- 你的低成本是真低成本，不是统计噪音。
- 但这份低成本对应的是明显更弱的判别深度和更差的标签平衡。

### 3.3 和几乎空白 cheatsheet 的对比

对于 `<= 0.2 KB` 的极短 cheatsheet：

- 平均 accuracy: `51.68%`
- 平均 F1: `37.8%`
- 平均 parse: `96.32%`

你的记录：

- accuracy: `51.6%`
- F1: `31.3%`
- parse: `100.0%`

这很关键：

- 你的 accuracy 几乎等于“极短 cheatsheet”组的平均水平。
- 但你的 F1 还低于极短组平均。

也就是说，你的 `3.91 KB` prompt 在最终效果上，并没有明显跑赢“几乎什么都不写”的方案；它只是在 parse 上更稳、在成本上更低。

这不是长度优化成功，而是“额外内容没有转化成稳定的判别收益”。

## 4. 为什么你的 cheatsheet 成本这么低

这是最容易误读的一点。

很多人会直觉认为：

> cheatsheet 小，所以便宜。

但你的数据告诉我们，事情没有这么简单。

### 4.1 成本不是只由 cheatsheet 大小决定

全榜里：

- baseline 只有 `0.46 KB`，平均成本却是 `$0.00048`
- 你是 `3.91 KB`，平均成本却只有 `$0.00009`

如果成本只由 prompt size 决定，这种现象很难出现。

因此更合理的解释是：

- 成本由输入 token 决定
- 也由输出 token 决定
- 还很可能由模型是否展开较长推理路径决定

也就是说，成本更像：

> 输入长度 + 输出长度 + 实际推理轨迹长度

而不是单纯：

> cheatsheet 字节数

### 4.2 你自己的截图几乎直接说明了原因

你补充的截图里，你的 prompt 在三模型上的平均成本大约是：

- Gemma 4 31B IT: `$0.00012`
- GPT-OSS 120B: `$0.00006 ~ 0.00007`
- Llama 3.3 70B: `$0.00009`

而榜首的对应成本大约是：

- Gemma 4 31B IT: `$0.00079 ~ 0.00082`
- GPT-OSS 120B: `$0.00046 ~ 0.00050`
- Llama 3.3 70B: `$0.00051`

也就是说，榜首通常比你贵大约 `6x ~ 8x`。

这和两份 prompt 的输出契约完全一致：

- 你的 `P1.2.5` 要求“第一行只输出一个 token：`true` 或 `false`”
- 榜首 prompt 要求先写四个 `PARSE` 行，再写规则轨迹，再写 `VERDICT / REASONING / PROOF / COUNTEREXAMPLE`

这会直接导致：

- 榜首 completion token 更长
- 榜首必须真的展开结构解析
- 榜首更难用“直觉一跳”直接结束

因此你的低成本，很大一部分来自：

1. 输出极短
2. prompt 允许模型很早停机
3. prompt 没有强迫模型把结构信息显式展开

### 4.3 你的 prompt 本身也在鼓励“快速收敛”

你的 `P1.2.5` 有几条关键指导：

- “先跑 mandatory TRUE checks”
- “如果 mandatory collapse rule fires，立即输出 true”
- “如果没有 TRUE checks 命中，且看不到短推导，就选 false”

这三句的组合效果非常强：

- 先给模型一个很快的正向出口
- 再给模型一个很快的负向出口
- 中间没有要求它系统地枚举结构特征、验证多个判别器或输出反例轨迹

这很像一个“早停式启发式路由器”。

它的好处是：

- 快
- 便宜
- parse 很稳

它的坏处是：

- 一旦前几个启发式偏了，后面没有足够机制纠偏
- 模型更容易用模糊的“像不像”而不是稳定的结构判别来结束决策

所以你的低成本，不是免费午餐，而是和“浅层决策”绑定在一起的。

## 5. 为什么你的表现不好

### 5.1 你的 `P1.2.5` 本来就不是“均衡主线”，而是“高召回挖掘支线”

从 [docs/项目工作历程与阶段性成果总结.md](docs/%E9%A1%B9%E7%9B%AE%E5%B7%A5%E4%BD%9C%E5%8E%86%E7%A8%8B%E4%B8%8E%E9%98%B6%E6%AE%B5%E6%80%A7%E6%88%90%E6%9E%9C%E6%80%BB%E7%BB%93.md) 可以看出：

- `P1_2_3` 是稳态、保守、false 侧强的主分支
- `P1_2_5` 是为了补回 `true` 漏判而开出的高召回支线

你本地 `smoke` 上：

- `P1_2_3`: accuracy `0.5469`，true acc `0.2258`，false acc `0.8485`
- `P1_2_5`: accuracy `0.5781`，true acc `0.6452`，false acc `0.5152`

这说明 `P1_2_5` 的设计目标从一开始就不是“平衡且稳健”，而是：

- 救回更多 true
- 接受 false 侧损失

也就是说，它更像一个“高召回规则发现器”，不是天然适合直接拿去做多模型统一提交的 prompt。

### 5.2 你的 prompt 有明显的单侧偏置风险

你的 prompt 中，真正强约束的内容主要集中在：

- 一组 TRUE collapse checks
- 一组比较宽泛的 FALSE heuristics

问题在于：

- TRUE 规则相对具体，而且很多带“立即输出 true”
- FALSE 部分更多是自然语言上的“如果明显更强、如果没有短推导、如果像是更具体形状”

这会产生一个不对称：

- 正向触发是硬规则
- 负向触发很多时候只是弱直觉

这种结构在某些模型上会把 prompt 推成：

- 要么过早放行 TRUE
- 要么在没有强结构 scaffold 的情况下，回落到默认 false

两边都容易形成偏置。

### 5.3 你的 prompt 缺少“显式结构化中间层”

榜首 prompt 的第一大优势不是内容更“聪明”，而是它强制模型先做结构化解析：

- 每个 side 的 fully parenthesized shape
- vars set
- occ counts
- op count
- bare side
- leftmost / rightmost variable
- left/right depth

这是非常关键的。

因为这类任务真正稳定的信号往往不是自然语言直觉，而是：

- 左右边界是否保持
- 变量集合是否变化
- 计数奇偶性是否变化
- bare side 与 product side 的关系
- 某些浅层结构是否映射到投影、仿射、常值等行为

你的 prompt 没有要求模型把这些特征显式写出来，只是说：

- 比较变量集
- 看有没有 lone variable
- 看 substitution / renaming
- 如果 same LHS 可以做 brief self-composition

这让模型“知道你想让它看结构”，但没有被迫把结构真正算出来。

结果就是：

- 结构计算变成隐式、可跳过
- 模型更容易凭表面印象替代特征计算

### 5.4 你的 FALSE 侧缺少硬分离器和硬探针

榜首方案里有几类很强的 FALSE 机制：

- `S1-S5`: separator rules
- `A1-A10`: affine probes
- `H1-H6`: heuristic rejects
- `B1/B2a/B2b/B2c`: fallback decision tree

尤其 `S1-S5` 非常重要：

- `LP(A) and not LP(B) -> FALSE`
- `RP(A) and not RP(B) -> FALSE`
- `SET(A) and not SET(B) -> FALSE`
- `XOR(A) and not XOR(B) -> FALSE`
- `AB(A) and not AB(B) -> FALSE`

这些规则不是“像不像更强”这种模糊语言，而是明确的结构不变量分离器。

再往后，`A1-A10` 甚至用小模数仿射模型做 cheap falsifier probe：

- 如果 Eq1 在某个小模型下恒成立
- 但 Eq2 在同模型下不成立
- 那么直接 FALSE

这本质上是在 prompt 里手工塞进了一个小型的“程序化反例检测器”。

你的 `P1.2.5` 没有这种层级的 FALSE 证据机制。

所以一旦 TRUE checks 没命中，你只能让模型在“更强 / 更具体 / 没有短推导”这些比较模糊的线索上做判断。

这会直接伤害 F1，尤其是跨模型 F1。

### 5.5 你的 prompt 很依赖模型自己补全“短推导”

你的关键 fallback 是：

- “If no short rewriting or substitution path is visible after the TRUE checks, prefer false.”

这句话很短，但副作用很大。

它实际上把一个最难的部分外包给了模型自己的隐式能力：

- 什么叫 short
- 什么叫 visible
- 什么叫 substitution path
- 什么叫 composition obvious

不同模型会有完全不同的内部解释。

于是同一 prompt 在不同模型上容易出现：

- 某模型觉得“显而易见”，于是过度判真
- 某模型觉得“不够显然”，于是过度判假
- 某模型干脆退化成单标签输出

这也是你截图里跨模型表现分化这么大的原因之一。

## 6. 你补充的两张图说明了什么

这两张图很有价值，因为它们把“官方三模型表现轮廓”直接展示出来了。

## 6.1 榜首不是单模型偶然爆点，而是结构上更可迁移

榜首的三模型三数据集表现大致是：

| Model | normal Acc/F1 | hard Acc/F1 | extra_hard Acc/F1 |
| --- | --- | --- | --- |
| Gemma 4 31B IT | `85.7 / 84.8` | `81.8 / 82.5` | `60.7 / 64.2` |
| GPT-OSS 120B | `88.3 / 88.1` | `82.0 / 83.4` | `62.5 / 66.6` |
| Llama 3.3 70B | `50.2 / 36.5` | `63.0 / 55.6` | `48.0 / 23.3` |

这个轮廓说明：

- GPT-OSS 和 Gemma 上都很强
- Llama 虽然明显更弱，但并没有完全塌成单标签
- 它的跨模型迁移不是完美，但明显是“仍可用”的

## 6.2 你的 prompt 在 GPT-OSS 和 Llama 上出现了明显失衡

你的截图是：

| Model | normal Acc/F1 | hard Acc/F1 | extra_hard Acc/F1 |
| --- | --- | --- | --- |
| Gemma 4 31B IT | `61.8 / 71.2` | `54.8 / 68.7` | `30.0 / 46.2` |
| GPT-OSS 120B | `50.3 / 18.1` | `52.8 / 18.9` | `63.7 / 50.7` |
| Llama 3.3 70B | `49.5 / 1.3` | `51.0 / 6.4` | `50.0 / 0.0` |

这组数非常值得注意：

- 你的 Llama accuracy 接近随机，但 F1 几乎归零
- 这几乎就是单标签塌缩的信号
- GPT-OSS 在 normal/hard 上 accuracy 也接近随机，但 F1 非常低

这意味着：

- 你的 prompt 不是简单地“做得不够好”
- 而是在某些模型上把判别边界推成了非常不平衡的输出行为

特别是：

- `extra_hard` 上 GPT-OSS accuracy `63.7` 甚至略高于榜首的 `62.5`
- 但 F1 只有 `50.7`，比榜首低 `15.9` 点

这说明：

- 你的某些 split 上 accuracy 偶尔不差
- 但这不是一个健康的、平衡的判别器
- 它更像是利用了 split 分布，或者在某一类标签上赌对了更多样本

换句话说：

> 你的 prompt 偶尔能拿到看起来还行的 accuracy，但它没有稳定地学会“何时判真、何时判假”，而榜首更接近一个平衡分类器。

### 6.3 这和 `Less is more` 的核心结论是同向的

`Less is more.md` 的几个重要结论正好能解释这组现象：

- prompt 长度和效果不是单调关系
- 更复杂的规则系统会降低跨模型可迁移性
- ordering effect 非常强
- 很多局部最优 prompt 在换 split 或换 provider 时会崩

你的截图给出的最强信号是：

- 你的 prompt 在不同模型上并没有保持稳定的标签平衡
- 榜首至少在 GPT-OSS / Gemma 上做到了强稳定，在 Llama 上也没有完全塌缩

这说明榜首方案的强，不只是“规则更多”，而是“规则更结构化、更可执行、更少依赖模型自己脑补”。

## 7. 为什么几乎空白 cheatsheet 有时会更好

这件事表面反直觉，其实很符合这个任务的本质。

### 7.1 因为这个任务里，“额外文字”不等于“额外有效结构”

如果额外文字只是：

- 一些广义的数学常识
- 一些模糊的判断原则
- 一些看似合理的 guardrail

那它带来的可能不是新能力，而是：

- 干扰注意力
- 给模型更多互相冲突的软约束
- 让模型更早进入错误的启发式分支

在这种情况下，短 prompt 反而有优势，因为它：

- 没有过度干扰基座模型已有的内部先验
- 让模型按自己最熟悉的方式做推断
- 避免了“半懂不懂地执行复杂规则”

### 7.2 你的 prompt 就存在“加了东西但没变成程序”的问题

你的 `3.91 KB` 不是空的，但也不是一个显式可执行的 classifier。

它处于一个中间态：

- 比极短 prompt 多了很多规则意图
- 但这些规则又没有被编码成硬特征和硬规则链

于是最坏的情况就是：

- 你既没有保留基座模型最自然的判断方式
- 也没有给模型足够强的显式程序来约束它

这就会出现：

> 比空 prompt 复杂很多，但还不够结构化，因此“多出来的内容”主要制造了干扰，而不是稳定收益。

### 7.3 `Less is more` 也明确观察到这个现象

论文里最关键的一个经验判断是：

- 有些非常短的 prompt，在强模型上与复杂 prompt 的差距并不大
- 甚至在跨模型迁移时更稳

这不是因为“少就是好”，而是因为：

- prompt 只能在模型已有能力边界内做路由
- 它不能凭空教会模型完整数学
- 当 prompt 超过模型的稳定执行能力后，继续加内容只会进入 cognitive load collapse

所以：

- 短 prompt 胜出时，往往不是它信息更多
- 而是它干扰更少

## 8. 为什么有些 `9 KB` 左右的 cheatsheet 还是会比你差

这同样不能简单用“长就更好”理解。

### 8.1 全榜统计只显示“弱正相关”，不是决定性关系

在全榜上：

- cheatsheet size 和 accuracy 的相关系数约为 `0.218`
- cheatsheet size 和 F1 的相关系数约为 `0.218`
- cheatsheet size 和 parse rate 的相关系数几乎为 `0`

这说明：

- 更长的 prompt 平均略有帮助
- 但帮助很有限
- 长度本身几乎不解释 parse 成败

换句话说，长度只解释了很小一部分方差。

真正决定效果的是：

- 这些字节编码了什么结构
- 规则之间是否一致
- 是否能跨模型执行
- 是否过拟合某个 split

### 8.2 长 prompt 有两种完全不同的类型

同样是 `9 KB` 左右，可能有两种本质不同的 prompt：

1. 判别性字节多
   - 结构特征
   - 明确规则链
   - 小模型反例探针
   - 明确 fallback

2. 说明性字节多
   - 冗长原则
   - 模糊启发式
   - 多个互相竞争的规则
   - 没有可执行中间表征

榜首属于第一种。

很多表现差的 `9 KB` prompt 很可能属于第二种，或者属于：

- 对某个 split 局部过拟合
- 对某个模型能跑，对另一个模型直接过载

### 8.3 榜单里已经能看到长 prompt 的失败样本

例如 `>= 9 KB` 组里虽然均值比全体略好，但底部仍然有很多明显失败例子：

- `Hrushikesh Pawar`: `42.0% / 37.2%`
- `Zer00logy`: `46.9% / 39.2%`
- `Eva 00`: `51.8% / 27.1%`
- `rndsrc`: `51.9% / 14.4%`

也就是说：

- 长 prompt 不是不会崩
- 它只是更有机会在“信息密度高、规则编码好”的情况下跑出来

一旦规则冲突、顺序错误、字节浪费在说明文字上，它照样会很差。

## 9. 榜首方案为什么这么强：它和你的 `P1.2.5` 区别到底在哪

这一节是最关键的。

## 9.1 不是“长短差异”，而是“架构差异”

下面这张表可以概括你和榜首的根本区别：

| 维度 | 你的 `P1.2.5` | 榜首方案 |
| --- | --- | --- |
| prompt 大小 | `3.91 KB` | `9.83 KB` |
| 输出契约 | 只输出 `true/false` 一个 token | 强制输出 parse、规则名、proof/counterexample |
| 核心范式 | 自然语言启发式 router | 显式 parse-first classifier |
| 中间表示 | 隐式 | 显式 |
| TRUE 侧 | 少量 collapse / substitution 规则 | identity / collapse / forced behavior / contradiction motifs |
| FALSE 侧 | 模糊 stronger-shape heuristics | separators + affine probes + heuristic rejects |
| fallback | “看不到短推导就 false” | Layer B 决策树 |
| 模型依赖 | 很强，依赖模型自己理解“短推导” | 较弱，更多依赖显式可计算特征 |
| 成本 | 极低 | 明显更高 |

### 9.2 榜首先强制 parse，再允许判定

榜首 prompt 最重要的设计是：

> Step 0 不是可选的，而是 mandatory parse。

这很强，因为它逼模型先把四个 side 变成结构对象：

- shape
- vars
- occs
- op count
- bare
- leftmost / rightmost variable
- left/right depth

这一步把任务从“凭感觉看两个式子”变成了：

- 先做结构抽取
- 再做规则判别

这实际上是在 prompt 内手工制造一个“中间表示层”。

你的 `P1.2.5` 没有这层。

所以你的模型在很多时候并不是“算完结构再判断”，而是“直接在原式上做受 prompt 引导的印象判断”。

### 9.3 榜首的规则是 typed rules，你的规则更像 prose rules

榜首的很多规则是 typed 的：

- `LP`, `RP`, `SET`, `XOR`, `AB`
- `kind(E)`
- `shortest_len(E)`
- `occ(E)`
- `rhsCounts`
- `topShape`
- `xTop`

这些都是离散特征。

一旦特征算出来，后续规则就变成：

- if condition -> TRUE/FALSE

这会带来两个好处：

1. 模型执行时歧义更小
2. 多模型之间更容易共享同一个 decision surface

你的规则更多是 prose style：

- clearly stronger
- extra symmetry
- more specific shape
- no short derivation visible
- clear same-left-hand-side composition

这些表达很适合作为人类写作说明，但不适合作为跨模型稳定执行的判别器。

### 9.4 榜首的 FALSE 机制更“硬”

榜首最大的优势之一，是它并不把 FALSE 判定主要交给“感觉像不成立”。

它有三层硬机制：

1. 不变量分离器
   - `LP/RP/SET/XOR/AB`
2. 小模数仿射探针
   - `A1-A10`
3. fallback tree
   - `B1/B2a/B2b/B2c`

这三层都非常像程序。

你的 `P1.2.5` 没有这种程度的 FALSE machinery。

因此你的 FALSE 决策更依赖模型语义直觉，而榜首更多依赖结构判别和 cheap falsifier。

### 9.5 榜首的 fallback 远强于你的 fallback

你的 fallback 本质上是：

- 如果 TRUE checks 不命中
- 且看不到短 derivation
- 那就 false

这是一个很弱的 fallback，因为它没有真正把“未命中规则的空间”继续细分。

榜首的 Layer B 则是一个小决策树：

- 先计算 `M`
- 再看 `S`
- 再看 `V`
- 然后落到 `B1/B2a/B2b/B2c`

这意味着：

- 即使前面所有显式规则都没命中
- 榜首仍然有一个结构化、可重复的 fallback

这对降低“最后几步靠模型脑补”非常关键。

### 9.6 榜首不是更像“数学解释器”，而是更像“手工特征分类器”

这点非常重要。

榜首并不是在要求模型：

- 真正做严谨代数证明
- 真正搜索所有可能 counterexample

它更像是在让模型执行一个手工设计的结构分类器。

这和 `Less is more` 里的 router hypothesis 非常一致：

> 在这类任务里，prompt 真正能稳定提升的，往往不是“让模型学会数学”，而是“把题目路由到一组结构模式上”。

榜首方案比你的强，不是因为它更会“讲道理”，而是因为它更彻底地把任务变成了 pattern classification。

### 9.7 榜首的成本高是有原因的，而且这部分成本很多是“必要成本”

榜首比你贵 `6x ~ 8x`，主要来自：

- 更长的输入 prompt
- 更长的输出格式
- 更强制性的结构展开

这部分成本不是纯浪费。

它买来的东西是：

- 更稳定的中间表示
- 更少的歧义空间
- 更好的跨模型可迁移性
- 显著更高的 F1

当然，这不意味着必须照搬 `9.83 KB`。

真正该学的是：

> 不是把 prompt 变长，而是把 prompt 的字节尽可能变成“判别结构”。

## 10. 你和榜首相比，最本质的失分点是什么

如果把问题压缩到一句话，我会这样说：

> 你输的不是知识点数量，而是“决策边界的可执行性”。

更具体地说，有五个核心失分点：

1. 你没有强制 parse-first。
2. 你没有把关键结构特征 typed 化。
3. 你没有足够强的 FALSE hard evidence。
4. 你的 fallback 太依赖模型自己判断“短推导可见不可见”。
5. 你的 prompt 是高召回支线思路，不是跨模型平衡 classifier 思路。

因此最终结果是：

- parse 很稳
- cost 很低
- 但标签平衡性很差
- GPT-OSS / Llama 容易塌
- accuracy 偶有看起来还行的 split，但 F1 不健康

## 11. 这对后续 prompt 设计有什么启发

如果你后面要继续做下一版，不建议简单走这两条老路：

- 继续给 `P1.2.5` 加几条自然语言规则
- 或者简单把榜首整个 `9.83 KB` 风格照抄

更好的方向是：

1. 保留你“低成本、短输出”的优点，但增加一个更轻量的 parse-first scaffold。
2. 把现在的 TRUE / FALSE prose heuristics 改写成 typed features + ordered rules。
3. 明确加入少量硬 separator，而不是只写“Equation 2 looks stronger”。
4. 给 fallback 一个小决策树，而不是“没看出短推导就 false”。
5. 区分“研究用高召回支线 prompt”和“正式提交用平衡 classifier prompt”，不要让两者目标混在一起。
6. 如果要控制成本，优先压缩输出格式和无效解释文本，而不是牺牲中间结构层。

一句更直接的设计建议是：

> 下一版最值得尝试的，不是“更长”或“更短”，而是“更程序化但仍然足够轻”。

也就是：

- 不必像榜首那样输出整套大块 parse 文本
- 但至少要让模型在内部或极短外显格式里，先算出几个硬特征，再判定

## 12. 最终判断

综合榜单、论文、项目总结、你补充的截图和榜首 prompt 结构，我的最终判断是：

- 你的 `P1.2.5` 是一个典型的“局部有效、低成本、高召回倾向、但跨模型很脆”的 prompt。
- 它能在某些场景下补回真例，符合你本地实验里“高召回挖掘支线”的定位。
- 但它不是一个成熟的多模型稳健 classifier，所以 rank `274` 这个结果并不意外。
- 你的低成本大多来自“短输出 + 早停启发式”，不是来自“同等推理质量下的优化”。
- 榜首方案真正领先的地方，是把任务从自然语言启发式改造成了准程序化的结构分类器。

如果把一句话作为这份文档的结尾，我会写：

> 你的 `P1.2.5` 更像一个便宜的启发式路由器；榜首方案更像一个昂贵但有效的手工特征分类器。前者胜在快，后者胜在判别边界稳定，而比赛成绩最终更奖励后者。

## 13. 追加附录：`P1.2.5`、`rank33`、`rank1` 原文逐段精读

这一附录回答你新提出的问题：不仅要比较三份 prompt 的总体风格，还要尽量贴着原文，按“每行或每段”的粒度分析它们各自到底在做什么。

说明：

- 对较短的 `P1.2.5`，我基本按行块分析。
- 对较长的 `rank33` 与 `rank1`，我按段落和规则块分析；对于关键规则，再单独拆开。
- 下面的“好/坏”不是在评价数学正确性本身，而是在评价它们作为 leaderboard cheatsheet 时，对模型行为的约束方式、可执行性、稳定性和成本结构。

## 14. 你的 `P1.2.5` 逐行精读

原文：`prompts/complete/P1.2.5_minimal_rule_missing_hard_composition.txt`

### 14.1 第 1 行

`You are solving an equational implication problem over magmas.`

这一行只是角色设定，作用是把模型拉进题型语境。它有两个特点：

- 好处：非常短，不浪费字节。
- 局限：它没有指定“怎么解”，只指定“你在解什么”。

也就是说，这一行只建立主题，不建立算法。

### 14.2 第 3-4 行

`Task:`  
`Determine whether Equation 1 implies Equation 2.`

这两行继续做任务定义，清楚但极简。问题在于：

- 它把任务说清了；
- 但没有把任务拆成可执行的步骤。

因此模型是否会去做 parse、找不变量、找反例、做重写，完全取决于它自己的内部习惯。

### 14.3 第 6-8 行

`Semantics:`  
`- Output true if and only if every magma satisfying Equation 1 also satisfies Equation 2.`  
`- Output false if there exists at least one magma satisfying Equation 1 but not Equation 2.`

这三行是语义金线，定义本身正确，也很重要，因为它在提醒模型：

- `TRUE` 是全称蕴含；
- `FALSE` 是存在性反例。

但它仍然是“语义层定义”，不是“求解层算法”。  
也就是：模型被提醒了判定标准，却没有被迫提供判定证据。

### 14.4 第 10-14 行

`Output contract:`  
`- Return exactly one token on the first line.`  
`- Allowed outputs: true or false.`  
`- Do not write labels, markdown, explanations, or extra text before the answer.`  
`- If you reason internally, do not reveal it.`

这是整份 `P1.2.5` 最关键的一段之一，因为它几乎直接决定了你的“低成本 + 高脆弱性”。

- 第 11-13 行极强地压缩了输出空间，这对 `parse success=100%` 非常有利。
- 第 14 行把全部推理都推回模型内部，不允许它外显中间结构。

这带来的收益是：

- completion 极短；
- 格式极稳；
- 成本极低。

这带来的代价是：

- 没有外显 parse，就没有“被迫算结构”的约束；
- 没有外显 rule trace，就没有“被迫按规则执行”的约束；
- 模型可以在一个非常浅的启发式层面提前结束。

从 prompt 工程角度看，这一段不是中性的格式要求，而是在主动鼓励早停。

### 14.5 第 16-25 行

`Use the following cheatsheet if helpful:`  
`Decision semantics:`  
`- TRUE means every magma satisfying Equation 1 must also satisfy Equation 2.`  
`- FALSE means there exists at least one magma satisfying Equation 1 but not Equation 2.`  
`Output discipline:`  
`- The final visible answer must be a single token: true or false.`  
`- Run the mandatory TRUE checks before using any conservative false heuristic.`  
`- If a mandatory collapse rule fires, answer true immediately and do not let later guardrails override it.`  
`- If none of the TRUE checks fire and no short derivation is visible, choose false.`

这里真正重要的是后半段。

- `if helpful` 这三个词其实偏弱。它意味着下面规则更像建议，不像硬执行协议。
- “先跑 mandatory TRUE checks”会把模型决策顺序强行偏向 `TRUE` 侧。
- “collapse rule fires 就立即 true”给 `TRUE` 开了硬出口。
- “看不到 short derivation 就 false”给 `FALSE` 开了软出口。

这就是 `P1.2.5` 的核心控制结构：

1. 先找几个高召回 `TRUE` 触发器；
2. 命中就立即放行；
3. 否则如果没有短证据，就回落 `FALSE`。

这个结构的优点是快，缺点是高度依赖模型主观判断：

- 什么叫 “mandatory”；
- 什么叫 “short derivation”；
- 什么叫 “visible”；
- 什么时候可以认为没有必要再查。

`rank1` 的强，恰恰就在于它把这些主观词几乎全换成了 typed features 和 rule names。

### 14.6 第 27-32 行：Mandatory TRUE checks

这一块是你整份 prompt 的“正向放行器”。

#### 第 28 行

`Singleton-collapse rule ... Output true immediately ...`

这一行是最强、最安全、也最有价值的 `TRUE` 规则之一。  
它本质上抓的是“裸变量等于不含该变量的项”导致 singleton collapse。

优点：

- 数学上强；
- 很多真实真例会被这条救回；
- 解释力高。

风险：

- 需要模型先正确识别“变量是否出现在另一侧”；
- 但你没有强制它显式列变量集，因此这步仍是隐式做的。

#### 第 29 行

`Symmetric singleton rule ...`

这是第 28 行的镜像版，属于必要补全。  
它的存在说明你已经意识到“方向性”不能成为误差源。

这条是好规则，几乎没什么 prompt 级副作用。

#### 第 30 行

`Disjoint-sides collapse rule ...`

这条规则是你 prompt 里“收益高，但也容易过宽”的代表。  
它试图把“左右变量完全不相交”解释成某种强 collapse 现象。

问题不在动机，而在表达方式：

- 它是自然语言概括，不是带可检查条件的 typed rule；
- 模型如果没先显式算变量集，很容易在复杂式子里错判“是否 disjoint”；
- “treat this as collapse law”这种措辞，给了模型很强的放行暗示。

所以这条更像“高召回矿灯”，不像“高精度判别器”。

#### 第 31 行

`Constant-operation rule ... In a constant magma, any equation whose two sides both contain * is true. Output true.`

这条是你 prompt 里最像“小定理模板”的一条。  
它的意图很清楚：识别某些会强迫运算退化为常值的结构。

优点：

- 一旦成立，后续很多题确实会自动转真；
- 它解释了为什么 `P1.2.5` 特别擅长救某些 true-heavy 家族。

问题：

- 这条仍然没有一个强制 parse scaffold；
- “binary term on one side and disjoint variable set on the other side” 这种条件，在隐式判断时仍可能漂移。

#### 第 32 行

`Substitution-instance rule ... output true.`

这是整块里最保守、最标准、最可靠的一条。

- 它几乎就是 syntax-level entailment shortcut；
- 很适合作为前置快筛。

如果 `P1.2.5` 只有这种规则，它会更保守，也更稳；现在的问题是它把这类安全规则和更宽的 collapse rule 放在同一层，且都设成“立即 true”。

### 14.7 第 34-38 行：Safe FALSE checks

这一段表面上叫 “safe FALSE checks”，但其实并不真的 “safe”；它们大多是合理启发式，不是硬分离器。

#### 第 35 行

`If Equation 2 is clearly stronger ... prefer false.`

最大问题在 `clearly stronger`。  
这是人类读者能懂、但模型不易稳定执行的表述。

- 什么算 stronger；
- stronger 是语法更强还是语义更强；
- 强多少才算 clearly。

所以它更像直觉标签，不像规则。

#### 第 36 行

`If Equation 2 introduces extra symmetry, idempotence, or a more specific shape ... prefer false.`

这条比第 35 行更具体一点，因为它点名了 symmetry / idempotence / specific shape。

但它仍然是“模式提醒”，不是“判别特征”。  
模型会被提醒去怀疑这类目标式，但不会被迫先算出离散结构量。

#### 第 37 行

`If Equation 1 reuses variables across both sides ... treat this as extra evidence for false ...`

这一行体现出你已经在利用“变量复用”作为结构信号，这比纯口语启发式更接近 feature engineering。

问题是：

- 这里的信号仍被写成 prose；
- “extra evidence” 不是判决条件；
- “unless a short exact derivation ... is obvious” 又把决定权退回给模型主观感受。

#### 第 38 行

`If no short rewriting or substitution path is visible after the TRUE checks, prefer false.`

这几乎就是 `P1.2.5` 最大的失分点。

因为它把最难、最不稳定的一步，直接外包给模型：

- 何为 short；
- 何为 visible；
- 何为 rewriting path；
- 何为 enough evidence。

`rank1` 的整个成功，某种意义上就是在避免出现这类句子。  
它宁可变长，也要把“看不看得出来”换成“特征是否满足”。

### 14.8 第 40-45 行：Reasoning discipline

`- First compare variable sets on each side of Equation 1.`  
`- Then check whether a side is a lone variable absent from the opposite side.`  
`- Then check whether Equation 2 is a direct substitution instance or renaming consequence of Equation 1.`  
`- If Equation 2 keeps the same exposed left-hand side as Equation 1, allow one brief self-composition check before falling back to false.`  
`- Only after those checks use structural-complexity heuristics.`

这一段其实是 `P1.2.5` 最接近“解题程序”的地方。

它的优点是：

- 先变量集；
- 再裸变量；
- 再 substitution；
- 再 same-LHS composition；
- 最后再用复杂度启发式。

这个顺序并不差，甚至可以看成一个轻量版 pipeline。

但它的致命不足是：

- 没有强制输出变量集；
- 没有强制输出裸变量判断；
- 没有强制输出 same-LHS composition 轨迹；
- 所以这些步骤都可能被模型跳过或模糊执行。

换句话说，`P1.2.5` 不是完全没有 pipeline，而是 pipeline 没有 externalization。

### 14.9 第 47-52 行：Anti-bias reminders

`- Do not use "Equation 2 has more variables" as a false signal ...`  
`- Do not default to false just because the equations look different syntactically.`  
`- A collapse law in Equation 1 can make many seemingly stronger Equation 2 laws automatically true.`  
`- In same-left-hand-side shared-variable equations, extra depth alone is not enough evidence for false.`  
`- In shared-variable equations, repeated x * x ... is not enough to justify true.`

这五行很有意思，它们像是你在和模型“打补丁”。

好处：

- 你已经知道模型会犯哪些偏差；
- 你在主动防止几类常见误判；
- 这说明 `P1.2.5` 不是随手写的，而是有实验反馈的。

坏处：

- 这些提醒是“不要这样”，不是“应该怎样做”；
- 它们能抑制部分偏差，但不能替代正向结构判别；
- 一旦与前面的 `TRUE`/`FALSE` 启发式冲突，模型未必知道谁优先。

所以这块更像 error patch list，不像统一决策体系。

### 14.10 第 54-57 行

`Equation 1: { equation1 }`  
`Equation 2: { equation2 }`  
`Final answer:`

这是标准注入位，配合前面的单 token 约束，进一步鼓励模型：

- 快速读题；
- 快速内部判断；
- 快速单词输出。

这会让它很适合“省钱 submit”，但不适合“强约束分类器”。

### 14.11 对 `P1.2.5` 的一句话归纳

如果把你的这份 prompt 压缩成一句工程画像，我会写成：

> 它不是一个真正的 rule engine，而是一个“带若干强 true triggers、若干弱 false heuristics、以及单 token 早停输出”的轻量启发式路由器。

这解释了三件事为什么同时出现：

- 成本极低；
- parse 极稳；
- 跨模型 F1 很脆。

## 15. `rank33.md` 逐段精读

原文：`docs/model_cheatsheet/rank33.md`

这份 prompt 和你的 `P1.2.5` 相比，已经明显更“solver-like”；但它仍然没有走到 `rank1` 那种 typed classifier 的程度。

### 15.1 第 1-3 行：角色设定与任务绑定

`You are a mathematician specializing in equational theories of magmas.`  
`Your task is to determine whether Equation 1 ... implies Equation 2 ...`

这一开头比你的 `P1.2.5` 更正式，也更强地把模型绑定到“数学判定者”身份。  
这类 persona 本身不会直接提高正确率，但会抬高模型对“需要解释、需要证明、需要反例”的预期。

### 15.2 第 8-17 行：Task Definition

这一段做了三件事：

- 定义输入是 `Eq1` 与 `Eq2`；
- 重申目标是全体 magma 上的蕴含；
- 最关键的是规定：`TRUE` 时给 proof sketch，`FALSE` 时给 finite counterexample 并验证。

这比 `P1.2.5` 强很多，因为它把“证据义务”引入了求解过程。  
也就是说，这份 prompt 默认不是让模型凭感觉二分类，而是让它生产 witness。

但它也埋下了成本上涨和 hallucination 风险：

- proof sketch 比单 token 长得多；
- finite counterexample 需要模型真去构造；
- 如果模型构不出来，它可能开始编。

### 15.3 第 21-31 行：Canonical Parsing & Normalization

这一段是 `rank33` 很扎实的地方。

- 解析为二叉树；
- 去掉无关空白；
- 变量按首次出现做 canonicalization；
- 比较时考虑 side swap、renaming、alpha-equivalent shape。

这说明作者已经非常清楚：这类题很多命中点，其实是 syntax-level invariant。

和你的 `P1.2.5` 相比，它更像在告诉模型：

- 不要只看表面词形；
- 要先做结构归一化；
- 再比较。

不过，这里仍然只有“指示”，没有外显结构槽位。  
所以模型理论上应该 parse，但并不被迫写出来。

### 15.4 第 35-48 行：Fast Decision Filters

这块把快筛分成了 `Immediate TRUE` 与 `Immediate FALSE`。

`Immediate TRUE` 三条：

- `Eq2` 左右相同；
- `Eq2` 只是 `Eq1` 的重命名或换边；
- `Eq1` collapse 到极强/投影型行为。

这三条思路都很正统，比你的 `P1.2.5` 更克制。  
它没有一上来就大面积暗示“看到某些 pattern 就立刻 true”，而是只给最经典的快筛。

`Immediate FALSE` 两条：

- 找到一个有限 magma 反例；
- 如果 model checker / candidate search 返回验证反例，就立即 false。

这两条非常强，因为它把 `FALSE` 建立在 witness 上，而不是建立在 “looks stronger” 上。

但它的问题也很明显：

- 它假设模型能像小型搜索器那样工作；
- 却没有给模型一个具体、廉价、强约束的搜索协议。

所以 `rank33` 比你的 `P1.2.5` 更严谨，但也更依赖模型自身推理质量。

### 15.5 第 52-79 行：Proof-Oriented Strategy

这一段是 `rank33` 的主心骨之一，分三层：

1. substitution/rewrite；
2. property extraction；
3. universalization/trivialization。

优点很明显：

- 它给了 `TRUE` 判定一个合理求证顺序；
- 比你的 `P1.2.5` 更强调“先证，再判真”；
- 还要求 concise but explicit。

尤其第 58-60 行“从 `Eq1` 建双向 rewrite 规则，尝试把 `L2` 重写到 `R2`”这一点，已经相当接近真正的 theorem-proving workflow。

但它的限制也很清楚：

- 没有限制重写深度如何选择；
- 没规定什么时候算 reachability 成立；
- 没要求输出具体的中间 canonical form。

所以它是一份“好方法论”，但不是“硬控制程序”。

### 15.6 第 82-108 行：Counterexample-Oriented Strategy

这一段比你的 `P1.2.5` 强很多，也是 `rank33` 能排到前列的重要原因之一。

它不仅说“优先找反例”，还进一步给出候选家族：

- 所有 `2x2` 表；
- left-zero / right-zero / constant；
- projection 与 near-projection；
- boolean-like 小表；
- modular-linear forms；
- random / hill-climbed tables。

这里的价值在于：

- 它把 `FALSE` 变成“有限模型搜索”问题；
- 它把模型注意力导向若干高收益家族；
- 它默认要求验证 `Eq1` 全赋值成立、`Eq2` 存在违反赋值。

这就是为什么 `rank33` 比你的 prompt 更像“严肃 solver”。

但它的局限也很真实：

- 它没有像 `rank1` 那样，把最常见的反例家族预压缩成固定 probe；
- 它仍然期待模型临场“找表 + 验证表”；
- 这一步既贵，又容易不稳定。

### 15.7 第 111-123 行：Heuristic Signals

这段其实很聪明，因为它明确说：

- heuristics 只是指导，不是替代 proof/counterexample。

列出的信号包括：

- subterm coverage；
- variable overlap；
- complexity gradient；
- rough strength ordering；
- rewrite reachability overlap。

这比你的 `P1.2.5` 更成熟，因为它区分了：

- “排序信号”；
- “决定性证据”。

但它也说明这份 prompt 仍然没有离开 “LLM as reasoner” 范式。  
它是在教模型怎么思考，不是在把 decision surface 写死。

### 15.8 第 127-145 行：Minimal Solve Pipeline + Failure Modes

这一段进一步把 workflow 组织成：

1. parse；
2. true filter；
3. rewrite proof；
4. finite model search；
5. heuristic ranking；
6. final verdict。

这是 `rank33` 很强的一点：它不是零散规则堆砌，而是完整 solve pipeline。

后面的 failure modes 也很有价值：

- 不要无 derivation 判真；
- 不要无 counterexample 判假；
- 不要把启发式当形式证明；
- 不要忘 side swap / renaming；
- 不要输出坏格式。

这类“错误禁止清单”能显著改善严谨性。

### 15.9 第 148-157 行：Output Template

这一段有一个非常值得注意的地方：

- 它要求输出 `VERDICT / MODEL_NAME / REASONING / PROOF / COUNTEREXAMPLE / OUTPUT_RESULT`；
- 但文末第 173-177 行又只要求 `VERDICT / REASONING / PROOF / COUNTEREXAMPLE`。

也就是说，这份 prompt 内部其实有轻微格式不一致。

这类不一致为什么重要：

- 强模型通常能自己协调过去；
- 弱一点的模型可能会犹豫到底输出哪套格式；
- 即便最终 parse 没崩，它也会增加一点执行噪声。

这很可能也是 `rank33` 没有继续向上冲到 `rank1` 那个层级的一个小原因：  
它的方法论不错，但契约没有 `rank1` 那么“像程序”。

### 15.10 第 161-169 行：Distilled Practice Rule

`When uncertain:`  
`- Prefer searching for a counterexample first.`  
`- If no counterexample appears ... attempt a structured proof.`  
`- Never return a final verdict without one of ...`

这一段等于给 `rank33` 定了一个总的偏好：

- 不确定时先找反例；
- 反例失败再去做 proof；
- 没 witness 不许给终局判断。

这让它比你的 `P1.2.5` 少了很多“主观短路”空间。  
你的 prompt 不确定时会掉进“没看出短推导就 false”；`rank33` 不确定时会掉进“继续找 witness”。

这就是两者的根本差别之一。

### 15.11 第 173-177 行：最终格式约束

这里再次强调：

- `VERDICT` 必须严格；
- `REASONING` 非空；
- `PROOF` / `COUNTEREXAMPLE` 二选一承担证据义务。

这说明 `rank33` 最终还是把自己定位成“witness-producing solver”，不是“cheap classifier”。

### 15.12 对 `rank33` 的一句话归纳

如果压成一句话，我会把 `rank33` 定义为：

> 一份强调 parse、proof、counterexample 和验证义务的通用型 formal-solver prompt。

它比你的 `P1.2.5` 强在：

- 更重证据；
- 更像解题流程；
- 更少纯口语式 `false` 启发。

它比 `rank1` 弱在：

- 没把结构特征 typed 化；
- 没把高频真/假模式预编译成 deterministic rule bank；
- 很多关键步骤仍然依赖模型临场“自己会做”。

## 16. `rank1.md` 逐段精读

原文：`docs/model_cheatsheet/rank1.md`

这份就是榜首风格的核心文本。  
和前两份相比，它最本质的变化不是“更长”，而是“更像一个手工实现的判别程序”。

### 16.1 第 1-5 行：任务设定 + deterministic classifier

`You are deciding whether source law A ... implies target law B ...`  
`A magma is ...`  
`Rules: deterministic classifier. Apply rules in order; stop at the FIRST that fires. Never invent witnesses. If no rule fires, apply the Layer B decision tree at the end.`

第 5 行是全篇灵魂。

因为从这一句开始，模型的身份就不是“会证明/会找反例的数学家”，而是：

- 一个顺序规则系统；
- 一个 first-match classifier；
- 一个有 fallback tree 的有限状态决策器。

这和 `rank33` 的差别非常大：

- `rank33` 让模型像 solver；
- `rank1` 让模型像 classifier。

leaderboard 上后者更成功，说明在这道题里，稳定的结构路由比临场求证更重要。

### 16.2 第 7-11 行：输出契约

`OUTPUT FORMAT — first write the PARSE block and brief rule trace ...`

这一段直接把高成本写进 prompt 了：

- 先写 `PARSE`；
- 再写 rule trace；
- 最后写四个固定行。

它的坏处是显然的：

- 贵；
- 长；
- completion 多。

但它买来的东西也非常明确：

- 模型必须显式 parse；
- 模型必须显式承认自己用了哪条 rule；
- 模型更难偷懒一跳结束。

所以榜首不是“高成本浪费”，而是“高成本换执行约束”。

### 16.3 第 13-33 行：Step 0 Mandatory Parse

这部分是 `rank1` 压过其他 prompt 的第一层核心。

它要求对 `A.L / A.R / B.L / B.R` 四个 side 都写：

- `shape`
- `vars`
- `occs`
- `op`
- `bare`
- `lm`
- `rm`
- `ldepth`
- `rdepth`

这一步的意义极大：

- 它把隐式结构理解变成显式结构抽取；
- 它把后续规则的输入统一成固定 feature slots；
- 它降低了不同模型对“结构”的自由解释空间。

尤其值得强调的是：

- `lm/rm` 为边界不变量服务；
- `ldepth/rdepth` 为投影型、路径型、仿射 shortcut 服务；
- `occs` 为计数与 parity 规则服务；
- `bare` 为裸变量/乘积分叉提供统一入口。

你的 `P1.2.5` 也在想这些东西，但只是提醒模型“去看一看”；榜首则要求“先把它们都算出来再说”。

### 16.4 第 35-51 行：Step 1 Features

这一段是在 parse 之上再做二级特征压缩。

它定义了：

- `vars(E)`、`size(E)`、`dup(E)`
- `LP(E)`、`RP(E)`
- `SET(E)`、`XOR(E)`、`AB(E)`
- `bare(E)`
- 若 `bare(E)`，再定义 `kind / shortest_len / occ`

这一步非常像手工 feature engineering。

尤其几个符号值得注意：

- `LP/RP`：左端点、右端点是否保持；
- `SET`：变量集合守恒；
- `XOR`：奇偶守恒；
- `AB`：逐变量计数完全守恒；
- `kind`：裸变量在 product 侧出现的路径类型；
- `shortest_len`：最浅出现深度；
- `occ`：出现次数。

这等于把“看结构”进一步离散化成“看布尔/小整数特征”。  
一旦做到这一步，后面的规则就不再是 prose，而是 if-condition。

### 16.5 第 53-57 行：Identity / Collapse (TRUE)

`X1` 到 `X3` 是第一层安全真例快筛。

- `X1`: `B.L = B.R` 语法相同，直接真。
- `X2`: `A` 与 `B` 同构，只差重命名/换边，直接真。
- `X3`: `A` 是 `x=y` 或者有一侧是裸变量且该变量不在另一侧，直接真。

这三条相当稳，而且和 `P1.2.5` 的强 true triggers 有亲缘关系。  
区别在于：

- `rank1` 先 parse，再基于结构触发；
- `P1.2.5` 是口语描述直接触发。

### 16.6 第 59-64 行：Forced Behavior

这一组 `F1-F4` 是榜首非常高价值的规则层。

- `F1`: `x = x*y` 强迫左投影 `a*b=a`，然后看 `LP(B)`。
- `F2`: `x = y*x` 强迫右投影 `a*b=b`，然后看 `RP(B)`。
- `F3`: 同左子、异右子，导向 `a*b=f(a)` 型一元依赖，再检查 `leftmost,left-depth`。
- `F4`: 同右子、异左子，导向 `a*b=g(b)` 型一元依赖，再检查 `rightmost,right-depth`。

这一层的厉害之处在于：

- 它不是一般性的“看起来像 projection”；
- 它是直接把某些 `Eq1` 模式编译成具体运算行为；
- 然后用极小的结构不变量去验证 `Eq2`。

这就是高信息密度字节。  
几行文字，换来的是一整类题的稳定判别。

### 16.7 第 66-89 行：Source Contradiction Motifs (TRUE)

这是榜首最“特征工程化”的部分，也是最像从公开题分布中蒸馏出来的 pattern bank。

先看第 68-74 行，它为这组 motif 定义了额外特征：

- `rhsVars`
- `rhsCounts`
- `Lx/Rx`
- `topShape`
- `xTop`
- `xCount`
- `square`

也就是说，`rank1` 不是停在通用 parse，而是继续为某个高价值题族建专门二级特征。

下面这些规则可以分别看：

- `C1`：`rhsVars=4` 且 `Lx=F, Rx=F`，抓的是大变量数、边界都不贴裸变量的强真型。
- `C2`：`rhsCounts="113"` 且双边界都不贴 `x`，抓某类高度不平衡计数真例。
- `C3`：`xTop=left + square + m-v`，这是非常具体的局部树型 detector。
- `C4`：`112` 计数、双边界不贴 `x`、`xTop=right`、`v-m`，针对特定右侧嵌入模式。
- `C5`：`1112` 版本的 `C4`，覆盖更宽变量配置。
- `C6`：三变量、`xTop=right`、`v-m`、`xCount=2`，抓右挂双出现。
- `C7`：三变量、双边界不贴 `x`、`xTop=left`、`m-v`、`xCount=2`，是 `C6` 的镜像偏左版本。
- `C8`：三变量、`Lx=T`、`xTop=left`、`m-v`，显式使用左边界贴合。
- `C9`：`122` 计数、`Lx=T`、`Rx=F`、`xTop=both`、`v-m`，是边界 + 计数 + 顶层切分的组合规则。
- `C10`：`122` 计数、`Lx=F`、`Rx=T`、`xCount=2`，对应另一种边界粘附模式。
- `C11`：`113` 计数、双边界不贴 `x`、`xTop=right`、`v-m`。
- `C12`：`113` 计数、双边界不贴 `x`、`xTop=left`、`m-v`。
- `C13`：`1112` 计数、`Lx=F`、`Rx=T`，是一个更粗的高频真型。
- `C14`：当 `B` 也是 bare 型时，若 `rhsCounts="113"` 且 `Rx=T` 且无 square，则直接真。

这整块说明了榜首方案一个非常本质的特征：

- 它不是单纯在写“数学原则”；
- 它是在写“高频成功子族的特征索引”。

风险当然也有：

- 这类规则更可能带分布特异性；
- 更像是从赛题生态中蒸馏出的经验模式；
- 如果换题域，可能掉得比通用 prompt 更快。

但在这次 leaderboard 上，这正是高分来源。

### 16.8 第 91-97 行：Separators (FALSE)

这五条是榜首最漂亮的 `FALSE` machinery 之一。

- `S1`: `LP(A)` 成立但 `LP(B)` 不成立，直接假。
- `S2`: `RP(A)` 成立但 `RP(B)` 不成立，直接假。
- `S3`: `SET(A)` 成立但 `SET(B)` 不成立，直接假。
- `S4`: `XOR(A)` 成立但 `XOR(B)` 不成立，直接假。
- `S5`: `AB(A)` 成立但 `AB(B)` 不成立，直接假。

这些规则的强处在于：

- 都是明确不变量；
- 都是 typed condition；
- 都是单步硬分离器；
- 完全不像“Eq2 looks stronger”那种模糊话。

如果只挑一块来说明为什么你的 prompt 会输，这五条已经够说明问题了。  
因为你的 `FALSE` 侧缺的正是这种“无争议硬证据”。

### 16.9 第 99-116 行：Affine Probes (FALSE)

这一段是榜首第二层大杀器。

第 101-102 行先定义了仿射小模型语义：

- `u*v = p*u + q*v + c (mod m)`
- 若 `A` 在该模型下恒真、`B` 不恒真，则直接假。

这等于把 prompt 内部塞进了一个廉价的、手工挑选的小模型反例探针库。

第 104-106 行的 `A1 shortcut` 更进一步：

- 直接把某类模型下的值简化为 `rightmost_leaf + right_depth mod 3`；
- 于是无需真正展开整棵求值树，就能快速 falsify。

第 108-111 行的 `A7 shortcut` 也是同一路数：

- 用左右分支数决定系数；
- 将一类反例检测压缩成路径计数。

第 113-116 行列出 `A1-A10` 探针族：

- `A1-A5` 主要是 mod 3 的不同线性型；
- `A6-A9` 转到 mod 4；
- `A10` 用 mod 5。

本质上，这一整块是在做：

- 小模型族覆盖；
- 低成本反例搜索；
- 人工选出的高收益 falsifier bank。

`rank33` 想做反例搜索，但把这件事交给模型临场完成；  
`rank1` 直接把一部分搜索结果预编译成固定 probe。  
这就是两者的层级差。

### 16.10 第 118-125 行：Heuristic Rejects

这一块虽叫 heuristic，但已经比一般 heuristics 硬得多，因为它完全建立在 typed features 上。

- `H1`: `kind(A)=M` 且变量多，而 `kind(B)=X`，判假。
- `H2`: `kind(A)=L`、`shortest_len=1`、重复多，且 `B` 也重复多但变量少，判假。
- `H3`: `kind(A)=M`、`occ(A)=2`、非 `RP`、且 `Lx(A)=F`，判假。
- `H4`: `shortest_len(A)=1` 且 `occ(A)=3`，无条件式强拒绝。
- `H5`: `kind(A)=M`、`shortest_len=3`、`occ=2`，判假。
- `H6`: `kind(A)=L`，但 `B` 有 `occ(B)=2` 且四变量，判假。

这一组说明：

- 榜首并不是所有规则都要求形式证明级别的正确性；
- 它也接受经验性 reject；
- 但即便经验 reject，也被写成了 typed pattern，而不是 prose intuition。

### 16.11 第 127-142 行：Layer B Decision Tree

这是榜首的第三层保险。

它先定义三个 fallback 整数：

- `M`：`Eq1` 中每个变量跨两侧的总出现次数的最小值；
- `S`：`Eq1` 左边的 `*` 数；
- `V`：`Eq1` 左边的不同变量数。

然后按树判：

- `B1`: 若 `M >= 2`，判假。
- `B2a`: 否则若 `M=1` 且左边是 bare，判真。
- `B2b`: 否则若左边是两变量单乘积，判真。
- `B2c`: 其余判假。

这块极其重要，因为它解决了一个常见问题：

- 如果所有精细规则都没命中，怎么办？

你的 `P1.2.5` 的答案是：

- “没看出短推导就 false”。

榜首的答案是：

- “落到一个仍然结构化、仍然 deterministic 的小决策树”。

这就是为什么它哪怕在 rule miss 区域，也比你的 prompt 稳得多。

### 16.12 第 144-178 行：Worked Examples

这一块容易被忽略，但其实很关键。

它给了四类示范：

- `F2` 真例；
- `A1` 假例；
- `B1` 假例；
- `B2a` 真例。

这些例子的作用不是增加知识点，而是：

- 教模型如何真的执行前面那套 parse/rule system；
- 把抽象规则变成 trace 模板；
- 降低模型误读规则的概率。

从成本上看，例子当然更贵；  
但从执行稳定性看，这些示范很可能贡献了大量收益。

### 16.13 对 `rank1` 的一句话归纳

如果压缩成一句话，我会这样定义榜首 prompt：

> 它不是在“教模型怎么想”，而是在“给模型一个近似手工编码的结构分类器，并要求它先算中间特征，再按规则顺序执行”。

这就是它为什么贵，但也为什么强。

## 17. 三份 prompt 的直接对照结论

如果把三份 prompt 放在一条轴上，它们大概是这样：

- `P1.2.5`：单 token、早停、true-trigger 偏强、false 侧偏口语的轻量启发式路由器。
- `rank33`：强调 parse、proof、counterexample、验证义务的通用 solver prompt。
- `rank1`：显式 parse + typed features + ordered rules + probe bank + fallback tree 的手工特征分类器。

它们对应三种完全不同的胜负逻辑。

### 17.1 为什么 `P1.2.5` 会落后于 `rank33`

不是因为你不会写规则，而是因为：

- 你不给模型外显证据义务；
- 你让模型可以非常早停；
- 你的 `FALSE` 决策很多靠 prose heuristic；
- 你的 fallback 是主观的 “看不出短推导”。

而 `rank33` 至少要求：

- parse；
- rewrite/proof；
- counterexample；
- validation。

即使它不如 `rank1` 程序化，它也比你的 prompt 更难“凭印象直接交卷”。

### 17.2 为什么 `rank33` 能到前列，但仍输给 `rank1`

因为 `rank33` 的核心范式仍然是：

- 让模型当 solver；
- 临场找 proof 或 counterexample。

而 `rank1` 的核心范式是：

- 让模型当 classifier；
- 先抽特征；
- 再跑规则；
- 必要时用廉价 probe falsify；
- 最后再走 fallback tree。

前者更通用，后者更像针对这类题和这类模型精心蒸馏过的决策边界。  
比赛结果更奖励后者。

### 17.3 为什么榜首方案比你的 prompt 贵很多，但这份成本大多不是浪费

因为它把很多本来会留给模型“脑补”的步骤，改成了显式执行：

- parse block；
- feature block；
- rule trace；
- probe logic；
- structured fallback。

这些步骤都会增加 token，尤其 completion token。  
但它们换来的不是“更会讲道理”，而是“更难乱判”。

### 17.4 对你最有价值的启发

如果只提炼一条对你后续最有用的结论，那就是：

> 你下一版最值得借鉴的，不是榜首的长度，而是它把隐式判断改成显式特征、把 prose heuristic 改成 ordered typed rules、把主观 fallback 改成结构化 fallback 的方式。

具体到工程上，最应该迁移的是：

- 轻量 parse-first scaffold；
- 少量硬 separator；
- 少量高收益 projection / unary-dependence detector；
- 一个真正的 fallback tree；
- 必要时加入 1-2 个极便宜的小模型 probe。

最不应该继续保留的，是：

- “if helpful” 这种软约束起手；
- “no short derivation is visible” 这种主观 fallback；
- 只靠 anti-bias reminders 修补、却不建设中间结构层。

如果把这一附录再压成一句话结尾，我会写成：

> `P1.2.5`、`rank33`、`rank1` 的差异，不是“写得多还是少”，而是“让模型凭感觉判断、让模型当 solver、还是把模型压成一个显式特征分类器”这三种范式差异；排行榜最终明显更偏爱第三种。
