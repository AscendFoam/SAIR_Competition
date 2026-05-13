# T04: External Prompt Source Collection — 通俗解释

## 一、这个 task 在做什么（通俗版）

SAIR 竞赛 Stage1 结束后，项目从"参赛冲刺"转向"赛后科研"。科研需要一个**公开 prompt 语料库（corpus）**——也就是收集各路参赛者、官方、论文里出现过的 prompt，给它们打上来源标签、许可声明、结构标签，然后统一做实验对比。

T03（上一个任务）已经建立了一份"候选登记表"（candidate register），里面列了 11 个 prompt 候选。但其中有两个是"占位符"——只知道大概来源（一个来自 GitHub，一个来自官方贡献者网络），没有填具体的 URL、作者是谁、能不能合法使用。

T04 的核心工作就是：

1. **把占位符的真实来源补上**——找到 GitHub 仓库的 URL，确认作者、确认许可证。
2. **决定这些文件能不能提交到 git**——之前这些文件被 `.gitignore` 排除了，研究状态只留在本地，换台电脑就丢了。
3. **更新所有相关文档**——登记表、清单、审计报告、交接文档。

简单来说，T04 就是在"把科研材料整理好，补齐出处，确保不会因为 git 配置问题丢失研究进度"。

## 二、任务实现详解

### 2.1 任务目标

T04 的目标是进入 Phase 1（公开语料与 provenance 清洗阶段），具体要完成五件事：

1. **Git tracking 决策**：决定 prompt corpus 管理文件是否以及如何纳入 git 版本控制。
2. **Raw index 更新**：为外部来源创建索引记录，包含 URL、作者、许可信息。
3. **Candidate register 更新**：把两个 public placeholders 的来源信息补齐。
4. **Manifest 和 audit 更新**：更新清单文件和审计报告，反映最新状态。
5. **Handoff 更新**：更新交接文档，记录任务完成情况。

### 2.2 任务流程

Worker 按以下步骤执行：

**Step 1：Git tracking 决策**

选择方案一——在 `.gitignore` 中添加窄白名单（narrow allowlist）。具体规则：

- 放开 `data/external/prompt_corpus/` 目录下的 `.md` 和 `.jsonl` 文件
- 放开 `data/interim/prompt_corpus/` 目录下的 `.md`、`.json` 和 `.jsonl` 文件
- 不放开 `data/raw/`、其他 `data/interim/` 产物，也不放开未来可能出现的外部 prompt 原文镜像

这种做法的精妙之处在于：先忽略整个目录（`data/external/prompt_corpus/*`），再用白名单逐个放行特定扩展名。这保证了只有管理文件会被追踪，而不会意外把大量数据文件提交到 git。

**Step 2：外部来源核验**

Worker 通过 web lookup 核验了两个外部占位项：

- **GitHub 来源**：确认了 `israelcazares/sair-prompt-engineering` 仓库的存在，验证了 MIT 许可证，记录了作者 "Manuel Israel Cazares / Bytepro AI"。该仓库包含 40+ prompt 变体的实验研究。
- **Contributor Network 来源**：只找到一个 SAIR 官方 LinkedIn 帖子作为来源锚点，但该帖子仅提及 Contributor Network 的存在，没有解析到具体的贡献者 prompt 页面。因此这个条目保持为 `structure_only`（只记录结构信息，不存原文）。

**Step 3：更新 raw index**

创建了 `data/external/prompt_corpus/raw_index.jsonl`，包含两条记录，每条记录包含：source_id、source_type、source_url、author_or_team、retrieved_or_checked_on、license_or_tos_note、prompt_text_storage、recommended_register_action 和 notes。

**Step 4：更新 candidate register**

更新了 `candidate_register_v0.jsonl` 中两个 public placeholder 的条目：
- `public_placeholder_ce_first_github`：补上了 source_url、author_or_team、license_or_tos_note，将 storage_status 保持为 `metadata_only`（文本尚未镜像），将 recompute_eligibility 提升为 `direct_recompute`（因为 MIT 许可已确认，后续可合法导入）。
- `public_placeholder_contributor_prompt`：补上了 source_url（LinkedIn 帖子）和 author_or_team（SAIR, host-level），保持 `structure_only`。

