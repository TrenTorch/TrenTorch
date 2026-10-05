"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/04-show-attend-tell/02-doubly-stochastic/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sat-doubly-stochastic")
doubly_stochastic_penalty = _module.doubly_stochastic_penalty


import numpy as np


def test_1_each_location_attended_exactly_once_gives_zero():
    alpha = np.eye(3)
    assert abs(doubly_stochastic_penalty(alpha)) < 1e-12


def test_2_ignored_location_is_penalized():
    alpha = np.array([[1.0, 0.0], [1.0, 0.0]])
    assert abs(doubly_stochastic_penalty(alpha) - 2.0) < 1e-12


def test_3_penalty_is_nonnegative():
    rng = np.random.default_rng(0)
    alpha = rng.random((4, 3))
    assert doubly_stochastic_penalty(alpha) >= 0


def test_4_returns_a_python_float():
    assert isinstance(doubly_stochastic_penalty(np.eye(2)), float)


def test_5_over_attended_location_is_penalized():
    alpha = np.array([[1.0], [1.0]])
    assert abs(doubly_stochastic_penalty(alpha) - 1.0) < 1e-12


def test_6_does_not_mutate_alpha():
    alpha = np.eye(2)
    doubly_stochastic_penalty(alpha)
    np.testing.assert_array_equal(alpha, np.eye(2))

