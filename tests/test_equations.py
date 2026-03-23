from sair_competition.parse.equations import canonicalize_equation, split_equation


def test_canonicalize_equation_handles_alpha_equivalence() -> None:
    assert canonicalize_equation("x = x * y") == canonicalize_equation("a = a * b")


def test_split_equation_returns_both_sides() -> None:
    left, right = split_equation("x = (y * z)")
    assert left == "x"
    assert right == "(y * z)"

