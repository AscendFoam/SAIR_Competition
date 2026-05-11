# Corpus Audit Summary

状态：seed scaffold only，尚未完成 corpus 收集。

## Purpose

本报告用于审计 prompt corpus 的来源质量、可复现性和公开边界。

## Current Snapshot

- corpus size: `0`
- ready prompt count: `0`
- target prompt count: `8-12`
- status: `seed_scaffold_not_collected`

## Fields To Fill In After Collection

- corpus size
- source counts
- hash coverage
- missing metadata counts
- license or ToS notes
- prompt text storage exceptions

## Known Constraints

- 主分析只覆盖公开且可复现语料。
- 若 prompt 原文不能合法入库，只保留 provenance、hash 和结构摘要。
- released final evaluation subsets 只能用于 `post-release analysis`，不能反向指导 prompt 选择。

## Next Actions

1. 建立 `raw_index` 实际记录并纳入本地 prompt 历史。
2. 完成第一批 `8-12` 个候选 prompt 的 provenance 检查。
3. 为可存储 prompt 计算 hash、bytes 和粗粒度 token estimate。
4. 标记缺失 metadata、license 风险和需要 hash-only 处理的来源。
