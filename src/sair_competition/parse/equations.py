from __future__ import annotations

import re


VARIABLE_PATTERN = re.compile(r"\b[a-z]\b")
TOKEN_PATTERN = re.compile(r"[a-z]|[()*=]")


def extract_variables(equation: str) -> list[str]:
    """Extract variable symbols from a simple equation string."""

    return sorted(set(VARIABLE_PATTERN.findall(equation)))


def count_binary_ops(equation: str, operator: str = "*") -> int:
    """Count occurrences of the magma operator."""

    return equation.count(operator)


def split_equation(equation: str) -> tuple[str, str]:
    """Split an equation into left and right sides."""

    parts = equation.split("=")
    if len(parts) != 2:
        raise ValueError(f"Equation must contain exactly one '=': {equation}")
    return parts[0].strip(), parts[1].strip()


def canonicalize_variables(text: str) -> str:
    """Rename variables by first occurrence so alpha-equivalent equations match."""

    mapping: dict[str, str] = {}
    next_index = 0
    rendered: list[str] = []

    for token in TOKEN_PATTERN.findall(text.replace(" ", "")):
        if len(token) == 1 and token.isalpha():
            if token not in mapping:
                mapping[token] = chr(ord("a") + next_index)
                next_index += 1
            rendered.append(mapping[token])
        else:
            rendered.append(token)
    return "".join(rendered)


def canonicalize_equation(equation: str) -> str:
    """Canonicalize variable naming across a full equation string."""

    return canonicalize_variables(equation)
