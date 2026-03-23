from sair_competition.eval.parser import parse_bool_output


def test_parse_bool_output_accepts_verdict_label() -> None:
    assert parse_bool_output("VERDICT: TRUE") is True


def test_parse_bool_output_uses_last_verdict_label() -> None:
    raw = "VERDICT: TRUE\nREASONING: reconsidering\nVERDICT: FALSE"
    assert parse_bool_output(raw) is False
