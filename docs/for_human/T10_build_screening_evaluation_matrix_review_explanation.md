# T10 Build Screening Evaluation Matrix — Review Explanation

## 一、这个任务在做什么（通俗版）

T10 做的事情可以用一个比喻来理解：

想象你是一个医学研究的负责人，手头有 9 种候选药物（对应 9 条 prompt），需要在正式临床试验（对应完整评测）之前做一个快速初筛。初筛不是要排名谁最好，而是要淘汰明显有问题的——比如药物有严重副作用（prompt 会导致模型输出无法解析）、完全无效（prompt 让模型只会回答 TRUE 或只会回答 FALSE）、或者生产批次不一致（prompt 文件与记录不匹配）。

T10 就是制定这个初筛方案的任务。具体来说：

1. **确定哪些药进入初筛**：9 条 text-ready 的本地 prompt 全部进入，排除 1 条只有元数据的 GitHub 记录和 1 条只有结构信息的 Contributor Network 记录。这条规矩是 T06 定下的，T10 只是执行。

2. **确定初筛做哪些检查**：
   - 用一组 64 道题（smoke split）测试每条 prompt
   - 只用一个便宜的模型跑一遍
   - 检查输出能不能解析（parse success rate >= 95%）
   - 检查有没有全部答 TRUE 或全部答 FALSE 的"塌缩"现象

3. **确定哪些药物特征可以用来比较**：T09 已经分好了，8 个高方差字段（比如 prompt 长度、规则密度、反例策略等）可以用来比较，10 个低方差字段（比如所有 prompt 都有的特征）只能当描述性标签。

4. **确定从初筛到正式试验的入选规则**：
   - 淘汰条件：解析失败、全部答 TRUE、全部答 FALSE、执行不可复现
   - 入围条件：在剩余候选中具有独特的结构特征
   - 目标：最终选 3-5 条进入正式评测

5. **把上面的决定写进正式配置文件**：把原来模糊的 "repeats: 1-3" 替换为具体的整数 `1`，把 "prompt_set: to_be_determined" 替换为 9 条实际 prompt ID。

打个比方：T10 就是写出了一份临床试验的初筛方案（protocol），但还没有实际跑实验。方案明确规定了做什么检查、用什么标准淘汰、最终选多少人进入正式试验。后续的 T11 才是实际跑初筛，T12 是写初筛报告。

## 二、任务实现的详细解释

### 2.1 任务目标

T10 的核心目标是将现有 screening seed template、T06 corpus boundary 和 T09 taxonomy adjudication 收敛成一个正式、可执行、可 review 的 Stage A screening evaluation matrix。具体包括：

1. 明确 9 条 text-ready local prompts 为 screening 候选池。
2. 明确 8 个高方差字段可用作 screening 比较/分组维度。
3. 明确 10 个低方差字段只能 descriptive-only，不作为 shortlist 主依据。
4. 明确 screening 用 smoke split（64 problems），可选扩展到 dev hard problems。
5. 明确 screening 用 1 个低成本模型、temperature=0、max_tokens=256、repeats=1。
6. 将 `repeats` 从说明性字符串 `"1-3"` 收敛为正式整数。
7. 定义 shortlist 淘汰条件（E1-E4）、入围条件（I1-I2）、目标规模（3-5）。

### 2.2 任务流程

Worker 的工作流程大致如下：

**Step 1：建立 screening matrix（screening_matrix_v1.md，约 222 行）**

Worker 定义了完整的 screening evaluation matrix，包含：

- **Scope / Non-scope**：screening 只做 parse 稳定性检查和初步 true/false 观察分析，不产出论文结论、不跑 released subsets、不做 cross-model 比较、不修改 prompt/taxonomy/corpus。
- **Candidate pool**：9 条 text-ready local prompts，排除 2 条 non-text-ready records（GitHub metadata-only 和 Contributor Network structure-only）并给出具体理由。
- **Dataset splits**：smoke (64 problems, 31 true + 33 false, 50 normal + 4 hard1 + 10 hard2) 作为主 split；dev hard (174 problems) 作为可选扩展。禁止使用 holdout、audit 或 released subsets。
- **Model config**：1 个低成本模型，temperature=0, max_tokens=256, provider_route=to_fill。其他字段 frozen。
- **Run artifacts**：每条 run 必须产出 run_config.json、summary.json、predictions.jsonl、prompt_hash_manifest.json。
- **Metrics & gates**：parse_success_rate >= 0.95 为 hard gate；all-true/all-false collapse 为 BLOCK；near-collapse 为 WARNING。
- **Field usage rules**：8 个 screening fields（prompt_bytes_bucket、rule_or_heuristic_block、false_filter_orientation、proof_like_true_support、cheatsheet_density、opening_strategy、ambiguity_handling、verdict_contract）可用于分组比较。10 个 low-variance fields（7 zero-variance + 3 near-zero/low-variance）只能 descriptive-only。
- **Reporting boundary**：继承 T09 Adjudication 4——extractor 输出报告"extractor behavior"，manual coding 报告"taxonomy truth"。

**Step 2：建立 candidate registry（screening_candidate_registry_v1.md，约 123 行）**

