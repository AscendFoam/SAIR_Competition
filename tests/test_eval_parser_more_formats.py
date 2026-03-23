from sair_competition.eval.parser import parse_bool_output


def test_parse_bool_output_accepts_bold_verdict_label() -> None:
    assert parse_bool_output("**VERDICT:** FALSE") is False


def test_parse_bool_output_accepts_single_token_line_with_markdown() -> None:
    assert parse_bool_output("`true`") is True
