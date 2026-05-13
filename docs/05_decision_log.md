# Decision Log

本文件记录影响研究方向、架构或复现实验解释的关键决策。普通执行细节写入 `docs/07_handoff.md`。

## D001: Stage1 后续主线切换为 prompt textual distillation research

日期：2026-05-11

决策：

后续主线从“继续优化 Stage1 prompt 刷榜”切换为“基于公开 prompt 生态的 textual distillation 与鲁棒性研究”。

理由：

- Stage1 最终提交已收口。
- 仓库已有数据、评测、tagger 和 analysis 资产。
- 继续刷 prompt 容易陷入局部 wording 调参，科研价值低。
- corpus、taxonomy、统一复算和 robustness gap 更容易形成可发表贡献。

影响：

- `docs/02_experiment_plan.md` 作为研究基准。
- `docs/04_task_board.md` 以 Phase 0 到 Phase 7 组织任务。
- Stage2 只保留轻量规则跟踪和资产映射。

## D002: Released final evaluation subsets 只作为后赛事实证分析

日期：2026-05-11

决策：

任何 released final evaluation subsets 的使用必须标注为 `post-release analysis`，不得作为 prompt selection reward，不得包装成赛时盲测泛化。

理由：

- subsets 已公开，存在后视镜风险。
- 论文可信度依赖清晰区分 screening、recomputed benchmark 和 post-release analysis。

影响：

- `docs/06_eval_protocol.md` 明确三类评测。
- reviewer 必须检查是否有泄漏式叙事。

## D003: Prompt taxonomy 和 problem family tagger 分层维护

日期：2026-05-11

决策：

prompt taxonomy 描述 prompt 结构，family tagger 描述题目结构，两者不合并。

理由：

- 合并标签会让解释对象混乱。
- 真正的研究价值来自 prompt feature 和 problem family 的交叉分析。

影响：

- `configs/research/prompt_feature_taxonomy.yaml` 后续只定义 prompt 结构标签。
- family-conditioned metrics 在 analysis 层完成。

## D004: 默认单 worker 顺序执行

日期：2026-05-11

决策：

除非 Captain 拆出互不依赖且文件范围不重叠的任务，否则默认单 worker 顺序执行。

理由：

- 当前任务主要涉及治理文档、schema、目录和评测协议，状态强相关。
- 并行会增加文档状态冲突和 review 成本。

影响：

- `docs/04_task_board.md` 始终维护一个 Current Unique Task。

## D005: 接受 T01 review verdict 并进入 T02

日期：2026-05-12

决策：

`docs/review/T01_research_scaffold_review.md` verdict 为 `PASS`，Captain 接受该结论，标记 `T01_research_scaffold` 完成，并将 Current Unique Task 切换到 `T02_paper_outline_contribution_matrix`。

理由：

- Reviewer 未发现 blocking issue。
- T01 输出均为 scaffold/seed/example 状态，没有伪造 corpus 或实验完成事实。
- JSON/YAML 和 JSONL 示例已通过 reviewer 独立验证。
- 没有越界修改 `src/`、`tests/`、prompt wording 或历史 artifacts。

非阻塞事项处理：

- `repeats: "1-3"` 作为 example template 暂时接受，正式 runner config 在 T10 前收敛。
- `storage_policy` typo 放入 T03 清理范围。
- taxonomy 字段映射、`compression_style`、`ce_search_depth` 放入 T02/T07 后续约束。

## D006: T02 优先于 T03

日期：2026-05-12

决策：

下一任务先做 T02，而不是直接做 T03 corpus candidate register。

理由：

- T01 已创建 paper outline v0，但 outline 仍是高层 scaffold。
- 先建立 claim/evidence/status 矩阵，可以约束后续 corpus 收集和 taxonomy 标注服务于论文主张。
- T02 不需要网络和 API 成本，适合作为进入真实数据登记前的低风险收敛任务。

## D007: 接受 T02 review verdict 并进入 T03

日期：2026-05-12

决策：

`docs/review/T02_paper_outline_contribution_matrix_review.md` verdict 为 `PASS`，Captain 接受该结论，标记 `T02_paper_outline_contribution_matrix` 完成，并将 Current Unique Task 切换到 `T03_prompt_corpus_candidate_register`。

理由：

- Reviewer 未发现 blocking issue。
- T02 输出明确区分 supported、planned、unsupported/forbidden wording，没有把未运行实验写成结果。
- 修改范围符合任务包，未触碰代码、prompt、configs、data 或 artifacts。
- paper claim guardrail 已能约束 T03 后续 corpus 收集。

非阻塞事项处理：

