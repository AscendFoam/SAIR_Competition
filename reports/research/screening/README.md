# Screening Reports

本目录用于记录 Stage A `screening` 评测设计、结果和 shortlist 决策。

## 当前状态

Matrix defined, execution not started. T10 已完成 screening evaluation matrix 设计，T11 尚未执行 screening。

## 文件清单

| 文件 | 说明 |
|---|---|
| `screening_matrix_v1.md` | Screening evaluation matrix：候选池、split、model config、metrics、gates、field usage rules |
| `screening_candidate_registry_v1.md` | 9 条 text-ready 候选的 registry：分类（core/contrast）、structural coverage、excluded records |
| `screening_shortlist_rules_v1.md` | Shortlist 决策规则：elimination conditions、inclusion conditions、deduplication、coverage test |

## 待完成

- T11: Run screening on 9 prompt candidates using smoke split.
- T12: Write screening summary and shortlist report.

## 设计原则

- 排查 parse collapse、all-true/all-false collapse。
- 形成 3-5 个 prompt 的 shortlist 进入 recomputed benchmark。
- Screening 结果不直接用于论文性能结论，只用于排除和 shortlist 决策。
- 10 个低方差 taxonomy 字段不作为 shortlist 主决策依据。
