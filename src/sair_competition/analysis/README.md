# analysis — 错误分析、实验对比与离线规则资产管理

本模块是项目中功能最丰富的分析层，提供错误分类与报告、实验候选对比、家族标签回填，以及完整的离线规则资产生命周期管理（构建 → 审计 → 合并 → 审查集生成）。

## 文件清单

| 文件 | 职责 |
| --- | --- |
| `__init__.py` | 包初始化 |
| `error_taxonomy.py` | 错误分类体系定义（8 个类别） |
| `error_report.py` | 错误分析报告生成 |
| `experiment_report.py` | 实验候选运行对比与排名 |
| `family_slice.py` | 家族标签回填到预测文件 |
| `offline_rule_assets.py` | 离线规则资产构建、附加、审计 |
| `offline_rule_review.py` | 离线规则轴合并与审查集生成 |
| `positive_signal_candidate.py` | 为高价值子型生成“程序化正信号候选”准备报告 |

## 错误分类体系 (`error_taxonomy.py`)

| 错误类别 | 代码 | 说明 |
| --- | --- | --- |
| **FORMAT** | `FORMAT` | 模型输出无法解析为布尔值 |
| **RULE_MISSING** | `RULE_MISSING` | Prompt 缺少处理该案例所需的规则 |
| **RULE_CONFLICT** | `RULE_CONFLICT` | Prompt 规则冲突或过拟合 |
| **PROMPT_AMBIGUOUS** | `PROMPT_AMBIGUOUS` | 指令措辞存在歧义 |
| **FALSE_FILTER_WEAK** | `FALSE_FILTER_WEAK` | 对非蕴含案例过于倾向输出 true |
| **OVERCOMPRESSION** | `OVERCOMPRESSION` | 压缩导致规则文本难以理解 |
| **MODEL_SPECIFIC** | `MODEL_SPECIFIC` | 失败与特定模型家族相关 |
| **HARD_COMPOSITION** | `HARD_COMPOSITION` | 案例需要多条规则组合推理 |

## 核心 API

### `error_report.py` — 错误报告

| 函数签名 | 说明 |
| --- | --- |
| `analyze_prediction_errors(predictions_path, output_dir) -> dict` | 从预测文件构建错误报告，输出 `summary.json` 和 `summary.md` |
| `infer_error_category(row: dict) -> str` | 推断单条预测记录的错误类别；预测正确时返回 `"CORRECT"` |

#### 推断逻辑

```
parsed=False           → FORMAT
prediction == answer   → CORRECT
prediction=True, answer=False:
  eq2 变量数或运算符数显著更大 → FALSE_FILTER_WEAK
  否则                      → RULE_CONFLICT
prediction=False, answer=True:
  两方程 α-等价             → RULE_MISSING
  来源为 hard*              → HARD_COMPOSITION
  否则                      → RULE_MISSING
其他                    → MODEL_SPECIFIC
```

#### 报告输出内容

- 整体指标（accuracy、parse_success_rate）
- 错误分桶统计（按类别计数）
- 按来源分组的错误分布
- 按家族标签和焦点组的子集分析
- 前 25 条错误样例

### `experiment_report.py` — 实验对比

#### `CandidateSnapshot` 数据类

存储单个实验候选的完整快照，包括候选 ID、prompt 路径与大小、模型/供应商、行数、各项准确率、平均延迟、错误分桶等。

| 函数签名 | 说明 |
| --- | --- |
| `compare_candidate_runs(candidate_dirs, output_dir, baseline_dir) -> dict` | 对比多个候选实验运行，按 balanced_accuracy 排名，输出对比报告和与基线的差值 |

#### 排名依据

按 `(balanced_accuracy, accuracy, parse_success_rate)` 降序排列，balanced_accuracy 为 true_accuracy 和 false_accuracy 的均值。

### `family_slice.py` — 标签回填

| 函数签名 | 说明 |
| --- | ---|
| `attach_family_tags_to_predictions(predictions_path, tagged_dataset_path, output_path) -> dict` | 将已标注数据集中的 `family_tags` 和 `family_signals` 回填到预测文件中；优先按 `problem_id` 匹配，回退到按方程对匹配 |

### `offline_rule_assets.py` — 离线规则资产

#### 核心数据类

| 数据类 | 说明 |
| --- | --- |
| `RuleAssetTemplate` | 规则资产模板（不可变）：rule_id、焦点组、主标签、触发标签集、规则文本、规则类型 |
| `OfflineRuleAsset` | 完整规则资产：含模板信息 + 统计指标（支持数、置信度、机会分数、当前主线准确率等） |

#### 预定义模板（`RULE_ASSET_TEMPLATES`）

9 个模板覆盖 3 大焦点组：

| 焦点组 | 规则 ID 前缀 | 数量 |
| --- | --- | --- |
| `singleton_collapse` | `OA_TRUE_SINGLETON_*` | 3 |
| `disjoint_sides` | `OA_TRUE_DISJOINT_*` | 3 |
| `constant_operation_candidate` | `OA_TRUE_CONSTANT_*` | 3 |

#### 函数

