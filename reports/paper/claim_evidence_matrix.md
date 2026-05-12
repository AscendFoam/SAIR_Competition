# Claim Evidence Matrix

状态：claim guardrail，供后续 worker 和 reviewer 共同约束措辞。

## CL1

- claim text: 本研究把 SAIR Stage1 公开 prompt 生态建模为一个 provenance-aware textual distillation 研究对象。
- linked RQ: `RQ1-RQ6`
- needed artifact: research framing docs、paper outline、corpus schema
- current evidence: `docs/02_experiment_plan.md`、`docs/05_decision_log.md` D001、D006、T01 scaffold
- missing evidence: 无需额外实验，但需要后续 corpus 真正落地
- allowed wording now: “We study” / “We frame” / “We plan to analyze”
- forbidden wording now: “We have completed the public corpus analysis”

## CL2

- claim text: 一个带 provenance 的 prompt corpus schema 与 manifest 机制已经设计完成，可作为后续公开语料清洗基础。
- linked RQ: `RQ1`
- needed artifact: corpus source registry、manifest、README boundary note
- current evidence: T01 scaffold files、`docs/review/T01_research_scaffold_review.md`
- missing evidence: raw index real entries、hash coverage、license audit
- allowed wording now: “We provide a schema and manifest scaffold”
- forbidden wording now: “We collected a complete public corpus”

## CL3

- claim text: Prompt taxonomy 与 problem family tagger 是分层维护的两个标签体系。
- linked RQ: `RQ1-RQ4`
- needed artifact: taxonomy schema、decision log、future mapping note
- current evidence: `docs/05_decision_log.md` D003、`docs/02_experiment_plan.md` 6.4、T01 taxonomy scaffold
- missing evidence: experiment plan section 6.2 to YAML field mapping
- allowed wording now: “We separate prompt taxonomy from problem-family labels”
- forbidden wording now: “Our taxonomy implementation is finalized and complete”

## CL4

- claim text: taxonomy mapping from experiment plan section 6.2 to YAML fields 是后续 manual coding 前置条件。
- linked RQ: `RQ1-RQ2`
- needed artifact: mapping note or taxonomy report
- current evidence: `docs/08_risks_and_open_questions.md` R11、`docs/review/T01_research_scaffold_review.md`
- missing evidence: explicit mapping document or integrated T07 report
- allowed wording now: “Field mapping remains an explicit prerequisite”
- forbidden wording now: “The YAML already fully matches the section 6.2 feature list”

## CL5

- claim text: `compression_style` 和 `ce_search_depth` 目前是 taxonomy 缺口，尚未进入最终结论层。
- linked RQ: `RQ2`
- needed artifact: taxonomy decision or audit note
- current evidence: `docs/02_experiment_plan.md` 6.2、`docs/08_risks_and_open_questions.md`、`docs/review/T01_research_scaffold_review.md`
- missing evidence: T07 前的明确保留/合并/删除决策
- allowed wording now: “These fields remain open taxonomy design questions”
- forbidden wording now: “compression_style and ce_search_depth are already captured in TAX_V1”

## CL6

- claim text: 本项目已有统一的三阶段评测 protocol，可约束 screening、recomputed benchmark 与 post-release analysis。
- linked RQ: `RQ2-RQ5`
- needed artifact: protocol doc、example eval matrix、future finalized configs
- current evidence: `docs/06_eval_protocol.md`、T01 example eval matrix、`docs/05_decision_log.md` D002
- missing evidence: finalized runner configs and actual research run outputs
- allowed wording now: “We define a staged evaluation protocol”
- forbidden wording now: “We have already run the full protocol and obtained final results”

## CL7

- claim text: `released final evaluation subsets` 只能作为 `post-release analysis`。
- linked RQ: `RQ4-RQ5`
- needed artifact: protocol, risks, paper wording constraints
- current evidence: `docs/06_eval_protocol.md`、`docs/08_risks_and_open_questions.md` R3、`docs/05_decision_log.md` D002
- missing evidence: future reports must actually keep this label
- allowed wording now: “released final evaluation subsets are used only for post-release analysis”
- forbidden wording now: “released final evaluation subsets serve as blind test generalization evidence”

## CL8

- claim text: 现有 Stage1 工程资产足以支撑研究 setup，包括 fixed splits、CLI、family tagger、offline rule assets 与 `P1_2_3` / `P1_2_5` 风险画像。
- linked RQ: `RQ2-RQ4`
- needed artifact: local reports and inventory
- current evidence: `docs/项目工作历程与阶段性成果总结.md`、`README.md`、`docs/02_experiment_plan.md`
- missing evidence: 无需新增实验，但需要在论文中控制其位置，只作 background/setup
- allowed wording now: “The repository already contains reusable engineering assets”
- forbidden wording now: “These assets already prove the paper’s main structural findings”

## CL9

- claim text: `P1_2_3` 与 `P1_2_5` 可以作为风险画像对照研究对象。
- linked RQ: `RQ2-RQ4`
- needed artifact: local historical reports, later unified recomputation
- current evidence: `docs/项目工作历程与阶段性成果总结.md`、`docs/02_experiment_plan.md` 10.1-10.2
- missing evidence: unified research-protocol recomputation and family-conditioned analysis
- allowed wording now: “We treat P1_2_3 and P1_2_5 as candidate contrast cases”
- forbidden wording now: “Our paper has already established definitive comparative findings for P1_2_3 vs P1_2_5”

## CL10

- claim text: 后续论文将报告 prompt 结构与性能、迁移和鲁棒性的统计关系。
- linked RQ: `RQ2-RQ4`
- needed artifact: corpus, taxonomy, screening, full eval, statistical analysis
- current evidence: only planning docs and candidate hypotheses
- missing evidence: all empirical artifacts from T03-T20
- allowed wording now: “We plan to quantify” / “We will test whether”
- forbidden wording now: “We show” / “We find” / “We demonstrate” in the present tense

## CL11

- claim text: feature-aware textual distillation improves robustness.
- linked RQ: `RQ5`
- needed artifact: distilled prompt variants, controlled ablations, full eval, robustness analysis
- current evidence: none; only method plan exists in `docs/02_experiment_plan.md`
- missing evidence: T16-T20 outputs
- allowed wording now: “We plan to evaluate whether feature-aware textual distillation improves robustness”
- forbidden wording now: “feature-aware textual distillation improves robustness” 

## CL12

- claim text: 论文会提供 reproducibility / attribution package。
- linked RQ: cross-cutting
- needed artifact: release manifest, reproducibility statement, attribution and storage boundary note
- current evidence: planning docs and repository discipline
- missing evidence: T21-T22 deliverables
- allowed wording now: “We intend to release a reproducibility and attribution package within the public boundary”
- forbidden wording now: “A full public reproducibility package is already available”

## Reviewer Followups To Preserve

- `forbidden wording`: do not write method outcomes in result tense before T16-T20.
- `forbidden wording`: do not describe released final evaluation subsets as blind test evidence.
- `forbidden wording`: do not imply taxonomy field drift has been resolved before T07.
- `forbidden wording`: do not imply `compression_style` or `ce_search_depth` are already settled.
