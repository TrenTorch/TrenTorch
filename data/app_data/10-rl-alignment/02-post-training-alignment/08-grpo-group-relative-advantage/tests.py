"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/08-grpo-group-relative-advantage/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
grpo_group_relative_advantage = _module.grpo_group_relative_advantage
grpo_policy_gradient_loss = _module.grpo_policy_gradient_loss


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_advantage_has_zero_mean():
    adv = grpo_group_relative_advantage(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
    assert np.isclose(adv.mean(), 0.0, atol=1e-8)


def test_02_advantage_has_unit_ish_standard_deviation():
    adv = grpo_group_relative_advantage(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
    assert np.isclose(adv.std(), 1.0, atol=1e-4)


# --- General-case coverage --------------------------------------------


def test_03_best_reward_gets_the_highest_advantage():
    rewards = np.array([3.0, 9.0, 1.0, 5.0])
    adv = grpo_group_relative_advantage(rewards)
    assert np.argmax(adv) == np.argmax(rewards)


def test_04_worst_reward_gets_the_lowest_advantage():
    rewards = np.array([3.0, 9.0, 1.0, 5.0])
    adv = grpo_group_relative_advantage(rewards)
    assert np.argmin(adv) == np.argmin(rewards)


def test_05_relative_ordering_is_preserved():
    rewards = np.array([2.0, 8.0, 5.0, 1.0])
    adv = grpo_group_relative_advantage(rewards)
    assert np.all(np.argsort(rewards) == np.argsort(adv))


# --- Parameter handling -------------------------------------------------


def test_06_all_equal_rewards_give_near_zero_advantage():
    rewards = np.full(6, 4.0)
    adv = grpo_group_relative_advantage(rewards, eps=1e-8)
    assert np.allclose(adv, 0.0, atol=1e-4)


def test_07_policy_gradient_loss_matches_hand_computation():
    log_probs = np.array([-1.0, -2.0])
    advantages = np.array([2.0, -1.0])
    loss = grpo_policy_gradient_loss(log_probs, advantages)
    # -mean([-1*2, -2*-1]) = -mean([-2, 2]) = -0
    assert np.isclose(loss, 0.0)


# --- Edge cases ---------------------------------------------------------


def test_08_larger_eps_changes_result_only_for_near_constant_rewards():
    rewards = np.full(4, 5.0)
    adv_small_eps = grpo_group_relative_advantage(rewards, eps=1e-8)
    adv_large_eps = grpo_group_relative_advantage(rewards, eps=1.0)
    assert np.allclose(adv_small_eps, 0.0)
    assert np.allclose(adv_large_eps, 0.0)  # numerator is exactly zero either way


def test_09_single_sample_group_has_zero_advantage():
    adv = grpo_group_relative_advantage(np.array([7.0]))
    assert np.isclose(adv[0], 0.0)


# --- Independent correctness oracle -----------------------------------


def test_10_advantage_scales_correctly_with_reward_spread():
    # Directly targets a mutant that forgets to divide by std (using
    # only mean-centering): a group with a WIDE reward spread and a
    # group with a NARROW spread but the same relative ranking should
    # produce advantages of similar MAGNITUDE (normalized), not
    # wildly different raw magnitudes.
    narrow = grpo_group_relative_advantage(np.array([4.9, 5.0, 5.1]))
    wide = grpo_group_relative_advantage(np.array([0.0, 50.0, 100.0]))
    assert np.isclose(narrow.std(), wide.std(), atol=1e-3)
