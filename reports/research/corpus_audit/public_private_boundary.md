# Public/Private Asset Boundary

日期：2026-05-16

## Status

本说明基于 `corpus_v1.jsonl` 的当前快照编写，服务于 `post-release analysis` 研究流程。

当前边界说明只覆盖已登记的 11 条 `corpus_v1` 记录，不代表完整 public prompt ecosystem coverage，也不代表任何后续 public release package 已经获批。

## Authoritative Snapshot

- authoritative corpus snapshot: `data/interim/prompt_corpus/corpus_v1.jsonl`
- supporting reports:
  - `data/interim/prompt_corpus/duplicate_report_v1.json`
  - `data/interim/prompt_corpus/missing_metadata_report_v1.json`
  - `data/interim/prompt_corpus/prompt_corpus_manifest.json`
- T05 review verdict: `PASS`

下游任务不得回退到 `candidate_register_v0.jsonl` 重新推断 eval eligibility。T07 taxonomy 与 T10 screening 必须以 `corpus_v1.jsonl` 的 `text_ready`、`eligible_for_recompute` 和 `corpus_inclusion_status` 为准。

## Asset Classes

| Asset class | Count | Full text stored locally | Local path/hash exists | Can enter T07 taxonomy | Can enter T10 screening | Can enter public release package | Required note |
|---|---:|---|---|---|---|---|---|
| repository-local text-ready records | 9 | Yes | Yes | Yes | Yes, but only after T10 starts and only via `corpus_v1` gating | Metadata yes; full text not automatically public | Keep local provenance, hash, path, release-boundary note |
| GitHub MIT metadata-only record | 1 | No | No | No for full-text feature coding; provenance note only | No | Metadata-only record may be released; raw prompt text may not be released from this repo until a later reviewed mirror/import task records file-level provenance | Cite source URL, author/team, MIT note, and no-mirror status |
| Contributor Network structure-only record | 1 | No | No | No for full taxonomy; boundary/risk note only | No | Structure-only note may be released; raw prompt text may not | Cite host-level provenance only and unresolved prompt-level attribution |
| excluded / not-for-release records | 0 | No | No | No | No | No | Reserve for future rejected assets |

## Direct Recompute Gate

Direct recompute is allowed only when all of the following are true:

1. `corpus_inclusion_status = included_text_ready`
2. `text_ready = true`
3. `prompt_text_path` is non-empty and points to a local file
4. `prompt_sha256` is non-empty
5. the record remains inside the reviewed `corpus_v1` snapshot

Current result:

- direct-recompute-ready records: `9`
- provenance-eligible but not text-ready records: `1`
- structure-only records: `1`

## T07 Taxonomy Gate

T07 may use:

- the 9 repository-local text-ready records as the primary feature-coding pool
- the GitHub metadata-only record only as a provenance/reference note, not as a full-text coding target
- the Contributor Network structure-only record only as a limitation or boundary example, not as a full-text coding target

T07 may not:

- infer missing prompt text from metadata-only records
- promote structure-only records into full taxonomy rows
- use `prompt_tokens_est = 0` as evidence for length-bucket claims

## T10 Screening Gate

T10 may only screen records that satisfy the direct recompute gate above.

That means:

- allowed now: the 9 text-ready local records
- not allowed now: the 1 GitHub metadata-only record
- not allowed now: the 1 Contributor Network structure-only record

A later task may change this only after review-backed status updates in `corpus_v1.jsonl` and the manifest.

## Public Release Boundary

Current release posture is intentionally narrower than local research eligibility.

- Repository-local text-ready records are locally reproducible research assets, not automatically public full-text release assets.
- Metadata-only and structure-only records may appear in a public reproducibility package as provenance tables, hashes, counts, and boundary notes, but not as mirrored raw prompt text.
- `released final evaluation subsets` are not prompt sources. They remain dataset assets for `post-release analysis` only.
- API raw outputs, `.env`, private data, and unreviewed prompt mirrors remain outside any future public package.

## Required Attribution and Limitation Notes

- repository-local text-ready records: preserve source ref, local path, SHA256, byte size, and release-boundary wording
- GitHub metadata-only record: preserve GitHub URL, author/team, MIT license note, and explicit statement that no raw prompt text is mirrored locally
- Contributor Network structure-only record: preserve host-level SAIR attribution and explicit statement that prompt-level provenance is unresolved
- any future mirrored external prompt: must add file-level path, SHA256, byte size, license note, and attribution before it can become text-ready

## Open Boundary Issues

1. The GitHub MIT record is provenance-eligible but still has no local mirrored file, path, or hash.
2. The Contributor Network record still lacks a stable first-party prompt-level URL and resolved attribution terms.
3. `prompt_tokens_est` remains `0` for all 11 records, so token-based length analysis is not yet supportable.
4. Any future public release package still needs a separate release-manifest decision; this note does not grant public full-text release by itself.
