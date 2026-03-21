from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class PublicProblem:
    """Canonical schema for a public competition problem."""

    equation1: str
    equation2: str
    problem_id: str | None = None
    answer: bool | None = None
    source: str | None = None
    split: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EvalRecord:
    """Single evaluation result for one problem and one prompt/model pair."""

    answer: bool
    problem_id: str | None = None
    prediction: bool | None = None
    parsed: bool = True
    source: str | None = None
    raw_output: str | None = None
    latency_ms: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
