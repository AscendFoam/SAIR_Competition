# T03 Prompt Corpus Candidate Register - 通俗解释

## 这个 Task 在做什么？

### 背景

SAIR Stage1 数学推理竞赛已经结束。项目从"参赛提交"切换到了"后赛事实证科研"。这意味着我们不再追求"谁的 prompt 分数高"，而是要把 Stage1 当成一个公开的 prompt 文本蒸馏研究平台——研究 prompt 的结构、长度、模块顺序、内容来源如何影响模型的表现和鲁棒性。

要做这样的研究，首先需要一个**清晰的候选 prompt 清单**。就像做菜之前先把所有食材列出来一样，我们需要把所有可能用到的 prompt 列出来，并标注每个 prompt 的来源、存储状态、是否可以复算、版权状态等信息。

T03 就是建立这个"食材清单"的第一步。

### 具体做了什么

Worker 建立了第一批 prompt 候选登记表（candidate register v0），共登记了 11 个候选 prompt，包括：

1. **本地历史 prompt（9个）**：项目中已有的一组 prompt 文件，从最简 baseline（P0）到最终提交版（P1.2.5）再到各种变体。这些文件的哈希值和字节数都是从实际文件计算的真实值，经 reviewer 独立验证完全正确。

2. **外部公开 prompt 占位符（2个）**：代表未来可能纳入的 GitHub 上的公开 prompt 和官方贡献者网络中的 prompt。由于这些外部来源的 URL、作者、许可状态尚未核验，当前只做"只有元数据"或"只有结构信息"的记录，不复制原文。

同时，Worker 还编写了详细的**来源管理规则**（provenance rules），定义了：
- 来源类型（本地、官方、GitHub、论文、贡献者网络、社交媒体）
- 存储资格（哪些可以存全文，哪些只能存元数据）
- 复算资格（哪些可以直接重跑评测，哪些需要先审许可）
- 公私资产边界（不混入未公开的私有 prompt）
- 归因政策（每个公开 prompt 必须保留来源和作者信息）
- 后赛事项规则（已公开的评测子集只能用于"后赛事实证分析"）

### T01/T02 Review 的清理项

此外，Worker 还修复了前两个任务 review 中指出的轻量问题：

- **`outline.md` 绝对路径修正**：论文大纲中有一个指向 `D:/Codes/Math/...` 的绝对 Windows 路径链接，已改为相对路径 `contribution_list.md`。
- **`contribution_list.md` 增加 rejected claim 示例**：新增了 C8 条目，明确标注为 `unsupported_do_not_claim`，表示"继续大规模搜索 prompt 冲击排行榜"这个方向已被排除，不能作为论文贡献。这是一个反例声明，提醒后续写作不要把不该声称的东西写进论文。

### 代码变化与配置变化

本次任务没有修改任何代码（`src/`）或测试（`tests/`），也没有改动 prompt 原文。变化集中在数据和文档层：

| 文件 | 变化 |
|---|---|
| `data/interim/prompt_corpus/candidate_register_v0.jsonl` | 新建，11行候选登记 |
| `data/interim/prompt_corpus/provenance_rules.md` | 新建，来源管理规则 |
| `data/interim/prompt_corpus/prompt_corpus_manifest.json` | 更新，记录候选登记状态 |
| `data/external/prompt_corpus/raw_index.example.jsonl` | 已存在（T01 创建），本次未改动内容 |
| `reports/research/corpus_audit/summary.md` | 更新候选登记统计 |
| `reports/paper/outline.md` | 修正绝对路径链接 |
| `reports/paper/contribution_list.md` | 增加 C8 rejected claim |
| `docs/07_handoff.md` | 更新为 T03 已执行待 review |

### 对后续开发的意义

这个候选登记表是后续一系列任务的基础：

- **T04** 将核验外部候选的真实来源 URL、作者和许可状态。
- **T05** 将把这些候选规范化为正式的 corpus schema，去重，生成缺失元数据报告。
- **T07** 将为每个候选做结构标注（taxonomy），描述它的模块组成、顺序、输出格式等特征。
- **T10-T12** 将用这个候选池跑小样本筛选实验，选出 3-5 个代表性 prompt。
- 最终，这些 prompt 的结构和表现数据将支撑论文的核心分析。

简单说，T03 搭好了"数据货架"，后续任务才可以在上面放东西、做分析。

## Review 结果解释

### Verdict: PASS

本次 review 的结论是 **PASS**（通过）。理由如下：

1. **任务目标全部完成**：候选登记了 11 个 prompt（任务要求 8-12 个），覆盖了所有 5 个必须包含的 prompt，加上 baseline、本地对照和外部占位符。来源管理规则写清了全部 7 个必要主题。

2. **没有伪实现**：所有本地 prompt 的哈希值和字节数都是从实际文件计算的真实值，经独立验证完全正确。外部占位符诚实地标注为"无原文、无 URL、无许可确认"，没有编造数据。

3. **没有越界**：8 个改动文件全部在允许列表内。没有修改代码、测试、prompt 原文、配置文件。没有下载外部数据、没有跑 API 评测。

4. **状态诚实**：manifest 明确标注 `candidate_register_v0_not_cleaned`，corpus_size 仍为 0。没有把候选登记表写成已完成的 corpus。

5. **Hygiene 清理到位**：绝对路径链接已修正，rejected claim 示例已添加。

有一个非阻塞的小事项：`data/` 目录下的文件因为 `.gitignore` 规则不会被 git 跟踪。Worker 已经如实报告了这个问题。这需要项目负责人后续决定是否需要调整 git 策略，但不影响任务本身的完成质量。
