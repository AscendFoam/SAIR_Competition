from sair_competition.eval.baselines import get_baseline_predictors


def test_canonical_match_predictor_flags_identical_equations() -> None:
    predictors = {predictor.name: predictor for predictor in get_baseline_predictors()}
    predictor = predictors["canonical_match"]
    row = {
        "equation1": "x = x * y",
        "equation2": "a = a * b",
    }
    assert predictor.predict(row) is True

