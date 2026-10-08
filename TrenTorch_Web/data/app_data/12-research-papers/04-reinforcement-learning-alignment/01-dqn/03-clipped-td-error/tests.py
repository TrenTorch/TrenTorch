"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/01-dqn/03-clipped-td-error/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dqn-clipped-td-error")
clipped_td_error = _module.clipped_td_error


import numpy as np


def test_1_small_errors_are_unchanged():
    np.testing.assert_allclose(clipped_td_error(np.array([0.2, -0.5]), 1.0), [0.2, -0.5])


def test_2_large_positive_error_is_clipped_to_c():
    np.testing.assert_allclose(clipped_td_error(np.array([10.0]), 1.0), [1.0])


def test_3_large_negative_error_is_clipped_to_minus_c():
    np.testing.assert_allclose(clipped_td_error(np.array([-7.0]), 2.0), [-2.0])


def test_4_is_symmetric():
    rng = np.random.default_rng(0)
    x = rng.normal(size=20) * 5
    np.testing.assert_allclose(clipped_td_error(x, 1.0), -clipped_td_error(-x, 1.0))


def test_5_keeps_the_shape():
    assert clipped_td_error(np.ones((2, 3)) * 9, 1.0).shape == (2, 3)


def test_6_does_not_mutate_the_input():
    x = np.array([5.0])
    clipped_td_error(x, 1.0)
    np.testing.assert_array_equal(x, [5.0])

