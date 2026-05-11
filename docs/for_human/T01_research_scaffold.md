# T01_research_scaffold：通俗解释与 Review 说明

## 一、这个 Task 在做什么（通俗解释）

SAIR 项目之前是在参加一个数学推理竞赛（Stage1），用精心编写的 prompt（提示词）让大模型判断代数等式是否成立。参赛阶段已经结束，现在项目要转型：不再追求"刷分"，而是把这段参赛经历变成一篇学术研究。

要写研究论文，首先需要一套研究基础设施——就像盖楼之前要先搭脚手架一样。T01 就是这个"搭脚手架"的任务：

- 创建存放研究数据的目录结构
- 定义数据格式的模板文件（比如 prompt 语料的登记表长什么样）
- 定义 prompt 结构分类体系（taxonomy）的初始版本
- 定义评测实验的三阶段模板
- 写论文大纲初稿
- 更新交接文档，说明当前进度

这个任务**只搭架子、不填数据**——所有文件都是空模板或示例记录，没有一个字假装"实验已经做完了"。

## 二、实现细节

### 任务目标

按照 [docs/tasks/phase_0_research_setup/T01_research_scaffold.md](docs/tasks/phase_0_research_setup/T01_research_scaffold.md) 的要求，创建 5 类产出：

1. **研究配置种子文件**（3 个 JSON/YAML 文件）
2. **Prompt 语料目录**（README + 示例索引 + manifest）
3. **报告脚手架**（6 个子目录的 README/summary 草稿）
4. **论文大纲 v0**（outline.md）
5. **交接文档更新**（docs/07_handoff.md）

### 具体文件变化

#### configs/research/（研究配置模板）

| 文件 | 作用 |
|------|------|
| [README.md](configs/research/README.md) | 目录说明 |
| [corpus_sources.example.json](configs/research/corpus_sources.example.json) | prompt 语料来源登记模板，定义了 6 种来源类型（official / contributor_network / github / paper / local / social），给出 3 个示例来源 |
| [prompt_feature_taxonomy.yaml](configs/research/prompt_feature_taxonomy.yaml) | prompt 结构特征分类体系 v0，覆盖 7 大类（长度特征、结构模块、模块顺序、反例策略、TRUE 策略、输出稳定性、来源追踪），每类 3-6 个字段 |
| [evaluation_matrix.example.json](configs/research/evaluation_matrix.example.json) | 三阶段评测矩阵模板（screening / recomputed benchmark / post-release analysis），每个阶段定义了 prompt 集合、数据集、模型配置、必需指标和数据泄漏注意事项 |

#### data/external/prompt_corpus/ 和 data/interim/prompt_corpus/（语料目录）

| 文件 | 作用 |
|------|------|
| [raw_index.example.jsonl](data/external/prompt_corpus/raw_index.example.jsonl) | 3 条示例记录，演示语料索引格式，每条都有 `example_only: true` 标记 |
| [prompt_corpus_manifest.json](data/interim/prompt_corpus/prompt_corpus_manifest.json) | 语料清单文件，明确标注 `status: "seed_scaffold_not_collected"`，corpus_size 为 0 |

#### reports/research/（研究报告目录）

6 个子目录各自有 README 或 summary 草稿：
- corpus_audit/summary.md — 语料审计报告模板
- taxonomy/README.md — taxonomy 报告说明
- screening/README.md — 筛选评测说明
- full_eval/README.md — 完整评测说明
- statistical_analysis/README.md — 统计分析说明
- figures/figure_notes.md — 论文图表备注

#### reports/paper/（论文目录）

| 文件 | 作用 |
|------|------|
| [outline.md](reports/paper/outline.md) | 论文大纲 v0，包含工作标题、核心主张、6 个研究问题（RQ1-RQ6）、5 项贡献、10 节论文结构、7 张计划图表、当前证据状态（全部标记为"未开始"）和"尚不支持的结论"列表 |

#### docs/07_handoff.md（交接文档更新）

更新了 3 处状态说明：任务状态从"Ready for worker"改为"Worker 已完成 / 待 reviewer 审查"；Worker 执行边界改为过去时态描述；未验证事项列表更新为当前实际状态。

### 对后续开发的意义

T01 建立的研究脚手架是后续所有任务的基石：

- **T02-T03**（Milestone 0 剩余任务）将基于这个脚手架填充真实的 prompt 语料和精炼论文大纲
- **T04-T06**（Milestone 1 语料收集）将使用 `corpus_sources.example.json` 和 `raw_index.example.jsonl` 定义的格式来登记和索引真实 prompt
- **T07-T09**（Milestone 2 taxonomy）将基于 `prompt_feature_taxonomy.yaml` 做手工标注和 feature extractor 开发
- **T10-T12**（Milestone 3 筛选评测）将基于 `evaluation_matrix.example.json` 配置和运行实验
- 论文大纲中的 RQ 和 section skeleton 直接指导后续所有实验设计和论文写作

### 验证方式

Worker 报告所有验证通过。本次 review 独立重新验证：

1. `validate-layout` CLI 通过 — 新目录不破坏现有布局
2. 3 个 JSON 文件均可被 `json.tool` 正确解析
3. JSONL 文件 3 行均可被 `json.loads` 解析，且都有 `example_only: true`
4. YAML 文件可被 `yaml.safe_load` 解析，覆盖全部 7 个必需 taxonomy 大类

## 三、为什么给出 PASS 的 Review 结果

### 判定理由

1. **任务目标全部达成**：任务包要求的 5 类产出全部落地，18 个允许文件路径都有对应内容。

2. **无伪实现**：所有文件都明确标注为 scaffold/seed/example，没有把模板伪装成真实数据。manifest 写着 `corpus_size: 0`，outline 写着"planning scaffold，非结果定稿"，每个 JSONL 示例都有 `example_only: true`。

3. **无越界修改**：`src/`、`tests/`、`prompts/complete/`、`artifacts/`、`docs/04_task_board.md` 均无变更。T01 未被标记为完成。

4. **Taxonomy 覆盖度足够**：YAML 文件覆盖了任务包要求的全部 7 个大类（length features、structural modules、module order、counterexample strategy、TRUE strategy、output stability、provenance and public-work relation），字段设计合理，可用于后续手工标注。

5. **后赛事纪律合规**：所有涉及 released final evaluation subsets 的地方都标注了 `post-release analysis`；evaluation matrix 明确规定不得在这些子集上调参后宣称盲测泛化。

6. **验证完整**：任务包要求的验证命令（validate-layout、JSON 解析、JSONL 解析）全部通过，且本次 review 独立复验确认。

### 发现的非阻塞问题

发现 4 个小问题（详见 review 文档），均不影响 scaffold 的使用：一个 `repeats` 字段类型问题、一个 storage_policy 拼写、taxonomy 字段命名与实验计划略有差异、以及少数实验计划中列出的字段在 YAML 中被合并或省略。这些都是后续 Phase 2 可以在手工标注时解决的细节问题。

综合判断：T01 作为 Phase 0 的脚手架任务，完成质量达标，给予 **PASS**。
