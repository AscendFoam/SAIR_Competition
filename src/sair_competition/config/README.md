# config — 环境变量与 API 配置管理

本模块负责从 `.env` 文件加载 API 密钥、端点地址和模型名称等配置，为评估模块（`eval.local_runner`、`eval.openai_compatible`）提供统一的 API 设置对象。

## 文件清单

| 文件 | 职责 |
| --- | --- |
| `__init__.py` | 包初始化 |
| `env.py` | 环境变量加载与 API 配置解析 |

## 核心 API

### `env.py`

#### `OpenAICompatibleSettings` 数据类

不可变配置对象，封装 OpenAI 兼容 API 所需的全部参数。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `provider_name` | `str` | — | 供应商标识（如 `"deepseek"`） |
| `api_key` | `str` | — | API 密钥 |
| `base_url` | `str` | — | API 基础 URL（末尾斜杠会被自动移除） |
| `model` | `str` | — | 模型名称 |
| `timeout_seconds` | `float` | `120.0` | 请求超时时间（秒） |

#### 函数

| 函数签名 | 说明 |
| --- | --- |
| `load_dotenv(path: str \| Path) -> dict[str, str]` | 解析 `.env` 文件为字典，跳过注释行和空行，自动去除引号 |
| `resolve_openai_compatible_settings(dotenv_path, model, provider_name) -> OpenAICompatibleSettings` | 从 `.env` 文件解析 API 配置，按优先级查找多个环境变量名 |

#### 环境变量查找优先级

| 配置项 | 查找顺序 |
| --- | --- |
| API 密钥 | `DEEPSEEK_API_KEY` → `OPENAI_API_KEY` → `LLM_API_KEY` |
| 基础 URL | `DEEPSEEK_BASE_URL` → `OPENAI_BASE_URL` → `LLM_BASE_URL` |
| 模型名称 | `--model` 参数 → `DEEPSEEK_MODEL` → `OPENAI_MODEL` → `LLM_MODEL` |

## `.env` 文件示例

```env
# DeepSeek 配置
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

# 或使用通用变量名
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.example.com/v1
LLM_MODEL=gpt-4o
```

## 依赖关系

- **被依赖方**: `eval.openai_compatible`、`eval.local_runner`
- **无项目内依赖**，仅使用标准库 `dataclasses`、`pathlib`
