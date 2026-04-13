# data — 数据模型定义与文件 I/O

本模块定义了竞赛数据的核心数据模式（`PublicProblem`、`EvalRecord`），提供 JSONL 文件读写工具，并实现公开数据集的标准化准备和确定性数据拆分。

## 文件清单

| 文件 | 职责 |
| --- | --- |
| `__init__.py` | 包初始化 |
| `io.py` | JSONL 文件读写工具函数 |
| `schemas.py` | 核心数据模式定义（dataclass） |
| `public_data.py` | 公开数据集标准化与元数据提取 |
| `splits.py` | 确定性分层抽样拆分 |

## 核心 API

### `io.py` — JSONL 读写

| 函数签名 | 说明 |
| --- | --- |
| `read_jsonl(path: str \| Path) -> list[dict]` | 读取 JSONL 文件，返回字典列表；自动跳过空行 |
| `write_jsonl(path: str \| Path, rows: Iterable[dict \| object]) -> None` | 将字典或 dataclass 实例逐行写入 JSONL；自动创建父目录 |
| `load_models(path: str \| Path, model_cls: type[T]) -> list[T]` | 读取 JSONL 并通过关键字参数构造指定类的实例 |

### `schemas.py` — 数据模式

#### `PublicProblem` — 公开竞赛问题

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `equation1` | `str` | — | 前提方程 |
| `equation2` | `str` | — | 目标方程 |
| `problem_id` | `str \| None` | `None` | 问题唯一标识 |
| `answer` | `bool \| None` | `None` | 真实标签（方程 1 是否蕴含方程 2） |
| `source` | `str \| None` | `None` | 数据来源（`normal` / `hard1` / `hard2`） |
| `split` | `str \| None` | `None` | 所属拆分（`smoke` / `dev` / `holdout` / `audit`） |
| `metadata` | `dict[str, Any]` | `{}` | 扩展元数据 |

#### `EvalRecord` — 单条评估结果

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `answer` | `bool` | — | 真实标签 |
| `problem_id` | `str \| None` | `None` | 问题唯一标识 |
| `prediction` | `bool \| None` | `None` | 模型预测结果 |
| `parsed` | `bool` | `True` | 模型输出是否成功解析为布尔值 |
| `source` | `str \| None` | `None` | 数据来源 |
| `raw_output` | `str \| None` | `None` | 模型原始输出文本 |
| `latency_ms` | `int \| None` | `None` | 推理延迟（毫秒） |
| `metadata` | `dict[str, Any]` | `{}` | 扩展元数据 |

### `public_data.py` — 数据集准备

| 函数签名 | 说明 |
| --- | --- |
| `prepare_public_dataset(raw_dir, interim_dir) -> dict` | 读取 `data/raw/` 下的官方数据文件，标准化后写入 `data/interim/public_all.jsonl`，同时生成辅助注册表和统计摘要 |
| `build_split_manifest(split_rows: dict[str, list[dict]]) -> dict` | 为各拆分生成按来源/标签分组的统计清单 |

#### 处理的官方文件

| 文件名 | 来源标记 |
| --- | --- |
| `normal.jsonl` | `normal` |
| `hard1.jsonl` | `hard1` |
| `hard2.jsonl` | `hard2` |

#### 输出文件

| 输出路径 | 内容 |
| --- | --- |
| `interim/public_all.jsonl` | 标准化后的全部问题 |
| `interim/benchmarks_registry.jsonl` | benchmarks 注册表 |
| `interim/prompt_templates_registry.jsonl` | 提示词模板注册表 |
| `interim/leaderboard_snapshot.jsonl` | 排行榜快照 |
| `interim/model_registry.jsonl` | 模型注册表 |
| `interim/public_dataset_summary.json` | 数据集统计摘要 |

### `splits.py` — 数据拆分

| 函数签名 | 说明 |
| --- | --- |
| `make_frozen_splits(dataset_path, output_dir, split_targets, seed) -> dict` | 创建确定性的分层拆分，按 `(source, answer)` 分组后按比例分配，保证可复现 |

#### 拆分策略

1. 按 `(source, answer)` 二元组分组
2. 每组内按 `problem_id` 排序后使用固定种子随机打乱
3. 按比例将每组行数分配到各拆分（最大余额法）
4. 各拆分内按 `(source, index, problem_id)` 排序
5. 输出 `manifest.json` 记录完整的拆分元信息

## 依赖关系

- **项目内依赖**: `features.problem_features`（用于数据标准化时提取结构特征）、`data.io`
- **被依赖方**: 几乎所有上层模块均依赖 `data.io` 的读写函数
