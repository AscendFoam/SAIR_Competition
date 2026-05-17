# Corpus Audit Summary

状态：T05 review 已以 `PASS` 接受 `corpus_v1` 规范化结果。当前 authoritative snapshot 是 `data/interim/prompt_corpus/corpus_v1.jsonl`，共 11 条记录，其中 9 条 text-ready、1 条 metadata-only、1 条 structure-only；尚未进入 taxonomy 或 screening。

## Purpose

本报告用于审计 prompt corpus 的来源质量、可复现性、缺失元数据和公开边界，并为 T07 taxonomy 与 T10 screening 提供唯一可引用的 corpus 事实口径。

## Review Status

- upstream normalization task: `T05_normalize_prompt_corpus_v1`
- review verdict: `PASS`
- review file: `docs/review/T05_normalize_prompt_corpus_v1_review.md`
- authoritative downstream snapshot: `data/interim/prompt_corpus/corpus_v1.jsonl`
- boundary note: `reports/research/corpus_audit/public_private_boundary.md`

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

Current interpretation:

- 9 records are ready for local direct recompute.
- 1 record is provenance-eligible but still metadata-only.
- 1 record is structure-only and must stay out of eval.
- `corpus_v1` is a research snapshot, not complete public ecosystem coverage.

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

Policy-exempt local gaps:

- `9` repository-local text-ready records do not have `source_url`.
- This is expected and non-blocking because `source_ref` plus `prompt_text_path` already provide the reproducible local anchor.
- These `source_url` omissions should not be treated as equal in severity to missing external file provenance.

Actionable external gaps:

- `public_placeholder_ce_first_github`
  - status: eligible but not mirrored
  - missing: local path, SHA256, byte size derived from a mirrored file
  - consequence: cannot enter eval or full-text taxonomy coding yet
- `public_placeholder_contributor_prompt`
  - status: host-level provenance only
  - missing: stable prompt-level URL, local path, SHA256
  - consequence: must remain structure-only and out of eval

Cross-record metadata notes:

- missing author or team: `0`
- missing license note: `0`
- unresolved storage eligibility: `0`
- `prompt_tokens_est` remains `0` for all `11` records

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

## Downstream Use Rules

- `corpus_v1.jsonl` is the only authoritative corpus snapshot for T07 and T10 gating.
- Only records with `text_ready = true`, non-empty local path, and non-empty SHA256 may enter direct recompute.
- Metadata-only and structure-only records cannot enter eval until a later reviewed task changes their status.
- Token estimates are currently unavailable and must not be used to support length-bucket or token-based claims yet.

## License and Boundary Notes

- 本地 prompt 可以登记 path、hash 和 byte size，但仍需遵守 release boundary；local reproducibility does not imply automatic public full-text release.
- 已核验的 GitHub 外部候选来自公开 MIT repo，但 T05 与 T06 仍不复制原文，只保留 metadata-only 记录。
- contributor-network 候选目前只有官方 SAIR host-level post 可核验，仍不得复制原文，也不得进入直接复算。
- released final evaluation subsets 不是 prompt source；它们只用于后续 `post-release analysis`。

## Remaining Risks

1. GitHub MIT source 已许可但未镜像，本地仍没有 external text-ready record。
2. contributor-network 占位项仍缺稳定 first-party prompt URL 与明确归因条款。
3. `prompt_tokens_est` 仍全部为 `0`，后续若做长度分桶需要补估算。
4. 若下游 worker 回退使用 `candidate_register_v0.jsonl` 而不是 `corpus_v1.jsonl`，会重新引入 schema drift 风险。

## Next Actions

1. T07 以前继续以 `corpus_v1.jsonl` 为唯一下游输入快照，不要从 candidate register 重新推断 eligibility。
2. 若后续确有需要，再单独决定是否镜像 MIT GitHub prompt 文件并补本地 hash/token estimate。
3. 继续寻找 contributor-network 的稳定 first-party URL；若始终无法确认 prompt-level provenance，则保持 structure-only 或降级为 excluded。
4. 在 T07 前补 token estimate，避免长度相关 taxonomy 或统计分析误读。
