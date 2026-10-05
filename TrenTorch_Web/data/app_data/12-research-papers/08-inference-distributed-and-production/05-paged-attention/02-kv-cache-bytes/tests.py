"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/05-paged-attention/02-kv-cache-bytes/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vllm-kv-cache-bytes")
kv_cache_bytes = _module.kv_cache_bytes


def test_1_hand_value():
    assert kv_cache_bytes(2, 4, 8, 16, 2) == 4096


def test_2_scales_linearly_with_sequence_length():
    assert kv_cache_bytes(1, 1, 1, 10, 1) == 10 * kv_cache_bytes(1, 1, 1, 1, 1)


def test_3_keys_and_values_are_both_stored():
    assert kv_cache_bytes(1, 1, 1, 1, 1) == 2


def test_4_zero_sequence_costs_nothing():
    assert kv_cache_bytes(4, 4, 4, 0, 2) == 0


def test_5_returns_an_integer():
    assert isinstance(kv_cache_bytes(1, 2, 3, 4, 2), int)


def test_6_doubling_layers_doubles_the_cache():
    assert kv_cache_bytes(4, 2, 2, 2, 2) == 2 * kv_cache_bytes(2, 2, 2, 2, 2)

