# T06 语料库审计与公私资产边界说明

## 一、这个任务在做什么（通俗解释）

经过前面 T01 到 T05 的逐步推进，项目已经建立了一个包含 11 条记录的 prompt 语料库（`corpus_v1`）。但这 11 条记录并不都是"拿来就能跑评测"的——其中有 9 条是我们自己仓库里的本地 prompt 文件，可以直接用；1 条是 GitHub 上别人的 prompt（只知道它的来源和许可信息，但没有把原文下载到仓库里）；还有 1 条是 SAIR 贡献者网络上的 prompt（只知道它存在，连具体内容都还没定位到）。

**T06 的核心任务就是：把这些记录分门别类，明确告诉后续的 worker 哪些能用、哪些不能用、哪些只能做参考。**

打个比方：你整理了一个资料柜，里面有 9 份完整的文件（可以随时翻阅）、1 份只有索引卡片（知道文件在哪但没拿过来）、1 份只有口头传闻（听说有这个文件但不确定）。T06 就是给这个资料柜贴上标签，写清楚每类资料的"使用权限"——避免后面有人把索引卡片当成完整文件来引用。

## 二、任务实现详解

### 2.1 任务目标

T06 的目标不是新增 prompt 或跑评测，而是：

1. 新增一份"公私资产边界说明"（`public_private_boundary.md`），把 11 条记录分成 4 类，对每类写清楚是否能进入后续任务。
2. 更新已有的 corpus audit summary，把 T05 的审查结论（PASS）写进去，并明确 `corpus_v1` 是唯一权威快照。
3. 在 manifest 和 provenance rules 中补充下游使用规则。
4. 更新 handoff 文档，记录 T06 已执行但待 review。

### 2.2 具体变更

#### 新增文件：`reports/research/corpus_audit/public_private_boundary.md`

这是本次任务的核心产出。它包含：

- **资产分类表**：把 11 条记录分为 4 类（本地 text-ready、GitHub metadata-only、Contributor Network structure-only、已排除），对每类说明是否有本地全文、是否有 hash、能否进 T07 taxonomy、能否进 T10 screening、能否进入公开发布包、需要什么归因说明。
- **直接复算门槛**：列出 5 个条件（`included_text_ready` + `text_ready=true` + 非空本地路径 + 非空 SHA256 + 仍在已审查快照内），全部满足才允许进入直接复算。当前满足的是 9 条。
- **T07 门槛**：明确 T07 可以用 9 条 text-ready 记录做特征编码，metadata-only 只能做参考注释，structure-only 只能做边界案例说明。
- **T10 门槛**：明确 T10 只能对满足直接复算门槛的记录做筛选，即当前只有 9 条可进入。
- **公开发布边界**：明确本地可复算不等于可公开发布全文；released final evaluation subsets 不是 prompt 来源。

#### 更新文件：`reports/research/corpus_audit/summary.md`

主要变化：

- 在开头加入 T05 review `PASS` 状态和 `corpus_v1` 作为权威快照的声明。
- 新增 "Review Status" 区域，记录上游任务、审查结论和关键文件路径。
- 把 9 条本地记录缺少 `source_url` 的情况重新归类为"政策豁免"（policy-exempt），和 2 条外部记录的可操作缺失区分开来，避免看起来 11 条记录都有同等紧迫的 metadata 问题。
- 新增 "Downstream Use Rules" 区域，明确只有 text-ready + hash 记录才能进入直接复算，token 估计暂不可用不能用于长度分桶断言。
- 风险列表从 T05-era 的 4 条调整为 T06-era 的 4 条，新增"schema drift 风险"（下游 worker 误用旧的 candidate register）。

#### 更新文件：`data/interim/prompt_corpus/prompt_corpus_manifest.json`

主要变化：

- 新增 `boundary_note_path` 指向边界说明文件。
- 新增 `downstream_use_policy` 结构，以机器可读方式记录权威快照路径、taxonomy 和 screening 的输入限制、以及 metadata-only 和 structure-only 是否允许进入 eval。
- `records_present` 新增边界说明文件路径。
- `planned_next_steps` 和 `notes` 更新为 T06 后的口径。

**计数完全未改变**：`corpus_v1_record_count=11`、`text_ready_count=9`、`eligible_count=10` 等均与 T05 保持一致。

#### 更新文件：`data/interim/prompt_corpus/provenance_rules.md`

新增 "Downstream Use Gates" 区域：

