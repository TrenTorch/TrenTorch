"""
pytest data/app_data/06-inference/02-kv-cache-and-decoding/05-prefix-cache-lookup-reuse/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"06-inference/02-kv-cache-and-decoding/{Path(__file__).resolve().parent.name}")
prefix_cache_lookup = _module.prefix_cache_lookup
_chained_hashes = _module._chained_hashes


def test_no_match_empty_store():
    result = prefix_cache_lookup([9, 9, 9, 9], block_size=2, cache_store=[])
    assert result["blocks_reused"] == 0
    assert result["reused_tokens"] == 0
    assert result["tokens_to_prefill"] == [9, 9, 9, 9]


def test_full_match_reuses_everything():
    existing = _chained_hashes([1, 2, 3, 4], block_size=2)
    result = prefix_cache_lookup([1, 2, 3, 4], block_size=2, cache_store=existing)
    assert result["blocks_reused"] == 2
    assert result["reused_tokens"] == 4
    assert result["tokens_to_prefill"] == []


def test_partial_prefix_match():
    existing = _chained_hashes([1, 2, 3, 4], block_size=2)
    result = prefix_cache_lookup([1, 2, 3, 4, 5, 6], block_size=2, cache_store=existing)
    assert result["blocks_reused"] == 2
    assert result["reused_tokens"] == 4
    assert result["tokens_to_prefill"] == [5, 6]


def test_trailing_partial_block_never_counts_as_reused():
    existing = _chained_hashes([1, 2], block_size=2)
    result = prefix_cache_lookup([1, 2, 3], block_size=2, cache_store=existing)
    assert result["blocks_reused"] == 1
    assert result["reused_tokens"] == 2
    assert result["tokens_to_prefill"] == [3]


def test_divergent_second_block_does_not_produce_false_hit():
    # A later block that happens to look identical to some unrelated
    # cached block must NOT count as a hit if the chain leading to it
    # differs -- otherwise this would be plain block dedup, not prefix caching.
    existing = _chained_hashes([1, 2, 3, 4], block_size=2)  # chain via [1,2] then [3,4]
    # New request diverges after the first block: [1,2] then [9,9], but a
    # totally different earlier chain happens to also produce [9,9] as its
    # SECOND block somewhere else in the store -- must still not match here
    # since the chained hash incorporates the full prefix.
    result = prefix_cache_lookup([1, 2, 9, 9], block_size=2, cache_store=existing)
    assert result["blocks_reused"] == 1  # only the first block ([1,2]) matches
    assert result["tokens_to_prefill"] == [9, 9]


def test_updated_store_includes_new_hashes():
    result = prefix_cache_lookup([5, 6, 7, 8], block_size=2, cache_store=[])
    new_hashes = _chained_hashes([5, 6, 7, 8], block_size=2)
    assert set(result["updated_cache_store"]) == {str(h) for h in new_hashes}
