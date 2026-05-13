# Corpus Audit Summary

状态：candidate register v0 已建立，但 normalized corpus 仍未完成。

## Purpose

本报告用于审计 prompt corpus 的来源质量、可复现性和公开边界。

## Current Snapshot

- corpus size: `0`
- ready prompt count: `0`
- candidate register size: `11`
- direct recompute candidates: `9`
- metadata-only candidates: `1`
- structure-only candidates: `1`
- target prompt count: `8-12`
- status: `candidate_register_v0_not_cleaned`

## Candidate Source Counts

- local: `9`
- github: `1`
- contributor_network: `1`
- official: `0`
- paper: `0`
- social: `0`

## Hash Coverage

- hashed candidates: `9`
- without hash: `2`
- scope: `candidate_register_v0`

## Missing Metadata

- external placeholder source URLs: missing
- external placeholder license confirmations: missing
- external placeholder author or team verification: missing
- prompt token estimates: not filled yet

## License and ToS Notes

- 本地 prompt 可以登记 path、hash 和 byte size，但仍需遵守 release boundary。
- GitHub / contributor-network placeholder 当前不复制原文，只保留 metadata-only 或 structure-only 记录。
- released final evaluation subsets 不是 prompt source；它们只用于后续 `post-release analysis`。

## Next Actions

1. 在 T04 核验外部候选的 source URL、author、license 和 attribution。
2. 在 T05 为 direct-recompute 候选补齐 normalized corpus schema、去重和缺失 metadata 报告。
3. 为 candidate register 中的本地文件补 token estimate，并决定是否纳入首批 analyzable corpus。
4. 对 metadata-only 和 structure-only 候选保留 provenance hygiene，不提前升级为 direct recompute。
