"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/10-instructgpt/02-kl-penalized-reward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-kl-penalized-reward")
kl_penalized_reward = _module.kl_penalized_reward


def test_1_identical_policy_and_reference_leave_reward_unchanged():
    assert kl_penalized_reward(2.5, -3.0, -3.0, 0.1) == 2.5


def test_2_zero_beta_ignores_the_penalty():
    assert kl_penalized_reward(1.0, -1.0, -5.0, 0.0) == 1.0


def test_3_policy_drifting_above_reference_is_penalized():
    assert kl_penalized_reward(1.0, -1.0, -3.0, 0.5) == 1.0 - 0.5 * 2.0


def test_4_policy_below_reference_is_rewarded():
    assert kl_penalized_reward(1.0, -4.0, -2.0, 0.5) == 1.0 + 0.5 * 2.0


def test_5_larger_beta_gives_a_lower_reward():
    assert kl_penalized_reward(1.0, -1.0, -2.0, 1.0) < kl_penalized_reward(1.0, -1.0, -2.0, 0.1)


def test_6_matches_a_hand_computed_case():
    assert abs(kl_penalized_reward(3.0, -2.0, -4.0, 0.25) - 2.5) < 1e-12

