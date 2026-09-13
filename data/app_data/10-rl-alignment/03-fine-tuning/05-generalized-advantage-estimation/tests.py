"""
pytest data/app_data/10-rl-alignment/03-fine-tuning/05-generalized-advantage-estimation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/03-fine-tuning/{Path(__file__).resolve().parent.name}")
td_residuals = _module.td_residuals
generalized_advantage_estimation = _module.generalized_advantage_estimation


def _random_episode(seed, T=6):
    rng = np.random.default_rng(seed)
    rewards = rng.normal(size=T)
    values = rng.normal(size=T)
    next_values = np.roll(values, -1)
    next_values[-1] = 0.0
    dones = np.zeros(T)
    dones[-1] = 1.0
    return rewards, values, next_values, dones


def _bruteforce_gae(rewards, values, next_values, dones, gamma, lam):
    deltas = td_residuals(rewards, values, next_values, dones, gamma)
    T = len(rewards)
    advantages = np.zeros(T)
    for t in range(T):
        total = 0.0
        coeff = 1.0
        for k in range(T - t):
            total += coeff * deltas[t + k]
            if dones[t + k]:
                break
            coeff *= gamma * lam
        advantages[t] = total
    return advantages


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_td_residual_matches_hand_computation():
    rewards = np.array([1.0])
    values = np.array([0.5])
    next_values = np.array([2.0])
    dones = np.array([0.0])
    delta = td_residuals(rewards, values, next_values, dones, gamma=0.9)
    # 1.0 + 0.9*2.0 - 0.5 = 2.3
    assert np.allclose(delta, [2.3])


def test_02_gae_matches_brute_force_summation():
    rewards, values, next_values, dones = _random_episode(0)
    gamma, lam = 0.99, 0.95
    fast = generalized_advantage_estimation(rewards, values, next_values, dones, gamma, lam)
    slow = _bruteforce_gae(rewards, values, next_values, dones, gamma, lam)
    assert np.allclose(fast, slow)


# --- General-case coverage --------------------------------------------


def test_03_lambda_zero_reduces_to_plain_td_residual():
    rewards, values, next_values, dones = _random_episode(1)
    gamma = 0.9
    gae = generalized_advantage_estimation(rewards, values, next_values, dones, gamma, lam=0.0)
    deltas = td_residuals(rewards, values, next_values, dones, gamma)
    assert np.allclose(gae, deltas)


def test_04_lambda_one_reduces_to_monte_carlo_advantage():
    rewards, values, next_values, dones = _random_episode(2)
    gamma = 0.99
    gae = generalized_advantage_estimation(rewards, values, next_values, dones, gamma, lam=1.0)

    T = len(rewards)
    returns = np.zeros(T)
    running = 0.0
    for t in reversed(range(T)):
        running = rewards[t] + gamma * (1 - dones[t]) * running
        returns[t] = running
    mc_advantage = returns - values
    assert np.allclose(gae, mc_advantage)


def test_05_done_flag_stops_bootstrapping_from_the_next_episode():
    rewards = np.array([1.0, 1.0])
    values = np.array([0.0, 0.0])
    next_values = np.array([0.0, 1000.0])  # a huge (wrong) bootstrap if done were ignored
    dones = np.array([1.0, 0.0])
    delta = td_residuals(rewards, values, next_values, dones, gamma=0.9)
    assert np.isclose(delta[0], 1.0)  # 1.0 + 0.9*0*(1-1) - 0.0


# --- Parameter handling -------------------------------------------------


def test_06_gae_shape_matches_input_length():
    rewards, values, next_values, dones = _random_episode(3, T=10)
    gae = generalized_advantage_estimation(rewards, values, next_values, dones, gamma=0.99, lam=0.95)
    assert gae.shape == (10,)


def test_07_intermediate_lambda_lies_between_the_two_extremes_in_magnitude():
    rewards, values, next_values, dones = _random_episode(4)
    gamma = 0.99
    gae_lam0 = generalized_advantage_estimation(rewards, values, next_values, dones, gamma, lam=0.0)
    gae_lam1 = generalized_advantage_estimation(rewards, values, next_values, dones, gamma, lam=1.0)
    gae_mid = generalized_advantage_estimation(rewards, values, next_values, dones, gamma, lam=0.5)
    assert not np.allclose(gae_mid, gae_lam0)
    assert not np.allclose(gae_mid, gae_lam1)


# --- Edge cases ---------------------------------------------------------


def test_08_single_step_episode():
    rewards = np.array([3.0])
    values = np.array([1.0])
    next_values = np.array([0.0])
    dones = np.array([1.0])
    gae = generalized_advantage_estimation(rewards, values, next_values, dones, gamma=0.9, lam=0.95)
    assert np.isclose(gae[0], 2.0)  # just the TD residual, no future to look ahead to


def test_09_zero_rewards_and_perfect_value_predictions_give_zero_advantage():
    T = 5
    values = np.array([1.0, 1.0, 1.0, 1.0, 0.0])
    next_values = np.roll(values, -1)
    next_values[-1] = 0.0
    rewards = values - 0.9 * next_values  # engineered so delta is always 0
    dones = np.zeros(T)
    dones[-1] = 1.0
    gae = generalized_advantage_estimation(rewards, values, next_values, dones, gamma=0.9, lam=0.95)
    assert np.allclose(gae, 0.0, atol=1e-9)


# --- Independent correctness oracle -----------------------------------


def test_10_multi_episode_gae_never_leaks_across_episode_boundaries():
    # Directly targets a mutant that ignores `dones` in the recursive
    # backward pass (letting `running` carry over into an earlier,
    # unrelated episode): two independent single-episode computations
    # concatenated must match one combined multi-episode computation.
    r1, v1, nv1, d1 = _random_episode(5, T=4)
    r2, v2, nv2, d2 = _random_episode(6, T=4)
    gamma, lam = 0.95, 0.9

    gae1 = generalized_advantage_estimation(r1, v1, nv1, d1, gamma, lam)
    gae2 = generalized_advantage_estimation(r2, v2, nv2, d2, gamma, lam)

    combined_rewards = np.concatenate([r1, r2])
    combined_values = np.concatenate([v1, v2])
    combined_next_values = np.concatenate([nv1, nv2])
    combined_dones = np.concatenate([d1, d2])
    combined_gae = generalized_advantage_estimation(
        combined_rewards, combined_values, combined_next_values, combined_dones, gamma, lam
    )
    assert np.allclose(combined_gae, np.concatenate([gae1, gae2]))
