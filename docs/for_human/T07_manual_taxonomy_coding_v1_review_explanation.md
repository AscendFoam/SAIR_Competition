# T07 Manual Taxonomy Coding — Review Explanation

## 一、这个任务在做什么（通俗版）

想象你有一堆「考试攻略」（prompt），每个攻略的写法、长短、侧重点都不一样。你想搞清楚：这些攻略到底有什么结构上的不同？哪些结构因素可能会影响考试分数？

T07 就是给 9 份本地可用的攻略做「结构体检」——人工阅读每份攻略的全文，按照一套预先定义好的分类标准（taxonomy），把每份攻略的结构特征逐一标记下来。比如：

- 这份攻略有多长？短 / 中 / 长 / 快到上限了？
- 它的规则是用纯文字写的，还是混了数学符号？
- 它是先教你怎么判断「对」还是先教你怎么判断「错」？
- 它有没有防止模型乱猜的「护栏」？
- 它的输出格式要求严不严格？

做完这件事后，我们就有了 9 份攻略的结构化画像，后续可以拿这些画像去做统计分析和自动化提取。

## 二、任务实现的详细解释

### 2.1 任务目标

T07 的核心目标是将 T06 确认的语料库边界转化为结构化输入，具体包括：

1. 对 9 条 text-ready（本地有全文的）prompt 做手工 taxonomy 编码
2. 为这 9 条记录补上 token 数量估算（之前全是 0）
3. 撰写 taxonomy 报告，说明编码池、字段定义和 feature 分布
4. 建立 experiment plan 6.2 节到 YAML schema 的映射表
5. 更新 handoff 文档

### 2.2 任务流程

Worker 的工作流程大致如下：

**Step 1：读取 prompt 全文并编码**

逐条阅读 9 份本地 prompt 文件的全文，按照 `prompt_feature_taxonomy.yaml` 中定义的 27 个字段进行手工编码。每个字段对应 prompt 的一个结构维度：

- **长度特征** (4-5 个字段)：byte 长度分桶、token 估算分桶、规则密度、压缩风格
- **结构模块** (6 个字段)：是否有任务框架、输出契约严格度、是否有分步推理、是否有示例等
- **模块顺序** (3 个字段)：开头策略、verdict 位置、示例是否在规则前
- **反例策略** (4 个字段)：反例要求程度、有限模型搜索提示、false 过滤倾向、CE 搜索深度
- **TRUE 策略** (3 个字段)：类证明支持强度、恒等式指导、歧义处理
- **输出稳定性** (3 个字段)：解析友好度、是否要求最终 token、格式冗余
- **来源关系** (3 个字段)：来源可信度、是否基于公开工作、发布前后关系

**Step 2：写入 `prompt_features_v1.jsonl`**

将编码结果写入新的 JSONL 文件，每条记录包含：prompt_id（用于关联回语料库）、27 个 taxonomy 字段值、manual_coding_note（编码说明）和 coder_note（编码者的补充说明）。

**Step 3：回填 token 估算**

在 `corpus_v1.jsonl` 中为 9 条 text-ready 记录补填 `prompt_tokens_est`，方法是用字节数除以 4 取整。2 条非 text-ready 记录（GitHub metadata-only 和 Contributor Network structure-only）保持 0 不变。

**Step 4：更新 taxonomy YAML**

在 seed scaffold 基础上新增：
- `compression_style`（自然语言 / 符号 / 混合）
- `ce_search_depth`（隐式 / 浅层 / 显式多步）
- `bucket_boundary_notes`（分桶边界文档）

**Step 5：撰写报告**

- `taxonomy_v1.md`：完整编码报告，包括编码池说明、token 估算方法、feature 分布、prompt 家族分组
- `taxonomy_mapping_note.md`：experiment plan 6.2 节每个字段到 YAML schema 的对应关系

### 2.3 关键配置/数据变化

| 文件 | 变化 |
|---|---|
| `prompt_features_v1.jsonl` | 新增，9 条记录，每条 27 个 taxonomy 字段 + 元数据 + 编码说明 |
| `corpus_v1.jsonl` | 9 条 text-ready 记录的 `prompt_tokens_est` 从 0 变为 bytes/4 估算值 |
| `prompt_feature_taxonomy.yaml` | 版本从 TAX_V1_SEED 升级到 TAX_V1_MANUAL_CODING，新增 3 个字段/节 |
| `taxonomy_v1.md` | 新增，约 210 行的编码报告 |
| `taxonomy_mapping_note.md` | 新增，约 133 行的映射表 |
| `taxonomy README.md` | 更新为反映 T07 完成后的状态 |
| `docs/07_handoff.md` | 更新 T07 执行结果和后续 worker 边界 |

### 2.4 对后续开发的意义

1. **T08 (Extractor Skeleton)**：有了 27 个字段的编码示例和详细的 mapping note，T08 可以据此设计自动化 feature extractor。每条记录的 `manual_coding_note` 和 `coder_note` 提供了编码决策的 ground truth 参考。

2. **T09 (Self-Audit)**：T07 只有单编码者，T09 应复核编码一致性和边界案例。

3. **T10 (Screening Matrix)**：有了 length bucket 和结构特征，T10 可以设计覆盖不同结构类型的 screening 候选集。

4. **论文贡献**：taxonomy 本身是论文的核心贡献之一（贡献 C2: Prompt Feature Taxonomy）。T07 的编码结果将为后续的统计分析（Spearman correlation、配对检验、回归模型）提供自变量。

5. **Milestone 2 推进**：T07 是 Milestone 2 的第一个任务，通过后才能安全进入 T08 和 T09。

## 三、为什么给出 PASS 的 review 结果

### 检查结果总结

| 检查维度 | 结果 | 说明 |
|---|---|---|
| 任务目标是否完成 | 是 | 全部 5 项交付物均已产出 |
| 是否有伪实现/mock | 否 | 27 个字段逐一阅读 prompt 全文后手工编码 |
| 是否越界修改 | 否 | 所有修改文件均在 allowed list 内 |
| 是否违反 forbidden scope | 否 | 未动 src/tests/prompts/artifacts，未跑 eval，未提升 non-text-ready 记录 |
| 文档是否过度宣称 | 否 | token estimate 诚实标注为启发式，未伪称精确计数；placeholder 字段明确标注为 deferred |
| 验证是否充分 | 是 | JSONL 格式校验、字段值合规性校验、text-ready gating 一致性、记录计数均通过 |
| 是否破坏已有功能 | 否 | corpus_v1.jsonl 仅新增 token 估算值和 notes 后缀，其余字段不变 |

### 唯一发现的小问题

Token 估算的文档描述为 `floor(bytes/4)`，但实际数据使用的是 `round(bytes/4)`（四舍五入）。例如 P0 的 511 bytes 得到 128 tokens（round），而 floor(511/4) = 127。差异在 ±1 以内，不影响 length bucket 分配，属于文档描述与数据实现的轻微不一致。这不需要阻止任务通过，但建议在后续任务中修正文档。

### 总体判断

T07 的执行质量高、范围控制严格、文档诚实完整。Worker 没有把计划写成事实，没有伪实现，没有越过 T06 boundary gate。所有交付物都为后续任务留下了清晰、可解析的输入。PASS。
