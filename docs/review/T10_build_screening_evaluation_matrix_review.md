# Review: T10_build_screening_evaluation_matrix

Verdict: PASS

## Summary

T10 worker 完成了 screening evaluation matrix 的设计与文档收敛。产出 3 份新建文档（screening_matrix_v1.md、screening_candidate_registry_v1.md、screening_shortlist_rules_v1.md），更新了 evaluation_matrix.example.json（prompt_set 替换为 9 条实际 ID、repeats 统一为整数、collapse_checks 新增），同步更新了 configs README、screening README 和 handoff。

候选池严格限定为 9 条 text-ready local prompts，遵守 T06 boundary gate。8 个高方差字段列为 screening 可用维度，10 个低方差字段正确降为 descriptive-only。Shortlist rules 定义了 E1-E4 淘汰条件（parse failure、all-true、all-false、non-reproducible）和 I1-I2 入围条件（structural uniqueness、no near-duplicate），assembly procedure 分 4 步执行，目标 3-5 prompts。`repeats` 已从 `"1-3"` 说明性字符串收敛为正式整数 `1`。所有验证命令通过。

## Blocking Issues

无。

## Non-Blocking Issues

### N1. screening_matrix_v1.md Section 8 字段分布计数有 3 处转录错误

Reviewer 逐条交叉比对 `prompt_features_v1.jsonl` 实际值与 matrix Section 8 表格声明值，发现 3 个字段分布不一致：

| 字段 | matrix 声明 | 实际数据 | 偏差 |
|---|---|---|---|
| `opening_strategy` | trivial_first:5, unknown:1 | trivial_first:6, unknown:1 | P2.0.2 实际为 trivial_first，matrix 总计仅 8 而非 9 |
| `proof_like_true_support` | weak:2 | weak:3 | P2.0.2 的 weak 未计入 |
| `cheatsheet_density` | light:1 | light:2 | P2.0.2 的 light 未计入 |

三处错误均为同一来源：P2.0.2 在 distribution 统计中被遗漏。T09 self_audit_v1.md Section 3.1/3.2 的分布数据是正确的（trivial_first:6, weak:3, light:2），matrix 未能准确转录。

**影响：低。** 分布计数不影响 screening gates（parse/collapse thresholds 是硬编码数值）、shortlist assembly（Step 2 anchors 基于正确的个别 prompt 属性而非聚合统计）或 JSON config。但读者若用 distribution 表做独立验证会发现不一致。

**建议：** 未来 doc hygiene 时修正，或在 Section 8 表格中注明"参见 self_audit_v1.md Section 3.1/3.2 以获取权威分布"。

### N2. screening_candidate_registry_v1.md Section 4 与 Section 1 内部不一致

- Section 1 "Core Candidates" 表格：P2.0.2 opening_strategy = trivial_first（正确，与 prompt_features_v1.jsonl 一致）
- Section 4 "Opening strategy" 汇总表：P2.0.2 被列为 unknown（不正确）

Section 4 的汇总表是 N1 中 opening_strategy 错误的直接来源。同一文档内两处表格对同一 prompt 给出不同分类。

**影响：低。** Section 1 是候选定义的权威表格（per-candidate data 正确），Section 4 是汇总视图。但内部不一致可能误导读者。

**建议：** 修正 Section 4 使其与 Section 1 和实际数据一致。

### N3. .claude/settings.json 工具权限变更

diff 中可见 `.claude/settings.json` 变更，与 T08/T09 review 中的相同 issue 一致。这是 IDE 自动积累的工具权限记录，不属于 T10 worker 的有意修改，不应进入正式提交。

### N4. screening_matrix_v1.md 未显式标注 T09 分类出处

matrix Section 8 继承了 self_audit_v1.md Section 4.1/4.4 和 conflict_resolution_v1.md Adjudication 3 的字段分类结论，但仅写"from self_audit_v1.md Section 4.1"未附 section 编号。对 reader 追溯决策链条略有不便。

**影响：极低。** 分类结论本身正确，只是出处标注粒度可以更细。

## Missing Tests

无。T10 是文档/配置设计任务，不涉及代码修改。Worker 运行的验证命令充分：

- `python -m sair_competition.cli validate-layout`：pass
- `python -m json.tool configs/research/evaluation_matrix.example.json`：pass（JSON 语法合法）
- 3 个新 .md 文件存在性检查：pass

Reviewer 独立运行了以下额外验证：

- `prompt_features_v1.jsonl` 字段值分布交叉验证：发现 3 处计数错误（见 N1）
- `smoke.jsonl` 验证：64 problems, 31 True, 33 False, 50 normal + 4 hard1 + 10 hard2（基于 source 字段）— 全部准确
- `dev.jsonl` hard problem count 验证：174 hard (44 hard1 + 130 hard2) — 与 matrix optional expansion 描述一致
- `evaluation_matrix.example.json` 所有 9 个 prompt_id 与 `corpus_v1.jsonl` 匹配验证：全部匹配

