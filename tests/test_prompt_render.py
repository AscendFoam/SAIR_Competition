from sair_competition.prompting.render import render_complete_prompt_for_problem


def test_render_complete_prompt_for_problem_supports_common_placeholders() -> None:
    template = "A={ equation1 }\nB={{ equation2 }}"
    rendered = render_complete_prompt_for_problem(template, "x = x * y", "x = x * x")
    assert "x = x * y" in rendered
    assert "x = x * x" in rendered

