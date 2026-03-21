from __future__ import annotations

from pathlib import Path
from typing import Any

def load_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def render_template(template_text: str, variables: dict[str, Any]) -> str:
    rendered = template_text
    for key, value in variables.items():
        rendered = rendered.replace(f"{{{{ {key} }}}}", str(value))
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered


def build_complete_prompt(
    template_path: str | Path,
    cheatsheet_path: str | Path,
    variables: dict[str, Any] | None = None,
) -> str:
    """Render a complete prompt from a template and cheatsheet text."""

    resolved_variables = dict(variables or {})
    resolved_variables["cheatsheet"] = load_text(cheatsheet_path).strip()
    template_text = load_text(template_path)
    rendered = render_template(template_text, resolved_variables).strip()
    return f"{rendered}\n"
