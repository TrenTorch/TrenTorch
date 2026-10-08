"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/12-dpo/03-implicit-reward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dpo-implicit-reward")
implicit_reward = _module.implicit_reward


import numpy as np


def test_1_equal_policy_and_reference_give_zero():
    np.testing.assert_allclose(implicit_reward(np.array([-1.0]), np.array([-1.0]), 0.1), [0.0])


def test_2_matches_a_hand_value():
    assert abs(implicit_reward(np.array([-1.0]), np.array([-3.0]), 0.5)[0] - 1.0) < 1e-12


def test_3_scales_with_beta():
    a = implicit_reward(np.array([2.0]), np.array([0.0]), 1.0)
    b = implicit_reward(np.array([2.0]), np.array([0.0]), 4.0)
    np.testing.assert_allclose(b, 4 * a)


def test_4_negative_when_policy_is_less_likely_than_reference():
    assert implicit_reward(np.array([-5.0]), np.array([-1.0]), 1.0)[0] < 0


def test_5_keeps_the_shape():
    assert implicit_reward(np.zeros((2, 3)), np.zeros((2, 3)), 1.0).shape == (2, 3)


def test_6_does_not_mutate_inputs():
    lp = np.array([1.0])
    implicit_reward(lp, np.array([0.0]), 1.0)
    np.testing.assert_array_equal(lp, [1.0])

