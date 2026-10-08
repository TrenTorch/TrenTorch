"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/02-double-dqn/01-double-target/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-double-dqn-target")
double_q_target = _module.double_q_target


import numpy as np


def test_1_action_is_picked_by_online_and_valued_by_target():
    out = double_q_target(1.0, 0.5, 0, np.array([0.0, 5.0]), np.array([9.0, 1.0]))
    assert abs(out - (1.0 + 0.5 * 1.0)) < 1e-12


def test_2_terminal_returns_reward():
    assert double_q_target(2.0, 0.9, 1, np.array([1.0]), np.array([100.0])) == 2.0


def test_3_ties_pick_the_first_action():
    out = double_q_target(0.0, 1.0, 0, np.array([3.0, 3.0]), np.array([7.0, 2.0]))
    assert abs(out - 7.0) < 1e-12


def test_4_differs_from_plain_max_when_networks_disagree():
    online = np.array([0.0, 5.0])
    target = np.array([9.0, 1.0])
    plain = 1.0 * 9.0
    assert double_q_target(0.0, 1.0, 0, online, target) != plain


def test_5_returns_a_float():
    assert isinstance(double_q_target(1.0, 0.9, 0, np.array([1.0]), np.array([2.0])), float)


def test_6_does_not_mutate_inputs():
    online = np.array([1.0, 2.0])
    double_q_target(0.0, 1.0, 0, online, np.array([0.0, 0.0]))
    np.testing.assert_array_equal(online, [1.0, 2.0])

