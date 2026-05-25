# Screening Reports

本目录用于记录 Stage A `screening` 评测设计、执行结果和 shortlist 决策。

## 当前状态

三轮 screening 执行已完成，跨越三个 provider：

| Run | Provider | Model | Survivors | 结论 |
|---|---|---|---|---|
| T11 | DeepSeek | deepseek-chat | 0 | all-false collapse |
| T12 | DeepSeek | deepseek-v4-flash | 0 | 确认 collapse 不依赖模型架构 |
| **T12b** | **ZhipuAI** | **glm-4.7-flash** | **8** | **collapse 是 DeepSeek 特有** |

**关键发现：all-false collapse 和 parse collapse 是 DeepSeek-specific 的 provider 级别行为模式，不是 screening protocol 的设计缺陷。** 在 ZhipuAI glm-4.7-flash 上，9 个候选中有 8 个通过 elimination gates。

- P0 (relaxed format): DeepSeek 上 parse collapse（0.23-0.27），ZhipuAI 上 100% parse
- 其余 8 个 strict-format prompts: DeepSeek 上 all-false collapse（true_recall 0.00-0.03），ZhipuAI 上正常分布（true_recall 0.55-0.84）
- 仅 P1.1.1（minimal first draft）在两个 provider 上均被 E3 淘汰
- Shortlist formation 现已在 ZhipuAI 结果上可行

## 文件清单

| 文件 | 说明 |
|---|---|
| `screening_matrix_v1.md` | Screening evaluation matrix（T10 设计，已冻结） |
| `screening_candidate_registry_v1.md` | 9 条候选 registry（T10 设计，已冻结） |
| `screening_shortlist_rules_v1.md` | Shortlist 决策规则（T10 设计，已冻结） |
| `screening_execution_manifest_v1.md` | T11 执行 manifest（deepseek-chat） |
| `screening_second_model_manifest_v1.md` | T12 执行 manifest（deepseek-v4-flash） |
| `screening_model_comparison_note_v1.md` | T11 vs T12 模型对比笔记 |
| `screening_provider_route_availability_v1.md` | T12b provider 路由可用性评估 |
| `screening_third_route_manifest_v1.md` | T12b 执行 manifest（glm-4.7-flash） |
| `screening_cross_provider_note_v1.md` | T12b cross-provider 对比笔记 |

## 已完成

- T10: Build screening evaluation matrix
- T11: Run screening on 9 prompt candidates using smoke split with deepseek-chat
- T12: Rerun screening with alternate model (deepseek-v4-flash), write comparison note
- T12b: Run screening on non-DeepSeek provider (ZhipuAI glm-4.7-flash), 8/9 survivors

## 待完成

- Shortlist formation（基于 ZhipuAI 结果，8 survivors 可用）
- 如需更稳定 shortlist，可考虑在 ZhipuAI 上重复运行

## 设计原则

- 排查 parse collapse、all-true/all-false collapse。
- 形成 3-5 个 prompt 的 shortlist 进入 recomputed benchmark。
- Screening 结果不直接用于论文性能结论，只用于排除和 shortlist 决策。
- 10 个低方差 taxonomy 字段不作为 shortlist 主决策依据。
