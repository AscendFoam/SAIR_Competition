# eval — 模型评估基础设施

本模块提供完整的评估管线：指标计算、基线预测器、模型输出解析、基线评估运行器、API 评估运行器，以及轻量级 OpenAI 兼容 HTTP 客户端。

## 文件清单

| 文件 | 职责 |
| --- | --- |
| `__init__.py` | 包初始化 |
| `metrics.py` | 评估指标计算（准确率、解析成功率、按来源分组等） |
| `baselines.py` | 4 种基线预测器定义 |
| `parser.py` | 模型输出文本 → 布尔值解析 |
| `baseline_runner.py` | 基线预测器批量评估运行器 |
| `local_runner.py` | 基于 OpenAI 兼容 API 的完整 prompt 评估运行器 |
| `openai_compatible.py` | 最小化 OpenAI 兼容 API 客户端 |

## 核心 API

### `metrics.py` — 指标计算

#### `EvalMetrics` 数据类

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `total` | `int` | 总样本数 |
| `parsed` | `int` | 成功解析的样本数 |
| `parse_success_rate` | `float` | 解析成功率 |
| `correct` | `int` | 预测正确的样本数 |
| `accuracy` | `float` | 总体准确率 |
| `true_total` | `int` | 真实标签为 True 的样本数 |
| `true_correct` | `int` | True 样本预测正确数 |
| `false_total` | `int` | 真实标签为 False 的样本数 |
| `false_correct` | `int` | False 样本预测正确数 |
| `true_accuracy` | `float \| None` | True 类准确率 |
| `false_accuracy` | `float \| None` | False 类准确率 |
| `by_source` | `dict[str, float]` | 按数据来源分组的准确率 |

提供 `to_dict()` 和 `to_json(indent)` 方法用于序列化。

| 函数签名 | 说明 |
| --- | --- |
| `compute_metrics(records: Iterable[dict]) -> EvalMetrics` | 从评估记录列表计算全部指标 |

### `baselines.py` — 基线预测器

| 预测器 | 名称 | 策略 |
| --- | --- | --- |
| `AlwaysFalsePredictor` | `always_false` | 始终返回 False |
| `AlwaysTruePredictor` | `always_true` | 始终返回 True |
| `CanonicalMatchPredictor` | `canonical_match` | 仅当两方程 α-等价时返回 True |
| `StructuralV1Predictor` | `structural_v1` | 基于变量数、运算符数、侧形状的启发式预测器 |

| 函数签名 | 说明 |
| --- | --- |
| `get_baseline_predictors() -> list[BaselinePredictor]` | 返回全部 4 种预测器实例 |

### `parser.py` — 输出解析

`parse_bool_output` 采用多策略依次尝试解析模型输出：

1. **VERDICT 模式**: 匹配 `VERDICT: TRUE/FALSE` 格式（支持 Markdown 装饰符号）
2. **行级匹配**: 查找仅包含 `true` 或 `false` 的独立行
3. **单 token 模式**: 整个输出中仅有一个 `true` 或 `false` 单词

| 函数签名 | 说明 |
| --- | --- |
| `parse_bool_output(raw_output: str) -> bool \| None` | 解析模型原始输出；无法解析时返回 `None` |

### `baseline_runner.py` — 基线评估

| 函数签名 | 说明 |
| --- | --- |
| `run_baseline_suite(dataset_path, output_dir, predictor_names, prompt_path) -> dict` | 对数据集运行指定或全部基线预测器，输出各预测器的预测结果和指标摘要 |

### `local_runner.py` — API 评估

| 函数签名 | 说明 |
| --- | --- |
| `run_complete_prompt_eval(dataset_path, prompt_path, output_dir, dotenv_path, model, limit, temperature, max_tokens) -> dict` | 使用 OpenAI 兼容 API 对数据集运行完整 prompt 评估，逐条发送请求并记录延迟和原始输出 |

### `openai_compatible.py` — API 客户端

#### `CompletionResult` 数据类

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `raw_output` | `str` | 模型输出文本 |
| `latency_seconds` | `float` | 请求耗时（秒） |
| `response_json` | `dict` | 完整 API 响应 JSON |

#### `OpenAICompatibleClient` 类

基于 `urllib.request` 的最小化 HTTP 客户端，无第三方依赖。

| 方法 | 说明 |
| --- | --- |
| `complete(prompt, temperature, max_tokens) -> CompletionResult` | 发送 chat completion 请求并返回结果 |

URL 解析规则：
- 末尾为 `/chat/completions` → 直接使用
- 末尾为 `/v1` → 追加 `/chat/completions`
- 其他 → 追加 `/v1/chat/completions`

## 数据流

```
                    ┌─────────────────────┐
                    │   数据集 (JSONL)     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                 ▼
    ┌─────────────────┐ ┌──────────────┐ ┌──────────────────┐
    │ baseline_runner  │ │ local_runner │ │  (其他预测器)     │
    │ 基线预测器评估    │ │ API 评估     │ │                  │
    └────────┬────────┘ └──────┬───────┘ └────────┬─────────┘
             │                 │                   │
             ▼                 ▼                   ▼
    ┌──────────────────────────────────────────────────────┐
    │              predictions.jsonl + summary.json         │
    └──────────────────────────┬───────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  analysis 模块    │
                    │  错误分析 & 报告   │
                    └──────────────────┘
```

## 依赖关系

- **项目内依赖**: `config.env`、`data.io`、`parse.equations`、`prompting.compose`、`prompting.render`
- **被依赖方**: `analysis.error_report`、`analysis.offline_rule_assets`、`cli.py`
- **无第三方依赖**（HTTP 客户端使用标准库 `urllib`）