- 声明 `corpus_v1.jsonl` 是权威快照，`candidate_register_v0.jsonl` 只是 provenance 输入。
- 明确各类记录的使用限制（text-ready 可复算、metadata-only 只能做 provenance/audit、structure-only 只能做结构说明）。
- 指向 `public_private_boundary.md` 作为权威边界参考。

#### 更新文件：`docs/07_handoff.md`

- 更新日期为 2026-05-16。
- T06 状态从"Ready for worker"改为"已执行，待 review"。
- 新增"本轮实际改动文件"列表和"边界摘要"。
- 未验证事项更新为反映 T06 完成后的状态。

### 2.3 验证方式

Worker 执行并通过了以下验证：

1. `python -m sair_competition.cli validate-layout`：仓库布局检查通过。
2. `python -m json.tool prompt_corpus_manifest.json`：JSON 格式合法。
3. 边界说明文件包含所有必要关键词（text-ready、metadata-only、structure-only、post-release analysis、direct recompute）。
4. Summary 文件包含所有必要关键词（T05 review、authoritative、policy-exempt、token）。
5. `git diff --name-only`：所有变更文件均在允许列表内。

### 2.4 对后续开发的意义

T06 为 T07（taxonomy 编码）和 T10（screening 评测）建立了明确的准入规则：

- **T07** 只能对 9 条 text-ready 记录做全文特征编码。metadata-only 和 structure-only 记录不能被当作"有全文可分析的 prompt"来处理。
- **T10** 只能对满足直接复算门槛的 9 条记录做筛选评测。
- `corpus_v1.jsonl` 是唯一的权威语料快照，下游任务不能回退到 `candidate_register_v0.jsonl` 重新推断使用权限。
- 本地可复算不等于可公开发布，后续如需发布复现包，需要单独的 release-manifest 任务来决定哪些 prompt 全文可以公开。

这些规则防止了一个关键的工程风险：下游 worker 误把 metadata-only 记录当作可复算 prompt 跑评测，或者把 structure-only 记录当作有全文的 taxonomy 编码目标。

## 三、为什么给出 PASS 的 review 结论

### 核心判断

T06 的任务包要求非常明确：基于已有的 `corpus_v1` 写清审计和边界，不改代码、不跑评测、不复制外部 prompt 原文。Worker 的执行完全满足这些要求。

### 具体理由

1. **所有要求的产出都已落地。** 边界说明文件覆盖了 4 个资产类别、直接复算门槛、T07/T10 门槛、公开发布边界和归因要求。Summary 更新了 T05 review 状态、权威快照声明、policy-exempt 分组和 token 限制。Manifest 和 provenance rules 补充了下游使用规则。Handoff 正确记录了执行状态和变更文件。

2. **数据准确无误。** 边界说明文件中的所有数字（9 text-ready、1 metadata-only、1 structure-only、0 excluded）都与 `corpus_v1.jsonl` 的实际内容一致。Manifest 中的计数未做任何修改。资产分类表的每一行都映射到具体的 `corpus_v1` 记录。

3. **没有越界。** 没有修改 `src/`、`tests/`、`prompts/complete/`、`configs/research/`、`artifacts/`。没有修改 `corpus_v1.jsonl`、`duplicate_report_v1.json`、`missing_metadata_report_v1.json`。没有复制外部 prompt 原文。没有跑 API 评测。没有把 metadata-only 或 structure-only 记录提升为 text-ready。没有修改 `docs/04_task_board.md`。

4. **没有伪实现。** 所有声明都有对应的 `corpus_v1` 记录支撑。没有把计划写成事实——边界说明明确标注"不代表完整 public prompt ecosystem coverage"和"不代表任何后续 public release package 已经获批"。

5. **验证充分。** Worker 执行了任务包要求的所有验证命令，结果均为 pass。验证命令覆盖了仓库布局、JSON 合法性、关键内容模式和变更范围。我作为 reviewer 独立重新确认了所有验证命令的结果。

### 存在的轻微问题（非阻塞）

- Handoff 中的 "eval-eligible now: 9" 和 manifest 中的 "eligible_count: 10" 使用的"eligible"含义不同（前者指"现在就能跑评测"，后者指"provenance 上允许未来跑评测"）。语义上是正确的，但单独看数字时可能引起混淆。不过边界说明文件的解释足够清晰，不会造成实际误用。

这些问题不影响任务的正确完成，标记为 non-blocking。
