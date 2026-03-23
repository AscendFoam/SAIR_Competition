from pathlib import Path

from sair_competition.data.io import write_jsonl
from sair_competition.data.splits import make_frozen_splits


def test_make_frozen_splits_produces_exact_sizes(tmp_path: Path) -> None:
    dataset_path = tmp_path / "public_all.jsonl"
    rows = []
    for idx in range(10):
        rows.append(
            {
                "problem_id": f"normal_{idx:04d}",
                "index": idx,
                "source": "normal",
                "equation1": "x = x",
                "equation2": "x = x",
                "answer": idx % 2 == 0,
                "split": None,
                "metadata": {},
            }
        )
    write_jsonl(dataset_path, rows)

    manifest = make_frozen_splits(
        dataset_path=dataset_path,
        output_dir=tmp_path / "splits",
        split_targets={"smoke": 2, "dev": 4, "holdout": 2, "audit": 2},
        seed=123,
    )

    assert manifest["splits"]["smoke"]["count"] == 2
    assert manifest["splits"]["dev"]["count"] == 4
    assert manifest["splits"]["holdout"]["count"] == 2
    assert manifest["splits"]["audit"]["count"] == 2

