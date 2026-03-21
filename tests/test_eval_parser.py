from sair_competition.eval.parser import parse_bool_output


def test_parse_bool_output_accepts_clean_true() -> None:
    assert parse_bool_output("true") is True


def test_parse_bool_output_accepts_clean_false() -> None:
    assert parse_bool_output("FALSE") is False


def test_parse_bool_output_rejects_explanations() -> None:
    assert parse_bool_output("true because equation1 is stronger") is None