- `contribution_list.md` 未实际使用 `unsupported_do_not_claim`：deferred，T03 任务包要求新增 rejected/unsupported claim register 或说明，最终论文草稿前复核。
- C7 更像内部项目 justification：accepted，保留为 setup/motivation，不作为最终论文主贡献。
- `outline.md` 绝对 Windows 链接：deferred 到 T03 hygiene fix。
- abstract tense preference：accepted，无需立即修；后续 paper draft 再统一时态。

## D008: T03 进入 prompt candidate register，而不是直接执行 corpus collection

日期：2026-05-12

决策：

下一任务是建立 `prompt candidate register v0` 和 provenance rules，不直接下载外部 prompt、不跑 API、不进入正式 Phase 1 collection。

理由：

- 当前仍处于 Phase 0，重点是候选边界和来源规则。
- 先把本地 prompt、官方 archetype、可公开/不可公开候选、结构级记录资格分清楚，可以降低后续版权、归因和数据泄漏风险。
- T03 可吸收 T02 review 的链接和 unsupported claim 小清理，不需要单开任务。

## D009: 接受 T03 review verdict 并进入 Phase 1

日期：2026-05-13

决策：

`docs/review/T03_prompt_corpus_candidate_register_review.md` verdict 为 `PASS`，Captain 接受该结论，标记 `T03_prompt_corpus_candidate_register` 完成，并将 Current Unique Task 切换到 `T04_external_prompt_source_collection`。

理由：

- Reviewer 未发现 blocking issue。
- Candidate register v0 覆盖 11 个候选，满足 `8-12` 启动目标。
- 9 个本地 prompt 的 SHA256 和 byte size 已被 reviewer 独立验证。
- Public placeholders 未伪造数据，仍标注为 metadata-only / structure-only。
- Manifest 仍标注 `candidate_register_v0_not_cleaned`，没有把 candidate register 写成 completed corpus。

非阻塞事项处理：

- `data/` prompt corpus 文件被 `.gitignore` 排除：deferred 到 T04 前置决策，T04 任务包必须处理 tracking strategy。
- `prompt_tokens_est` 为 0：accepted for v0，deferred 到 corpus normalization 或 taxonomy coding。
- external placeholders 缺少 URL、author、license：deferred 到 T04 主任务。
- `configs/research/corpus_sources.example.json` typo 未改：accepted because T03 forbidden scope 禁止修改该目录；后续 config hygiene 时处理。

## D010: T04 允许核验外部 provenance，但仍不复制外部 prompt 原文

日期：2026-05-13

决策：

T04 可以核验外部候选的公开 URL、作者/团队、license/ToS 和 storage eligibility，但不得复制外部 prompt 原文到仓库，除非来源许可明确允许且任务包要求写入。

理由：

- T03 已建立 public placeholders，但缺少真实 provenance。
- Phase 1 的目标是 provenance cleaning，不是扩大不可控 prompt 文本仓库。
- 继续保护 public/private asset boundary，避免版权和归因风险。

## D011: 接受 T04 review verdict 并进入 T05

日期：2026-05-13

决策：

`docs/review/T04_external_prompt_source_collection_review.md` verdict 为 `PASS`，Captain 接受该结论，标记 `T04_external_prompt_source_collection` 完成，并将 Current Unique Task 切换到 `T05_normalize_prompt_corpus_v1`。

理由：

- Reviewer 未发现 blocking issue。
- `.gitignore` 已采用窄 allowlist，解决 prompt corpus governance files 普通 git tracking 问题，同时没有放开私有 raw/interim 数据。
- `raw_index.jsonl` 已记录 2 个外部 source 的 provenance 状态。
- GitHub public source 已核验 URL、作者和 MIT license；Contributor Network source 被保守地保留为 structure-only。
- 没有复制外部 prompt 原文，没有跑 API，没有触碰代码或 prompt wording。

非阻塞事项处理：

- `direct_recompute_count` 语义混合：deferred 到 T05，任务包必须拆分 eligible 与 text-ready。
- Contributor Network 依赖 LinkedIn host-level provenance：deferred 到 T05/T06 寻找稳定一手 URL，否则保持 structure-only。
- 外部候选数量仍少：deferred 到 T05/T06 主动寻找 GitHub/paper candidates。
- `raw_index.example.jsonl` schema 落后：deferred 到 T05 对齐。

## D012: T05 先 normalize corpus v1，不启动 eval

日期：2026-05-13

决策：

T05 只将候选登记规范化为 `corpus_v1.jsonl`、生成 duplicate/missing metadata report，并修正计数语义；仍不启动 screening、API eval 或 prompt 改写。

理由：

- 评测前必须有稳定 corpus snapshot 和 manifest。
- 当前 GitHub external source 虽可许可镜像，但是否导入具体 prompt 文件需要单独记录来源、hash 和 attribution。
- `post-release analysis` 纪律仍要求 prompt selection 不使用 released subsets。
