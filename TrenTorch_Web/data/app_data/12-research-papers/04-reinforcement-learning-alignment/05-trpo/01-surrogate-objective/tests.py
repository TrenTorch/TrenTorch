"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/05-trpo/01-surrogate-objective/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-trpo-surrogate")
surrogate_objective = _module.surrogate_objective


import numpy as np


def test_1_unit_ratio_gives_the_mean_advantage():
    assert abs(surrogate_objective(np.ones(3), np.array([1.0, 2.0, 3.0])) - 2.0) < 1e-12


def test_2_matches_a_hand_value():
    assert abs(surrogate_objective(np.array([2.0, 0.5]), np.array([1.0, 1.0])) - 1.25) < 1e-12


def test_3_zero_advantages_give_zero():
    assert surrogate_objective(np.array([3.0]), np.array([0.0])) == 0.0


def test_4_returns_a_python_float():
    assert isinstance(surrogate_objective(np.ones(2), np.ones(2)), float)


def test_5_negative_advantage_lowers_the_objective():
    assert surrogate_objective(np.ones(1), np.array([-1.0])) < 0


def test_6_does_not_mutate_inputs():
    r = np.array([2.0])
    surrogate_objective(r, np.array([1.0]))
    np.testing.assert_array_equal(r, [2.0])

