# Review: T07_manual_taxonomy_coding_v1

Verdict: PASS

## Summary

T07 worker 对 9 条 text-ready local prompt 完成了手工 taxonomy 编码，产出了 `prompt_features_v1.jsonl`（9 条记录，27 个 taxonomy 字段），回填了 `corpus_v1.jsonl` 的 token estimate，更新了 taxonomy YAML（新增 `compression_style`、`ce_search_depth`、`bucket_boundary_notes`），撰写了 taxonomy v1 报告和 experiment-plan 6.2 mapping note，并更新了 handoff 和 taxonomy README。

所有交付物均满足任务目标，未违反 forbidden scope，无伪实现，文档诚实且可复核。

## Blocking Issues

无。

## Non-Blocking Issues

### N1. Token estimate 公式文档存在 floor vs round 不一致

`taxonomy_v1.md` 第 24 行描述 token 估算方法为 `floor(prompt_bytes / 4)`，但实际数据使用的是 `round(prompt_bytes / 4)`（标准四舍五入）。例如 P0 的 511 bytes → 128 tokens（round），而 floor(511/4) = 127。

影响：不影响 bucketing 结果（差异在 ±1 以内），但文档描述与数据不一致。

建议：在 T08 或后续修正中将描述改为 "bytes/4 四舍五入"，或者将实际值改为 floor。当前状态可接受，因为 task 本身声明了 "不要伪称为精确计数"。

### N2. 低方差字段的 T08 设计影响

`ce_search_depth` (8:1:0)、`finite_model_search_hint` (全 false)、`examples_block` (全 none)、`identity_or_invariant_guidance` (全 false) 等字段在当前 9 条样本上无区分度。

这些字段被正确保留（为 corpus expansion 准备），但 T08 extractor 设计时应注意不要让这些字段主导 feature 空间或统计模型。已在 taxonomy_v1.md 第 167-176 行和 worker report 中充分记录，无需现在处理。

### N3. P1.2.3 bucket 边界敏感性

P1.2.3 的 3501 bytes 刚好跨过 3500-byte 的 long/medium 边界。如果边界调整，该记录会移到 medium bucket。已在 taxonomy_v1.md 第 50 行和 coder_note 中明确记录。

## Missing Tests

无。本任务是手工编码任务，验证手段为 JSONL 格式校验、字段值合规性校验和 text-ready gating 一致性检查，均已通过：

- `validate-layout`: pass
- JSONL parse: pass (9 valid features + 11 valid corpus)
- text-ready gating: features records == corpus text-ready records, 无 non-text-ready 泄漏
- YAML allowed_values: 所有字段值均在 schema 允许范围内
- Record count: exactly 9

## Suspicious Implementation Details

无。未发现伪实现、mock、stub、hardcoded outputs 或将计划写成事实的情况。

具体检查点：

1. Token estimate 诚实标注为 bytes/4 启发式，未伪称 tokenizer 精确计数。
2. 2 条 non-text-ready records 未被提升为 full-text coded。
3. Taxonomy report 明确标注了哪些字段是 placeholder，哪些是已支持。
4. Handoff 未将 T07 标记为完成（worker 执行，待 review）。
5. 未修改 `docs/04_task_board.md`。
6. 未实现 extractor（只有手工编码）。
7. YAML 更新仅限于 seed scaffold 调整，未引入 extractor implementation detail。

## Allowed Files Compliance

Worker 修改的文件全部在 allowed list 内：

- `data/interim/prompt_corpus/prompt_features_v1.jsonl` (new) ✓
- `data/interim/prompt_corpus/corpus_v1.jsonl` (updated, token backfill only) ✓
- `configs/research/prompt_feature_taxonomy.yaml` (updated) ✓
- `reports/research/taxonomy/taxonomy_v1.md` (new) ✓
- `reports/research/taxonomy/taxonomy_mapping_note.md` (new) ✓
- `reports/research/taxonomy/README.md` (updated) ✓
- `docs/07_handoff.md` (updated) ✓

注：`CLAUDE.md` 和 `.claude/settings.json` 在 git diff 中可见，但这些修改未出现在 worker report 中，且 `CLAUDE.md` 在本次会话开始前已处于 staged 状态（initial git status 显示 `M CLAUDE.md`），属于用户/IDE 的变更，不属于 T07 worker 范围。

## Forbidden Scope Compliance

- 未修改 `src/` ✓
- 未修改 `tests/` ✓
- 未修改 `prompts/complete/` ✓
- 未修改 `artifacts/` ✓
- 未运行 API eval ✓
- 未下载/镜像外部 prompt 原文 ✓
- 未将 metadata-only / structure-only 提升为 full-text coded ✓
- 未将 taxonomy scaffold 伪写成 extractor ✓
- 未修改 `docs/04_task_board.md` ✓

## Recommended Next Action

T07 review 通过后：

1. Captain 在 `docs/04_task_board.md` 勾选 T07。
2. 可以安全启动 T08 (extractor skeleton)，基于 `prompt_features_v1.jsonl` 和 taxonomy YAML 设计 feature extractor。
3. T10 (screening matrix) 可并行准备，使用 9 条 text-ready records 作为候选池。
4. T01 review 中 deferred 的 `compression_style` 和 `ce_search_depth` 已在 T07 中解决。
5. T09 self-audit 应在 T08 开始前复核编码一致性（单编码者 bias）。
