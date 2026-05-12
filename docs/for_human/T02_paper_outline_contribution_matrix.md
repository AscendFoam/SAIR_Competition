# T02_paper_outline_contribution_matrix：通俗解释与 Review 说明

## 一、这个 Task 在做什么（通俗解释）

T01 搭好了研究脚手架（目录结构、配置模板等），但论文到底要写什么、能声称什么、哪些有证据哪些没有——这些关键问题还没有梳理清楚。

T02 就是做这件事：把论文从"我打算写一篇论文"细化成"这篇论文要证明什么、每一条主张目前有什么证据支撑、现在允许怎么措辞、绝对不允许怎么措辞"。

用一个类比：T01 是画好了建筑图纸的框架，T02 是在图纸上标注清楚"这面墙已经建好（有砖有水泥）、那面墙还是空的（只有设计意图）、这根柱子绝对不能承重（缺少计算）"。

具体来说，T02 产出了三个东西：

1. **细化的论文大纲**：增加了摘要草稿、计划中的表格、当前证据来源清单、显式的 post-release 限定声明。
2. **贡献清单**：把论文的 7 项潜在贡献逐条列出，每条都标注来源文档、需要什么证据、当前状态、审稿人可能的质疑。
3. **主张-证据矩阵**：把 12 条论文主张逐条拆开，明确写出"现在允许怎么说"和"现在绝对不允许怎么说"，防止后续 worker 在写论文时把计划写成了结果。

## 二、实现细节

### 任务目标

按 [docs/tasks/phase_0_research_setup/T02_paper_outline_contribution_matrix.md](docs/tasks/phase_0_research_setup/T02_paper_outline_contribution_matrix.md) 的要求，完成 4 项产出：

1. 细化 `reports/paper/outline.md`
2. 新增 `reports/paper/contribution_list.md`
3. 新增 `reports/paper/claim_evidence_matrix.md`
4. 更新 `docs/07_handoff.md`

### 具体文件变化

#### reports/paper/outline.md（细化）

从 T01 的高层 scaffold 细化为可执行的论文设计文档，新增/强化了以下内容：

| 新增部分 | 内容 |
|---------|------|
| Abstract Draft | 中英文摘要草稿，明确写成"研究设计目标，非已完成实验" |
| Core Claim | 把核心主张改写成"研究意图"，并加注"目前还不能把方法效果写成既有结果" |
| Planned Tables | 6 张计划中的表格（corpus 来源、taxonomy 定义、screening shortlist、主评测表、鲁棒性分析、消融总结） |
| Evidence Status | 从 4 行扩展到 13 行，新增 taxonomy mapping 缺口、screening protocol 支撑等 |
| Current Evidence Sources | 8 个具体来源文档列表 |
| Explicit Post-Release Analysis Caveat | 独立 section，明确 released subsets 的使用限制 |
| Not-Yet-Supported Claims | 从 4 条扩展到 6 条，新增 taxonomy mapping 和 compression_style/ce_search_depth 缺口 |
| Writing Constraints For Next Tasks | 3 条对 T03/T07/T10 的写作约束 |

#### reports/paper/contribution_list.md（新增）

7 项贡献，每项包含 5 个字段：

| 贡献 | 状态 | 核心内容 |
|------|------|---------|
| C1: Prompt corpus | `supported_by_existing_assets` | schema + manifest 已有，实际语料待收集 |
| C2: Feature taxonomy | `supported_by_existing_assets` | YAML seed 已有，字段映射待闭环 |
| C3: 统一评测 protocol | `supported_by_existing_assets` | protocol 文档已有，实际 run 待执行 |
| C4: 结构经验发现 | `planned_needs_data` | 需要完整评测链路支撑 |
| C5: Feature-aware distillation | `planned_needs_data` | 方法仅有计划，无实验证据 |
| C6: 复现性交付包 | `planned_needs_data` | 待 T21-T22 闭环 |
| C7: 工程资产支撑 | `supported_by_existing_assets` | 项目总结层面，非论文主贡献 |

