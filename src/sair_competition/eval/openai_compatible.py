from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

from sair_competition.config.env import OpenAICompatibleSettings


@dataclass(slots=True)
class CompletionResult:
    """API 聊天补全请求的结果。

    Attributes:
        raw_output: 模型输出的文本内容。
        latency_seconds: 请求耗时（秒）。
        response_json: 完整的 API 响应 JSON。
    """

    raw_output: str
    latency_seconds: float
    response_json: dict


class OpenAICompatibleClient:
    """Minimal OpenAI-compatible chat completions client."""

    def __init__(self, settings: OpenAICompatibleSettings) -> None:
        """初始化客户端。

        Args:
            settings: OpenAI 兼容 API 配置对象。
        """
        self.settings = settings

    def complete(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ) -> CompletionResult:
        """发送聊天补全请求并返回结果。

        使用 ``urllib.request`` 发送 POST 请求到 OpenAI 兼容的
        ``/v1/chat/completions`` 端点。

        Args:
            prompt: 用户提示词文本。
            temperature: 采样温度，默认 0.0（确定性输出）。
            max_tokens: 最大生成 token 数，默认 512。

        Returns:
            包含输出文本、延迟和完整响应的 :class:`CompletionResult`。

        Raises:
            RuntimeError: HTTP 错误、网络错误或响应解析失败时抛出。
        """
        endpoint = _resolve_chat_completions_url(self.settings.base_url)
        payload = {
            "model": self.settings.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=self.settings.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP error from completion endpoint: {exc.code} {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Network error while calling completion endpoint: {exc}") from exc

        latency = time.perf_counter() - started
        response_json = json.loads(body)
        raw_output = _extract_message_text(response_json)
        return CompletionResult(raw_output=raw_output, latency_seconds=latency, response_json=response_json)


def _resolve_chat_completions_url(base_url: str) -> str:
    """根据基础 URL 推断完整的聊天补全端点地址。

    - 以 ``/chat/completions`` 结尾 → 直接使用
    - 以 ``/v1`` 结尾 → 追加 ``/chat/completions``
    - 其他 → 追加 ``/v1/chat/completions``

    Args:
        base_url: API 基础 URL。

    Returns:
        完整的聊天补全端点 URL。
    """
    if base_url.endswith("/chat/completions"):
        return base_url
    if base_url.endswith("/v1"):
        return f"{base_url}/chat/completions"
    return f"{base_url}/v1/chat/completions"


def _extract_message_text(response_json: dict) -> str:
    """从 API 响应 JSON 中提取助手的文本消息。

    支持字符串格式和 OpenAI 多部分内容格式的响应。

    Args:
        response_json: 完整的 API 响应 JSON。

    Returns:
        提取的文本内容。

    Raises:
        RuntimeError: 响应中无 ``choices`` 或 ``content`` 字段时抛出。
    """
    choices = response_json.get("choices") or []
    if not choices:
        raise RuntimeError("Completion response did not include choices.")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
        return "\n".join(parts).strip()
    raise RuntimeError("Completion response did not include a usable message content field.")
