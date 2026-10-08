"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/01-flashattention/01-softmax-merge/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-flash-online-softmax-merge")
online_softmax_merge = _module.online_softmax_merge


import math


def test_1_merged_sum_equals_direct_sum():
    m1, l1 = 2.0, math.exp(1 - 2) + math.exp(0)
    m2, l2 = 3.0, 1.0
    m, l = online_softmax_merge(m1, l1, m2, l2)
    direct = math.exp(1 - 3) + math.exp(2 - 3) + math.exp(3 - 3)
    assert abs(m - 3.0) < 1e-12 and abs(l - direct) < 1e-12


def test_2_merging_with_an_empty_block_is_identity():
    m, l = online_softmax_merge(1.0, 2.0, float("-inf"), 0.0)
    assert m == 1.0 and abs(l - 2.0) < 1e-12


def test_3_equal_maxes_add_the_sums():
    m, l = online_softmax_merge(0.0, 1.0, 0.0, 2.0)
    assert m == 0.0 and abs(l - 3.0) < 1e-12


def test_4_is_order_independent():
    a = online_softmax_merge(1.0, 2.0, 3.0, 4.0)
    b = online_softmax_merge(3.0, 4.0, 1.0, 2.0)
    assert abs(a[0] - b[0]) < 1e-12 and abs(a[1] - b[1]) < 1e-12


def test_5_returns_a_tuple():
    assert isinstance(online_softmax_merge(0.0, 1.0, 0.0, 1.0), tuple)


def test_6_does_not_mutate_inputs():
    l1 = 2.0
    online_softmax_merge(0.0, l1, 0.0, 1.0)
    assert l1 == 2.0

