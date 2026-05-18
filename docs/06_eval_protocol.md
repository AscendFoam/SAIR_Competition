# Evaluation Protocol

## Captain Status Update (2026-05-18, T11 Review)

- `T11_run_screening_on_selected_prompt_candidates` is accepted by Captain as `PASS_WITH_WARNINGS`.
- The first live Stage A screening run is complete on `deepseek / deepseek-chat`, and it yielded a screening failure with zero surviving prompts.
- This outcome is treated as a provider/model behavior finding under the frozen protocol, not as a reason to rewrite Stage A gates retroactively.
- The next protocol step is `T12_rerun_screening_with_alternate_low_cost_model`: rerun the same 9 prompts on the same smoke split with the same frozen non-model settings, varying only provider/model and documenting whether collapse persists.

日期：2026-05-12

## 1. 基本原则

本项目后续实验分为三类：

1. `screening`: 小样本筛选，用于检查 parse stability、true/false collapse 和候选是否值得进入完整评测。
2. `recomputed benchmark`: 统一配置下的复算，用于论文主结果。
3. `post-release analysis`: 在已公开 released final evaluation subsets 上做后赛事实证分析。

纪律：

- 不把 `post-release analysis` 包装成赛时未知盲测。
- 不在 released subsets 上调 prompt。
- 不只汇报 accuracy，必须同时报告 parse、recall、cost/time 或明确说明无法获得。
- 每个 run 必须保存 prompt hash、dataset version、model/provider config 和 parser/metrics 版本。

## 2. 数据切分

当前本地固定切分：

- `data/interim/splits/smoke.jsonl`: 快速回归和格式检查。
- `data/interim/splits/dev.jsonl`: 开发与结构分析。
- `data/interim/splits/holdout.jsonl`: 本地稳定性检查。
- `data/interim/splits/audit.jsonl`: 人工审阅与边界案例。

研究中可引用的 released subsets：

- `evaluation_normal`
- `evaluation_hard`
- `evaluation_extra_hard`
- `evaluation_order5`

这些 released subsets 必须统一称为 released final evaluation subsets，并标注为后赛事实证分析。

## 3. Prompt 候选集合

第一批候选优先来自：

1. `P1.2.3_implicit_guardrail_v2`
2. `P1.2.5_minimal_rule_missing_hard_composition`
3. `P2.0.0_official_balanced_strict_v0`
4. `P2.0.1_official_counterexample_first_strict_v0`
5. `P2.0.2_official_fast_filters_strict_v0`
6. minimal no-cheatsheet baseline
7. 可合法复现的 public CE-first prompt
8. 可合法复现的 public trivial-first prompt
9. human distilled prompt v0
10. LLM-assisted distilled prompt v0
11. feature-aware distilled prompt v0
12. 可选 public contributor prompt

如果 prompt 原文不可合法存储或复现，只做结构级编码，不纳入直接复算。

## 4. 三阶段评测

### Stage A: Screening

目标：

- 检查 parse success rate。
- 初步观察 true/false recall。
- 排除 all-true、all-false、格式不稳和不可复现候选。

建议：

- prompt 数量：`8-12`
- model：先用低成本 proxy 或当前可用 API
- repeats：`1`
- 数据：`smoke` 加 hard 分层子样本

进入下一阶段条件：

- parse success rate 接近 `1.0`
- 无明显塌缩
- 至少代表一种有研究意义的结构类型

### Stage B: Full Recomputed Benchmark

目标：

- 形成论文主表。
- 比较 prompt、model、split 的稳定性。

建议：

- prompt 数量：`3-5`
- model：官方三模型或最接近组合
- 数据：本地固定切分和 released final evaluation subsets
- repeats：`1-3`，按预算决定

必须输出：

- `predictions.jsonl`
- `raw_outputs.jsonl` 或等价缓存
- `summary.json`
- `metrics.csv`
- `run_config.json`
- `prompt_hash_manifest.json`

### Stage C: Ablation and Robustness

建议消融：

- `short / medium / near-cap`
- `trivial-first / CE-first`
- `strict formatting / relaxed formatting`
- `with examples / no examples`
- `false-filter heavy / balanced / true-recall oriented`
- `universal prompt / model-specific prompt`

目标不是找最高分，而是验证结构因素。

## 5. 指标

必须优先报告：

