# Review: T09_taxonomy_self_audit_and_conflict_resolution

Verdict: PASS

## Summary

T09 worker 完成了 taxonomy self-audit 和 conflict resolution，产出 `self_audit_v1.md` 和 `conflict_resolution_v1.md` 两份报告，对 4 项已知问题给出了明确 adjudication：P2.0.2 `counterexample_requirement` 从 `optional` 校正为 `absent`（唯一数据修改）；`rule_or_heuristic_block` heuristic 接受；10 个低方差字段排除出统计模型；extractor/manual reporting boundary 明确区分。校正后 extractor 与 manual coding 达成 9/9 一致（63/63 字段对）。所有验证通过：validate-layout OK，90 项 extractor tests 全部通过，JSONL 数据 9 条记录无 schema 违规。

## Blocking Issues

无。

## Non-Blocking Issues

### N1. self_audit_v1.md Section 3.3 零方差字段计数：正文列出 7 个但实际计数不一致

- Section 3.3 标题标注"Zero-variance fields (single value across all 9)"，列出了 7 个字段。但 `extractor_v1_notes.md` 的 Low-Variance Fields 部分也将 `provenance_status` 和 `post_release_relation` 列为 zero-variance（共 7 个 zero-variance + 3 个 near-zero/low-variance = 10 个低方差字段）。
- 两份文档的低方差字段列表一致（7 zero + 3 near/low = 10），但 `self_audit_v1.md` Section 3.4 "Near-zero-variance fields" 只列出 1 个字段（`ce_search_depth`），而 `conflict_resolution_v1.md` Adjudication 3 Group C 列出 2 个字段（`counterexample_requirement` + `builds_on_public_work`）。
- 实际上 `self_audit_v1.md` Section 3.2 将 `counterexample_requirement`（2 unique）和 `builds_on_public_work`（2 unique）列为 "Moderate-variance fields"，而 `conflict_resolution_v1.md` 将它们归入 Group C "Low-variance categorical fields"。分类略有分歧，但不影响最终策略（所有 10 个字段均被排除出统计模型）。
- 影响：低。两份文档最终策略一致（retained, excluded from models, descriptive-only），但读者可能注意到分类归属不完全对齐。
- 建议：未来 audit 时统一分类口径。

### N2. self_audit_v1.md Section 2.2 "19 fields" vs 实际 placeholder 字段数

- Section 2.2 列出 19 个 placeholder 字段名称，但 Section 2.1 表格中 `counterexample_requirement` 已被标注为 8/9 → 9/9，属于 rule-ized 字段。T08 extractor 的 7 个 rule-ized 字段不变，但 total fields = 7 rule-ized + 19 placeholder + 3 length fields（`prompt_bytes`, `prompt_tokens_est`, `prompt_bytes_bucket`/`prompt_tokens_est_bucket` 算作 2 个 bucket + 2 个 raw count）。
- 这个计数不影响核心结论，但如果严格计数 taxonomy 的 27 字段（如 T07 定义），需要确认 7 + 19 = 26（少了 1 个），还是 7 + 19 + compression_style 等。
- 实际情况：T07 定义了 27 个 taxonomy fields。T08 rule-ized 7 个。剩下 20 个 manual-only。`self_audit_v1.md` 列出的 19 个 placeholder 少了 `compression_style`（已列在上方 "19 fields" 清单中实际包含 `compression_style`——检查后确认清单确实包含 19 个字段，而 taxonomy 共 27 个字段中 7 个 rule-ized + 19 个 placeholder + 1 个 `compression_style` 出现在 19 列表中 = 27 个字段正确）。
- 经逐条核对：Section 2.2 列出的 19 个字段确实覆盖了所有非 rule-ized 字段（含 `compression_style`）。计数正确，不影响结论。

### N3. .claude/settings.json 工具权限变更

- diff 中可见 `.claude/settings.json` 变更。与 T08 review 的 N4 相同，这是 IDE 自动积累的工具权限，不属于 T09 worker 的有意修改。
- 不影响代码逻辑。

### N4. self_audit_v1.md Section 7 标题 "Recommendations for T09 Adjudication Input"

- 这份文档本身就是 T09 的 self-audit 输出，但 Section 7 仍然写 "Recommendations for T09 Adjudication Input"，语气像是 T09 之前的预审建议。
- 这是文档组织的小瑕疵——Section 7 列出的是 self-audit 发现的问题清单，这些问题的 adjudication 已在 `conflict_resolution_v1.md` 中完成。
- 影响：低。读者如果只看 `self_audit_v1.md` 末尾，可能误以为 adjudication 尚未完成。但 `conflict_resolution_v1.md` 已覆盖所有 5 个问题。
- 建议：未来版本可在 Section 7 添加一句说明这些 adjudication 已在 `conflict_resolution_v1.md` 中完成。

