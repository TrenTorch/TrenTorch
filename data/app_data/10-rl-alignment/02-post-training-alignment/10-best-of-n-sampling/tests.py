"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/10-best-of-n-sampling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
best_of_n_select = _module.best_of_n_select
expected_best_of_n_reward = _module.expected_best_of_n_reward


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_selects_the_highest_reward_response():
    responses = ["a", "b", "c"]
    rewards = [1.0, 9.0, 4.0]
    best_response, best_reward = best_of_n_select(responses, rewards)
    assert best_response == "b"
    assert best_reward == 9.0


def test_02_expected_reward_increases_with_larger_n():
    pool = np.linspace(1.0, 10.0, 20)
    small_n = expected_best_of_n_reward(pool, n=1, num_trials=3000, seed=0)
    large_n = expected_best_of_n_reward(pool, n=16, num_trials=3000, seed=0)
    assert large_n > small_n


# --- General-case coverage --------------------------------------------


def test_03_expected_reward_never_exceeds_pool_maximum():
    pool = np.array([1.0, 5.0, 3.0, 8.0])
    for n in (1, 4, 32):
        result = expected_best_of_n_reward(pool, n, num_trials=1000, seed=1)
        assert result <= pool.max() + 1e-9


def test_04_expected_reward_at_n_equals_one_approximates_pool_mean():
    pool = np.array([2.0, 4.0, 6.0, 8.0])
    result = expected_best_of_n_reward(pool, n=1, num_trials=20000, seed=2)
    assert np.isclose(result, pool.mean(), atol=0.2)


def test_05_diminishing_returns_as_n_grows():
    pool = np.linspace(0.0, 10.0, 50)
    gains = []
    prev = expected_best_of_n_reward(pool, n=1, num_trials=4000, seed=3)
    for n in (2, 4, 8, 16):
        current = expected_best_of_n_reward(pool, n=n, num_trials=4000, seed=3)
        gains.append(current - prev)
        prev = current
    assert gains[0] > gains[-1]  # the first doubling helps more than the last


# --- Parameter handling -------------------------------------------------


def test_06_best_of_n_select_returns_matching_index_pair():
    responses = ["x", "y", "z", "w"]
    rewards = [0.5, 0.5, 0.9, 0.1]
    response, reward = best_of_n_select(responses, rewards)
    assert response == "z"
    assert reward == 0.9


def test_07_deterministic_given_the_same_seed():
    pool = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    a = expected_best_of_n_reward(pool, n=3, num_trials=100, seed=42)
    b = expected_best_of_n_reward(pool, n=3, num_trials=100, seed=42)
    assert a == b


# --- Edge cases ---------------------------------------------------------


def test_08_single_response_is_always_selected():
    response, reward = best_of_n_select(["only"], [3.0])
    assert response == "only"
    assert reward == 3.0


def test_09_uniform_reward_pool_gives_constant_expected_reward():
    pool = np.full(10, 7.0)
    result = expected_best_of_n_reward(pool, n=5, num_trials=100, seed=0)
    assert np.isclose(result, 7.0)


# --- Independent correctness oracle -----------------------------------


def test_10_matches_a_manual_monte_carlo_reimplementation():
    # Directly targets a mutant that takes the MEAN of the sample
    # instead of the MAX (best-of-n's entire point is to pick the
    # best, not average over the sampled group).
    pool = np.array([1.0, 2.0, 3.0, 10.0])
    result = expected_best_of_n_reward(pool, n=4, num_trials=500, seed=7)

    rng = np.random.default_rng(7)
    manual = np.mean([rng.choice(pool, size=4, replace=True).max() for _ in range(500)])
    assert np.isclose(result, manual)
