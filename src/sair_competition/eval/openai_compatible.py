from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

from sair_competition.config.env import OpenAICompatibleSettings


@dataclass(slots=True)
class CompletionResult:
    raw_output: str
    latency_seconds: float
    response_json: dict


class OpenAICompatibleClient:
    """Minimal OpenAI-compatible chat completions client."""

    def __init__(self, settings: OpenAICompatibleSettings) -> None:
        self.settings = settings

    def complete(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ) -> CompletionResult:
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
    if base_url.endswith("/chat/completions"):
        return base_url
    if base_url.endswith("/v1"):
        return f"{base_url}/chat/completions"
    return f"{base_url}/v1/chat/completions"


def _extract_message_text(response_json: dict) -> str:
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
