"""
T12 Screening Runner (Second Model) - reruns all 9 screening prompts with deepseek-v4-flash.
Uses direct API calls with thinking disabled since deepseek-v4-flash defaults to reasoning mode
which consumes all max_tokens in reasoning_tokens, leaving no room for content output.
Temporary execution script, not a permanent code asset.
"""
import json
import hashlib
import sys
import time
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "src"))

from sair_competition.config.env import resolve_openai_compatible_settings
from sair_competition.data.io import read_jsonl, write_jsonl
from sair_competition.eval.parser import parse_bool_output
from sair_competition.eval.metrics import compute_metrics
from sair_competition.prompting.compose import load_text
from sair_competition.prompting.render import render_complete_prompt_for_problem

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SCREENING_DIR = PROJECT_ROOT / "artifacts" / "research_runs" / "screening_second_model"
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

# frozen from T10 matrix, except model
PROVIDER = "deepseek"
MODEL = "deepseek-v4-flash"
TEMPERATURE = 0.0
MAX_TOKENS = 256


def load_corpus_sha256():
    from sair_competition.data.io import read_jsonl as _read
    records = _read(CORPUS_PATH)
    return {r["prompt_id"]: r["prompt_sha256"] for r in records}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def call_api(endpoint, api_key, prompt, max_retries=3):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "thinking": {"type": "disabled"},
    }
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    last_error = None
    for attempt in range(1, max_retries + 1):
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            latency = time.perf_counter() - started
            content = body["choices"][0]["message"]["content"] or ""
            return content.strip(), latency
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code not in {408, 429, 500, 502, 503, 504} or attempt >= max_retries:
                raise RuntimeError(f"HTTP error: {exc.code} {detail}") from exc
            last_error = exc
        except (urllib.error.URLError, TimeoutError, ConnectionResetError) as exc:
            if attempt >= max_retries:
                raise RuntimeError(f"Network error: {exc}") from exc
            last_error = exc
        time.sleep(attempt * 1.0)
    raise RuntimeError(f"Failed after retries: {last_error}")


def write_run_config(run_dir, prompt_id, prompt_path):
    config = {
        "screening_phase": "Stage_A_screening_second_model",
        "prompt_id": prompt_id,
        "prompt_path": str(prompt_path),
        "dataset_path": str(SMOKE_PATH),
        "dataset_version": "smoke_v1_64",
        "provider": PROVIDER,
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "reasoning_mode": "default",
        "thinking_disabled": True,
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


def write_summary(run_dir, prompt_id, prediction_rows):
    metrics = compute_metrics(prediction_rows)
    parse_counter = {}
    for r in prediction_rows:
        key = "parsed" if r.get("parsed") else "unparsed"
        parse_counter[key] = parse_counter.get(key, 0) + 1
    summary = {
        "dataset_path": str(SMOKE_PATH),
        "prompt_id": prompt_id,
        "provider": PROVIDER,
        "model": MODEL,
        "row_count": len(prediction_rows),
        "parse_counter": parse_counter,
        "metrics": metrics.to_dict(),
    }
    with open(run_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    return summary


def main():
    settings = resolve_openai_compatible_settings(
        DOTENV_PATH, model=MODEL, provider_name=PROVIDER
    )
    endpoint = settings.base_url.rstrip("/") + "/chat/completions"
    corpus_hashes = load_corpus_sha256()
    rows = read_jsonl(SMOKE_PATH)
    results = []

    for prompt_id, rel_prompt_path in PROMPTS:
        prompt_path = PROJECT_ROOT / rel_prompt_path
        run_dir = SCREENING_DIR / prompt_id
        run_dir.mkdir(parents=True, exist_ok=True)

        prompt_template = load_text(prompt_path)
        prediction_rows = []

        # resume support
        preds_path = run_dir / "predictions.jsonl"
        existing_ids = set()
        if preds_path.exists():
            existing = read_jsonl(preds_path)
            prediction_rows = list(existing)
            existing_ids = {r["problem_id"] for r in existing}

        print(f"\n{'='*60}")
        print(f"Running: {prompt_id} ({MODEL})")
        print(f"Output:  {run_dir}")
        print(f"Existing: {len(existing_ids)}, Remaining: {len(rows) - len(existing_ids)}")
        start_time = time.time()

        try:
            for row in rows:
                if row["problem_id"] in existing_ids:
                    continue
                prompt = render_complete_prompt_for_problem(
                    complete_prompt_text=prompt_template,
                    equation1=row["equation1"],
                    equation2=row["equation2"],
                )
                raw_output, latency = call_api(endpoint, settings.api_key, prompt)
                parsed = parse_bool_output(raw_output)
                parsed_ok = parsed is not None
                prediction_rows.append({
                    "problem_id": row["problem_id"],
                    "source": row["source"],
                    "split": row.get("split"),
                    "equation1": row["equation1"],
                    "equation2": row["equation2"],
                    "answer": row["answer"],
                    "prediction": parsed,
                    "parsed": parsed_ok,
                    "raw_output": raw_output,
                    "latency_seconds": latency,
                    "prompt_path": str(prompt_path),
                    "model": MODEL,
                    "provider": PROVIDER,
                    "family_tags": row.get("family_tags") or [],
                    "family_signals": row.get("family_signals") or {},
                })
                # save incrementally
                write_jsonl(preds_path, prediction_rows)

            elapsed = time.time() - start_time

            write_run_config(run_dir, prompt_id, prompt_path)
            hash_manifest = write_prompt_hash_manifest(
                run_dir, prompt_id, prompt_path, corpus_hashes.get(prompt_id, "")
            )
            summary = write_summary(run_dir, prompt_id, prediction_rows)
            metrics = summary["metrics"]

            result = {
                "prompt_id": prompt_id,
                "status": "completed",
                "elapsed_seconds": round(elapsed, 1),
                "model": MODEL,
                "provider": PROVIDER,
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
            print(f"  Done in {elapsed:.1f}s")
            print(f"  Acc: {metrics.get('accuracy'):.4f}  Parse: {metrics.get('parse_success_rate'):.4f}")
            print(f"  T_rec: {metrics.get('true_accuracy')}  F_rec: {metrics.get('false_accuracy')}")

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

    with open(SCREENING_DIR / "screening_second_model_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"All {MODEL} screening runs complete.")
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
