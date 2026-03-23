from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class OpenAICompatibleSettings:
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
    for key in keys:
        value = dotenv.get(key)
        if value:
            return value
    if required:
        return None
    return None
