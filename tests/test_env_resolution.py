from pathlib import Path

from sair_competition.config.env import load_dotenv, resolve_openai_compatible_settings


def test_load_dotenv_infers_provider_specific_aliases_from_comments(tmp_path: Path) -> None:
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text(
        "\n".join(
            [
                "# Deepseek API 密钥",
                "OPENAI_API_KEY='deepseek-key'",
                "# Minimax API 密钥",
                "MINIMAX_API_KEY='minimax-key'",
                "# Deepseek API 地址",
                "OPENAI_BASE_URL='https://deepseek.example'",
                "# Minimax API 地址",
                "OPENAI_BASE_URL='https://minimax.example'",
            ]
        ),
        encoding="utf-8",
    )

    dotenv = load_dotenv(dotenv_path)

    assert dotenv["DEEPSEEK_API_KEY"] == "deepseek-key"
    assert dotenv["DEEPSEEK_BASE_URL"] == "https://deepseek.example"
    assert dotenv["MINIMAX_API_KEY"] == "minimax-key"
    assert dotenv["MINIMAX_BASE_URL"] == "https://minimax.example"


def test_resolve_openai_compatible_settings_defaults_to_deepseek_reasoner(tmp_path: Path) -> None:
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text(
        "\n".join(
            [
                "# Deepseek API 密钥",
                "OPENAI_API_KEY='deepseek-key'",
                "# Deepseek API 地址",
                "OPENAI_BASE_URL='https://deepseek.example'",
            ]
        ),
        encoding="utf-8",
    )

    settings = resolve_openai_compatible_settings(dotenv_path=dotenv_path, provider_name="deepseek")

    assert settings.api_key == "deepseek-key"
    assert settings.base_url == "https://deepseek.example"
    assert settings.model == "deepseek-reasoner"


def test_resolve_openai_compatible_settings_supports_minimax_provider(tmp_path: Path) -> None:
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text(
        "\n".join(
            [
                "MINIMAX_API_KEY='minimax-key'",
                "MINIMAX_BASE_URL='https://minimax.example'",
            ]
        ),
        encoding="utf-8",
    )

    settings = resolve_openai_compatible_settings(dotenv_path=dotenv_path, provider_name="minimax")

    assert settings.api_key == "minimax-key"
    assert settings.base_url == "https://minimax.example"
    assert settings.model == "MiniMax-M2.7"
