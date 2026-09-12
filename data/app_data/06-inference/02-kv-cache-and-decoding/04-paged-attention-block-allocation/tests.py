"""
pytest data/app_data/06-inference/02-kv-cache-and-decoding/04-paged-attention-block-allocation/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

paged_attention_allocate = load_solution(
    f"06-inference/02-kv-cache-and-decoding/{Path(__file__).resolve().parent.name}"
).paged_attention_allocate


def test_single_sequence_spanning_two_blocks():
    result = paged_attention_allocate(
        block_size=4, total_blocks=4,
        events=[("append", "a")] * 5,
    )
    assert len(result["block_tables"]["a"]) == 2
    assert result["free_blocks_remaining"] == 2
    assert result["out_of_memory_at_event"] is None


def test_free_then_reuse():
    result = paged_attention_allocate(
        block_size=2, total_blocks=2,
        events=[("append", "a"), ("append", "a"), ("free", "a"),
                ("append", "b"), ("append", "b")],
    )
    assert "a" not in result["block_tables"]
    assert len(result["block_tables"]["b"]) == 1
    assert result["free_blocks_remaining"] == 1


def test_out_of_memory():
    result = paged_attention_allocate(
        block_size=2, total_blocks=1,
        events=[("append", "a"), ("append", "a"), ("append", "a")],
    )
    assert result["out_of_memory_at_event"] == 2


def test_two_sequences_interleaved():
    result = paged_attention_allocate(
        block_size=3, total_blocks=4,
        events=[("append", "a"), ("append", "b"), ("append", "a"),
                ("append", "b"), ("append", "a"), ("append", "b")],
    )
    assert len(result["block_tables"]["a"]) == 1
    assert len(result["block_tables"]["b"]) == 1
    assert result["free_blocks_remaining"] == 2


def test_exactly_filling_last_block_does_not_over_allocate():
    result = paged_attention_allocate(
        block_size=4, total_blocks=2,
        events=[("append", "a")] * 4,
    )
    assert len(result["block_tables"]["a"]) == 1
    assert result["free_blocks_remaining"] == 1
