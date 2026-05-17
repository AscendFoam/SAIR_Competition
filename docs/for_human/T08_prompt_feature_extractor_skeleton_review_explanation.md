# T08 Prompt Feature Extractor Skeleton — Review Explanation

## 一、这个任务在做什么（通俗版）

上一个任务 T07 做了"人工体检"——有人逐条阅读 9 份考试攻略（prompt），按照一份 27 项的检查表，手工标记每份攻略的结构特征。但这有一个问题：**只有人能做这件事**。如果以后多了几十份新攻略，全部手工标记太慢、太累、容易不一致。

T08 的目标就是把这 27 项检查表中**最核心、最适合自动化的 7 项**变成程序。这样以后来一份新攻略，跑一遍程序就能自动得到这 7 项的结构画像，剩下的 20 项仍然需要人工判断。

打个比方：T07 是请了一位专家给 9 位学生做了详细体检报告（27 项指标全测）。T08 是造了一台自动体检机，目前只能测 7 项基本指标（身高、体重、血压、心率……），但速度快、可重复、不疲劳。这台机器不替代专家，但可以在专家到来之前先做一轮快速筛查。

同时，T08 顺手修了一个文档小错误——上一个任务里文档写的是"取整方法 A"，但实际数据用的是"取整方法 B"。现在文档和数据统一了。

## 二、任务实现的详细解释

### 2.1 任务目标

T08 的核心目标是将 T07 的人工 taxonomy 转化为可重复运行的最小代码骨架（extractor skeleton），具体包括：

1. 实现一个 extractor 入口，可对 text-ready local prompt 产出结构化 features
2. 输出字段与 `prompt_features_v1.jsonl` 的 schema 兼容
3. 至少覆盖一组高价值、可规则化、在 9 条样本上有区分度的字段
4. 提供 focused tests 验证 extractor 输出正确性
5. 统一 token estimate 文档口径（`floor` → `round`）
6. 撰写 extractor note 说明覆盖状态和局限性

### 2.2 任务流程

Worker 的工作流程大致如下：

**Step 1：实现核心提取模块 `prompt_features.py`**

新建 `src/sair_competition/analysis/prompt_features.py`，包含：

- **长度特征**：基于字节数和 token 估算值（`round(bytes/4)`）进行分桶。桶边界与 taxonomy YAML 完全一致（short/medium/long/near_cap）。
- **verdict_contract**：通过检测 "exactly one token"、"single token"、"VERDICT: TRUE/FALSE" 等关键词判断输出契约严格度。
- **rule_or_heuristic_block**：通过检测 "Mandatory TRUE checks"、"override"、"Fast TRUE/FALSE" 等关键词判断规则块密度。
- **opening_strategy**：通过检测 "Counterexample-first"、"Balanced solve"、"singleton collapse" 等关键词判断开局策略。
- **counterexample_requirement**：通过检测 "counterexample-first policy"、"falsification"、"counterexample search/construct" 等关键词判断反例要求程度。
- **explicit_final_token**：通过检测 "exactly one token"、"single token" 判断是否要求单 token 输出。

这 7 个字段的选择有明确的理由：
- 2 个长度字段是最基础的结构度量，纯数值计算，完全可靠。
- 5 个文本字段都有明显的、在当前 9 条 corpus 中已验证的 keyword pattern。
- 其余 20 个字段要么缺乏可靠的 keyword pattern（如 `ambiguity_handling`），要么在当前 corpus 上无区分度（如 `finite_model_search_hint` 全为 false），因此暂时留为 placeholder。

**Step 2：实现数据类和批量提取**

定义 `ExtractedFeatures` dataclass，包含全部 27 个 taxonomy 字段。7 个 rule-ized 字段由提取逻辑填充，19 个 placeholder 字段返回 `unknown`/`None`。`extraction_version` 标记为 `T08_v1_skeleton`。

实现三种提取入口：
- `extract_features(prompt_id, prompt_text)`: 从文本字符串提取
- `extract_features_from_file(prompt_id, file_path)`: 从磁盘文件提取（使用 `read_bytes()` 保证字节数准确）
- `extract_features_from_corpus(corpus_path)`: 从 corpus JSONL 批量提取，自动跳过非 text-ready 记录

**Step 3：添加 CLI 入口**

在 `cli.py` 中新增 `extract-prompt-features` 命令，支持两种模式：
- Single-prompt 模式：`--prompt-path` + `--prompt-id`，输出 JSON 到 stdout
- Batch 模式：`--corpus-path`，提取所有 text-ready 记录，可选 `--output-path` 写入 JSONL

**Step 4：编写 focused tests**

新建 `tests/test_prompt_feature_extractor.py`，共 90 项测试：
- Schema/parseability 测试（5 项）
- 长度分桶边界值测试（5 项）
- 核心字段与 manual coding 对齐测试（63 项 = 9 prompts × 7 fields）
- Boundary gate 测试（4 项）
- 完整 round-trip 测试（1 项）
- Byte count 一致性测试（1 项）

