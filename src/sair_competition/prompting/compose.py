from __future__ import annotations

from pathlib import Path
from typing import Any

def load_text(path: str | Path) -> str:
    """读取文本文件内容。

    Args:
        path: 文件路径。

    Returns:
        文件的 UTF-8 文本内容。
    """
    return Path(path).read_text(encoding="utf-8")


def render_template(template_text: str, variables: dict[str, Any]) -> str:
    """使用变量字典替换模板中的占位符。

    支持 ``{{ key }}`` 和 ``{{key}}`` 两种占位符格式。

    Args:
        template_text: 包含占位符的模板文本。
        variables: 占位符名到替换值的映射。

    Returns:
        替换后的文本。
    """
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
