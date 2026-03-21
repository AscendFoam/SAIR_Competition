from pathlib import Path

from sair_competition.prompting.compose import build_complete_prompt


def test_build_complete_prompt_renders_template(tmp_path: Path) -> None:
    template_path = tmp_path / "template.j2"
    cheatsheet_path = tmp_path / "cheatsheet.txt"
    template_path.write_text("Cheatsheet: {{ cheatsheet }} | {{ equation1 }} | {{ equation2 }}", encoding="utf-8")
    cheatsheet_path.write_text("Only output true or false.", encoding="utf-8")

    rendered = build_complete_prompt(
        template_path=template_path,
        cheatsheet_path=cheatsheet_path,
        variables={"equation1": "x=x*y", "equation2": "x=x*x"},
    )

    assert "Only output true or false." in rendered
    assert "x=x*y" in rendered
    assert "x=x*x" in rendered

