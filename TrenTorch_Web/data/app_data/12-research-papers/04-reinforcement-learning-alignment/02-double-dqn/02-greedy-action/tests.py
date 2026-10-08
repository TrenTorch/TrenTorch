"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/02-double-dqn/02-greedy-action/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-double-dqn-greedy-action")
greedy_action = _module.greedy_action


import numpy as np


def test_1_picks_the_largest_value():
    assert greedy_action(np.array([1.0, 3.0, 2.0])) == 1


def test_2_ties_pick_the_first():
    assert greedy_action(np.array([5.0, 5.0])) == 0


def test_3_returns_a_python_int():
    assert isinstance(greedy_action(np.array([0.0, 1.0])), int)


def test_4_single_action():
    assert greedy_action(np.array([-3.0])) == 0


def test_5_negative_values_are_compared_correctly():
    assert greedy_action(np.array([-5.0, -1.0, -3.0])) == 1


def test_6_does_not_mutate_input():
    q = np.array([2.0, 1.0])
    greedy_action(q)
    np.testing.assert_array_equal(q, [2.0, 1.0])

