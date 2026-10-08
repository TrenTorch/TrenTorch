"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/08-multi-query-attention/01-kv-elems/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mqa-kv-elems")
kv_cache_elems = _module.kv_cache_elems


def test_1_multi_query_has_one_kv_head():
    assert kv_cache_elems(1, 1, 4, 8) == 64


def test_2_more_kv_heads_cost_more():
    assert kv_cache_elems(1, 8, 4, 8) > kv_cache_elems(1, 1, 4, 8)


def test_3_keys_and_values_both_counted():
    assert kv_cache_elems(1, 1, 1, 1) == 2


def test_4_zero_sequence_costs_nothing():
    assert kv_cache_elems(2, 2, 0, 4) == 0


def test_5_returns_an_integer():
    assert isinstance(kv_cache_elems(1, 2, 3, 4), int)


def test_6_linear_in_layers():
    assert kv_cache_elems(4, 1, 2, 2) == 2 * kv_cache_elems(2, 1, 2, 2)

