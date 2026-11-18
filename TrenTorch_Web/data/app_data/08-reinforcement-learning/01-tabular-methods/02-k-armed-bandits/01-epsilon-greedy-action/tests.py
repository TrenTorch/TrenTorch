"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

epsilon_greedy_action = load_solution(__file__).epsilon_greedy_action


Q = np.array([0.1, 0.9, 0.5, 0.2])


def test_epsilon_zero_always_exploits():
    rng = np.random.default_rng(0)
    assert all(epsilon_greedy_action(Q, 0.0, rng) == 1 for _ in range(200))


def test_epsilon_one_explores_every_arm():
    rng = np.random.default_rng(0)
    seen = {epsilon_greedy_action(Q, 1.0, rng) for _ in range(400)}
    assert seen == {0, 1, 2, 3}


def test_greedy_arm_frequency_matches_theory():
    rng = np.random.default_rng(1)
    n = 20000
    hits = sum(epsilon_greedy_action(Q, 0.2, rng) == 1 for _ in range(n))
    # P(best) = 1 - eps + eps / k = 0.8 + 0.05
    assert abs(hits / n - 0.85) < 0.015


def test_exploit_ties_go_to_lowest_index():
    rng = np.random.default_rng(0)
    assert epsilon_greedy_action(np.array([0.5, 0.5, 0.1]), 0.0, rng) == 0


def test_same_seed_same_choices():
    a = [epsilon_greedy_action(Q, 0.5, r) for r in [np.random.default_rng(7)] * 10]
    b = [epsilon_greedy_action(Q, 0.5, r) for r in [np.random.default_rng(7)] * 10]
    assert a == b


def test_returns_python_int():
    assert isinstance(epsilon_greedy_action(Q, 0.3, np.random.default_rng(0)), int)