## Missing Tests

无。T09 是文档/数据审计任务，不涉及代码修改，因此无需新增 tests。

Worker 运行的验证命令充分：
- `validate-layout`：pass
- `pytest tests/test_prompt_feature_extractor.py -q`：90 passed（确保数据校正没有破坏 extractor tests）
- JSONL 验证：9 条记录，P2.0.2 校正确认
- Extractor-manual agreement：63/63（100%）

Reviewer 额外运行了：
- 所有 coded values 对照 taxonomy YAML `allowed_values` 检查：0 violations
- P2.0.2 prompt 原文审查：确认 prompt 确实不含 counterexample search instruction，adjudication 理由成立
- `self_audit_v1.md` 中的 field variance 统计交叉验证：所有数字与实际数据一致

## Suspicious Implementation Details

无。未发现伪实现、虚假 adjudication、掩盖分歧或静默数据改动。

具体检查点：

1. **数据修改有理有据**：P2.0.2 `counterexample_requirement` 从 `optional` 改为 `absent`，adjudication 给出了 4 条明确理由，且 reviewer 已通过阅读 prompt 原文确认 prompt 确实不含 counterexample search instruction。
2. **coder_note 透明**：P2.0.2 记录的 `coder_note` 追加了 T09 adjudication 说明，不是静默改动。
3. **数据修改最小**：仅改 1 条记录的 1 个字段。其余 8 条记录无任何修改。
4. **extractor tests 仍然通过**：90 项 tests 中 P2.0.2 `counterexample_requirement` 的 expected 值本来就是 `absent`（使用 extractor 输出值），校正后 manual coding 也变为 `absent`，tests 无需改动。
5. **adjudication 不过度宣称**：`rule_or_heuristic_block` heuristic 被明确标注为 "accept as-is for skeleton scope" 而非 "validated for all future prompts"。
6. **低方差字段策略可执行**：明确列出 10 个字段（7 zero-variance + 3 near-zero/low-variance），给出具体使用规则（retained, excluded from models, descriptive-only, re-evaluate after expansion）。
7. **不支持的 claim 清晰列出**：Section 6 列出 6 个不能用当前数据支持的 claim，措辞诚实。
8. **未修改 `src/` 或 `tests/`**：T09 的 forbidden scope 禁止修改代码，worker 严格遵守。
9. **未越过 T06 boundary gate**：所有分析限于 9 条 text-ready records。
10. **未修改 `docs/04_task_board.md`**：Worker 未标记 T09 为完成。

## Allowed Files Compliance

Worker 修改的文件全部在 allowed list 内：

- `data/interim/prompt_corpus/prompt_features_v1.jsonl` (P2.0.2 correction) ✓
- `reports/research/taxonomy/self_audit_v1.md` (new) ✓
- `reports/research/taxonomy/conflict_resolution_v1.md` (new) ✓
- `reports/research/taxonomy/extractor_v1_notes.md` (updated) ✓
- `reports/research/taxonomy/README.md` (updated) ✓
- `docs/07_handoff.md` (updated) ✓

注：`.claude/settings.json` 在 diff 中可见，但这是 IDE 自动积累的工具权限，不属于 T09 worker 的有意修改。

## Forbidden Scope Compliance

- 未修改 `src/` 与 `tests/` ✓
- 未修改 `prompts/complete/` ✓
- 未跑 API eval ✓
- 未越过 T06 boundary gate 给非 text-ready records 做 full-text coding ✓
- 未修改 `docs/04_task_board.md` ✓
- 未标记 T09 为完成 ✓

## Recommended Next Action

T09 review 通过后：

1. Captain 在 `docs/04_task_board.md` 勾选 T09。
2. 可以安全启动 T10 (screening evaluation matrix)。T09 的 field usage classification（Section 4）为 T10 提供了直接可用的筛选维度。
3. T10 应使用：
   - High-variance fields（Section 4.1）作为筛选维度和统计分析输入
   - Low-variance fields（Section 4.4）仅做描述性标签
   - Manual coding 作为 authoritative reference，extractor 作为 cross-check
4. T19 (statistical analysis) 应严格遵守 low-variance field policy，不将 10 个低方差字段作为独立变量。
5. Milestone 2 的退出条件——"taxonomy report 能解释字段、边界案例和复核结果"——已在 T07 + T08 + T09 三份报告中完整满足。
