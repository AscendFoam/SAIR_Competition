# T09 Taxonomy Self-Audit and Conflict Resolution — Review Explanation

## 一、这个任务在做什么（通俗版）

前两个任务 T07 和 T08 做了两件事：

- **T07**：一位专家手工给 9 份考试攻略（prompt）逐项打标签，共 27 项指标。
- **T08**：造了一台自动体检机，能自动测量其中 7 项指标。

但这两套结果之间有一个小矛盾：对于第 P2.0.2 号攻略，专家说它的"反例要求程度"是"可选的"（optional），而机器说是"没有"（absent）。虽然只差一个字，但到底谁对？

T09 就是请一个仲裁员来解决这个矛盾。仲裁员不是随便拍脑袋，而是：

1. **重新阅读 P2.0.2 的原文**，看它到底有没有让模型"去找反例"的指令。
2. **检查其他 8 份攻略的标签**，看有没有其他类似矛盾。
3. **清点哪些指标所有人都一样**（比如 9 份攻略全都有"系统目标框架"），这些指标在统计上没有区分度，不能拿来做分析。
4. **定规矩**：机器的结果和专家的结果将来怎么在报告里引用？谁说了算？

打个比方：T09 就像是体检报告的最终审核——自动体检机测了 7 项，专家手测了 27 项，审核员把两者对了一遍，纠正了一处手测错误，并且明确告诉大家"哪些指标可以做统计、哪些只能当背景信息"。

## 二、任务实现的详细解释

### 2.1 任务目标

T09 的核心目标是对 T07 手工编码和 T08 extractor 做自审和冲突收口，具体包括：

1. 产出 self-audit report，覆盖 sample coverage、field variance、manual vs extractor 对齐和 field usage 分类。
2. 产出 conflict resolution report，对已知分歧做明确 adjudication（裁决）。
3. 如确有必要，对 `prompt_features_v1.jsonl` 做最小修正。
4. 更新 `extractor_v1_notes.md` 反映 T09 结果。

### 2.2 任务流程

Worker 的工作流程大致如下：

**Step 1：建立 self-audit 基线（`self_audit_v1.md`）**

Worker 首先对整个 taxonomy 做了全面的自审：

- **Sample coverage**：确认 9 条 text-ready 记录被编码，2 条 non-text-ready 记录被排除，T06 boundary gate 得到遵守。4 个结构家族（A: 最小基线, B: 护栏重度, C: 官方原型, D: 外部保留）中 Family D 为空。
- **Field variance analysis**：将 27 个字段按方差分为四类：
  - High-variance（>= 3 个不同值）：7 个字段，可用于统计分析和筛选。
  - Moderate-variance（2 个不同值但分布不极端）：11 个字段，可用于分组和叙述。
  - Zero-variance（所有 9 条记录值相同）：7 个字段。
  - Near-zero-variance（9:1 或 8:1 分割）：1 个字段。
- **Manual vs extractor mismatch table**：列出唯一的分歧——P2.0.2 `counterexample_requirement`（manual: optional, extractor: absent）。总体一致率 98.4%（62/63）。
- **Single-coder bias assessment**：承认 T07 为单编码者，列出最容易受主观偏差影响的字段和最不容易受影响的字段。
- **不支持的 claim**：明确列出 6 个不能用当前数据支持的结论，例如"prompt 长度与性能单调相关"、"trivial-first 优于 CE-first"等。

**Step 2：裁决已知分歧（`conflict_resolution_v1.md`）**

Worker 对 5 个问题逐一做了 adjudication：

**Adjudication 1：P2.0.2 `counterexample_requirement`**

- 问题：专家标注为 `optional`，机器输出为 `absent`。
- 裁决：以 `absent` 为准。
- 理由：P2.0.2 的 "Fast FALSE filters" 是结构性启发式规则（如"新变量"、"额外对称性"），不是反例搜索指令。它的 "stay conservative" 回退策略是歧义处理指令，不是反例构造指令。专家将"有 false-filter 启发式"与"鼓励反例搜索"混淆了。
- 行动：修改 `prompt_features_v1.jsonl` 中 P2.0.2 记录的 `counterexample_requirement` 从 `optional` 改为 `absent`，更新 `coder_note`。

**Adjudication 2：`rule_or_heuristic_block` 的 `override` 关键词启发式**

- 问题：extractor 用 "override" 关键词区分 `saturated` 和 `extended`，这是一个脆弱的启发式规则。
- 裁决：当前接受。
- 理由：9 条 prompt 全部正确。人工编码仍是权威来源。未来语料扩展时需重新评估。
- 行动：无需代码改动，在 `extractor_v1_notes.md` 添加 adjudication 说明。

**Adjudication 3：低方差字段策略**

- 问题：10 个字段方差为零或接近零。
- 裁决：保留在 schema 中，排除出统计模型，仅做描述性标签。
- 理由：当前 9 条 prompt 中这些字段无区分度。但未来语料扩展（如加入外部 prompt）可能引入方差，保留可避免 schema 中断。
- 行动：无需数据改动，在文档中记录策略。

**Adjudication 4：extractor/manual reporting boundary**

- 问题：如何区分"extractor 行为稳定性"和"人工编码一致性"两种不同主张？
- 裁决：extractor 输出报告"extractor behavior"，人工编码报告"taxonomy truth"。两者都存在时以人工编码为准。
- 行动：无需代码或数据改动，在 `extractor_v1_notes.md` 记录。

**Adjudication 5：`prompt_features_v1.jsonl` 最小修正**

- 评估全部 9 条记录后，确认只有 P2.0.2 需要修正，其余 8 条记录无问题。

**Step 3：同步更新关联文档**