Worker 对 9 条候选做了结构化分类：

- **6 core candidates**：每条代表一种独特结构类型——P0（baseline，唯一 relaxed format）、P1.2.3（guardrail mainline，extended rules）、P1.2.5（rule-saturated high-recall，RC1 提交版本）、P2.0.0（balanced archetype，唯一 balanced opening）、P2.0.1（CE-first archetype，唯一 counterexample_first）、P2.0.2（fast-filters archetype，最短 strict prompt）。
- **3 contrast candidates**：提供 family 内变异——P1.1.1（early draft vs mature，rule density progression）、P1.2.2（pre-mainline vs mainline，guardrail strengthening）、P1.2.8（narrow singleton vs shared variable，anti-bias contrast）。
- **0 deferred candidates**：全部 9 条进入 screening，没有延迟候选。
- **Excluded records**：2 条 non-text-ready records 被排除，理由具体且引用 T06 boundary gate。
- **Coverage gaps**：诚实列出 6 个已知覆盖缺口（无 external prompts、无 near_cap、仅 1 个 CE-first、仅 1 个 balanced、仅 1 个 relaxed-format、无 examples）。

**Step 3：建立 shortlist rules（screening_shortlist_rules_v1.md，约 169 行）**

Worker 定义了可机械执行的 shortlist 决策规则：

- **Elimination E1-E4**：parse failure (< 0.95)、all-true collapse (true_recall >= 0.95 AND false_recall <= 0.10)、all-false collapse (false_recall >= 0.95 AND true_recall <= 0.10)、non-reproducible execution（artifact 缺失或 hash 不匹配）。
- **Inclusion I1-I2**：structural uniqueness（至少在某个轴上是唯一代表）和 no near-duplicate（5 个关键字段全部相同才算 near-duplicate）。
- **Assembly procedure**：4 步流程——先淘汰（E1-E4）、再放锚点（P0/P2.0.0/P2.0.1/P1.2.5 只要存活就进入）、然后按优先级填 slot（P1.2.3 > P2.0.2 > P1.1.1 > P1.2.2 > P1.2.8）、最后 cap at 5。
- **Deduplication tiebreaker**：4 级（parse_rate > accuracy > 字段多样性 > 字母序）。
- **Structural coverage test**：shortlist 必须满足 4 个覆盖维度（length diversity、rule density、opening strategy、provenance diversity）中的至少 3 个。
- **Special cases**：处理 P0 elimination（报告为 baseline failure）、all Family C elimination（报告为 provenance diversity failure）、all long prompts elimination 等极端情况。

**Step 4：收敛配置文件（evaluation_matrix.example.json）**

Worker 更新了 machine-readable config：

- `prompt_set`：从 6 个模糊名称替换为 9 条实际 prompt_id。
- `dataset_set`：从 ["smoke", "hard_slice_sample"] 收窄为 ["smoke"]，hard_slice_sample 降级为 optional_expansion_dataset。
- `repeats`：screening/recomputed/post-release 三阶段均统一为 `1`，附加 expansion_note 说明扩展条件（需 Captain 审批）。
- 新增 `collapse_checks` 块：定义 all_true_collapse、all_false_collapse、parse_collapse 的精确判定条件。
- 新增 `companion_docs` 块：指向 3 份 screening 文档。
- `required_run_artifacts` 中 `metrics.csv` 改为 `predictions.jsonl`（与实际 runner 输出更匹配）。
- `status` 从 `"seed_example_only"` 更新为 `"screening_matrix_defined"`。

**Step 5：同步更新关联文档**

- `configs/research/README.md`：更新为反映 T10 收敛状态，添加 screening config 要点汇总表，明确 screening 配置已冻结。
- `reports/research/screening/README.md`：从"仅完成模板"更新为"matrix defined, execution not started"，列出文件清单和设计原则。
- `docs/07_handoff.md`：完全重构，从 T09 聚焦切换到 T10 聚焦。清理了 T01-T09 的详细 review 记录（改为简明摘要），添加 T10 worker 执行结果、下一位 worker 必读列表、T11 执行边界和 reviewer 重点。

### 2.3 关键数据/配置变化

| 文件 | 变化 |
|---|---|
| `screening_matrix_v1.md` | 新增。完整 screening evaluation matrix：scope、candidate pool、splits、model config、artifacts、metrics、gates、field usage rules、reporting boundary。 |
| `screening_candidate_registry_v1.md` | 新增。9 条候选的结构化 registry：6 core + 3 contrast 分类、non-candidate records、family distribution、structural coverage summary、6 个 coverage gaps。 |
| `screening_shortlist_rules_v1.md` | 新增。E1-E4 elimination、I1-I2 inclusion、4 步 assembly procedure、deduplication tiebreaker、structural coverage test、special cases handling。 |
| `evaluation_matrix.example.json` | 更新。prompt_set → 9 条实际 ID；repeats → 整数 1；新增 collapse_checks、companion_docs、optional_expansion_dataset。 |
| `configs/research/README.md` | 更新。反映 T10 收敛状态和 screening config 要点汇总表。 |
| `reports/research/screening/README.md` | 更新。"matrix defined, execution not started" 状态、文件清单、设计原则。 |
| `docs/07_handoff.md` | 更新。T10 执行结果、已完成任务摘要、T11 衔接说明、reviewer 重点。 |

