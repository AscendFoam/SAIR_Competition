# Corpus Audit Summary

状态：`corpus_v1` 已规范化，共 11 条记录，其中 9 条 text-ready、1 条 metadata-only、1 条 structure-only；尚未进入 taxonomy 或 screening。

## Purpose

本报告用于审计 prompt corpus 的来源质量、可复现性、缺失元数据和公开边界。

## Current Snapshot

- candidate count: `11`
- corpus_v1 record count: `11`
- corpus size: `11`
- text-ready count: `9`
- eligible count: `10`
- mirrored external count: `0`
- metadata-only count: `1`
- structure-only count: `1`
- excluded count: `0`
- target prompt count: `8-12`
- status: `corpus_v1_normalized_not_taxonomy_coded`

## External Provenance Status

- verified external source records: `2`
- externally storage-allowed source records: `1`
- mirrored external records: `0`
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

- records with SHA256: `9`
- records without SHA256: `2`
- text-ready without hash: `0`
- scope: `corpus_v1`

## Duplicate Summary

- duplicate by SHA256: `0`
- duplicate by normalized source URL: `0`
- duplicate by candidate_id: `0`
- duplicate by prompt_id: `0`
- action taken: none needed in T05

## Missing Metadata Summary

- missing source URL: `9` (all repository-local records; policy-exempt in T05)
- missing author or team: `0`
- missing license note: `0`
- missing prompt hash: `2`
- missing local text: `2`
- unresolved storage eligibility: `0`
- prompt_tokens_est still `0`: `11`

Actionable missing-metadata records:

- `public_placeholder_ce_first_github`: provenance-eligible, but no mirrored local file, hash, or byte size yet.
- `public_placeholder_contributor_prompt`: host-level provenance only; still lacks prompt-level page, local text, and hash.

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
  - `data/external/prompt_corpus/raw_prompts/` unless a later task explicitly mirrors a license-cleared file

## License and ToS Notes

- 本地 prompt 可以登记 path、hash 和 byte size，但仍需遵守 release boundary。
- 已核验的 GitHub 外部候选来自公开 MIT repo，但 T05 仍不复制原文，只保留 metadata-only 记录。
- contributor-network 候选目前只有官方 SAIR host-level post 可核验，仍不得复制原文。
- released final evaluation subsets 不是 prompt source；它们只用于后续 `post-release analysis`。

## Remaining Risks for T06

1. `eligible_count` 与 `text_ready_count` 已拆分，但 reviewer 仍需确认 `corpus_v1` 口径满足下游预期。
2. contributor-network 占位项仍缺稳定 first-party prompt URL 与明确归因条款。
3. GitHub MIT source 已许可但未镜像，本地仍没有 external text-ready record。
4. `prompt_tokens_est` 仍全部为 `0`，后续若做长度分桶需要补估算。

## Next Actions

1. 在 T06 基于 `corpus_v1` 重写 public/private asset boundary note，并确认结构级记录与可重算记录的叙事边界。
2. 若后续确有需要，再单独决定是否镜像 MIT GitHub prompt 文件并补本地 hash/token estimate。
3. 继续寻找 contributor-network 的稳定 first-party URL；若始终无法确认 prompt-level provenance，则保持 structure-only 或降级为 excluded。
4. 在 T07 前补 token estimate，避免长度相关 taxonomy 或统计分析误读。
