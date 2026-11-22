"""
3 tests in total
1. one where the file is valid with all the cirrect jsons
2 where file has some invalid jsons and the rest are valid
3 generate a 1 million recors file and then test the iterator
"""

import json
import tracemalloc
from pathlib import Path

from ai_engineeringroadmap.jsonl import iter_records

LLM_FILE = Path(__file__).resolve().parent.parent / "staticFiles" / "llm.jsonl"


def generate_valid_lines():
    with open(LLM_FILE, "w") as f:
        for i in range(10):
            model = "model-a" if i % 2 == 0 else "model-b"
            f.write(json.dumps({"model": model, "tokens": 10}) + "\n")


def generate_corrupt_json():
    with open(LLM_FILE, "w") as f:
        for i in range(10):
            if i % 3 == 0:
                f.write("{invalid_json: true}\n")  # Corrupt JSON
            else:
                model = "model-a" if i % 2 == 0 else "model-b"
                f.write(json.dumps({"model": model, "tokens": 10}) + "\n")


def test_valid_file():
    # Test with a valid file
    generate_valid_lines()
    records = list(iter_records(LLM_FILE))
    assert len(records) > 0  # Ensure we have records
    for record in records:
        assert isinstance(record, dict)  # Each record should be a dictionary


def test_corrupt_file():
    # Test with a file containing corrupt JSON
    generate_corrupt_json()
    records = list(iter_records(LLM_FILE))
    assert len(records) > 0  # Ensure we have records
    for record in records:
        assert isinstance(record, dict)  # Each record should be a dictionary


def make_big_file(path, n=1_000_000):
    with path.open("w") as f:
        for i in range(n):
            model = "model-a" if i % 2 else "model-b"
            f.write(json.dumps({"model": model, "tokens": 10}) + "\n")


def test_streams_1m_lines_under_50mb(tmp_path):
    big = tmp_path / "big.jsonl"  # tmp_path = temporary folder pytest gives you
    make_big_file(big)  # built BEFORE measuring, so it doesn't count

    tracemalloc.start()  # start measuring Python memory
    count = sum(1 for _ in iter_records(big))
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert count == 1_000_000
    assert peak < 50 * 1024 * 1024
