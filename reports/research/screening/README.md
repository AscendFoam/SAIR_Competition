# Screening Reports

本目录用于记录 Stage A `screening` 评测设计、执行结果和 shortlist 决策。

## 当前状态

T11 screening execution 已完成。9 条 text-ready local prompts 已在 smoke split 上使用 deepseek-chat 模型完成 screening。

**SCREENING FAILURE**: 所有 9 个候选均被 elimination gates 淘汰。0 个候选进入 shortlist。需 Captain 裁决。

- P0 (relaxed format): parse collapse (parse_success_rate = 0.27)
- 其余 8 个 strict-format prompts: all-false collapse (false_recall 0.97-1.00, true_recall 0.00-0.03)

## 文件清单

| 文件 | 说明 |
|---|---|
| `screening_matrix_v1.md` | Screening evaluation matrix（T10 设计，已冻结） |
| `screening_candidate_registry_v1.md` | 9 条候选 registry（T10 设计，已冻结） |
| `screening_shortlist_rules_v1.md` | Shortlist 决策规则（T10 设计，已冻结） |
| `screening_execution_manifest_v1.md` | T11 执行 manifest：所有 run 的 metrics、artifact 验证、elimination 判定 |

## 已完成

- T10: Build screening evaluation matrix
- T11: Run screening on 9 prompt candidates using smoke split with deepseek-chat

## 待完成

- T12: Write screening summary and shortlist report（需 Captain 先处理 screening failure）

## 设计原则

- 排查 parse collapse、all-true/all-false collapse。
- 形成 3-5 个 prompt 的 shortlist 进入 recomputed benchmark。
- Screening 结果不直接用于论文性能结论，只用于排除和 shortlist 决策。
- 10 个低方差 taxonomy 字段不作为 shortlist 主决策依据。
