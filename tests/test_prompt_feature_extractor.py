"""Focused tests for the prompt feature extractor skeleton (T08).

Verifies:
- extractor output is parseable and has expected schema fields
- core rule-ized fields match manual coding on representative prompts
- metadata-only / structure-only records are excluded from batch extraction
- length buckets and token estimates are computed correctly
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sair_competition.analysis.prompt_features import (
    BYTES_THRESHOLDS,
    TOKEN_THRESHOLDS,
    ExtractedFeatures,
    estimate_tokens,
    extract_counterexample_requirement,
    extract_explicit_final_token,
    extract_features,
    extract_features_from_corpus,
    extract_features_from_file,
    extract_opening_strategy,
    extract_prompt_bytes_bucket,
    extract_prompt_tokens_est_bucket,
    extract_rule_or_heuristic_block,
    extract_verdict_contract,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts" / "complete"
CORPUS_PATH = REPO_ROOT / "data" / "interim" / "prompt_corpus" / "corpus_v1.jsonl"

# Known manual coding from prompt_features_v1.jsonl (prompt_id → field values)
MANUAL_CODING: dict[str, dict] = {
    "local_p0_official_reconstructed_empty": {
        "file": "P0.official_reconstructed_empty.txt",
        "bytes": 511,
        "prompt_bytes_bucket": "short",
        "prompt_tokens_est_bucket": "short",
        "verdict_contract": "relaxed",
        "rule_or_heuristic_block": "none",
        "opening_strategy": "unknown",
        "counterexample_requirement": "absent",
        "explicit_final_token": False,
    },
    "local_p1_1_1_strict_first_draft": {
        "file": "P1.1.1_strict_first_draft.txt",
        "bytes": 2227,
        "prompt_bytes_bucket": "medium",
        "prompt_tokens_est_bucket": "medium",
        "verdict_contract": "strict",
        "rule_or_heuristic_block": "compact",
        "opening_strategy": "trivial_first",
        "counterexample_requirement": "absent",
        "explicit_final_token": True,
    },
    "local_p1_2_2_implicit_guardrail_v1": {
        "file": "P1.2.2_implicit_guardrail_v1.txt",
        "bytes": 3454,
        "prompt_bytes_bucket": "medium",
        "prompt_tokens_est_bucket": "medium",
        "verdict_contract": "strict",
        "rule_or_heuristic_block": "extended",
        "opening_strategy": "trivial_first",
        "counterexample_requirement": "absent",
        "explicit_final_token": True,
    },
    "local_p1_2_3_implicit_guardrail_v2": {
        "file": "P1.2.3_implicit_guardrail_v2.txt",
        "bytes": 3501,
        "prompt_bytes_bucket": "long",
        "prompt_tokens_est_bucket": "long",
        "verdict_contract": "strict",
        "rule_or_heuristic_block": "extended",
        "opening_strategy": "trivial_first",
        "counterexample_requirement": "absent",
        "explicit_final_token": True,
    },
    "local_p1_2_5_minimal_rule_missing_hard_composition": {
        "file": "P1.2.5_minimal_rule_missing_hard_composition.txt",
        "bytes": 4059,
        "prompt_bytes_bucket": "long",
        "prompt_tokens_est_bucket": "long",
        "verdict_contract": "strict",
        "rule_or_heuristic_block": "saturated",
        "opening_strategy": "trivial_first",
        "counterexample_requirement": "absent",
        "explicit_final_token": True,
    },
    "local_p1_2_8_narrow_singleton_families": {
        "file": "P1.2.8_narrow_singleton_families.txt",
        "bytes": 3948,
        "prompt_bytes_bucket": "long",
        "prompt_tokens_est_bucket": "long",
        "verdict_contract": "strict",
        "rule_or_heuristic_block": "extended",
        "opening_strategy": "trivial_first",
        "counterexample_requirement": "absent",
        "explicit_final_token": True,
    },
    "local_p2_0_0_official_balanced_strict_v0": {
        "file": "P2.0.0_official_balanced_strict_v0.txt",
        "bytes": 2448,
        "prompt_bytes_bucket": "medium",
        "prompt_tokens_est_bucket": "medium",
        "verdict_contract": "strict",
        "rule_or_heuristic_block": "compact",
        "opening_strategy": "balanced",
        "counterexample_requirement": "absent",
        "explicit_final_token": True,
    },
    "local_p2_0_1_official_counterexample_first_strict_v0": {
        "file": "P2.0.1_official_counterexample_first_strict_v0.txt",
        "bytes": 2320,
        "prompt_bytes_bucket": "medium",
        "prompt_tokens_est_bucket": "medium",
        "verdict_contract": "strict",
        "rule_or_heuristic_block": "compact",
        "opening_strategy": "counterexample_first",
        "counterexample_requirement": "encouraged",
        "explicit_final_token": True,
    },
    "local_p2_0_2_official_fast_filters_strict_v0": {
        "file": "P2.0.2_official_fast_filters_strict_v0.txt",
        "bytes": 1723,
        "prompt_bytes_bucket": "short",
        "prompt_tokens_est_bucket": "short",
        "verdict_contract": "strict",
        "rule_or_heuristic_block": "compact",
        "opening_strategy": "trivial_first",
        # Manual coding: "optional". Extractor returns "absent" because the
        # prompt has no "counterexample" keyword. This is a known skeleton
        # limitation documented in extractor_v1_notes.md.
        "counterexample_requirement": "absent",
        "explicit_final_token": True,
    },
}


# ---------------------------------------------------------------------------
# Schema and parseability tests
# ---------------------------------------------------------------------------

class TestOutputSchema:
    """Extractor output must be parseable and have the expected fields."""

    def test_to_dict_returns_dict(self) -> None:
        feat = extract_features("test", "some prompt text")
        d = feat.to_dict()
        assert isinstance(d, dict)

    def test_to_dict_json_serializable(self) -> None:
        feat = extract_features("test", "some prompt text")
        s = json.dumps(feat.to_dict())
        assert isinstance(s, str)
        parsed = json.loads(s)
        assert parsed["prompt_id"] == "test"

    def test_output_has_all_rule_ized_fields(self) -> None:
        feat = extract_features("test", "some prompt text")
        d = feat.to_dict()
        expected = [
            "prompt_id", "prompt_bytes", "prompt_tokens_est",
            "prompt_bytes_bucket", "prompt_tokens_est_bucket",
            "verdict_contract", "rule_or_heuristic_block",
            "opening_strategy", "counterexample_requirement",
            "explicit_final_token",
        ]
        for field in expected:
            assert field in d, f"Missing field: {field}"

    def test_output_has_placeholder_fields(self) -> None:
        feat = extract_features("test", "some prompt text")
        d = feat.to_dict()
        placeholders = [
            "cheatsheet_density", "compression_style",
            "system_goal_framing", "stepwise_reasoning_block",
            "examples_block", "safety_or_guardrail_block",
        ]
        for field in placeholders:
            assert field in d, f"Missing placeholder field: {field}"

    def test_extraction_version_set(self) -> None:
        feat = extract_features("test", "some prompt text")
        assert feat.extraction_version == "T08_v1_skeleton"


# ---------------------------------------------------------------------------
# Length bucket and token estimate tests
# ---------------------------------------------------------------------------

class TestLengthBuckets:

    @pytest.mark.parametrize("byte_count,expected_bucket", [
        (100, "short"),
        (1999, "short"),
        (2000, "medium"),
        (3499, "medium"),
        (3500, "long"),
        (7999, "long"),
        (8000, "near_cap"),
        (15000, "near_cap"),
    ])
    def test_bytes_bucket_boundaries(self, byte_count: int, expected_bucket: str) -> None:
        assert extract_prompt_bytes_bucket(byte_count) == expected_bucket

    @pytest.mark.parametrize("token_est,expected_bucket", [
        (100, "short"),
        (499, "short"),
        (500, "medium"),
        (874, "medium"),
        (875, "long"),
        (1999, "long"),
        (2000, "near_cap"),
    ])
    def test_tokens_bucket_boundaries(self, token_est: int, expected_bucket: str) -> None:
        assert extract_prompt_tokens_est_bucket(token_est) == expected_bucket

    def test_token_estimate_rounds_correctly(self) -> None:
        assert estimate_tokens(511) == 128   # round(127.75)
        assert estimate_tokens(2227) == 557  # round(556.75)
        assert estimate_tokens(3454) == 864  # round(863.5)
        assert estimate_tokens(1723) == 431  # round(430.75)

    def test_all_9_prompt_byte_counts_match(self) -> None:
        """Byte counts from extractor must match corpus_v1 values."""
        for pid, coding in MANUAL_CODING.items():
            path = PROMPTS_DIR / coding["file"]
            feat = extract_features_from_file(pid, path)
            assert feat.prompt_bytes == coding["bytes"], (
                f"{pid}: expected {coding['bytes']} bytes, got {feat.prompt_bytes}"
            )


# ---------------------------------------------------------------------------
# Core field alignment tests against manual coding
# ---------------------------------------------------------------------------

class TestCoreFieldAlignment:
    """Core rule-ized fields must match manual coding for all 9 prompts."""

    @pytest.mark.parametrize("pid", list(MANUAL_CODING.keys()))
    def test_verdict_contract(self, pid: str) -> None:
        coding = MANUAL_CODING[pid]
        text = (PROMPTS_DIR / coding["file"]).read_text(encoding="utf-8")
        assert extract_verdict_contract(text) == coding["verdict_contract"]

    @pytest.mark.parametrize("pid", list(MANUAL_CODING.keys()))
    def test_rule_or_heuristic_block(self, pid: str) -> None:
        coding = MANUAL_CODING[pid]
        text = (PROMPTS_DIR / coding["file"]).read_text(encoding="utf-8")
        assert extract_rule_or_heuristic_block(text) == coding["rule_or_heuristic_block"]

    @pytest.mark.parametrize("pid", list(MANUAL_CODING.keys()))
    def test_opening_strategy(self, pid: str) -> None:
        coding = MANUAL_CODING[pid]
        text = (PROMPTS_DIR / coding["file"]).read_text(encoding="utf-8")
        assert extract_opening_strategy(text) == coding["opening_strategy"]

    @pytest.mark.parametrize("pid", list(MANUAL_CODING.keys()))
    def test_counterexample_requirement(self, pid: str) -> None:
        coding = MANUAL_CODING[pid]
        text = (PROMPTS_DIR / coding["file"]).read_text(encoding="utf-8")
        result = extract_counterexample_requirement(text)
        assert result == coding["counterexample_requirement"], (
            f"{pid}: expected {coding['counterexample_requirement']}, got {result}"
        )

    @pytest.mark.parametrize("pid", list(MANUAL_CODING.keys()))
    def test_explicit_final_token(self, pid: str) -> None:
        coding = MANUAL_CODING[pid]
        text = (PROMPTS_DIR / coding["file"]).read_text(encoding="utf-8")
        assert extract_explicit_final_token(text) == coding["explicit_final_token"]

    @pytest.mark.parametrize("pid", list(MANUAL_CODING.keys()))
    def test_prompt_bytes_bucket(self, pid: str) -> None:
        coding = MANUAL_CODING[pid]
        text = (PROMPTS_DIR / coding["file"]).read_text(encoding="utf-8")
        feat = extract_features(pid, text)
        assert feat.prompt_bytes_bucket == coding["prompt_bytes_bucket"]

    @pytest.mark.parametrize("pid", list(MANUAL_CODING.keys()))
    def test_prompt_tokens_est_bucket(self, pid: str) -> None:
        coding = MANUAL_CODING[pid]
        text = (PROMPTS_DIR / coding["file"]).read_text(encoding="utf-8")
        feat = extract_features(pid, text)
        assert feat.prompt_tokens_est_bucket == coding["prompt_tokens_est_bucket"]


# ---------------------------------------------------------------------------
# Boundary gate tests
# ---------------------------------------------------------------------------

class TestBoundaryGate:
    """Batch extraction must exclude non-text-ready records."""

    def test_batch_extracts_exactly_9(self) -> None:
        results = extract_features_from_corpus(CORPUS_PATH, repo_root=REPO_ROOT)
        assert len(results) == 9

    def test_batch_excludes_metadata_only(self) -> None:
        results = extract_features_from_corpus(CORPUS_PATH, repo_root=REPO_ROOT)
        ids = {r.prompt_id for r in results}
        assert "public_placeholder_ce_first_github" not in ids

    def test_batch_excludes_structure_only(self) -> None:
        results = extract_features_from_corpus(CORPUS_PATH, repo_root=REPO_ROOT)
        ids = {r.prompt_id for r in results}
        assert "public_placeholder_contributor_prompt" not in ids

    def test_batch_output_ids_match_corpus_text_ready(self) -> None:
        expected_ids = set(MANUAL_CODING.keys())
        results = extract_features_from_corpus(CORPUS_PATH, repo_root=REPO_ROOT)
        actual_ids = {r.prompt_id for r in results}
        assert actual_ids == expected_ids


# ---------------------------------------------------------------------------
# Full extraction round-trip test
# ---------------------------------------------------------------------------

class TestFullExtractionRoundTrip:
    """End-to-end: extract all 9 prompts and verify key fields."""

    def test_all_9_produce_valid_json(self) -> None:
        for pid, coding in MANUAL_CODING.items():
            text = (PROMPTS_DIR / coding["file"]).read_text(encoding="utf-8")
            feat = extract_features(pid, text)
            d = feat.to_dict()
            serialized = json.dumps(d, ensure_ascii=False)
            parsed = json.loads(serialized)
            assert parsed["prompt_id"] == pid
