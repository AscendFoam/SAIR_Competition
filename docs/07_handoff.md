# Handoff

日期：2026-05-14

## 1. 当前项目状态

项目已从 Stage1 参赛收口切换到 Stage1 后赛事实证科研。核心基准文档是：

- `docs/02_experiment_plan.md`
- `docs/reference/AI_coding_workflow.md`

当前治理文档已初始化：

- `AGENTS.md`
- `CLAUDE.md`
- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## 2. Current Unique Task

`T06_corpus_audit_public_private_boundary`

任务包：

- `docs/tasks/phase_1_public_corpus/T06_corpus_audit_public_private_boundary.md`

状态：

- Ready for worker，尚未执行。
- T01、T02、T03、T04、T05 已通过 review 并由 Captain 标记完成。

T01 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T01_research_scaffold_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T01。
- Non-blocking followups: T03 清理 `storage_policy` typo；T07 前补 taxonomy mapping、`compression_style` 和 `ce_search_depth` 决策；T10 前收敛 `repeats` schema。

T02 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T02_paper_outline_contribution_matrix_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T02。
- Non-blocking followups: T03 修正 `outline.md` 绝对路径链接；T03/T21 前补 rejected/unsupported claim；C7 只保留为 setup/motivation。

T03 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T03_prompt_corpus_candidate_register_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T03。
- Candidate register: 11 candidates total; 9 direct-recompute local candidates; 1 metadata-only placeholder; 1 structure-only placeholder.
- Non-blocking followups: T04 处理 `data/*/prompt_corpus` git tracking strategy；T04 补 external placeholder URL/author/license；T05/T07 后续处理 token estimates。

T04 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T04_external_prompt_source_collection_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T04。
- Git tracking: `.gitignore` narrow allowlist for prompt corpus governance files。
- External provenance: GitHub MIT source verified but not mirrored; Contributor Network remains host-level / structure-only。
- Non-blocking followups: T05 split eligible/text-ready counts；T05/T06 seek stable contributor URL and more external candidates；T05 align raw_index example schema。

T05 review 判断：

- Verdict: `PASS`
- Review file: `docs/review/T05_normalize_prompt_corpus_v1_review.md`
- Captain action: accepted; `docs/04_task_board.md` 已勾选 T05。
- Corpus v1: 11 records; 9 text-ready; 10 eligible; 1 metadata-only; 1 structure-only; 0 mirrored external; 0 duplicates.
- Non-blocking followups: `corpus_v1.jsonl` 作为 authoritative corpus snapshot；token estimate deferred to T07；GitHub MIT mirror decision and Contributor Network stable URL deferred to T06 or later provenance task；missing metadata grouping cosmetic and not required now。

## 3. 下一位 Worker 需要先读

```text
README.md
AGENTS.md
docs/02_experiment_plan.md
docs/03_architecture.md
docs/04_task_board.md
docs/06_eval_protocol.md
docs/07_handoff.md
docs/08_risks_and_open_questions.md
docs/tasks/phase_1_public_corpus/T06_corpus_audit_public_private_boundary.md
docs/review/T05_normalize_prompt_corpus_v1_review.md
data/interim/prompt_corpus/corpus_v1.jsonl
data/interim/prompt_corpus/duplicate_report_v1.json
data/interim/prompt_corpus/missing_metadata_report_v1.json
data/interim/prompt_corpus/prompt_corpus_manifest.json
reports/research/corpus_audit/summary.md
```

## 4. Worker 执行边界

下一位 worker 只执行 T06：

- 基于 T05 `corpus_v1`、duplicate report、missing metadata report 和 manifest，重写或补强 corpus audit summary。
- 新增 public/private asset boundary note，清楚区分 public reproducible、local historical、metadata-only、structure-only、excluded/not-for-release。
- 明确 T07/T10 的使用规则：只有 text-ready + hash 覆盖记录可进入本地直接复算；metadata-only / structure-only 不进入 eval。
- 记录 GitHub MIT source 未镜像、Contributor Network 仅 host-level provenance、token estimates 仍为 0 的后续处理建议。

不要做：

- 不改 `src/`。
- 不跑 API eval。
- 不改 prompt wording。
- 不下载或镜像外部 prompt 原文。
- 不删除或重命名历史文档。
- 不改 `docs/04_task_board.md` 完成状态。

允许修改文件：

- `reports/research/corpus_audit/summary.md`
- `reports/research/corpus_audit/public_private_boundary.md`
- `data/interim/prompt_corpus/prompt_corpus_manifest.json`
- `data/interim/prompt_corpus/provenance_rules.md`
- `docs/07_handoff.md`

T05 corpus summary：

- `corpus_v1_record_count = 11`
- `eligible_count = 10`
- `text_ready_count = 9`
- `mirrored_external_count = 0`
- `metadata_only_count = 1`
- `structure_only_count = 1`
- `excluded_count = 0`
- duplicate report: no duplicates found in T05
- mirrored GitHub prompt text: no

## 5. Reviewer 重点

T06 reviewer 类型：normal。

重点检查：

- public/private asset boundary 是否准确反映 T05 corpus facts，而不是扩大结论。
- 是否把 9 条 text-ready local records、1 条 GitHub metadata-only record、1 条 contributor-network structure-only record 的下游使用规则写清楚。
- 是否明确 corpus v1 不是完整 public ecosystem coverage。
- 是否没有复制外部 prompt 原文、没有跑 eval、没有改 prompt wording。
- 是否为 T07 taxonomy 和 T10 screening 留下清晰的进入条件。

## 6. 完成 T06 后 Captain 要做

如果 review 为 `PASS`：

1. 在 `docs/04_task_board.md` 勾选 `T06`。
2. 更新本文件的当前状态。
3. 可以推荐进入 `T07`，但不直接执行。
4. 若 boundary note 混淆 public/private、把 metadata-only 或 structure-only 记录放入 eval，或把 corpus 写成完整生态覆盖，则阻止进入 T07。

如果 `PASS_WITH_WARNINGS`：

1. 把 warning 分类为 accepted、deferred、rejected。
2. deferred 写入 `docs/08_risks_and_open_questions.md`。
3. 再决定是否进入下一任务。

如果 `BLOCK`：

1. 只派修 blocking issue 的小任务。
2. 同一任务最多自动复审一次。
3. 第二次仍 BLOCK 则停止交给用户裁决。

## 7. 当前未验证事项

- T06 public/private asset boundary 尚未执行。
- GitHub MIT external source 仍未镜像，本地 external text-ready record 仍为 `0`。
- contributor-network 占位项仍只有 host-level official provenance，尚未解析到稳定的具体 prompt 页面。
- `prompt_tokens_est` 在 `corpus_v1` 中仍全部为 `0`。
- screening / recomputed benchmark / post-release analysis 仍未开始执行。
- T07 taxonomy 任务包尚未详细展开。
