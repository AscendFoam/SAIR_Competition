from pathlib import Path
from types import SimpleNamespace
from urllib.error import URLError

from sair_competition.config.env import OpenAICompatibleSettings
from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.eval.local_runner import run_complete_prompt_eval
from sair_competition.eval.openai_compatible import OpenAICompatibleClient


def test_run_complete_prompt_eval_resumes_from_partial_predictions(monkeypatch, tmp_path: Path) -> None:
    dataset_path = tmp_path / "dataset.jsonl"
    output_dir = tmp_path / "run"
    predictions_path = output_dir / "predictions.jsonl"
    prompt_path = tmp_path / "prompt.txt"
    dotenv_path = tmp_path / ".env"

    rows = [
        {
            "problem_id": "p1",
            "source": "normal",
            "split": "dev",
            "equation1": "x = y",
            "equation2": "x = y",
            "answer": True,
        },
        {
            "problem_id": "p2",
            "source": "normal",
            "split": "dev",
            "equation1": "x = y",
            "equation2": "x = z",
            "answer": False,
        },
    ]
    write_jsonl(dataset_path, rows)
    prompt_path.write_text("prompt", encoding="utf-8")
    dotenv_path.write_text("OPENAI_API_KEY='x'\nOPENAI_BASE_URL='https://example.com'\n", encoding="utf-8")

    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(
        predictions_path,
        [
            {
                "problem_id": "p1",
                "source": "normal",
                "split": "dev",
                "equation1": "x = y",
                "equation2": "x = y",
                "answer": True,
                "prediction": True,
                "parsed": True,
                "raw_output": "VERDICT: TRUE",
                "latency_seconds": 0.1,
                "prompt_path": str(prompt_path),
                "model": "demo-model",
                "provider": "demo-provider",
                "family_tags": [],
                "family_signals": {},
            }
        ],
    )

    monkeypatch.setattr("sair_competition.eval.local_runner.load_text", lambda _: "prompt")
    monkeypatch.setattr(
        "sair_competition.eval.local_runner.resolve_openai_compatible_settings",
        lambda dotenv_path, model=None, provider_name="deepseek": OpenAICompatibleSettings(
            provider_name="demo-provider",
            api_key="x",
            base_url="https://example.com",
            model=model or "demo-model",
        ),
    )
    monkeypatch.setattr(
        "sair_competition.eval.local_runner.render_complete_prompt_for_problem",
        lambda complete_prompt_text, equation1, equation2: f"{equation1} -> {equation2}",
    )

    calls: list[str] = []

    def fake_complete(self, prompt: str, temperature: float = 0.0, max_tokens: int = 256):
        calls.append(prompt)
        return SimpleNamespace(raw_output="VERDICT: FALSE", latency_seconds=0.2, response_json={})

    monkeypatch.setattr(OpenAICompatibleClient, "complete", fake_complete)

    summary = run_complete_prompt_eval(
        dataset_path=dataset_path,
        prompt_path=prompt_path,
        output_dir=output_dir,
        dotenv_path=dotenv_path,
        model="demo-model",
    )

    saved = read_jsonl(predictions_path)
    assert len(calls) == 1
    assert calls == ["x = y -> x = z"]
    assert len(saved) == 2
    assert summary["row_count"] == 2
    assert summary["metrics"]["accuracy"] == 1.0


def test_openai_compatible_client_retries_on_urlerror(monkeypatch) -> None:
    settings = OpenAICompatibleSettings(
        provider_name="demo-provider",
        api_key="x",
        base_url="https://example.com",
        model="demo-model",
        timeout_seconds=5.0,
    )
    client = OpenAICompatibleClient(settings)

    attempts = {"count": 0}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return b'{"choices":[{"message":{"content":"VERDICT: TRUE"}}]}'

    def fake_urlopen(request, timeout):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise URLError("temporary failure")
        return FakeResponse()

    monkeypatch.setattr("sair_competition.eval.openai_compatible.urllib.request.urlopen", fake_urlopen)
    monkeypatch.setattr("sair_competition.eval.openai_compatible.time.sleep", lambda _: None)

    result = client.complete(prompt="demo")

    assert attempts["count"] == 3
    assert result.raw_output == "VERDICT: TRUE"
