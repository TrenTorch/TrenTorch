"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
reward_model_loss = _module.reward_model_loss
preference_accuracy = _module.preference_accuracy


def test_1_no_opinion_is_ln2():
    assert np.isclose(reward_model_loss(np.array([1.0, 2.0]), np.array([1.0, 2.0])), np.log(2))


def test_2_hand_computed():
    loss = reward_model_loss(np.array([2.0]), np.array([0.0]))
    assert np.isclose(loss, -np.log(1 / (1 + np.exp(-2.0))))


def test_3_only_the_difference_matters():
    a, b = np.array([0.3, 1.2, -0.5]), np.array([0.1, 1.5, -0.9])
    assert np.isclose(reward_model_loss(a, b), reward_model_loss(a + 7.0, b + 7.0))


def test_4_stable_for_huge_differences():
    assert np.isclose(reward_model_loss(np.array([1000.0]), np.array([0.0])), 0.0, atol=1e-12)
    assert np.isclose(reward_model_loss(np.array([0.0]), np.array([1000.0])), 1000.0)


def test_5_wrong_ranking_costs_more_than_right_ranking():
    right = reward_model_loss(np.array([1.0]), np.array([0.0]))
    wrong = reward_model_loss(np.array([0.0]), np.array([1.0]))
    assert wrong > right


def test_6_accuracy_counts_strict_wins_only():
    acc = preference_accuracy(np.array([1.0, 0.5, 2.0, 0.0]), np.array([0.0, 0.5, 3.0, -1.0]))
    assert np.isclose(acc, 0.5)


def test_7_matches_naive_formula_and_does_not_mutate():
    rng = np.random.RandomState(0)
    a, b = rng.randn(20), rng.randn(20)
    sa, sb = a.copy(), b.copy()
    naive = np.mean(-np.log(1 / (1 + np.exp(-(a - b)))))
    assert np.isclose(reward_model_loss(a, b), naive)
    assert np.array_equal(a, sa) and np.array_equal(b, sb)
