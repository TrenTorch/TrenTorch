"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/08-multi-query-attention/03-saving-ratio/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mqa-saving-ratio")
saving_ratio = _module.saving_ratio


def test_1_multi_query_saves_by_the_head_count():
    assert saving_ratio(32, 1) == 32.0


def test_2_standard_multi_head_saves_nothing():
    assert saving_ratio(8, 8) == 1.0


def test_3_grouped_query_middle_ground():
    assert saving_ratio(8, 2) == 4.0


def test_4_returns_a_float():
    assert isinstance(saving_ratio(4, 2), float)


def test_5_ratio_is_at_least_one_when_kv_heads_divide_query_heads():
    assert saving_ratio(12, 3) >= 1.0


def test_6_halving_kv_heads_doubles_the_saving():
    assert saving_ratio(16, 2) == 2 * saving_ratio(16, 4)

