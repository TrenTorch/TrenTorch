"""
pytest data/app_data/06-inference/02-kv-cache-and-decoding/03-kv-cache-memory-footprint/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

kv_cache_memory_footprint = load_solution(
    f"06-inference/02-kv-cache-and-decoding/{Path(__file__).resolve().parent.name}"
).kv_cache_memory_footprint


def test_mha_example():
    result = kv_cache_memory_footprint(32, 32, 128, 2048, 1, 2, "mha")
    assert result["kv_heads_used"] == 32
    assert result["total_bytes"] == 1073741824
    assert result["total_mib"] == 1024.0


def test_gqa_shrinks_cache_proportionally_to_kv_heads():
    mha = kv_cache_memory_footprint(32, 32, 128, 2048, 1, 2, "mha")
    gqa = kv_cache_memory_footprint(32, 32, 128, 2048, 1, 2, "gqa", n_kv_heads=8)
    assert gqa["total_bytes"] == mha["total_bytes"] // 4  # 32/8 = 4x reduction


def test_mqa_uses_exactly_one_kv_head():
    result = kv_cache_memory_footprint(24, 16, 64, 4096, 8, 2, "mqa")
    assert result["kv_heads_used"] == 1
    assert result["total_bytes"] == 201326592


def test_int8_cache_matches_manual_calc():
    result = kv_cache_memory_footprint(40, 40, 128, 8192, 4, 1, "gqa", n_kv_heads=8)
    assert result["total_bytes"] == 2684354560
    assert result["total_mib"] == 2560.0


def test_variant_case_insensitive():
    a = kv_cache_memory_footprint(2, 4, 8, 16, 1, 2, "MHA")
    b = kv_cache_memory_footprint(2, 4, 8, 16, 1, 2, "mha")
    assert a == b


def test_gqa_without_n_kv_heads_raises():
    import pytest

    with pytest.raises(ValueError):
        kv_cache_memory_footprint(2, 4, 8, 16, 1, 2, "gqa")


def test_unknown_variant_raises():
    import pytest

    with pytest.raises(ValueError):
        kv_cache_memory_footprint(2, 4, 8, 16, 1, 2, "banana")
