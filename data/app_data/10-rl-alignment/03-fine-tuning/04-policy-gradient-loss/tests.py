"""
pytest data/app_data/10-rl-alignment/03-fine-tuning/04-policy-gradient-loss/tests.py
"""

import sys
from pathlib import Path

import math

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/03-fine-tuning/{Path(__file__).resolve().parent.name}")
discounted_returns = _module.discounted_returns
policy_gradient_loss = _module.policy_gradient_loss


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_discounted_returns_matches_hand_computation():
    rewards = np.array([1.0, 1.0, 1.0])
    dones = np.array([0.0, 0.0, 1.0])
    returns = discounted_returns(rewards, gamma=0.5, dones=dones)
    # G[2] = 1. G[1] = 1 + 0.5*1 = 1.5. G[0] = 1 + 0.5*1.5 = 1.75
    assert np.allclose(returns, [1.75, 1.5, 1.0])


def test_02_policy_gradient_loss_matches_hand_computation():
    log_probs = np.array([-1.0, -2.0])
    advantages = np.array([2.0, -1.0])
    loss = policy_gradient_loss(log_probs, advantages)
    assert math.isclose(loss, -np.mean([-2.0, 2.0]))


# --- General-case coverage --------------------------------------------


def test_03_episode_boundaries_reset_the_return_accumulation():
    rewards = np.array([10.0, 1.0, 1.0])
    dones = np.array([1.0, 0.0, 1.0])  # first episode is just one step
    returns = discounted_returns(rewards, gamma=0.9, dones=dones)
    assert math.isclose(returns[0], 10.0)  # not influenced by later rewards at all


def test_04_undiscounted_case_is_a_plain_reverse_cumulative_sum():
    rewards = np.array([1.0, 2.0, 3.0])
    dones = np.zeros(3)
    returns = discounted_returns(rewards, gamma=1.0, dones=dones)
    assert np.allclose(returns, [6.0, 5.0, 3.0])


def test_05_higher_gamma_gives_higher_early_returns_for_positive_rewards():
    rewards = np.array([0.0, 0.0, 10.0])
    dones = np.zeros(3)
    low_gamma = discounted_returns(rewards, gamma=0.1, dones=dones)
    high_gamma = discounted_returns(rewards, gamma=0.99, dones=dones)
    assert high_gamma[0] > low_gamma[0]


# --- Parameter handling -------------------------------------------------


def test_06_loss_decreases_as_log_prob_grows_for_a_positive_advantage_action():
    # The loss's SIGN at a point isn't the interesting property -- what
    # matters is the gradient direction: for a positive advantage,
    # increasing log_prob (making the action more likely) must LOWER
    # the loss, which is exactly what makes this a correct ascent
    # direction on the expected return.
    advantages = np.array([5.0])
    loss_low_logprob = policy_gradient_loss(np.array([-2.0]), advantages)
    loss_high_logprob = policy_gradient_loss(np.array([-0.5]), advantages)
    assert loss_high_logprob < loss_low_logprob


def test_07_zero_advantage_gives_zero_loss():
    log_probs = np.array([-1.0, -2.0, -3.0])
    assert math.isclose(policy_gradient_loss(log_probs, np.zeros(3)), 0.0)


# --- Edge cases ---------------------------------------------------------


def test_08_single_step_episode():
    returns = discounted_returns(np.array([5.0]), gamma=0.9, dones=np.array([1.0]))
    assert math.isclose(returns[0], 5.0)


def test_09_zero_gamma_return_equals_immediate_reward_only():
    rewards = np.array([1.0, 2.0, 3.0])
    dones = np.zeros(3)
    returns = discounted_returns(rewards, gamma=0.0, dones=dones)
    assert np.allclose(returns, rewards)


# --- Independent correctness oracle -----------------------------------


def test_10_multi_episode_returns_never_leak_across_boundaries():
    # Directly targets a mutant that ignores `dones` entirely (treating
    # the whole rewards array as one continuous episode): two
    # back-to-back episodes with very different reward structures
    # should give the SAME early return as if each were computed
    # independently, since a real done flag must reset the accumulator.
    episode_1 = discounted_returns(np.array([1.0, 1.0]), gamma=0.9, dones=np.array([0.0, 1.0]))
    combined = discounted_returns(
        np.array([1.0, 1.0, 100.0, 100.0]), gamma=0.9, dones=np.array([0.0, 1.0, 0.0, 1.0])
    )
    assert np.allclose(episode_1, combined[:2])
