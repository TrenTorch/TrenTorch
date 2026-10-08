"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/06-ppo/03-ppo-total-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ppo-total-loss")
ppo_total_loss = _module.ppo_total_loss


def test_1_zero_weights_give_negated_policy_objective():
    assert abs(ppo_total_loss(1.5, 9.0, 3.0, 0.0, 0.0) - (-1.5)) < 1e-12


def test_2_hand_computed_combination():
    # -(1 - 0.5 * 2 + 0.1 * 3) = -(1 - 1 + 0.3) = -0.3
    assert abs(ppo_total_loss(1.0, 2.0, 3.0, 0.5, 0.1) - (-0.3)) < 1e-12


def test_3_larger_value_error_increases_the_loss():
    assert ppo_total_loss(0.0, 5.0, 0.0, 1.0, 0.0) > ppo_total_loss(0.0, 1.0, 0.0, 1.0, 0.0)


def test_4_entropy_bonus_lowers_the_loss():
    assert ppo_total_loss(0.0, 0.0, 2.0, 0.0, 1.0) < ppo_total_loss(0.0, 0.0, 0.0, 0.0, 1.0)


def test_5_returns_a_float():
    assert isinstance(ppo_total_loss(1.0, 1.0, 1.0, 1.0, 1.0), float)


def test_6_is_linear_in_the_value_loss():
    a = ppo_total_loss(0.0, 1.0, 0.0, 2.0, 0.0)
    b = ppo_total_loss(0.0, 2.0, 0.0, 2.0, 0.0)
    assert abs((b - a) - 2.0) < 1e-12

