# T05: Normalize Prompt Corpus v1 — 通俗解释

## 一、这个 task 在做什么（通俗版）

T03 建了一份"候选登记表"（candidate register），T04 补齐了外部来源信息。但这些数据还是"原始登记"格式——字段不统一，有些关键语义模糊（比如"10 个可直接重算"到底是"本地有文本"还是"许可证允许但不一定有文本"？）。

T05 的工作就是把这份登记表**规范化（normalize）**，变成一个统一格式的、可以直接用于后续研究和评测的语料库（corpus v1）。

具体来说，T05 要做三件核心事：

1. **创建 corpus_v1.jsonl**：把 11 条候选记录统一为标准 schema，明确每一条是"文本就绪可以直接跑"（text_ready）、"只有元数据"（metadata_only）还是"只有结构信息"（structure_only）。
2. **生成去重报告和缺失元数据报告**：检查有没有重复的 prompt，列出哪些记录还缺关键信息。
3. **拆清计数**：把原来模糊的"10 个可直接重算"拆成 `eligible_count=10`（许可证允许重算）和 `text_ready_count=9`（本地文本已就绪可直接跑）。

另外，T05 还做了一个明确决定：**不把 GitHub 上 MIT 许可的 prompt 文件镜像到本地**。虽然许可证允许，但 T05 选择保持保守，等后续有明确需要时再处理。

## 二、任务实现详解

### 2.1 任务目标

T05 的核心目标是把 candidate register 从"登记簿"升级为"规范化语料库"，解决三个具体问题：

1. T04 review 指出的 `direct_recompute_count` 混合了"有资格"和"有文本"两种语义。
2. 缺少 duplicate report 和 missing metadata report。
3. `raw_index.example.jsonl` 的 schema 与实际 `raw_index.jsonl` 不对齐。

### 2.2 任务流程

**Step 1：创建 corpus_v1.jsonl**

Worker 把 11 条 candidate register 记录逐条转换为 corpus v1 schema。新 schema 增加了三个关键字段：

- `text_ready`：布尔值，表示本地是否已有文本可直接用于重算。
- `eligible_for_recompute`：布尔值，表示 provenance 和许可证是否允许重算（即使本地还没文本）。
- `corpus_inclusion_status`：枚举值（`included_text_ready` / `included_metadata_only` / `included_structure_only` / `excluded`）。

转换结果：
- 9 条本地记录 → `text_ready=true`, `eligible=true`, `included_text_ready`
- 1 条 GitHub 记录 → `text_ready=false`, `eligible=true`, `included_metadata_only`
- 1 条 Contributor Network 记录 → `text_ready=false`, `eligible=false`, `included_structure_only`

这个拆分直接解决了 T04 review 的核心关切：现在一眼就能看出哪些可以直接跑，哪些还需要额外操作。

**Step 2：生成 duplicate report**

`duplicate_report_v1.json` 检查了四种重复维度：
- SHA256 哈希重复 → 0
- 标准化来源 URL 重复 → 0
- candidate_id 重复 → 0
- prompt_id 重复 → 0

结论：当前无重复。报告还记录了一条有用的观察：目前 `prompt_id` 与 `candidate_id` 完全一致，如果未来一条 candidate 被拆成多个 prompt 文件，需要重新运行此报告。

**Step 3：生成 missing metadata report**

`missing_metadata_report_v1.json` 列出了每条记录缺失的字段：

- 9 条本地记录缺 `source_url`（severity: `info`）——这是策略豁免的，本地记录用 `source_ref` 和 `prompt_text_path` 作为溯源锚点。
- 2 条外部记录缺 `prompt_sha256` 和 `prompt_text_path`（severity: `actionable`）——需要后续任务处理。
- 全部 11 条记录的 `prompt_tokens_est` 为 0——暂不阻塞，但后续 taxonomy 分析需要补充。

**Step 4：更新 manifest**

`prompt_corpus_manifest.json` 从 T04 版本全面更新：
- 状态从 `candidate_register_v0_provenance_checked_not_normalized` → `corpus_v1_normalized_not_taxonomy_coded`
- `corpus_size` 从 `0` → `11`
- 拆分为 `eligible_count=10`、`text_ready_count=9`、`mirrored_external_count=0`
- 新增 `corpus_v1_summary` 子结构
- 新增 `duplicate_report_path` 和 `missing_metadata_report_path`
- `hash_coverage` 增加 `text_ready_with_sha256=9`、`text_ready_without_sha256=0`

**Step 5：对齐 raw_index example schema**

`raw_index.example.jsonl` 从 T03 的旧 schema（`prompt_id`, `prompt_sha256`, `builds_on_public_work`）重写为 T04 的标准 schema（`source_id`, `prompt_text_storage`, `recommended_register_action`）。同时新增了一条 `paper` 类型的示例记录。