## Suspicious Implementation Details

无。未发现伪实现、虚假声明、偷跑实验结论或隐藏数据修改。

逐项检查结果：

1. **候选池严格限定 9 条 text-ready records**：与 T06 boundary gate 一致，2 条 non-text-ready 记录明确排除并给出具体理由。
2. **10 个低方差字段全部降为 descriptive-only**：与 conflict_resolution_v1.md Adjudication 3 一致。7 个 zero-variance + 3 个 near-zero/low-variance（ce_search_depth、counterexample_requirement、builds_on_public_work）。
3. **manual coding 为 authoritative truth**：screening_matrix Section 8 "Reporting boundary" 正确继承 T09 Adjudication 4。
4. **repeats 已收敛为整数**：screening = 1, recomputed = 1 (可扩展), post-release = 1 (可扩展)。`"1-3"` 字符串已消除。expansion_note 写清扩展需要 Captain 审批。
5. **screening 不产出论文结论**：matrix 多处明确标注 "Screening results are NOT used as model selection signals or performance claims in the paper."
6. **shortlist rules 具体、可执行**：E1-E4 有明确数值阈值（parse < 0.95, true_recall >= 0.95 AND false_recall <= 0.10 等），deduplication 有 4 级 tiebreaker（parse_rate > accuracy > field diversity > alphabetical），不需要主观判断。
7. **未修改 src/、tests/、prompts/complete/**：T10 forbidden scope 被严格遵守。
8. **未修改 data/interim/prompt_corpus/ 中的文件**：prompt_features_v1.jsonl 的变更是 T09 的 P2.0.2 校正，不是 T10 worker 的修改。
9. **未修改 docs/04_task_board.md**：T10 worker 没有标记 T10 为完成。
10. **provider_route = to_fill**：正确保留了待填状态，没有伪造 model 信息。
11. **文档没有偷跑结论**：无性能预测、ranking、或 screening 结果假设。
12. **Task Required Decisions 全部回答**：7 个 Required Decisions 均有明确答案（候选池、screening 字段、descriptive-only 字段、split、model config、repeats、shortlist 标准）。
13. **Field Usage Rules preserved**：4 条 T09 继承规则全部保留在 screening_matrix Section 8。

## Allowed Files Compliance

Worker 修改的文件全部在 allowed list 内：

- `reports/research/screening/screening_matrix_v1.md` (new) ✓
- `reports/research/screening/screening_candidate_registry_v1.md` (new) ✓
- `reports/research/screening/screening_shortlist_rules_v1.md` (new) ✓
- `configs/research/evaluation_matrix.example.json` (updated) ✓
- `configs/research/README.md` (updated) ✓
- `reports/research/screening/README.md` (updated) ✓
- `docs/07_handoff.md` (updated) ✓

## Forbidden Scope Compliance

- 未修改 `src/`、`tests/`、`prompts/complete/` ✓
- 未修改 `data/interim/prompt_corpus/corpus_v1.jsonl` 或 `prompt_features_v1.jsonl` ✓
- 未跑 API eval、screening execution、released subset analysis ✓
- 未生成 `predictions.jsonl`、`raw_outputs.jsonl` 或任何真实 run artifact ✓
- 未把 metadata-only / structure-only records 提升为 screening 候选 ✓
- 未让 low-variance fields 成为主筛选维度 ✓
- 未修改 `docs/04_task_board.md` 或标记 T10 为完成 ✓

## Recommended Next Action

T10 review 通过后：

1. Captain 在 `docs/04_task_board.md` 勾选 T10。
2. 可以安全启动 T11 (run screening on selected prompt candidates)。
3. T11 应使用：
   - screening_matrix_v1.md 定义的 matrix 做执行（9 prompts, smoke split, 单模型）
   - screening_shortlist_rules_v1.md 做 shortlist 决策
   - evaluation_matrix.example.json screening phase 配置（填入 provider_route）
   - prompt_features_v1.jsonl（T09 corrected）作为字段来源
4. T11 必须填入 provider_route 实际值，但不得更改 frozen 字段（temperature, max_tokens, reasoning_mode, repeats, prompt_set, dataset_set）。
5. T11 应注意 P0 可能因 relaxed format 导致低 parse success rate；如果 P0 被淘汰，shortlist 将失去 baseline anchor，T12 报告必须注明此 coverage gap。
6. 建议在 T11 开始前修正 N1/N2 中的字段分布计数错误，以避免 T12 误用错误分布。
