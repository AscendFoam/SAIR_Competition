# Handoff

日期：2026-05-13

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

`T05_normalize_prompt_corpus_v1`

任务包：

- `docs/tasks/phase_1_public_corpus/T05_normalize_prompt_corpus_v1.md`

状态：

- Ready for worker。
- 尚未执行。
- T01、T02、T03、T04 已通过 review 并由 Captain 标记完成。

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
docs/tasks/phase_1_public_corpus/T05_normalize_prompt_corpus_v1.md
```

## 4. Worker 执行边界

下一轮 worker 只做 T05：

- 将 candidate register v0 规范化为 `corpus_v1.jsonl`。
- 生成 duplicate report 和 missing metadata report。
- 拆分 eligible/text-ready/mirrored external 计数。
- 决定是否镜像 MIT GitHub prompt 文件；若镜像，必须记录来源、hash、license 和 attribution。

不要做：

- 不改 `src/`。
- 不跑 API eval。
- 不改 prompt wording。
- 不下载外部数据。
- 不删除或重命名历史文档。
- 不标记任务完成。

## 5. Reviewer 重点

T05 reviewer 类型：normal。

重点检查：

- `corpus_v1.jsonl` 是否只包含 text-ready 或明确可复现记录。
- 是否生成 duplicate/missing metadata reports。
- Manifest 是否拆清 eligible 与 text-ready。
- 是否没有启动 eval、没有改 prompt wording、没有混入私有 prompt。
- 若镜像 MIT external prompt，是否保留 URL、license、author、hash 和 attribution。

## 6. 完成 T05 后 Captain 要做

如果 review 为 `PASS`：

1. 在 `docs/04_task_board.md` 勾选 `T05`。
2. 更新本文件的当前状态。
3. 推荐进入 `T06`，但不直接执行。
4. 若 corpus_v1 不可解析或 manifest 仍混淆 eligible/text-ready，阻止进入 T06。

如果 `PASS_WITH_WARNINGS`：

1. 把 warning 分类为 accepted、deferred、rejected。
2. deferred 写入 `docs/08_risks_and_open_questions.md`。
3. 再决定是否进入下一任务。

如果 `BLOCK`：

1. 只派修 blocking issue 的小任务。
2. 同一任务最多自动复审一次。
3. 第二次仍 BLOCK 则停止交给用户裁决。

## 7. 当前未验证事项

- normalized corpus 仍未采集完成，manifest 仅到 `candidate_register_v0_provenance_checked_not_normalized`。
- T05 尚未执行。
- contributor-network 占位项仍只有 host-level official provenance，尚未解析到稳定的具体 prompt 页面。
- screening / recomputed benchmark / post-release analysis 仍未开始执行。
- T05 之后的任务包尚未详细展开。
