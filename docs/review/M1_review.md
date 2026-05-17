# M1 Milestone Review

Reviewer: Codex Captain
Date: 2026-05-17
Milestone: `M1 Public Corpus and Provenance Cleaning`

## Verdict: Conditional

## Scope Reviewed

- `T04_external_prompt_source_collection`
- `T05_normalize_prompt_corpus_v1`
- `T06_corpus_audit_public_private_boundary`

## 1. 当前功能是否真的完成

Milestone 1 的目标基本完成，且 task-level review 已闭环：

- 已建立 external raw index 与 provenance hygiene。
- 已建立 `corpus_v1.jsonl`、duplicate report、missing metadata report。
- 已建立 `public_private_boundary.md`，明确 9 条 text-ready、1 条 metadata-only、1 条 structure-only 的下游边界。
- `corpus_v1.jsonl` 已被声明为 authoritative downstream snapshot。

就本 milestone 的定义而言，prompt corpus 与 provenance cleaning 已经达到“可分析 corpus”标准。

## 2. 是否能从干净环境运行

部分可以，不能过度表述为完全可重建：

- 当前仓库可通过 `python -m sair_competition.cli validate-layout`。
- `prompt_corpus_manifest.json` 与 `corpus_v1.jsonl` 可解析。
- 治理文件、manifest、audit summary 与 boundary note 彼此一致。

但仍存在 clean-environment 限制：

- GitHub MIT external source 仍是 metadata-only，未镜像到本地研究仓库。
- Contributor Network 仍只有 host-level provenance，缺稳定 prompt-level URL。
- 因此当前证明的是“review-backed local research snapshot 可读、可用”，不是“外部 public corpus 可从零完整重建”。

## 3. 是否有测试、demo 或实验结果

有基础验证，没有实验结果：

- `validate-layout` 通过。
- manifest JSON 与 `corpus_v1.jsonl` 解析通过。
- task-level reviewer 已独立复核 record counts、hash coverage、boundary gate。

当前没有：

- taxonomy 结果
- screening demo
- eval run
- experimental metrics

这与 milestone 定义一致，因为 Milestone 1 目标是 corpus/provenance cleaning，不是实验执行。

## 4. 是否存在伪完成

没有明显伪完成，但有两个需要持续防守的点：

- 不能把 metadata-only / structure-only 记录包装成 full-text ready 或 eval-ready。
- 不能把当前 corpus 状态写成完整 public ecosystem coverage 或完整 clean-room reconstruction。

T06 boundary note 已把这两个边界写清，所以当前不是伪完成；只是仍需在后续 milestone 里持续守住叙事口径。

## 5. 是否允许进入下一里程碑

允许，条件进入 Milestone 2。

条件：

1. T07/T10 只能使用 `corpus_v1.jsonl` 和 T06 boundary gates 决定 eligibility。
2. T07 只能对 9 条 text-ready local records 做 full-text taxonomy coding。
3. `prompt_tokens_est` 必须在 T07 中补足或给出 reviewable 估算规则，之后才能安全支持 length-bucket claims。
4. GitHub metadata-only 与 Contributor Network structure-only 仍不得进入 eval，除非未来 reviewed import/provenance task 改变状态。

## Summary

Milestone 1 已完成其应完成的治理与语料清洗目标，允许进入 Milestone 2。
结论为 `Conditional`，不是因为有 blocking defect，而是因为 clean-environment reproducibility 与外部 mirror/import 仍是有意保守留下的未决边界。
