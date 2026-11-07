"""
pytest data/app_data/06-inference/02-kv-cache-and-decoding/05-prefix-cache-lookup-reuse/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"06-inference/02-kv-cache-and-decoding/{Path(__file__).resolve().parent.name}")
prefix_cache_lookup = _module.prefix_cache_lookup


# The store is always built by prefix_cache_lookup itself (the same function
# under test), so any consistent choice of hash passes -- the tests never
# depend on one particular hash function or helper name.
def _store_after(tokens, block_size=2, store=()):
    return prefix_cache_lookup(list(tokens), block_size=block_size, cache_store=list(store))[
        "updated_cache_store"
    ]


def test_no_match_empty_store():
    result = prefix_cache_lookup([9, 9, 9, 9], block_size=2, cache_store=[])
    assert result["blocks_reused"] == 0
    assert result["reused_tokens"] == 0
    assert result["tokens_to_prefill"] == [9, 9, 9, 9]


def test_full_match_reuses_everything():
    existing = _store_after([1, 2, 3, 4])
    result = prefix_cache_lookup([1, 2, 3, 4], block_size=2, cache_store=existing)
    assert result["blocks_reused"] == 2
    assert result["reused_tokens"] == 4
    assert result["tokens_to_prefill"] == []


def test_partial_prefix_match():
    existing = _store_after([1, 2, 3, 4])
    result = prefix_cache_lookup([1, 2, 3, 4, 5, 6], block_size=2, cache_store=existing)
    assert result["blocks_reused"] == 2
    assert result["reused_tokens"] == 4
    assert result["tokens_to_prefill"] == [5, 6]


def test_trailing_partial_block_never_counts_as_reused():
    existing = _store_after([1, 2])
    result = prefix_cache_lookup([1, 2, 3], block_size=2, cache_store=existing)
    assert result["blocks_reused"] == 1
    assert result["reused_tokens"] == 2
    assert result["tokens_to_prefill"] == [3]


def test_divergent_second_block_does_not_produce_false_hit():
    existing = _store_after([1, 2, 3, 4])  # chain via [1,2] then [3,4]
    result = prefix_cache_lookup([1, 2, 9, 9], block_size=2, cache_store=existing)
    assert result["blocks_reused"] == 1  # only the first block ([1,2]) matches
    assert result["tokens_to_prefill"] == [9, 9]


def test_same_block_under_a_different_prefix_is_not_a_hit():
    # [1,2] and [3,4] are both in the store, but each was reached through a
    # different chain than this request's. Plain block dedup would reuse both;
    # a chained prefix match reuses neither.
    existing = _store_after([3, 4, 1, 2])
    result = prefix_cache_lookup([1, 2, 3, 4], block_size=2, cache_store=existing)
    assert result["blocks_reused"] == 0
    assert result["tokens_to_prefill"] == [1, 2, 3, 4]


def test_updated_store_adds_one_entry_per_full_block():
    assert len(_store_after([5, 6, 7, 8])) == 2
    assert len(_store_after([1, 2, 3])) == 1  # the trailing partial block is not stored


def test_updated_store_keeps_earlier_entries_without_duplicates():
    first = _store_after([1, 2])
    second = _store_after([9, 9], store=first)
    assert set(first) <= set(second)
    assert len(second) == 2
    assert len(_store_after([1, 2], store=first)) == 1
