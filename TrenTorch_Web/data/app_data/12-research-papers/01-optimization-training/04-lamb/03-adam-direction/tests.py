"""
pytest data/app_data/12-research-papers/01-optimization-and-training/04-lamb/03-adam-direction/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lamb-adam-direction")
lamb_direction = _module.lamb_direction


import numpy as np


def test_1_hand_value():
    np.testing.assert_allclose(lamb_direction(np.array([1.0]), np.array([1.0]), np.array([2.0]), 0.5, 0.0), [2.0])


def test_2_zero_decay_is_pure_adam_direction():
    np.testing.assert_allclose(lamb_direction(np.array([2.0]), np.array([4.0]), np.array([9.0]), 0.0, 0.0), [1.0])


def test_3_eps_keeps_denominator_positive():
    out = lamb_direction(np.array([1.0]), np.array([0.0]), np.array([0.0]), 0.0, 1e-3)
    assert np.isfinite(out[0]) and out[0] > 0


def test_4_keeps_the_shape():
    assert lamb_direction(np.ones((2, 2)), np.ones((2, 2)), np.ones((2, 2)), 0.1, 1e-8).shape == (2, 2)


def test_5_decay_term_scales_with_weights():
    a = lamb_direction(np.zeros(1), np.ones(1), np.array([1.0]), 0.5, 0.0)
    b = lamb_direction(np.zeros(1), np.ones(1), np.array([2.0]), 0.5, 0.0)
    np.testing.assert_allclose(b, 2 * a)


def test_6_does_not_mutate_inputs():
    w = np.array([2.0])
    lamb_direction(np.array([1.0]), np.array([1.0]), w, 0.5, 0.0)
    np.testing.assert_array_equal(w, [2.0])

