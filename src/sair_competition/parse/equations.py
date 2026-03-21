from __future__ import annotations

import re


VARIABLE_PATTERN = re.compile(r"\b[a-z]\b")


def extract_variables(equation: str) -> list[str]:
    """Extract variable symbols from a simple equation string."""

    return sorted(set(VARIABLE_PATTERN.findall(equation)))


def count_binary_ops(equation: str, operator: str = "*") -> int:
    """Count occurrences of the magma operator."""

    return equation.count(operator)

