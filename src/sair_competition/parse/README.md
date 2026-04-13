# parse — 方程解析与结构化分析工具

本模块提供方程字符串的底层解析能力，包括变量提取、运算符计数、方程拆分以及变量规范化（α-等价判定）。这些函数被 `features`、`eval`、`analysis` 等上层模块广泛依赖。

## 文件清单

| 文件 | 职责 |
| --- | --- |
| `__init__.py` | 包初始化，导出方程解析相关接口 |
| `equations.py` | 方程解析的核心实现 |

## 核心 API

### `equations.py`

#### 正则常量

| 常量 | 说明 |
| --- | --- |
| `VARIABLE_PATTERN` | 匹配单个小写字母变量（`\b[a-z]\b`） |
| `TOKEN_PATTERN` | 匹配方程中的 token（变量、括号、运算符、等号） |

#### 函数

| 函数签名 | 说明 |
| --- | --- |
| `extract_variables(equation: str) -> list[str]` | 从方程字符串中提取所有变量符号，去重并排序返回 |
| `count_binary_ops(equation: str, operator: str = "*") -> int` | 统计方程中 magma 运算符（默认 `*`）的出现次数 |
| `split_equation(equation: str) -> tuple[str, str]` | 按等号拆分方程，返回 `(左侧, 右侧)` 元组；等号数量不为 1 时抛出 `ValueError` |
| `canonicalize_variables(text: str) -> str` | 按首次出现顺序将变量重命名为 `a, b, c, ...`，用于 α-等价比较 |
| `canonicalize_equation(equation: str) -> str` | 对完整方程字符串执行变量规范化（内部调用 `canonicalize_variables`） |

## 使用示例

```python
from sair_competition.parse.equations import (
    extract_variables,
    count_binary_ops,
    split_equation,
    canonicalize_equation,
)

# 变量提取
extract_variables("x * y = y * x")  # ['x', 'y']

# 运算符计数
count_binary_ops("(a * b) * c = a * (b * c)")  # 3

# 方程拆分
lhs, rhs = split_equation("x * y = y * x")  # ('x * y', 'y * x')

# α-等价判定
canonicalize_equation("x * y = y * x") == canonicalize_equation("a * b = b * a")  # True
```

## 依赖关系

- **被依赖方**: `features.problem_features`、`features.family_tagger`、`eval.baselines`、`analysis.error_report`
- **无外部依赖**，仅使用标准库 `re`
