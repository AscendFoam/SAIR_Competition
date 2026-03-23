from sair_competition.analysis.error_report import infer_error_category


def test_infer_error_category_format() -> None:
    row = {"parsed": False}
    assert infer_error_category(row) == "FORMAT"


def test_infer_error_category_false_filter_weak() -> None:
    row = {
        "parsed": True,
        "prediction": True,
        "answer": False,
        "equation1": "x = y",
        "equation2": "x * y = z * w",
        "source": "normal",
    }
    assert infer_error_category(row) == "FALSE_FILTER_WEAK"
