"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
from math import comb

pass_at_k = _module.pass_at_k
mean_pass_at_k = _module.mean_pass_at_k


def test_1_k_equals_one_is_the_success_rate():
    assert np.isclose(pass_at_k(10, 3, 1), 0.3)


def test_2_hand_computed():
    # n=5, c=2, k=3: 1 - C(3,3)/C(5,3) = 1 - 1/10
    assert np.isclose(pass_at_k(5, 2, 3), 0.9)


def test_3_no_successes_gives_zero_and_all_successes_gives_one():
    assert pass_at_k(10, 0, 5) == 0.0
    assert np.isclose(pass_at_k(10, 10, 5), 1.0)


def test_4_fewer_failures_than_k_is_certain_success():
    assert pass_at_k(5, 3, 3) == 1.0


def test_5_matches_binomial_definition():
    for n, c, k in [(20, 4, 5), (30, 1, 10), (12, 6, 2), (50, 7, 20)]:
        assert np.isclose(pass_at_k(n, c, k), 1 - comb(n - c, k) / comb(n, k))


def test_6_monotone_in_k_and_in_c():
    assert pass_at_k(20, 3, 1) < pass_at_k(20, 3, 5) < pass_at_k(20, 3, 15)
    assert pass_at_k(20, 2, 5) < pass_at_k(20, 6, 5)


def test_7_large_n_does_not_overflow_and_mean_matches_loop():
    assert 0.0 < pass_at_k(5000, 40, 100) < 1.0
    ns, cs = [10, 20, 5], [2, 0, 5]
    assert np.isclose(mean_pass_at_k(ns, cs, 3), np.mean([pass_at_k(n, c, 3) for n, c in zip(ns, cs)]))
