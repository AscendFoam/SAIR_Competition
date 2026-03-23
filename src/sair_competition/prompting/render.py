from __future__ import annotations


def render_complete_prompt_for_problem(
    complete_prompt_text: str,
    equation1: str,
    equation2: str,
) -> str:
    """Inject equations into a prebuilt complete prompt using common placeholder styles."""

    rendered = complete_prompt_text
    replacements = {
        "{{ equation1 }}": equation1,
        "{{equation1}}": equation1,
        "{ equation1 }": equation1,
        "{equation1}": equation1,
        "{{ equation2 }}": equation2,
        "{{equation2}}": equation2,
        "{ equation2 }": equation2,
        "{equation2}": equation2,
    }
    for pattern, value in replacements.items():
        rendered = rendered.replace(pattern, value)
    return rendered