**Step 6：更新 provenance rules、audit summary、handoff**

- `provenance_rules.md`：新增 "Corpus v1 Status Semantics" 章节，明确解释 `eligible_for_recompute` 与 `text_ready` 的区别。
- `corpus_audit_summary.md`：更新状态、计数、新增 Duplicate Summary 和 Missing Metadata Summary 章节。
- `docs/07_handoff.md`：更新任务状态、改动文件列表、corpus summary。

### 2.3 代码/配置变化

| 文件 | 变化类型 | 说明 |
|---|---|---|
| `data/interim/prompt_corpus/corpus_v1.jsonl` | **新建** | 11 条规范化语料记录 |
| `data/interim/prompt_corpus/duplicate_report_v1.json` | **新建** | 去重报告（当前无重复） |
| `data/interim/prompt_corpus/missing_metadata_report_v1.json` | **新建** | 缺失元数据报告（2 条可操作 + 9 条策略豁免） |
| `data/interim/prompt_corpus/prompt_corpus_manifest.json` | 修改 | 拆分计数、更新状态、新增报告路径 |
| `data/interim/prompt_corpus/provenance_rules.md` | 修改 | 新增 corpus v1 语义定义章节 |
| `data/external/prompt_corpus/raw_index.example.jsonl` | 修改 | schema 对齐 + 新增 paper 类型示例 |
| `data/external/prompt_corpus/raw_index.jsonl` | 修改 | 仅更新 GitHub 记录的 notes 字段 |
| `reports/research/corpus_audit/summary.md` | 修改 | 全面更新状态、计数、新增报告章节 |
| `docs/07_handoff.md` | 修改 | 更新任务状态和改动列表 |

### 2.4 对后续开发的意义

1. **T06（corpus audit）可以基于 corpus_v1 工作**：不再依赖原始登记表，而是基于规范化的语料快照。
2. **T07（taxonomy coding）有了明确的"可标注"集合**：9 条 text-ready 记录可以直接读取文本并做结构标注。
3. **T10+（screening eval）有了明确的"可评测"集合**：9 条 text-ready 记录可以直接送入评测 pipeline，不会误把 metadata-only 的条目送进去。
4. **计数语义清晰**：后续任务如果需要知道"有多少可以直接跑"，看 `text_ready_count=9` 即可；如果需要知道"有多少许可上允许跑"，看 `eligible_count=10`。
5. **Duplicate 和 missing metadata 报告提供了可操作的后续清单**：T06/T07 可以按图索骥处理缺失项。

## 三、Review 结果解释

### Verdict: PASS

给出 PASS 的原因：

1. **全部 7 项要求输出已交付**：corpus_v1、duplicate report、missing metadata report、manifest 拆分、raw_index example schema 对齐、audit update、handoff update。每一项都有实质性内容，不是空壳。

2. **核心语义拆分正确**：9 条 text-ready 记录都有 hash 和 path，且 hash 经独立验证全部正确；2 条非 text-ready 记录都没有伪造 hash 或 path。`eligible` 和 `text_ready` 的区分逻辑清晰且一致。

3. **T04 review 的关键 followup 已解决**：
   - `direct_recompute_count` 混合问题 → 拆为 `eligible_count` + `text_ready_count`。
   - `raw_index.example.jsonl` schema 不对齐 → 已重写为 T04 schema。
   - `provenance_rules.md` 缺少语义解释 → 新增 "Corpus v1 Status Semantics" 章节。

4. **没有越界**：没有改 `src/`、`tests/`、`prompts/complete/`、`configs/research/`、`artifacts/`；没有跑 API eval；没有复制外部 prompt 原文；Contributor Network 保持 structure-only；没有标记任务完成。

5. **没有伪实现**：所有 9 条本地 hash 经独立计算验证全部正确。duplicate report 不只是返回"无重复"而是检查了四个维度。missing metadata report 区分了 `info`（策略豁免）和 `actionable`（需要后续操作），没有把所有缺失一视同仁。

6. **状态字段诚实**：manifest 状态为 `corpus_v1_normalized_not_taxonomy_coded`，准确反映了当前进度——已规范化但尚未做 taxonomy 标注。

### 非阻塞性注意事项

1. `candidate_register_v0.jsonl` 未被更新以匹配 corpus_v1 的新字段（如 `text_ready`），两者现在有轻微的 schema 差异。后续任务应以 `corpus_v1.jsonl` 为权威来源。
2. GitHub MIT prompt 未镜像——这是保守但合理的决定，后续如需外部 text-ready 覆盖可以单独处理。
3. `prompt_tokens_est` 仍全部为 0，T07 做 taxonomy 前需要补估算。
