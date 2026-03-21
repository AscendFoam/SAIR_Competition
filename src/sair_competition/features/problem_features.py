from __future__ import annotations

from sair_competition.parse.equations import count_binary_ops, extract_variables


def build_problem_features(equation1: str, equation2: str) -> dict[str, int]:
    """Create lightweight structural features for error analysis."""

    vars_eq1 = extract_variables(equation1)
    vars_eq2 = extract_variables(equation2)
    return {
        "num_vars_eq1": len(vars_eq1),
        "num_vars_eq2": len(vars_eq2),
        "num_ops_eq1": count_binary_ops(equation1),
        "num_ops_eq2": count_binary_ops(equation2),
    }

