"""
pytest data/app_data/12-research-papers/01-optimization-and-training/03-lars/01-trust-ratio/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lars-trust-ratio")
trust_ratio = _module.trust_ratio


import numpy as np


def test_1_hand_value():
    assert abs(trust_ratio(np.array([3.0, 4.0]), np.array([0.6, 0.8]), 0.5, 0.0) - 2.5) < 1e-12


def test_2_decay_enters_the_denominator():
    assert trust_ratio(np.array([3.0, 4.0]), np.array([0.6, 0.8]), 0.5, 0.1) < 2.5


def test_3_larger_weights_give_larger_ratio():
    a = trust_ratio(np.array([1.0, 0.0]), np.array([1.0, 0.0]), 1.0, 0.0)
    b = trust_ratio(np.array([2.0, 0.0]), np.array([1.0, 0.0]), 1.0, 0.0)
    assert b > a


def test_4_scales_linearly_with_eta():
    w, g = np.array([3.0, 4.0]), np.array([0.6, 0.8])
    assert abs(trust_ratio(w, g, 1.0, 0.0) - 2 * trust_ratio(w, g, 0.5, 0.0)) < 1e-12


def test_5_returns_a_float():
    assert isinstance(trust_ratio(np.ones(2), np.ones(2), 0.1, 0.0), float)


def test_6_does_not_mutate_inputs():
    w = np.array([3.0, 4.0])
    trust_ratio(w, np.array([0.6, 0.8]), 0.5, 0.0)
    np.testing.assert_array_equal(w, [3.0, 4.0])