- `extractor_v1_notes.md`：更新 P2.0.2 分歧状态（从 "known disagreement" 改为 "resolved"），更新低方差字段列表和策略，添加 T09 adjudication 确认，添加 reporting boundary 规则。
- `reports/research/taxonomy/README.md`：添加 T09 完成状态和文件清单。
- `docs/07_handoff.md`：更新当前任务状态、worker 执行结果、下一位 worker 需读文件、执行边界和未验证事项。

### 2.3 关键数据/配置变化

| 文件 | 变化 |
|---|---|
| `data/interim/prompt_corpus/prompt_features_v1.jsonl` | 1 条记录（P2.0.2）的 `counterexample_requirement` 从 `optional` 改为 `absent`，`coder_note` 追加 T09 adjudication 说明 |
| `reports/research/taxonomy/self_audit_v1.md` | 新增，约 200 行。Sample coverage、field variance 分类、manual vs extractor 对齐、single-coder bias 评估、不支持的 claim 列表 |
| `reports/research/taxonomy/conflict_resolution_v1.md` | 新增，约 157 行。5 项 adjudication，含争议描述、裁决理由和行动项 |
| `reports/research/taxonomy/extractor_v1_notes.md` | 更新。P2.0.2 分歧标记为 resolved，低方差字段重新分类（7 zero + 3 near/low = 10），添加 T09 reporting boundary 规则 |
| `reports/research/taxonomy/README.md` | 更新。添加 T09 完成状态、self-audit 和 conflict resolution 文件 |
| `docs/07_handoff.md` | 更新。T09 worker 执行结果、下一位 worker 边界（T10）、未验证事项更新 |

### 2.4 对后续开发的意义

1. **T10 (Screening Matrix)**：T09 的 field usage classification 为 T10 提供了直接可用的筛选维度。Section 4.1 列出的 7 个 high-variance fields 可以作为 screening 矩阵的行/列维度。Section 4.4 的 low-variance field policy 防止 T10 误用零方差字段。

2. **T19 (Statistical Analysis)**：T09 明确了哪些字段可以进入回归模型（high-variance fields），哪些只能做描述（low-variance fields），以及哪些需要 manual override。这为 T19 的统计方案设定了清晰边界。

3. **Milestone 2 收口**：T07（手工编码）+ T08（extractor skeleton）+ T09（self-audit 和 conflict resolution）共同完成了 Milestone 2 的退出条件——taxonomy report 能解释字段、边界案例和复核结果。

4. **论文贡献 C2**：T09 的 self-audit 和 conflict resolution 是论文贡献 C2 (Prompt Feature Taxonomy) 的质量控制环节。它使 taxonomy 不仅仅是人工标注的静态快照，而是一个经过自审、有明确局限性和使用边界的可信工具。

5. **Scope honesty 延续**：T09 延续了 T08 建立的 scope honesty 传统——明确标注不支持的 claim，诚实地承认 single-coder bias，不过度宣称 extractor 能替代人工。

## 三、为什么给出 PASS 的 review 结果

### 检查结果总结

| 检查维度 | 结果 | 说明 |
|---|---|---|
| 任务目标是否完成 | 是 | 全部 5 项交付物（self-audit、conflict resolution、数据修正、extractor notes 同步、文档更新）均已产出 |
| adjudication 是否有理有据 | 是 | P2.0.2 裁决基于 prompt 原文分析，reviewer 独立验证了 prompt 确实不含 counterexample search instruction |
| 数据修改是否透明 | 是 | 仅改 1 条记录的 1 个字段，coder_note 追加了 adjudication 说明，conflict_resolution 逐条列出理由 |
| 是否有伪实现/虚假 adjudication | 否 | 所有 adjudication 都有明确理由，低方差字段策略具体可执行 |
| 是否越过 forbidden scope | 否 | 未修改 src/tests，未跑 API eval，未修改 task board，未越过 boundary gate |
| 文档是否过度宣称 | 否 | 明确列出 6 个不支持的 claim，承认 single-coder bias，标注 Family D 为空 |
| 验证是否充分 | 是 | validate-layout pass，90 项 extractor tests 全部通过，JSONL schema 无违规，extractor-manual 63/63 一致 |
| 是否破坏已有功能 | 否 | extractor tests 全部通过，数据校正使 manual 和 extractor 对齐 |
| 统计数字是否准确 | 是 | Reviewer 独立验证了 field variance 统计，所有数字与实际数据一致 |

### P2.0.2 adjudication 的独立验证

作为 reviewer，我独立阅读了 P2.0.2 prompt 原文。该 prompt 的结构是：

1. 任务描述 + 输出契约
2. Fast TRUE filters（4 条结构性判断）
3. Fast FALSE filters（2 条结构性判断）
4. Fast-filter guardrails（3 条防护规则）
5. 变量占位符 + Final answer

Prompt 中确实没有任何"寻找反例"、"构造 magma 反例"、"counterexample"等措辞。"Fast FALSE filters"是基于公式结构的启发式判断（如"新变量"、"额外对称性"），而非反例搜索指令。"stay conservative"是歧义处理回退，不是反例构造指令。

因此，adjudication 将 `optional` 改为 `absent` 是正确的。这不仅是 extractor 行为描述，而是对 taxonomy 语义的准确校正。

### 总体判断

T09 的执行质量高、adjudication 有理有据、数据修改透明且最小。Worker 没有回避已知分歧，没有虚假裁决，没有让低方差字段成为统计模型的输入，没有越界修改代码或 task board。Self-audit 和 conflict resolution 两份报告为 T10 和 T19 提供了清晰、可信、可直接引用的 taxonomy 输入和使用边界。PASS。