- `accuracy`
- `strict_f1`
- `parse_success_rate`
- `true_recall`
- `false_recall`
- `avg_time_secs`
- `avg_cost_usd`
- `repeat_consistency`

本项目新增指标：

- `prompt_bytes`
- `prompt_tokens_est`
- `balanced_accuracy`
- `robustness_gap`
- `model_transfer_gap`
- `format_failure_rate`
- `family_conditional_accuracy`
- `family_conditional_recall`

如果某个指标无法获得，报告必须说明原因。

## 6. 推荐命令

仓库布局检查：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli validate-layout
```

family tagger 示例：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli tag-problem-families --dataset-path data/interim/splits/dev.jsonl --output-path data/interim/splits/dev_tagged.jsonl --summary-dir reports/experiments/dev_family_tags
```

complete prompt eval 示例：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli run-complete-prompt-eval --dataset-path data/interim/splits/smoke.jsonl --prompt-path prompts/complete/<candidate>.txt --output-dir artifacts/candidates/<run_id> --dotenv-path .env --model <model> --temperature 0 --max-tokens 256
```

错误分析示例：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli analyze-errors --predictions-path artifacts/candidates/<run_id>/predictions.jsonl --output-dir artifacts/candidates/<run_id>_analysis
```

候选对比示例：

```powershell
$env:PYTHONPATH='src'
python -m sair_competition.cli compare-candidates --candidate-dir artifacts/candidates/<run_a> --candidate-dir artifacts/candidates/<run_b> --output-dir reports/experiments/<comparison_id>
```

## 7. 结论判定纪律

一个 prompt 方法只有满足以下条件，才可作为论文方法结论：

- 不只在单一模型提升。
- 不只在单一 split 提升。
- 不以 parse failure 换取表面分数。
- 不用 released subsets 调参后宣称盲测泛化。
- 能解释 true/false tradeoff。
- 能报告成本与延迟，或明确说明不可获得。

## 8. Config Followups from T01 Review

T01 review 已确认 `configs/research/evaluation_matrix.example.json` 是可解析 seed template。后续正式评测配置必须进一步收敛：

- `repeats` 在正式 runner config 中不得使用 `"1-3"` 这种说明性字符串，应改为整数、整数列表或明确 schema。
- `post-release analysis` 仍只能用于最终鲁棒性分析，不能进入 prompt selection reward。
- 所有正式 run 仍必须保留 `run_config.json`、`metrics.csv`、`prompt_hash_manifest.json` 和 leakage notes。

这些事项不阻塞 T02；它们进入 T10 `Build screening evaluation matrix` 前的验收条件。

## 9. Claim Guardrails from T02

T02 已建立 `reports/paper/claim_evidence_matrix.md`。后续所有实验报告和论文草稿必须遵守：

- 没有 T03-T20 证据前，不使用 “we show / we find / improves robustness” 这类结果时态描述。
- `released final evaluation subsets` 只写作 `post-release analysis`。
- `P1_2_3` 与 `P1_2_5` 当前只能写作 candidate contrast cases，不能写作已完成统一 protocol 对照结论。
- feature-aware textual distillation 当前只能写作 method plan，不能写作有效方法。

T03 只建立候选登记和 provenance 边界，不产生 eval evidence。

## 10. Candidate Register Status from T03

T03 已建立 `candidate_register_v0`，但它不是 eval shortlist，也不是 normalized corpus。

当前约束：

- direct-recompute local candidates 可作为后续 screening 候选池来源，但仍需 T04/T05 provenance 和 corpus normalization。
- metadata-only / structure-only public placeholders 不可直接进入 eval。
- `prompt_tokens_est` 暂不可用于统计结论。
- `prompt_bytes` 和 SHA256 可用于 v0 hash coverage 和 size sanity check。

T04/T05 完成前，不应启动 T10 screening。

## 11. T04 Provenance Status

T04 已完成外部 provenance v0：

- `github_public_prompt_repo_cazares_2026`: URL、author/team、MIT license verified；raw prompt text not mirrored in T04。
- `contributor_network_stage1_official_post_2026`: host-level official provenance only；storage rights and specific prompt page unresolved；keep structure-only。

Eval implications:

- GitHub source may become direct-recompute only after T05 imports and hashes a specific prompt file, or records a reproducible retrieval path.
- Contributor Network source must not enter direct eval until stable prompt-level provenance exists.
- Manifest counts must distinguish eligible source from local text-ready prompt.

