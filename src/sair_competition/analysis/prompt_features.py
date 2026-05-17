"""Prompt feature extractor skeleton (T08).

Rule-based extraction of prompt structural features from local text-ready prompt
files. This is a **skeleton** — only a subset of fields are rule-ized. Manual
taxonomy coding (prompt_features_v1.jsonl) remains the authoritative reference.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Length-bucket thresholds (must match taxonomy YAML bucket_boundary_notes)
# ---------------------------------------------------------------------------

BYTES_THRESHOLDS: list[tuple[str, int, float]] = [
    ("short", 0, 2000),
    ("medium", 2000, 3500),
    ("long", 3500, 8000),
    ("near_cap", 8000, float("inf")),
]

TOKEN_THRESHOLDS: list[tuple[str, int, float]] = [
    ("short", 0, 500),
    ("medium", 500, 875),
    ("long", 875, 2000),
    ("near_cap", 2000, float("inf")),
]


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def estimate_tokens(byte_count: int) -> int:
    """Estimate token count using round(bytes/4). Matches corpus_v1 data."""
    return round(byte_count / 4)


def _bucketize(value: int, thresholds: list[tuple[str, int, float]]) -> str:
    for name, lo, hi in thresholds:
        if lo <= value < hi:
            return name
    return thresholds[-1][0]


# ---------------------------------------------------------------------------
# Field extractors
# ---------------------------------------------------------------------------

def extract_prompt_bytes_bucket(byte_count: int) -> str:
    return _bucketize(byte_count, BYTES_THRESHOLDS)


def extract_prompt_tokens_est_bucket(token_est: int) -> str:
    return _bucketize(token_est, TOKEN_THRESHOLDS)


# -- verdict_contract --------------------------------------------------------

def extract_verdict_contract(text: str) -> str:
    """Detect verdict output format contract strength.

    Returns one of: strict, relaxed, unknown.
    """
    if re.search(r"VERDICT:\s*(TRUE|FALSE)", text, re.IGNORECASE):
        return "relaxed"
    if re.search(r"exactly\s+one\s+token", text, re.IGNORECASE):
        return "strict"
    if re.search(r"single\s+token", text, re.IGNORECASE):
        return "strict"
    return "unknown"


# -- rule_or_heuristic_block --------------------------------------------------

def extract_rule_or_heuristic_block(text: str) -> str:
    """Estimate rule-block density from structural keywords.

    Returns one of: none, compact, extended, saturated.

    saturated is distinguished from extended by the presence of an explicit
    "do not let later guardrails override" clause (only in P1.2.5).
    """
    has_mandatory = bool(re.search(r"mandatory\s+true\s+check", text, re.IGNORECASE))
    has_override = bool(re.search(r"override", text, re.IGNORECASE))
    if has_mandatory and has_override:
        return "saturated"
    if has_mandatory:
        return "extended"
    compact_markers = [
        "fast true", "fast false", "safe true",
        "immediate true", "cautious false",
        "fast-filter", "fast filter",
    ]
    tl = text.lower()
    if any(m in tl for m in compact_markers):
        return "compact"
    return "none"


# -- opening_strategy ---------------------------------------------------------

_CE_FIRST_RE = re.compile(r"counterexample.first", re.IGNORECASE)
_BALANCED_RE = re.compile(r"balanced\s+(?:solve|order)", re.IGNORECASE)
_TRIVIAL_FIRST_MARKERS = [
    "singleton.collapse", "fast true", "safe true", "mandatory true",
    "immediate true",
]


def extract_opening_strategy(text: str) -> str:
    """Detect the first dominant reasoning strategy.

    Returns one of: trivial_first, counterexample_first, balanced, unknown.
    """
    if _CE_FIRST_RE.search(text):
        return "counterexample_first"
    if _BALANCED_RE.search(text):
        return "balanced"
    tl = text.lower()
    if any(re.search(p, tl) for p in _TRIVIAL_FIRST_MARKERS):
        return "trivial_first"
    return "unknown"


# -- counterexample_requirement -----------------------------------------------

def extract_counterexample_requirement(text: str) -> str:
    """Detect counterexample instruction strength.

    Returns one of: required, encouraged, optional, absent.

    Note: P2.0.2 manual coding is "optional" but the extractor returns "absent"
    because the prompt has no "counterexample" keyword.  P0's "COUNTEREXAMPLE"
    section name is excluded from matching.  See extractor_v1_notes.md.
    """
    if re.search(r"you\s+must\s+.*counterexample", text, re.IGNORECASE):
        return "required"
    if re.search(r"counterexample.first\s+policy", text, re.IGNORECASE):
        return "encouraged"
    if re.search(r"falsification", text, re.IGNORECASE):
        return "encouraged"
    # Match "counterexample" as instruction keyword, not as output section name.
    # P0 has "or COUNTEREXAMPLE after the verdict" — that's a section name, not
    # a CE instruction.  Only match if "counterexample" appears in a context
    # that suggests instruction (search, construction, lookup, table, hint).
    if re.search(r"counterexample\s+(?:search|construct|lookup|table|hint|instruction)", text, re.IGNORECASE):
        return "optional"
    return "absent"


# -- explicit_final_token -----------------------------------------------------

def extract_explicit_final_token(text: str) -> bool:
    """Detect whether the prompt demands an exact single-token output."""
    return bool(
        re.search(r"exactly\s+one\s+token", text, re.IGNORECASE)
        or re.search(r"single\s+token", text, re.IGNORECASE)
    )


# ---------------------------------------------------------------------------
# Output data class
# ---------------------------------------------------------------------------

@dataclass
class ExtractedFeatures:
    """Output schema for the prompt feature extractor skeleton.

    Fields marked ``unknown`` / ``None`` are placeholders that still require
    manual review.  See extractor_v1_notes.md for coverage status.
    """

    prompt_id: str
    prompt_bytes: int
    prompt_tokens_est: int
    prompt_bytes_bucket: str
    prompt_tokens_est_bucket: str

    # --- rule-ized fields (skeleton coverage) ---
    verdict_contract: str
    rule_or_heuristic_block: str
    opening_strategy: str
    counterexample_requirement: str
    explicit_final_token: bool

    # --- placeholder fields (not yet rule-ized) ---
    cheatsheet_density: str = "unknown"
    compression_style: str = "unknown"
    system_goal_framing: bool | None = None
    stepwise_reasoning_block: bool | None = None
    examples_block: str = "unknown"
    safety_or_guardrail_block: bool | None = None
    verdict_positioning: str = "unknown"
    examples_before_rules: bool | None = None
    finite_model_search_hint: bool | None = None
    false_filter_orientation: str = "unknown"
    ce_search_depth: str = "unknown"
    proof_like_true_support: str = "unknown"
    identity_or_invariant_guidance: bool | None = None
    ambiguity_handling: str = "unknown"
    parser_friendliness: str = "unknown"
    formatting_redundancy: str = "unknown"
    provenance_status: str = "unknown"
    builds_on_public_work: str = "unknown"
    post_release_relation: str = "unknown"

    extraction_version: str = "T08_v1_skeleton"

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Top-level extraction
# ---------------------------------------------------------------------------

def extract_features(prompt_id: str, prompt_text: str) -> ExtractedFeatures:
    """Extract structural features from a prompt text.

    Only a subset of fields are rule-ized.  All other fields return
    placeholder values and require manual review.
    """
    byte_count = len(prompt_text.encode("utf-8"))
    token_est = estimate_tokens(byte_count)

    return ExtractedFeatures(
        prompt_id=prompt_id,
        prompt_bytes=byte_count,
        prompt_tokens_est=token_est,
        prompt_bytes_bucket=extract_prompt_bytes_bucket(byte_count),
        prompt_tokens_est_bucket=extract_prompt_tokens_est_bucket(token_est),
        verdict_contract=extract_verdict_contract(prompt_text),
        rule_or_heuristic_block=extract_rule_or_heuristic_block(prompt_text),
        opening_strategy=extract_opening_strategy(prompt_text),
        counterexample_requirement=extract_counterexample_requirement(prompt_text),
        explicit_final_token=extract_explicit_final_token(prompt_text),
    )


def extract_features_from_file(prompt_id: str, file_path: Path) -> ExtractedFeatures:
    """Extract features from a prompt file on disk.

    Reads raw bytes so prompt_bytes matches the file size recorded in
    corpus_v1.jsonl (which was computed from the file on disk, not from
    decoded text).
    """
    raw = file_path.read_bytes()
    byte_count = len(raw)
    text = raw.decode("utf-8")
    token_est = estimate_tokens(byte_count)

    return ExtractedFeatures(
        prompt_id=prompt_id,
        prompt_bytes=byte_count,
        prompt_tokens_est=token_est,
        prompt_bytes_bucket=extract_prompt_bytes_bucket(byte_count),
        prompt_tokens_est_bucket=extract_prompt_tokens_est_bucket(token_est),
        verdict_contract=extract_verdict_contract(text),
        rule_or_heuristic_block=extract_rule_or_heuristic_block(text),
        opening_strategy=extract_opening_strategy(text),
        counterexample_requirement=extract_counterexample_requirement(text),
        explicit_final_token=extract_explicit_final_token(text),
    )


# ---------------------------------------------------------------------------
# Batch extraction from corpus
# ---------------------------------------------------------------------------

def extract_features_from_corpus(
    corpus_path: Path,
    *,
    repo_root: Path | None = None,
) -> list[ExtractedFeatures]:
    """Extract features for all text-ready records in a corpus JSONL.

    Non-text-ready records (metadata-only, structure-only) are silently
    skipped — they are not included in the output at all, mirroring the
    T06/T07 boundary gate.
    """
    if repo_root is None:
        from ..paths import REPO_ROOT
        repo_root = REPO_ROOT

    results: list[ExtractedFeatures] = []
    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if not rec.get("text_ready", False):
                continue
            prompt_path = rec.get("prompt_text_path", "")
            if not prompt_path:
                continue
            full_path = repo_root / prompt_path
            if not full_path.exists():
                continue
            features = extract_features_from_file(rec["prompt_id"], full_path)
            results.append(features)
    return results