| 函数签名 | 说明 |
| --- | --- |
| `build_offline_rule_assets(tagged_dataset_path, output_path, error_summary_path, report_path) -> dict` | 从标注数据集和错误摘要构建离线规则资产包（JSONL），按机会分数排序 |
| `load_offline_rule_assets(path) -> list[dict]` | 从 JSONL 加载规则资产 |
| `attach_offline_rule_assets(input_path, rule_assets_path, output_path) -> dict` | 将匹配的规则资产 ID 附加到数据行 |
| `audit_offline_rule_assets(predictions_path, rule_assets_path, output_dir) -> dict` | 在预测文件上审计每个规则资产的表现，输出优先级排序 |
| `match_offline_rule_assets(row, rule_assets) -> list[dict]` | 返回与行匹配的规则资产列表 |
| `row_matches_offline_rule_asset(row, asset) -> bool` | 判断行是否匹配某个规则资产 |

#### 资产生命周期指标

| 指标 | 计算方式 |
| --- | --- |
| `confidence` | 基于 true/false 计数判定：high / medium / low |
| `status` | `active_offline` / `candidate_offline` / `needs_review` |
| `opportunity_score` | `cleanliness × gap × support_true_count`，其中 cleanliness = true占比，gap = 1 - 当前主线准确率 |

### `offline_rule_review.py` — 轴合并与审查集

| 函数签名 | 说明 |
| --- | --- |
| `consolidate_offline_rule_axes(predictions_path, audit_summary_path, output_dir) -> dict` | 将具有完全相同行覆盖的资产合并为规范轴（canonical axis），构建父子层级关系 |
| `build_offline_rule_review_set(predictions_path, consolidation_summary_path, output_dir) -> dict` | 在规范轴基础上生成去重审查集，每行分配到最具体的轴，输出审查清单和 P0/P1 审查模板 |

#### 轴合并逻辑

1. 按行集合签名（sorted row keys tuple）对审计资产分组
2. 同一组内的资产合并为一个规范轴，首个资产作为主规则
3. 通过集合包含关系构建父子层级（子集 → 子节点）
4. 按优先级排序输出

#### 审查优先级

| 优先级 | 条件 |
| --- | --- |
| P0 | 轴深度 ≥ 2 或行数 ≤ 2（最稀少、最具体） |
| P1 | 轴深度 = 1 |
| P2 | 其他 |

#### 建议动作

| 动作 | 条件 |
| --- | --- |
| `expand_family_tagger` | 轴深度 ≥ 1 |
| `collect_more_examples` | 行数 ≤ 2 |
| `prepare_programmatic_positive_signal` | 其他 |

### `positive_signal_candidate.py` — 正信号候选准备

| 函数签名 | 说明 |
| --- | --- |
| `prepare_positive_signal_candidate(tagged_dataset_path, target_tag, output_dir, boundary_tags, rule_assets_path, signal_keys) -> dict` | 围绕某个高价值 family tag 生成离线准备报告，输出触发条件快照、命中样本清单、边界样本清单，以及与其他正向资产的重叠关系 |

当前这条链路除了直接围绕现有 family tag 准备候选外，也已经用于推进更窄的 shared-LHS residual 子型，例如：

- `TARGET_SHARED_LHS_NO_NEW_VARS_SINGLE_REUSE_MULTI_ANCHOR`
- `TARGET_SHARED_LHS_NO_NEW_VARS_MULTI_REUSE_SINGLE_ANCHOR`

其中第一条子型当前已经进入 offline asset 模板层，作为下一步更程序化正信号准备的正式候选；第二条仍保留为 secondary candidate。

#### 主要输出

- `summary.json`
- `summary.md`

#### 报告内容

- 目标标签在当前切分上的支持数、`true/false` 分布与来源分布
- 与目标标签相关的结构信号快照
- 指定 boundary tags 的样本清单与真假分布
- 与现有 offline rule assets 的重叠情况
- 一个轻量的离线 readiness 建议

## 完整分析流水线

```
原始数据集
    │
    ▼ tag_problem_families (features 模块)
标注数据集 (含 family_tags + family_signals)
    │
    ├──▶ run_baseline_suite / run_complete_prompt_eval (eval 模块)
    │         │
    │         ▼
    │    predictions.jsonl
    │         │
    │         ▼ attach_family_tags_to_predictions
    │    predictions_with_tags.jsonl
    │         │
    │         ▼ analyze_prediction_errors
    │    error_summary (error_buckets, family_tag_summary, ...)
    │
    ├──▶ build_offline_rule_assets (标注数据集 + 错误摘要)
    │         │
    │         ▼
    │    rule_assets.jsonl (9 个预定义模板对应的资产)
    │         │
    │         ▼ attach_offline_rule_assets
    │    predictions_with_assets.jsonl
    │         │
    │         ▼ audit_offline_rule_assets
    │    audit_summary (各资产在预测上的表现)
    │               │
    │               ▼ consolidate_offline_rule_axes
    │          canonical_axes (去重后的规范轴 + 父子层级)
    │               │
    │               ▼ build_offline_rule_review_set
    │          review_set.jsonl + annotation_checklist.md + p0_p1_review_template.md
    │
    └──▶ compare_candidate_runs (多个候选目录)
              │
              ▼
         comparison.json + comparison.md (排名 + 差值 + 推荐)
```

## 依赖关系

- **项目内依赖**: `data.io`、`eval.metrics`、`features.family_tagger`、`parse.equations`、`paths`
- **被依赖方**: `cli.py`（所有分析命令的入口）
- **无第三方依赖**