### 2.4 对后续开发的意义

1. **T11 (Run Screening)**：T10 的 matrix 是 T11 的直接执行方案。T11 只需填入 `provider_route` 实际值，然后按照 matrix 跑 9 条 run。所有其他参数已 frozen，T11 不应更改。

2. **T12 (Screening Summary)**：T10 的 shortlist rules 给 T12 提供了完全可机械执行的决策规则。T12 只需收集 metrics、按 E1-E4 → anchors → fill → cap 的流程产出 shortlist，不需要主观判断。

3. **T19 (Statistical Analysis)**：T10 明确了 8 个 screening fields 和 10 个 descriptive-only fields 的分界。T19 的统计模型应只使用 screening fields 作为自变量。

4. **Milestone 3 进度**：T10 是 Milestone 3 (Screening Evaluation) 的第一步。T10 + T11 + T12 完成后，Milestone 3 的退出条件应该可以满足。

5. **论文贡献 C3/C4**：T10 的 screening matrix 为论文实验设置部分（Section 4 Experimental Setup）提供了结构化 protocol 描述。Field usage rules 确保 screening 结果不会过度解读为因果结论。

6. **Scope honesty 延续**：T10 延续了 T09 建立的 scope honesty 传统——明确标注 6 个 coverage gaps，screening 结果明确标注为"NOT used as performance claims"。

## 三、为什么给出 PASS 的 review 结果

### 核心检查维度

| 检查维度 | 结果 | 说明 |
|---|---|---|
| 任务目标是否完成 | 是 | 全部 7 项 Required Decisions 有明确答案；5 项 Expected Output 全部产出 |
| Allowed files 合规 | 是 | 7 个文件全部在 allowed list 内 |
| Forbidden scope 合规 | 是 | 未修改 src/tests/prompts/data/，未跑 API eval，未修改 task board |
| 是否有伪实现/mock | 否 | 纯文档任务，provider_route 保留 to_fill 而非伪造值 |
| 候选池是否正确 | 是 | 限定 9 条 text-ready local prompts，遵守 T06 boundary gate |
| 低方差字段是否正确降级 | 是 | 10 个 low-variance fields 均标记为 descriptive-only |
| repeats 是否收敛 | 是 | 从 `"1-3"` 统一为整数 `1`，附 expansion_note |
| shortlist rules 是否可执行 | 是 | E1-E4 有数值阈值，I1-I2 有结构化条件，deduplication 有 4 级 tiebreaker |
| 是否有偷跑结论 | 否 | 无性能预测、无 ranking、无 screening 结果假设 |
| 是否破坏已有功能 | 否 | 纯文档任务，extractor tests 不受影响 |
| 验证是否充分 | 是 | validate-layout pass，JSON 语法 pass |

### 发现的非阻塞问题

Reviewer 用 Python 脚本逐条交叉比对 `prompt_features_v1.jsonl` 实际值与 screening_matrix_v1.md Section 8 的声明值，发现 3 处分布计数转录错误：

1. **opening_strategy**：matrix 声明 trivial_first:5, unknown:1；实际数据 trivial_first:6, unknown:1。P2.0.2 实际为 trivial_first，但在 candidate_registry Section 4 汇总表中被误列为 unknown。

2. **proof_like_true_support**：matrix 声明 weak:2；实际数据 weak:3（P1.1.1、P2.0.1、P2.0.2 均为 weak）。

3. **cheatsheet_density**：matrix 声明 light:1；实际数据 light:2（P2.0.1 和 P2.0.2 均为 light）。

三处错误的共同来源是 P2.0.2 在分布统计中被遗漏。candidate_registry_v1.md Section 4 "Opening strategy" 汇总表将 P2.0.2 列为 unknown，与同文档 Section 1 "Core Candidates" 表格中 P2.0.2 = trivial_first 矛盾（Section 1 是正确的）。

这些错误不影响 screening 核心逻辑：gates 阈值（parse < 0.95 等）是硬编码数值，anchor 选择（P0/P2.0.0/P2.0.1/P1.2.5）基于正确的个别 prompt 属性而非聚合统计，shortlist assembly 的 fill priority 也是基于个别 prompt 的 taxonomy 字段值。但分布数字不准确会让读者在独立验证时发现不一致。

### 总体判断

T10 的执行质量高、决策链条清晰、文档结构完善。Worker 正确继承了 T06 的 boundary gate（候选池严格限定 9 条 text-ready）、T09 的字段分类（8 screening + 10 descriptive-only）和 reporting boundary（manual = authoritative truth），没有偷跑实验结论或放松使用限制。Shortlist rules 具体、可机械执行，不会导致 T12 需要做主观判断。Config 收敛彻底（`"1-3"` → 整数 `1`，模糊名称 → 9 条实际 ID）。唯一的不足是 Section 8 的 3 处分布计数转录错误，不影响核心结论，属于未来 doc hygiene 的修正范围。PASS。
