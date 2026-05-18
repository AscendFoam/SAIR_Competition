# Research Configs

本目录存放 Stage1 后赛事实证科研用的机器可读配置。

T10 已把 screening evaluation matrix 从 seed template 收敛为正式定义。

## 文件约定

- `corpus_sources.example.json`: prompt corpus 来源登记模板。
- `prompt_feature_taxonomy.yaml`: prompt 结构特征 taxonomy v1（TAX_V1_MANUAL_CODING，T07 建立，T09 审计）。
- `evaluation_matrix.example.json`: 三阶段评测配置——screening / recomputed benchmark / post-release analysis。T10 已冻结 screening phase 配置。

## 使用原则

- Screening phase 配置已由 T10 冻结：9 条 prompt，smoke split，1 个 low-cost model，repeats = 1。T11 执行时 `provider_route` 需填入实际值，但其他字段不得更改。
- Recomputed benchmark phase 的 prompt_set 依赖 screening shortlist 结果（3-5 prompts），T11 完成前不得提前填入。
- Post-release analysis phase 的 prompt_set 依赖 recomputed benchmark 的 frozen shortlist，T14 完成前不得提前填入。
- `repeats` 已统一为整数。Screening = 1；recomputed benchmark 和 post-release analysis 默认 = 1，可扩展至 3 但需要 Captain 审批并在 config 中更新。
- 所有后赛事实验必须显式标注 `post-release analysis`。
- 不把未公开 prompt、API raw outputs、私有数据或敏感配置写入公开复现模板。
- 任何新字段都应与 `docs/02_experiment_plan.md`、`docs/06_eval_protocol.md` 和 `docs/03_architecture.md` 保持一致。

## Screening Matrix 配置要点

| 项 | 值 |
|---|---|
| screening prompt set | 9 条 text-ready local records |
| screening dataset | smoke (64 problems) |
| screening model | 1 个 low-cost model，provider_route = to_fill |
| screening repeats | 1 |
| shortlist target | 3-5 prompts |

详细 matrix 说明：`reports/research/screening/screening_matrix_v1.md`
