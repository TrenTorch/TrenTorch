"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/10-instructgpt/01-pairwise-reward-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-reward-pairwise-loss")
pairwise_reward_loss = _module.pairwise_reward_loss


import numpy as np


def test_1_equal_rewards_give_log_two():
    assert abs(float(pairwise_reward_loss(1.0, 1.0)) - np.log(2.0)) < 1e-12


def test_2_large_margin_in_favor_gives_near_zero_loss():
    assert float(pairwise_reward_loss(20.0, 0.0)) < 1e-8


def test_3_wrong_order_gives_large_loss():
    assert float(pairwise_reward_loss(0.0, 20.0)) > 19.0


def test_4_matches_negative_log_sigmoid_by_hand():
    margin = 0.7
    expected = -np.log(1 / (1 + np.exp(-margin)))
    assert abs(float(pairwise_reward_loss(margin, 0.0)) - expected) < 1e-12


def test_5_works_on_arrays():
    out = pairwise_reward_loss(np.array([0.0, 1.0]), np.array([0.0, 0.0]))
    np.testing.assert_allclose(out, [np.log(2.0), np.log1p(np.exp(-1.0))])


def test_6_does_not_mutate_inputs():
    r = np.array([1.0])
    pairwise_reward_loss(r, np.array([0.0]))
    np.testing.assert_array_equal(r, [1.0])

