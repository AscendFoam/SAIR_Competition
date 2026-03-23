from __future__ import annotations

import re


TRUE_TOKENS = {"true"}
FALSE_TOKENS = {"false"}
TOKEN_PATTERN = re.compile(r"[A-Za-z]+")
VERDICT_PATTERN = re.compile(
    r"[*_`#>\s-]*VERDICT[*_`]*\s*[*_`]*:\s*[*_`]*\s*(TRUE|FALSE)\b",
    re.IGNORECASE,
)
LINE_TOKEN_PATTERN = re.compile(r"^\s*[*_`\"']?(true|false)[*_`\"']?\s*$", re.IGNORECASE)


def parse_bool_output(raw_output: str) -> bool | None:
    """Parse a raw model output into a boolean if it cleanly maps to true/false."""

    verdict_matches = VERDICT_PATTERN.findall(raw_output)
    if verdict_matches:
        token = verdict_matches[-1].lower()
        if token in TRUE_TOKENS:
            return True
        if token in FALSE_TOKENS:
            return False

    for line in raw_output.splitlines():
        line_match = LINE_TOKEN_PATTERN.match(line)
        if not line_match:
            continue
        token = line_match.group(1).lower()
        if token in TRUE_TOKENS:
            return True
        if token in FALSE_TOKENS:
            return False

    tokens = TOKEN_PATTERN.findall(raw_output.strip().lower())
    if len(tokens) != 1:
        return None
    token = tokens[0]
    if token in TRUE_TOKENS:
        return True
    if token in FALSE_TOKENS:
        return False
    return None
