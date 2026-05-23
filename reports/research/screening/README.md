# Screening Reports

本目录用于记录 Stage A `screening` 评测设计、执行结果和 shortlist 决策。

## 当前状态

T11 + T12 screening execution 已完成。9 条 text-ready local prompts 分别在 smoke split 上使用 `deepseek-chat` 和 `deepseek-v4-flash` 完成了两轮 screening。

**SCREENING FAILURE**: 两个模型的结果完全一致——所有 9 个候选均被 elimination gates 淘汰。0 个候选进入 shortlist。需 Captain 裁决。

- P0 (relaxed format): parse collapse，两个模型 parse_success_rate 分别为 0.27 和 0.23
- 其余 8 个 strict-format prompts: all-false collapse，两个模型的 true_recall (0.00-0.03) 和 false_recall (0.97-1.00) 几乎完全相同
- 替代模型（MiniMax-M2.7, deepseek-reasoner）在 max_tokens=256 下无法产生可解析输出，已记录但不作为正式 screening run

## 文件清单

| 文件 | 说明 |
|---|---|
| `screening_matrix_v1.md` | Screening evaluation matrix（T10 设计，已冻结） |
| `screening_candidate_registry_v1.md` | 9 条候选 registry（T10 设计，已冻结） |
| `screening_shortlist_rules_v1.md` | Shortlist 决策规则（T10 设计，已冻结） |
| `screening_execution_manifest_v1.md` | T11 执行 manifest（deepseek-chat） |
| `screening_second_model_manifest_v1.md` | T12 执行 manifest（deepseek-v4-flash） |
| `screening_model_comparison_note_v1.md` | T11 vs T12 模型对比笔记 |

## 已完成

- T10: Build screening evaluation matrix
- T11: Run screening on 9 prompt candidates using smoke split with deepseek-chat
- T12: Rerun screening with alternate model (deepseek-v4-flash), write comparison note

## 待完成

- Shortlist formation（需 Captain 先处理 screening failure）
- 非 DeepSeek 提供商的 screening 测试（如 Captain 决定需要）

## 设计原则

- 排查 parse collapse、all-true/all-false collapse。
- 形成 3-5 个 prompt 的 shortlist 进入 recomputed benchmark。
- Screening 结果不直接用于论文性能结论，只用于排除和 shortlist 决策。
- 10 个低方差 taxonomy 字段不作为 shortlist 主决策依据。
