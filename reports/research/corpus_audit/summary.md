# Corpus Audit Summary

状态：candidate register v0 已建立，external provenance 已完成首轮核验，但 normalized corpus 仍未完成。

## Purpose

本报告用于审计 prompt corpus 的来源质量、可复现性和公开边界。

## Current Snapshot

- corpus size: `0`
- ready prompt count: `0`
- candidate register size: `11`
- direct recompute candidates: `10`
- metadata-only candidates: `1`
- structure-only candidates: `1`
- excluded candidates: `0`
- target prompt count: `8-12`
- status: `candidate_register_v0_provenance_checked_not_normalized`

## External Provenance Status

- verified external source records: `2`
- externally storage-allowed source records: `1`
- remaining structure-only external records: `1`
- excluded external records: `0`

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

## Git Tracking Strategy

- strategy: `.gitignore` narrow allowlist
- tracked governance paths:
  - `data/external/prompt_corpus/*.md`
  - `data/external/prompt_corpus/*.jsonl`
  - `data/interim/prompt_corpus/*.md`
  - `data/interim/prompt_corpus/*.json`
  - `data/interim/prompt_corpus/*.jsonl`
- explicitly still ignored:
  - `data/raw/*`
  - general `data/interim/*` outputs outside `prompt_corpus/`
  - future `data/external/prompt_corpus/raw_prompts/` mirrors unless separately approved

## Missing Metadata

- contributor-network underlying prompt page: unresolved
- contributor-network individual contributor attribution: unresolved
- file-level import decision for verified GitHub prompt text: pending later task
- prompt token estimates: not filled yet

## License and ToS Notes

- 本地 prompt 可以登记 path、hash 和 byte size，但仍需遵守 release boundary。
- 已核验的 GitHub 外部候选来自公开 MIT repo，但 T04 仍不复制原文，只记录 provenance 和可导入性。
- contributor-network 候选目前只有官方 SAIR host-level post 可核验，仍不得复制原文。
- released final evaluation subsets 不是 prompt source；它们只用于后续 `post-release analysis`。

## Next Actions

1. 在 T05 为 direct-recompute 候选补齐 normalized corpus schema、去重和缺失 metadata 报告。
2. 决定是否把已核验的 MIT GitHub prompt 文件导入本地并补 hash/token estimate。
3. 若后续无法解析 contributor-network 的具体 prompt 页面与归因条款，继续保持 structure-only 或降级为 excluded。
4. 在 T05/T07 前补 token estimate，并决定哪些 direct-recompute 候选进入首批 analyzable corpus。
