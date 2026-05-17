# Taxonomy Reports

本目录用于存放 prompt feature taxonomy 的定义、手工编码说明、自审记录和冲突解决文档。

## 当前状态

Taxonomy v1 manual coding 已由 T07 完成并通过 full-text 编码：

- taxonomy schema: `configs/research/prompt_feature_taxonomy.yaml` (TAX_V1_MANUAL_CODING)
- manual coding results: `data/interim/prompt_corpus/prompt_features_v1.jsonl` (9 records)
- taxonomy report: `reports/research/taxonomy/taxonomy_v1.md`
- experiment-plan-to-schema mapping: `reports/research/taxonomy/taxonomy_mapping_note.md`

## 已完成

- T07 manual taxonomy coding v1: 对 9 条 text-ready local prompt 做人工 taxonomy 编码。
- Token estimate backfill: 使用 bytes/4 启发式估算为 9 条 text-ready records 补齐 `prompt_tokens_est`。
- Seed scaffold 更新: 添加 `compression_style` 和 `ce_search_depth` 字段。
- Mapping note: 建立 experiment plan 6.2 节字段与 YAML taxonomy 字段的对应关系。

## 待完成

- T08: 基于 v1 manual coding 设计 prompt feature extractor skeleton。
- T09: Taxonomy self-audit and conflict resolution report。

## 文件清单

| 文件 | 说明 |
|---|---|
| `taxonomy_v1.md` | Taxonomy v1 手工编码报告，含编码池说明、token estimate 方法、length bucket 边界、feature 分布和 prompt 家族分组 |
| `taxonomy_mapping_note.md` | Experiment plan 6.2 节字段到 YAML taxonomy 字段的映射表 |
