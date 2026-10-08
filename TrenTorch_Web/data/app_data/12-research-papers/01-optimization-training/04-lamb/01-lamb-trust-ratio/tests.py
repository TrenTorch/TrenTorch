"""
pytest data/app_data/12-research-papers/01-optimization-and-training/04-lamb/01-lamb-trust-ratio/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lamb-trust-ratio")
lamb_trust_ratio = _module.lamb_trust_ratio


import numpy as np


def test_1_hand_value():
    assert abs(lamb_trust_ratio(np.array([3.0, 4.0]), np.array([0.6, 0.8])) - 5.0) < 1e-12


def test_2_equal_norms_give_one():
    assert abs(lamb_trust_ratio(np.array([1.0, 0.0]), np.array([0.0, 1.0])) - 1.0) < 1e-12


def test_3_scaling_r_inverts_the_ratio():
    a = lamb_trust_ratio(np.array([3.0, 4.0]), np.array([0.6, 0.8]))
    b = lamb_trust_ratio(np.array([3.0, 4.0]), np.array([1.2, 1.6]))
    assert abs(a - 2 * b) < 1e-12


def test_4_returns_a_python_float():
    assert isinstance(lamb_trust_ratio(np.ones(2), np.ones(2)), float)


def test_5_larger_weights_give_larger_ratio():
    r = np.array([1.0, 0.0])
    assert lamb_trust_ratio(np.array([5.0, 0.0]), r) > lamb_trust_ratio(np.array([1.0, 0.0]), r)


def test_6_does_not_mutate_inputs():
    w = np.array([3.0, 4.0])
    lamb_trust_ratio(w, np.array([0.6, 0.8]))
    np.testing.assert_array_equal(w, [3.0, 4.0])

