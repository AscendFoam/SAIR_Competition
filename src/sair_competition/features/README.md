# features — 问题结构特征提取与家族标签系统

本模块为方程对提取结构化特征并进行家族分类标注。家族标签系统是本项目错误分析和离线规则资产管理的基础设施，通过结构化的标签体系将方程对划分为不同的模式家族。

## 文件清单

| 文件 | 职责 |
| --- | --- |
| `__init__.py` | 包初始化，导出 `FAMILY_TAG_TAXONOMY`、`FAMILY_FOCUS_GROUPS`、`build_family_annotation`、`tag_problem_families` |
| `problem_features.py` | 轻量级结构特征提取（变量数、运算符数） |
| `family_tagger.py` | 完整的家族标签标注系统（45 个标签、3 大焦点组） |

## 核心 API

### `problem_features.py` — 轻量级特征

| 函数签名 | 说明 |
| --- | --- |
| `build_problem_features(equation1: str, equation2: str) -> dict[str, int]` | 返回包含 `num_vars_eq1`、`num_vars_eq2`、`num_ops_eq1`、`num_ops_eq2` 四个字段的字典 |

### `family_tagger.py` — 家族标签系统

#### 核心常量

**`FAMILY_TAG_TAXONOMY`** — 45 个家族标签定义

标签分为以下几大类：

| 前缀 | 含义 | 标签数 |
| --- | --- | --- |
| `EQ1_SINGLETON_COLLAPSE_*` | 方程 1 某一侧为孤立变量且不出现在另一侧 | 7 |
| `EQ1_DISJOINT_SIDES_*` | 方程 1 两侧变量集不相交 | 5 |
| `EQ1_CONSTANT_OPERATION_*` | 方程 1 为常量运算候选（不相交 + 至少一侧为二元项） | 5 |
| `TARGET_*` | 目标方程特征（重言式、α-等价、共享结构） | 5 |
| `SHARED_*` | 方程对共享左/右侧结构 | 2 |
| `EQ2_INTRODUCES_NEW_VARS` | 方程 2 引入了新变量 | 1 |
| `TARGET_SHARED_LHS_AND_NEW_VARS` | 共享左侧 + 新变量 + 右侧重用左侧变量 | 1 |
| `TARGET_LHS_AMPLIFICATION` | 方程 2 在右侧放大了方程 1 的左侧孤立变量 | 1 |

**`FAMILY_FOCUS_GROUPS`** — 三大焦点组

| 焦点组 | 说明 | 包含标签 |
| --- | --- | --- |
| `singleton_collapse` | 孤立变量坍缩族 | 7 个标签 |
| `disjoint_sides` | 两侧变量分离族 | 5 个标签 |
| `constant_operation_candidate` | 常量运算候选族 | 5 个标签 |

#### 核心函数

| 函数签名 | 说明 |
| --- | --- |
| `build_family_annotation(equation1: str, equation2: str) -> dict` | 为单对方程计算家族标签和结构信号，返回 `{"family_tags": [...], "family_signals": {...}}` |
| `tag_problem_families(dataset_path, output_path, summary_dir) -> dict` | 批量标注数据集并生成摘要报告（JSON + Markdown） |

#### `build_family_annotation` 输出结构

```python
{
    "family_tags": ["EQ1_SINGLETON_COLLAPSE_LHS", "TARGET_TAUTOLOGY", ...],
    "family_signals": {
        "eq1_var_count": 3,
        "eq2_var_count": 2,
        "eq1_op_count": 2,
        "eq2_op_count": 1,
        "eq1_lhs_kind": "var",        # "var" | "binary" | "unknown"
        "eq1_rhs_kind": "binary",
        "eq2_lhs_kind": "binary",
        "eq2_rhs_kind": "var",
        "eq1_side_vars_disjoint": True,
        "target_tautology": False,
        "target_alpha_eq_eq1": False,
        "shared_lhs_alpha": False,
        "shared_rhs_alpha": False,
        "eq2_introduces_new_vars": False,
        # ... 更多信号字段
    }
}
```

#### 标注流程

```
方程对 (equation1, equation2)
    ↓  split_equation
左/右侧分离
    ↓  extract_variables + count_binary_ops
变量集与运算符计数
    ↓  _classify_side
侧类型判定 (var / binary / unknown)
    ↓  结构信号计算
信号字典 (family_signals)
    ↓  规则匹配
家族标签集合 (family_tags)
    ↓  按 FAMILY_TAG_TAXONOMY 排序
有序标签列表
```

## 依赖关系

- **项目内依赖**: `parse.equations`（变量提取、运算符计数、方程拆分、规范化）、`data.io`
- **被依赖方**: `analysis.error_report`、`analysis.family_slice`、`analysis.offline_rule_assets`、`data.public_data`