**Step 5：修复 token estimate 文档口径**

将 `taxonomy_v1.md` 中的 `floor(prompt_bytes / 4)` 改为 `round(prompt_bytes / 4)`，同步修改 `prompt_feature_taxonomy.yaml` 中的 `estimation_method`。数据值未变，只是文档描述与数据统一。

**Step 6：撰写 extractor note 和更新文档**

- `extractor_v1_notes.md`：详细记录覆盖状态、已知分歧（P2.0.2）、低方差字段、CLI 用法、与 T09 的关系。
- 更新 `README.md` 反映 T08 完成状态。
- 更新 `docs/07_handoff.md` 添加 T08 执行结果。

### 2.3 关键代码/配置变化

| 文件 | 变化 |
|---|---|
| `src/sair_competition/analysis/prompt_features.py` | 新增，约 308 行。核心提取模块，包含 7 个 rule-ized 字段的提取逻辑、数据类和三种提取入口。 |
| `src/sair_competition/analysis/__init__.py` | 更新，导出 extractor symbols。 |
| `src/sair_competition/cli.py` | 更新，新增 `extract-prompt-features` CLI 命令（单 prompt 和批量模式）。 |
| `tests/test_prompt_feature_extractor.py` | 新增，约 338 行。90 项 focused tests。 |
| `reports/research/taxonomy/extractor_v1_notes.md` | 新增，约 137 行。覆盖状态、已知分歧和低方差字段说明。 |
| `reports/research/taxonomy/taxonomy_v1.md` | 更新，1 行。`floor` → `round`。 |
| `reports/research/taxonomy/README.md` | 更新，反映 T08 完成状态和文件清单。 |
| `configs/research/prompt_feature_taxonomy.yaml` | 更新，1 行。`estimation_method` 加入 `round()`。 |
| `docs/07_handoff.md` | 更新，添加 T08 执行结果、更新 worker 边界和未验证事项。 |

### 2.4 对后续开发的意义

1. **T09 (Self-Audit)**：T08 的 extractor output 与 manual coding 的对比为 T09 提供了直接的审计素材。唯一分歧（P2.0.2 `counterexample_requirement`）是需要 T09 裁决的边界案例。

2. **T10 (Screening Matrix)**：有了 extractor，未来新增 prompt 候选时可以快速自动获取 7 项基本特征，辅助 screening 筛选。但 screening 决策仍应基于 manual coding。

3. **论文贡献**：extractor 是论文贡献 C2 (Prompt Feature Taxonomy) 的工程实现部分。它使得 taxonomy 不仅是人工标注的静态快照，而是一个可重复、可扩展的工具。

4. **语料扩展**：当未来 corpus 从 9 条扩展到更多 prompt 时，extractor 可自动覆盖 7 个核心字段，减少人工编码工作量。但 worker 也诚实指出 keyword heuristic 可能需要针对新 prompt 调整。

5. **Scope honesty 示范**：T08 的实现方式是一个很好的示范——明确标注 skeleton 而非 full automation，保留 placeholder 而非伪造结果，记录分歧而非掩盖。这种诚实的工程态度对后续任务的 scope 控制有正向影响。

## 三、为什么给出 PASS 的 review 结果

### 检查结果总结

| 检查维度 | 结果 | 说明 |
|---|---|---|
| 任务目标是否完成 | 是 | 全部 5 项交付物均已产出 |
| 是否有伪实现/mock | 否 | 7 个字段基于 keyword/pattern 匹配，19 个字段诚实返回 unknown/None |
| 是否越界修改 | 否 | 所有修改文件均在 allowed list 内 |
| 是否违反 forbidden scope | 否 | 未动 corpus 数据、prompt 原文、task board |
| 文档是否过度宣称 | 否 | 明确标注 skeleton、不替代 manual coding、低方差字段不主导 |
| 验证是否充分 | 是 | 90 项 focused tests + CLI smoke + cross-check，对于 skeleton 来说充分 |
| 是否破坏已有功能 | 否 | validate-layout 通过，已有测试不受影响 |
| Token estimate 口径 | 已统一 | floor → round，文档与数据一致 |

### 唯一需要关注的已知分歧

P2.0.2 `counterexample_requirement` 存在 extractor (absent) vs manual (optional) 的分歧。这不是 bug——extractor 的 keyword heuristic 确实无法检测该 prompt 中隐含的 counterexample-like 推理。该分歧已充分记录在 `extractor_v1_notes.md` 和测试注释中，留给 T09 裁决。

### 总体判断

T08 的执行质量高、范围控制严格、scope honesty 出色。Worker 没有把 skeleton 写成 full automation，没有掩盖 extractor 的局限性，没有让低方差字段成为成功标准。Token estimate 文档口径的收口干净利落。所有交付物都为 T09 和后续任务留下了清晰、可复核的输入。PASS。