## 12. Corpus v1 Eval Eligibility from T05

T05 已通过 review，`corpus_v1.jsonl` 是后续 eval 候选池的 authoritative corpus snapshot，但不是 eval shortlist。

当前 eval eligibility：

- `included_text_ready`: 9 条本地记录，可在 T10 之后按 screening matrix 进入直接复算候选池。
- `included_metadata_only`: 1 条 GitHub MIT record，provenance-eligible 但未本地镜像、无 local path/hash，不能直接进入 eval。
- `included_structure_only`: 1 条 Contributor Network record，只有 host-level provenance，不能直接进入 eval。
- `excluded`: 0 条。

T10 前约束：

- 只允许 text-ready 且 SHA256 覆盖的 prompt 进入 screening execution。
- 若要使用 GitHub MIT prompt 原文，必须先通过独立任务镜像文件、记录 path/hash/byte size/license/attribution，并更新 manifest。
- Contributor Network record 在稳定 prompt-level provenance 和 storage terms 确认前不得进入 eval。
- `prompt_tokens_est=0` 不可用于长度分桶或 token-based analysis；T07 前需要补估算或明确改用 byte size。

## 13. Milestone 1 Gate After T06

Milestone 1 已做 milestone review，结论为 `Conditional`：

- corpus/provenance cleaning 已完成并可进入 Milestone 2；
- 但不能把当前状态误写成“可从干净环境完全重建所有 public corpus assets”。

对 T07/T10 的直接影响：

- T07 必须先产出可复核的 manual taxonomy 和 `prompt_tokens_est`/length-bucket 口径，T10 才能安全引用长度特征。
- T10 screening 候选池仍仅限于 9 条 text-ready local records，除非未来 reviewed import task 改变 GitHub metadata-only record 的状态。
- Milestone 2 的任何报告都不能把 metadata-only / structure-only 记录包装成已参与 full-text coding 或 eval。

## 14. Taxonomy Gate After T07

T07 已通过 review，意味着：

- `prompt_features_v1.jsonl` 可作为 T08 extractor skeleton 的人工基线；
- T10 未来可以引用 taxonomy 字段，但仍不应先于 T08/T09 启动主线执行。

当前约束：

- T08 需要先把 extractor 输出与人工基线对齐，再谈更大范围自动化。
- token estimate 目前仍是启发式，不是 tokenizer 精确计数；任何长度相关结论必须继续谨慎表述。
- 低方差字段可以保留，但不能在 screening 或统计解释中被误当成高信息量特征。

## 15. Self-Audit Gate After T08

T08 已通过 review，但 T10 仍不应直接启动。

原因：

- 当前已经同时存在 manual taxonomy 与 extractor skeleton，两者之间需要先做一致性自审。
- 已知存在至少一个字段分歧：P2.0.2 `counterexample_requirement`。
- 低方差字段和测试语义边界还需要在 T09 中写成明确结论。

因此，T10 前仍有一个硬门槛：

- T09 必须先给出 self-audit 与 conflict resolution note，确认哪些字段可直接用于 screening/reporting，哪些字段只能作为说明性标签。

## 16. Screening Gate After T09

T09 已通过 review，因此 T10 现在可以启动，但仍必须遵守以下 protocol：

- screening 候选池仅限于 9 条 `included_text_ready` local prompts；metadata-only / structure-only records 不得混入。
- T10 matrix 中可直接用于筛选或后续统计规划的字段，应优先来自 `self_audit_v1.md` Section 4.1；low-variance fields 仅可作为 descriptive labels。
- manual coding 是 taxonomy truth；extractor 输出只能作为 cross-check、批量辅助或一致性质量信号。
- T10 需要把 `repeats` 从 example/template 表达收敛为可执行的正式字段，不再沿用 `"1-3"` 这类说明性字符串。
- T11 在 T10 完成并通过 review 前，不得提前运行 screening execution。
## Captain Status Update (2026-05-18)

- `T10_build_screening_evaluation_matrix` has passed review and is now Captain-accepted.
- `T11_run_screening_on_selected_prompt_candidates` may now execute Stage A screening on the 9 text-ready local prompts.
- During T11, `provider_route` must be filled with the actual route used, but screening `prompt_set`, `dataset_set`, `repeats`, `temperature`, `max_tokens`, and `reasoning_mode` stay frozen from the T10 matrix unless Captain opens a new task.
