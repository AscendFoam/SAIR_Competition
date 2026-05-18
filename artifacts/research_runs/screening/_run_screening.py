"""
T11 Screening Runner - executes all 9 screening runs and produces required artifacts.
This is a temporary execution script, not a permanent code asset.
"""
import json
import hashlib
import sys
import os
import time
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "src"))

from sair_competition.eval.local_runner import run_complete_prompt_eval

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SCREENING_DIR = PROJECT_ROOT / "artifacts" / "research_runs" / "screening"
SMOKE_PATH = PROJECT_ROOT / "data" / "interim" / "splits" / "smoke.jsonl"
DOTENV_PATH = PROJECT_ROOT / ".env"
CORPUS_PATH = PROJECT_ROOT / "data" / "interim" / "prompt_corpus" / "corpus_v1.jsonl"

PROMPTS = [
    ("local_p0_official_reconstructed_empty", "prompts/complete/P0.official_reconstructed_empty.txt"),
    ("local_p1_1_1_strict_first_draft", "prompts/complete/P1.1.1_strict_first_draft.txt"),
    ("local_p1_2_2_implicit_guardrail_v1", "prompts/complete/P1.2.2_implicit_guardrail_v1.txt"),
    ("local_p1_2_3_implicit_guardrail_v2", "prompts/complete/P1.2.3_implicit_guardrail_v2.txt"),
    ("local_p1_2_5_minimal_rule_missing_hard_composition", "prompts/complete/P1.2.5_minimal_rule_missing_hard_composition.txt"),
    ("local_p1_2_8_narrow_singleton_families", "prompts/complete/P1.2.8_narrow_singleton_families.txt"),
    ("local_p2_0_0_official_balanced_strict_v0", "prompts/complete/P2.0.0_official_balanced_strict_v0.txt"),
    ("local_p2_0_1_official_counterexample_first_strict_v0", "prompts/complete/P2.0.1_official_counterexample_first_strict_v0.txt"),
    ("local_p2_0_2_official_fast_filters_strict_v0", "prompts/complete/P2.0.2_official_fast_filters_strict_v0.txt"),
]

def load_corpus_sha256():
    """Load SHA256 hashes from corpus_v1.jsonl."""
    from sair_competition.data.io import read_jsonl
    records = read_jsonl(CORPUS_PATH)
    return {r["prompt_id"]: r["prompt_sha256"] for r in records}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def write_run_config(run_dir, prompt_id, prompt_path, model, provider):
    config = {
        "screening_phase": "Stage_A_screening",
        "prompt_id": prompt_id,
        "prompt_path": str(prompt_path),
        "dataset_path": str(SMOKE_PATH),
        "dataset_version": "smoke_v1_64",
        "provider": provider,
        "model": model,
        "temperature": 0,
        "max_tokens": 256,
        "reasoning_mode": "default",
        "repeats": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(run_dir / "run_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def write_prompt_hash_manifest(run_dir, prompt_id, prompt_path, expected_sha256):
    actual_sha256 = sha256_file(prompt_path)
    manifest = {
        "prompt_id": prompt_id,
        "prompt_path": str(prompt_path),
        "expected_sha256": expected_sha256,
        "actual_sha256": actual_sha256,
        "sha256_match": actual_sha256 == expected_sha256,
    }
    with open(run_dir / "prompt_hash_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest

def main():
    corpus_hashes = load_corpus_sha256()
    results = []

    for prompt_id, rel_prompt_path in PROMPTS:
        prompt_path = PROJECT_ROOT / rel_prompt_path
        run_dir = SCREENING_DIR / prompt_id
        run_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"Running screening: {prompt_id}")
        print(f"Prompt file: {rel_prompt_path}")
        print(f"Output dir:  {run_dir}")
        start_time = time.time()

        try:
            summary = run_complete_prompt_eval(
                dataset_path=SMOKE_PATH,
                prompt_path=prompt_path,
                output_dir=run_dir,
                dotenv_path=DOTENV_PATH,
                provider_name="deepseek",
                model="deepseek-chat",
                temperature=0.0,
                max_tokens=256,
            )
            elapsed = time.time() - start_time

            # Write supplementary artifacts
            write_run_config(run_dir, prompt_id, prompt_path, summary["model"], summary["provider"])
            hash_manifest = write_prompt_hash_manifest(run_dir, prompt_id, prompt_path, corpus_hashes.get(prompt_id, ""))

            metrics = summary.get("metrics", {})
            result = {
                "prompt_id": prompt_id,
                "status": "completed",
                "elapsed_seconds": round(elapsed, 1),
                "model": summary["model"],
                "provider": summary["provider"],
                "row_count": summary["row_count"],
                "parse_counter": summary["parse_counter"],
                "accuracy": metrics.get("accuracy"),
                "parse_success_rate": metrics.get("parse_success_rate"),
                "true_recall": metrics.get("true_accuracy"),
                "false_recall": metrics.get("false_accuracy"),
                "true_total": metrics.get("true_total"),
                "true_correct": metrics.get("true_correct"),
                "false_total": metrics.get("false_total"),
                "false_correct": metrics.get("false_correct"),
                "sha256_match": hash_manifest["sha256_match"],
            }
            print(f"  Completed in {elapsed:.1f}s")
            print(f"  Accuracy: {metrics.get('accuracy'):.4f}")
            print(f"  Parse:    {metrics.get('parse_success_rate'):.4f}")
            print(f"  T recall: {metrics.get('true_accuracy')}")
            print(f"  F recall: {metrics.get('false_accuracy')}")

        except Exception as e:
            elapsed = time.time() - start_time
            result = {
                "prompt_id": prompt_id,
                "status": "failed",
                "elapsed_seconds": round(elapsed, 1),
                "error": str(e),
            }
            print(f"  FAILED: {e}")

        results.append(result)

    # Save consolidated results
    with open(SCREENING_DIR / "screening_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("All screening runs complete.")
    completed = sum(1 for r in results if r["status"] == "completed")
    failed = sum(1 for r in results if r["status"] == "failed")
    print(f"Completed: {completed}, Failed: {failed}")
    for r in results:
        if r["status"] == "completed":
            print(f"  {r['prompt_id']}: acc={r['accuracy']:.4f} parse={r['parse_success_rate']:.4f} T_rec={r['true_recall']} F_rec={r['false_recall']}")
        else:
            print(f"  {r['prompt_id']}: FAILED ({r.get('error', 'unknown')})")

if __name__ == "__main__":
    main()
