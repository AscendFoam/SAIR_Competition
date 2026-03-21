from __future__ import annotations

import re


TRUE_TOKENS = {"true"}
FALSE_TOKENS = {"false"}
TOKEN_PATTERN = re.compile(r"[A-Za-z]+")


def parse_bool_output(raw_output: str) -> bool | None:
    """Parse a raw model output into a boolean if it cleanly maps to true/false."""

    tokens = TOKEN_PATTERN.findall(raw_output.strip().lower())
    if len(tokens) != 1:
        return None
    token = tokens[0]
    if token in TRUE_TOKENS:
        return True
    if token in FALSE_TOKENS:
        return False
    return None