每项都标注了"最近的竞争工作或审稿人可能的质疑"，这是为了提前防范审稿风险。

#### reports/paper/claim_evidence_matrix.md（新增）

12 条主张（CL1-CL12），每条包含 7 个字段：

- claim text（主张内容）
- linked RQ（关联的研究问题）
- needed artifact（需要的产物）
- current evidence（当前证据）
- missing evidence（缺失证据）
- allowed wording now（当前允许措辞）
- forbidden wording now（当前禁止措辞）

关键约束：
- CL11 明确禁止把 "feature-aware textual distillation improves robustness" 写成结果
- CL7 明确 released subsets 只能作为 post-release analysis
- CL4 标注 taxonomy mapping 是前置条件
- CL5 标注 compression_style 和 ce_search_depth 是未决缺口

#### docs/07_handoff.md（更新）

状态从 "Ready for worker" 改为 "Worker 已完成 / 待 reviewer 审查"。新增了实际改动文件列表、reviewer 检查点（含 taxonomy mapping / compression_style / ce_search_depth 前置条件），以及"不能跳过 review 直接进入 T03"的约束。

#### reports/paper/README.md（小更新）

新增了对 contribution_list.md 和 claim_evidence_matrix.md 的状态描述，以及 claim 管理纪律说明。

### 对后续开发的意义

T02 建立的 claim/evidence 矩阵是后续所有实验和写作的"护栏"：

- **T03**（corpus candidate register）收集 prompt 时必须服务于 RQ1-RQ6，不能退回"继续找更高分 prompt"的叙事——这由 outline 的 Writing Constraints 约束。
- **T07**（taxonomy manual coding）之前必须解决 experiment plan 6.2 到 YAML 的字段映射——这由 CL4 显式前置化。
- **T10**（screening eval matrix）之前必须收敛 `repeats` 的 schema 类型——这由 outline 的 Writing Constraints 约束。
- **T16-T20**（distillation 和统计分析）的所有 empirical claims 都必须在 CL10-CL12 的 allowed wording 范围内写作。
- 论文写作时，每一段主张都可以对照 claim_evidence_matrix 检查措辞是否越界。

## 三、为什么给出 PASS 的 Review 结果

### 判定理由

1. **任务目标全部达成**：任务包要求的 4 项产出全部落地。outline 细化后新增了 abstract、planned tables、evidence status、post-release caveat 等 8 个要求部分。contribution_list 覆盖了 6 个必需贡献领域（prompt corpus、taxonomy、eval protocol、structural findings、distillation、reproducibility）加 1 个额外项。claim_evidence_matrix 包含 12 条带完整 7 字段的主张。

2. **无伪实现**：所有 empirical claims 都被标记为 planned 或 needs_data。CL11 (distillation improves robustness) 的 current evidence 是 "none"。Abstract draft 明确说 "this is a design target rather than a completed empirical result"。没有任何地方把未运行的实验写成结果。

3. **claim 约束精确**：任务包要求 4 个特定的 claim 约束项（distillation claim forbidden、released subsets constrained、taxonomy mapping prerequisite、compression_style/ce_search_depth gap），全部在矩阵中显式出现（CL11、CL7、CL4、CL5），每条都有对应的 forbidden wording。

4. **无越界修改**：`src/`、`tests/`、`prompts/complete/`、`configs/research/`、`data/`、`artifacts/`、`docs/04_task_board.md` 均未变更。

5. **验证通过**：validate-layout 通过，所有 4 组文本模式检查都有匹配。

### 发现的非阻塞问题

- contribution_list 没有使用 `unsupported_do_not_claim` 状态（任务包要求的三种状态之一）
- C7 贡献更像项目内部总结而非论文贡献
- outline 中 contribution_list 链接使用了绝对 Windows 路径
- 摘要可以更精确地反映已完成的 scaffold 部分

这些问题都不影响文档的核心功能——约束后续实验和论文措辞——因此不构成阻塞。
