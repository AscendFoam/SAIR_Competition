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
    """基线预测器抽象基类。

    所有基线预测器共享 ``name`` 和 ``description`` 字段，
    子类需实现 :meth:`predict` 方法。

    Attributes:
        name: 预测器唯一标识名。
        description: 预测器策略的一句话描述。
    """

    name: str
    description: str

    def predict(self, row: dict) -> bool:
        """对单条数据行进行预测。

        Args:
            row: 包含 ``equation1``、``equation2`` 等字段的数据行。

        Returns:
            预测结果布尔值（True 表示蕴含）。

        Raises:
            NotImplementedError: 子类必须实现此方法。
        """
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class AlwaysFalsePredictor(BaselinePredictor):
    """始终返回 False 的基线预测器。"""

    def predict(self, row: dict) -> bool:
        """始终返回 False。"""
        return False


@dataclass(frozen=True, slots=True)
class AlwaysTruePredictor(BaselinePredictor):
    """始终返回 True 的基线预测器。"""

    def predict(self, row: dict) -> bool:
        """始终返回 True。"""
        return True


@dataclass(frozen=True, slots=True)
class CanonicalMatchPredictor(BaselinePredictor):
    """α-等价匹配预测器：当两个方程规范化后相同时返回 True。"""

    def predict(self, row: dict) -> bool:
        """比较两个方程的规范化形式是否相同。

        通过 :func:`~sair_competition.parse.equations.canonicalize_equation` 将变量重命名
        后比较字符串是否相等。

        Args:
            row: 包含 ``equation1`` 和 ``equation2`` 字段的数据行。

        Returns:
            两方程 α-等价时返回 ``True``，否则 ``False``。
        """
        return canonicalize_equation(row["equation1"]) == canonicalize_equation(row["equation2"])


@dataclass(frozen=True, slots=True)
class StructuralV1Predictor(BaselinePredictor):
    """轻量级结构启发式预测器。

    使用变量数量、运算符数量、侧形状等多条启发式规则进行预测：
    先排除方程 2 变量数或运算符数明显多于方程 1 的情况，
    再检查共享左侧骨架、共享右侧骨架等模式。
    """

    def predict(self, row: dict) -> bool:
        """基于结构启发式规则预测方程蕴含关系。

        Args:
            row: 包含 ``equation1`` 和 ``equation2`` 字段的数据行。

        Returns:
            预测结果布尔值。
        """
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
    """返回所有预定义的基线预测器列表。

    Returns:
        包含 ``AlwaysFalsePredictor``、``AlwaysTruePredictor``、
        ``CanonicalMatchPredictor`` 和 ``StructuralV1Predictor`` 的列表。
    """
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

