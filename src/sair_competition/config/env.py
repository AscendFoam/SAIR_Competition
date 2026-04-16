from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_PROVIDER_MODELS = {
    "deepseek": "deepseek-reasoner",
    "minimax": "MiniMax-M2.7",
}

PROVIDER_ENV_PRIORITY = {
    "deepseek": {
        "api_key": ["DEEPSEEK_API_KEY", "OPENAI_API_KEY", "LLM_API_KEY"],
        "base_url": ["DEEPSEEK_BASE_URL", "OPENAI_BASE_URL", "LLM_BASE_URL"],
        "model": ["DEEPSEEK_MODEL", "OPENAI_MODEL", "LLM_MODEL"],
    },
    "minimax": {
        "api_key": ["MINIMAX_API_KEY", "OPENAI_API_KEY", "LLM_API_KEY"],
        "base_url": ["MINIMAX_BASE_URL", "OPENAI_BASE_URL", "LLM_BASE_URL"],
        "model": ["MINIMAX_MODEL", "OPENAI_MODEL", "LLM_MODEL"],
    },
}


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

    comment_context = ""
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            comment_context = ""
            continue
        if line.startswith("#"):
            comment_context = line[1:].strip().lower()
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        env[key] = value
        provider_alias = _provider_alias_from_comment(comment_context, key)
        if provider_alias and provider_alias not in env:
            env[provider_alias] = value
        comment_context = ""
    return env


def resolve_openai_compatible_settings(
    dotenv_path: str | Path,
    model: str | None = None,
    provider_name: str = "deepseek",
) -> OpenAICompatibleSettings:
    """Resolve API settings from common DeepSeek/OpenAI-compatible environment names."""

    dotenv = load_dotenv(dotenv_path)
    provider_name = provider_name.strip().lower()
    key_priority = PROVIDER_ENV_PRIORITY.get(provider_name) or {
        "api_key": ["OPENAI_API_KEY", "LLM_API_KEY"],
        "base_url": ["OPENAI_BASE_URL", "LLM_BASE_URL"],
        "model": ["OPENAI_MODEL", "LLM_MODEL"],
    }

    api_key = _first_present(
        dotenv,
        key_priority["api_key"],
    )
    base_url = _first_present(
        dotenv,
        key_priority["base_url"],
    )
    resolved_model = model or _first_present(
        dotenv,
        key_priority["model"],
        required=False,
    ) or DEFAULT_PROVIDER_MODELS.get(provider_name)

    if not api_key:
        raise ValueError(f"No API key found in .env for provider={provider_name}.")
    if not base_url:
        raise ValueError(f"No base URL found in .env for provider={provider_name}.")
    if not resolved_model:
        raise ValueError(f"No model found for provider={provider_name}.")

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


def _provider_alias_from_comment(comment_context: str, key: str) -> str | None:
    """Infer provider-specific aliases from nearby comment text in .env."""

    provider = None
    lowered = (comment_context or "").lower()
    if "deepseek" in lowered:
        provider = "deepseek"
    elif "minimax" in lowered:
        provider = "minimax"
    if not provider:
        return None

    if key == "OPENAI_API_KEY":
        return f"{provider.upper()}_API_KEY"
    if key == "OPENAI_BASE_URL":
        return f"{provider.upper()}_BASE_URL"
    if key == "OPENAI_MODEL":
        return f"{provider.upper()}_MODEL"
    return None
