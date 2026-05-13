# Contribution List

状态：planning with evidence tracking，非结果宣告。

## C1

- contribution statement: 构建一个带 provenance 的公开 prompt corpus schema、manifest 机制与来源边界说明。
- source in local docs: `docs/02_experiment_plan.md` 第 5.1-5.4、11.3、12 Phase 1；`docs/08_risks_and_open_questions.md` 的 R4、R7；`docs/review/T01_research_scaffold_review.md`。
- required evidence: corpus source registry、raw index、manifest、license or ToS audit、duplicate report、missing metadata report。
- current status: `supported_by_existing_assets`
- nearest competing work or likely reviewer objection: “这只是 schema，不是完成的 corpus”；需要在正文里承认当前只完成了机制与边界，不可提前宣称 coverage。

## C2

- contribution statement: 定义一个面向 Stage1 cheatsheet-style prompts 的 feature taxonomy，并与 problem family tags 分层维护。
- source in local docs: `docs/02_experiment_plan.md` 第 6 节、`docs/05_decision_log.md` D003、`docs/08_risks_and_open_questions.md` R11、`docs/review/T01_research_scaffold_review.md`。
- required evidence: taxonomy schema、manual coding guide、field mapping、conflict resolution note、prompt taxonomy 与 family tagger 边界说明。
- current status: `supported_by_existing_assets`
- nearest competing work or likely reviewer objection: “taxonomy 目前还是 seed，字段映射未闭环”；需要明确 T07 前必须补齐 mapping，并决定 `compression_style`、`ce_search_depth`。

## C3

- contribution statement: 建立统一的 `screening / recomputed benchmark / post-release analysis` 评测协议与结果记录规范。
- source in local docs: `docs/06_eval_protocol.md`、`docs/02_experiment_plan.md` 第 7 节、`docs/05_decision_log.md` D002。
- required evidence: finalized eval config schema、run artifacts contract、leakage notes、main table schema。
- current status: `supported_by_existing_assets`
- nearest competing work or likely reviewer objection: “你们只有 protocol，还没有正式 run outputs”；正文应把这部分写成 protocol contribution，不是 empirical result。

## C4

- contribution statement: 通过统一 protocol 量化 prompt 结构、模型迁移、分布偏移和 `P1_2_3` / `P1_2_5` 风险画像之间的关系。
- source in local docs: `docs/02_experiment_plan.md` RQ2-RQ4、10.1-10.3；`docs/项目工作历程与阶段性成果总结.md` 关于 `P1_2_3`、`P1_2_5`、family_tagger、offline rule assets、official playground 决策的章节。
- required evidence: prompt corpus、taxonomy annotations、screening results、recomputed benchmark、post-release analysis、family-conditioned metrics。
- current status: `planned_needs_data`
- nearest competing work or likely reviewer objection: “目前只有项目历史与风险画像，不是按统一研究 protocol 重算后的主结果”；需要等 T03-T15。

## C5

- contribution statement: 提出并验证一个 feature-aware textual distillation 方法家族，而不是继续做大规模 wording 搜索。
- source in local docs: `docs/02_experiment_plan.md` 第 8 节、15.1-15.4、17；`docs/08_risks_and_open_questions.md` R8。
- required evidence: distilled prompt variants、controlled ablations、cross-model and cross-split metrics、tradeoff analysis。
- current status: `planned_needs_data`
- nearest competing work or likely reviewer objection: “方法贡献过弱或只是 prompt rewriting”；必须靠 controlled variants 和 robustness evidence 回答。

## C6

- contribution statement: 形成带 attribution、release boundary、复现性说明和可公开资产边界的研究交付包。
- source in local docs: `docs/02_experiment_plan.md` 3.2、5.3、11、15；`docs/08_risks_and_open_questions.md` R7、R10；`docs/项目工作历程与阶段性成果总结.md` GitHub 同步注意事项。
- required evidence: reproducibility statement、release manifest、public/private asset boundary note、attribution policy。
- current status: `planned_needs_data`
- nearest competing work or likely reviewer objection: “你们的 release package 是否混入私有 prompt、raw outputs 或敏感资产”；需要到 T22 明确闭环。

## C7

- contribution statement: 说明 Stage1 已有工程资产为何足以支持后续科研，而不必退回 leaderboard 复盘或 Stage2 主线切换。
- source in local docs: `docs/02_experiment_plan.md` 第 2、3、10、13、17 节；`docs/05_decision_log.md` D001、D006；`docs/项目工作历程与阶段性成果总结.md` 阶段总结与 Stage1 收官章节。
- required evidence: asset inventory、fixed splits、CLI chain、family tagger / offline asset pipeline、handoff governance。
- current status: `supported_by_existing_assets`
- nearest competing work or likely reviewer objection: “这更像内部项目总结，而不是论文贡献”；在论文中应只作为 setup and motivation，不应占据结果 claim。

## C8

- contribution statement: 继续通过大规模 Stage1 prompt wording 搜索冲击 leaderboard ceiling，本身构成论文主贡献。
- source in local docs: `docs/02_experiment_plan.md` 2.2、4.3、17；`docs/08_risks_and_open_questions.md` R1、R2、R9。
- required evidence: 无；该方向已被当前研究 framing 明确排除。
- current status: `unsupported_do_not_claim`
- nearest competing work or likely reviewer objection: “这会把论文退化成比赛复盘或局部 prompt 调参总结”；该项保留为 rejected claim 示例，提醒后续写作不要把它误写成贡献。