**Step 5：更新 manifest、audit 和 handoff**

- Manifest 增加了 `external_provenance_status` 和 `git_tracking_strategy` 字段。
- Audit summary 增加了 External Provenance Status 和 Git Tracking Strategy 两个章节，更新了 Missing Metadata 部分。
- Handoff 更新了任务状态、实际改动文件列表和 git tracking 选择。

### 2.3 代码/配置变化

| 文件 | 变化类型 | 说明 |
|---|---|---|
| `.gitignore` | 修改 | 新增 9 行 narrow allowlist 规则 |
| `data/external/prompt_corpus/raw_index.jsonl` | 新建 | 2 条外部来源记录 |
| `data/interim/prompt_corpus/candidate_register_v0.jsonl` | 修改 | 更新 2 个 public placeholder 的来源信息 |
| `data/interim/prompt_corpus/provenance_rules.md` | 修改 | 新增 Git Tracking Strategy 章节，更新 Direct Recompute Eligibility 说明 |
| `data/interim/prompt_corpus/prompt_corpus_manifest.json` | 修改 | 新增外部 provenance 和 git tracking 字段 |
| `reports/research/corpus_audit/summary.md` | 修改 | 新增 External Provenance Status 和 Git Tracking Strategy 章节 |
| `docs/07_handoff.md` | 修改 | 更新任务状态、改动文件列表、reviewer 重点 |

### 2.4 对后续开发的意义

1. **T05（corpus normalization）可以安全启动**：git tracking 已解决，T05 不会遇到"文件无法提交"的问题。
2. **GitHub 外部候选可在 T05 导入**：MIT 许可已确认，T05 可以决定是否镜像该仓库的 prompt 文件并补充 hash/token estimate。
3. **Contributor network 条目保持受限**：直到找到更稳定的具体贡献者页面，该条目不会被升级为可重算。这避免了在没有明确许可的情况下使用外部内容。
4. **Phase 1 进度**：目前 11 个候选中有 9 个本地 + 1 个已核验的 GitHub 外部 + 1 个 structure-only。距离 8-12 个可分析 prompt 的目标已经接近，但 T05 需要考虑是否补充更多外部候选。

## 三、Review 结果解释

### Verdict: PASS

给出 PASS 的原因：

1. **任务目标全部完成**：五项要求输出（git tracking、raw index、candidate register、manifest/audit、handoff）都已交付，内容真实有效。

2. **没有伪实现或造假**：
   - 所有本地 prompt 文件的 SHA256 哈希值经过独立验证，与登记表记录一致。
   - GitHub 来源 URL 经过 web search 确认存在且确为 MIT 许可。
   - 没有复制任何外部 prompt 原文到仓库中。
   - 所有的状态字段（`corpus_size: 0`、`status: "...not_normalized"`）都如实反映了当前是"候选登记"而非"完成语料"。

3. **没有越界**：
   - 没有修改 `src/`、`tests/`、`prompts/complete/`、`configs/research/`、`artifacts/`。
   - 没有跑 API 评测。
   - 没有下载批量数据。
   - 没有标记任务为完成。

4. **Git tracking 策略合理且可验证**：通过 `git add --dry-run` 和 `git check-ignore` 独立确认了所有管理文件都可被 git 追踪。

5. **来源核验保守且诚实**：
   - GitHub 来源：验证了 MIT 许可，但仍未镜像原文（留给 T05 决定）。
   - Contributor network：只找到 LinkedIn 帖子级别的来源，诚实标记为 `structure_only`，没有夸大为已核验。

### 非阻塞性注意事项

虽然通过，但有几个值得后续关注的小问题：

1. `direct_recompute_count=10` 这个数字把"有资格导入"和"本地已有文本"混在了一起。目前文档中有解释，但后续任务可能需要更精细的区分。
2. Contributor network 的来源锚定在一个 LinkedIn 帖子上，不够稳定，后续应寻找更持久的第一方链接。
3. 目前只有 2 个外部来源，可能需要 T05/T06 补充更多外部候选才能达到研究目标。
