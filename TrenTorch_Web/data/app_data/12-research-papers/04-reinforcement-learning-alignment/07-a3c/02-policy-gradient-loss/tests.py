"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/07-a3c/02-policy-gradient-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-a3c-policy-gradient-loss")
policy_gradient_loss = _module.policy_gradient_loss


import math

import numpy as np


def test_1_matches_a_hand_value():
    assert abs(policy_gradient_loss(np.array([math.log(0.5)]), np.array([2.0])) - (-math.log(0.5) * 2)) < 1e-12


def test_2_zero_advantage_gives_zero_loss():
    assert policy_gradient_loss(np.array([-1.0, -2.0]), np.zeros(2)) == 0.0


def test_3_positive_advantage_rewards_higher_log_probability():
    lower_prob = policy_gradient_loss(np.array([-1.0]), np.array([1.0]))
    higher_prob = policy_gradient_loss(np.array([-0.5]), np.array([1.0]))
    assert higher_prob < lower_prob


def test_4_returns_a_python_float():
    assert isinstance(policy_gradient_loss(np.zeros(2), np.ones(2)), float)


def test_5_averages_over_the_batch():
    out = policy_gradient_loss(np.array([-1.0, -3.0]), np.array([1.0, 1.0]))
    assert abs(out - 2.0) < 1e-12


def test_6_does_not_mutate_inputs():
    lp = np.array([-1.0])
    policy_gradient_loss(lp, np.array([1.0]))
    np.testing.assert_array_equal(lp, [-1.0])

