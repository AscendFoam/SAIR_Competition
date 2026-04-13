from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class OpenAICompatibleSettings:
    """OpenAI 兼容 API 的不可变配置对象。

    封装调用聊天补全 API 所需的全部参数，包括供应商名称、
    密钥、基础 URL、模型名称和超时时间。

    Attributes:
        provider_name: 供应商标识（如 ``"deepseek"``）。
        api_key: API 认证密钥。
        base_url: API 基础 URL（不含 ``/chat/completions`` 后缀）。
        model: 模型名称（如 ``"deepseek-chat"``）。
        timeout_seconds: 请求超时时间（秒），默认 120。
    """

    provider_name: str
    api_key: str
    base_url: str
    model: str
    timeout_seconds: float = 120.0


def load_dotenv(path: str | Path) -> dict[str, str]:
    """Load a simple .env file without exposing values."""

    env: dict[str, str] = {}
    file_path = Path(path)
    if not file_path.exists():
        return env

    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        env[key] = value
    return env


def resolve_openai_compatible_settings(
    dotenv_path: str | Path,
    model: str | None = None,
    provider_name: str = "deepseek",
) -> OpenAICompatibleSettings:
    """Resolve API settings from common DeepSeek/OpenAI-compatible environment names."""

    dotenv = load_dotenv(dotenv_path)

    api_key = _first_present(
        dotenv,
        [
            "DEEPSEEK_API_KEY",
            "OPENAI_API_KEY",
            "LLM_API_KEY",
        ],
    )
    base_url = _first_present(
        dotenv,
        [
            "DEEPSEEK_BASE_URL",
            "OPENAI_BASE_URL",
            "LLM_BASE_URL",
        ],
    )
    resolved_model = model or _first_present(
        dotenv,
        [
            "DEEPSEEK_MODEL",
            "OPENAI_MODEL",
            "LLM_MODEL",
        ],
        required=False,
    )

    if not api_key:
        raise ValueError("No API key found in .env. Expected DEEPSEEK_API_KEY, OPENAI_API_KEY, or LLM_API_KEY.")
    if not base_url:
        raise ValueError("No base URL found in .env. Expected DEEPSEEK_BASE_URL, OPENAI_BASE_URL, or LLM_BASE_URL.")
    if not resolved_model:
        raise ValueError("No model found. Pass --model or set DEEPSEEK_MODEL / OPENAI_MODEL / LLM_MODEL in .env.")

    return OpenAICompatibleSettings(
        provider_name=provider_name,
        api_key=api_key,
        base_url=base_url.rstrip("/"),
        model=resolved_model,
    )


def _first_present(dotenv: dict[str, str], keys: list[str], required: bool = True) -> str | None:
    """从环境变量字典中按优先级查找第一个非空值。

    Args:
        dotenv: 环境变量字典。
        keys: 按优先级排列的变量名列表。
        required: 是否为必选项（当前实现中不影响行为）。

    Returns:
        第一个找到的非空值，若均不存在则返回 ``None``。
    """
    for key in keys:
        value = dotenv.get(key)
        if value:
            return value
    if required:
        return None
    return None
