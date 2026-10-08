"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/06-ppo/01-probability-ratio/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ppo-probability-ratio")
probability_ratio = _module.probability_ratio


import math

import numpy as np


def test_1_equal_log_probabilities_give_ratio_one():
    assert abs(probability_ratio(-1.0, -1.0) - 1.0) < 1e-12


def test_2_doubling_the_probability_gives_two():
    assert abs(probability_ratio(math.log(0.6), math.log(0.3)) - 2.0) < 1e-12


def test_3_ratio_is_always_positive():
    assert np.all(probability_ratio(np.array([-5.0, 0.0]), np.array([0.0, -3.0])) > 0)


def test_4_works_on_arrays():
    np.testing.assert_allclose(probability_ratio(np.zeros(2), np.zeros(2)), [1.0, 1.0])


def test_5_returns_a_float_for_scalars():
    assert isinstance(probability_ratio(0.0, 0.0), float)


def test_6_does_not_mutate_inputs():
    lp = np.array([0.5])
    probability_ratio(lp, np.array([0.0]))
    np.testing.assert_array_equal(lp, [0.5])

