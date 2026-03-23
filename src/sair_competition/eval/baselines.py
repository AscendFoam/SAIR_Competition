from __future__ import annotations

from dataclasses import dataclass

from sair_competition.parse.equations import (
    canonicalize_equation,
    canonicalize_variables,
    count_binary_ops,
    extract_variables,
    split_equation,
)


@dataclass(frozen=True, slots=True)
class BaselinePredictor:
    name: str
    description: str

    def predict(self, row: dict) -> bool:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class AlwaysFalsePredictor(BaselinePredictor):
    def predict(self, row: dict) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class AlwaysTruePredictor(BaselinePredictor):
    def predict(self, row: dict) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class CanonicalMatchPredictor(BaselinePredictor):
    def predict(self, row: dict) -> bool:
        return canonicalize_equation(row["equation1"]) == canonicalize_equation(row["equation2"])


@dataclass(frozen=True, slots=True)
class StructuralV1Predictor(BaselinePredictor):
    def predict(self, row: dict) -> bool:
        equation1 = row["equation1"]
        equation2 = row["equation2"]

        if canonicalize_equation(equation1) == canonicalize_equation(equation2):
            return True

        eq1_vars = extract_variables(equation1)
        eq2_vars = extract_variables(equation2)
        eq1_ops = count_binary_ops(equation1)
        eq2_ops = count_binary_ops(equation2)

        lhs1, rhs1 = split_equation(equation1)
        lhs2, rhs2 = split_equation(equation2)

        if len(eq2_vars) > len(eq1_vars):
            return False
        if eq2_ops > eq1_ops + 1:
            return False
        if canonicalize_variables(lhs1) == canonicalize_variables(lhs2) and eq2_ops <= eq1_ops:
            return True
        if canonicalize_variables(rhs1) == canonicalize_variables(rhs2):
            return True
        if len(rhs2.replace(" ", "")) > len(rhs1.replace(" ", "")) + 4 and eq2_ops >= eq1_ops:
            return False
        return False


def get_baseline_predictors() -> list[BaselinePredictor]:
    return [
        AlwaysFalsePredictor(
            name="always_false",
            description="Return false for every problem.",
        ),
        AlwaysTruePredictor(
            name="always_true",
            description="Return true for every problem.",
        ),
        CanonicalMatchPredictor(
            name="canonical_match",
            description="Return true only when the two equations are alpha-equivalent.",
        ),
        StructuralV1Predictor(
            name="structural_v1",
            description="A lightweight structural heuristic using variable, operator, and side-shape checks.",
        ),
    ]

