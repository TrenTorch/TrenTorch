"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

brier_score = load_solution(__file__).brier_score


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_coin_flip_scores_a_quarter():
    assert np.isclose(brier_score(np.array([1, 0]), np.array([0.5, 0.5])), 0.25)


def test_perfect_probabilities_score_zero():
    assert np.isclose(brier_score(np.array([1, 0, 1]), np.array([1.0, 0.0, 1.0])), 0.0)


def test_confident_and_wrong_scores_one():
    assert np.isclose(brier_score(np.array([1, 0]), np.array([0.0, 1.0])), 1.0)


def test_worked_example():
    # squared errors: (0.8 - 1)^2 = 0.04, (0.3 - 0)^2 = 0.09, mean 0.065
    assert np.isclose(brier_score(np.array([1, 0]), np.array([0.8, 0.3])), 0.065)


def test_score_is_bounded_between_zero_and_one():
    rng = np.random.default_rng(9)
    y = rng.integers(0, 2, size=40)
    p = rng.random(40)
    score = brier_score(y, p)
    assert 0.0 <= score <= 1.0


def test_one_extreme_miss_moves_the_score_by_a_bounded_amount():
    y = np.array([1, 1, 1, 1, 0])
    good = np.array([0.9, 0.9, 0.9, 0.9, 0.1])
    bad = good.copy()
    bad[0] = 0.0
    assert brier_score(y, bad) - brier_score(y, good) <= 1.0 / len(y)


def test_better_probabilities_lower_the_score():
    y = np.array([1, 0, 1])
    assert brier_score(y, np.array([0.9, 0.1, 0.9])) < brier_score(y, np.array([0.6, 0.4, 0.6]))


def test_flipping_labels_and_probabilities_keeps_the_score():
    y = np.array([1, 0, 1, 0])
    p = np.array([0.3, 0.6, 0.8, 0.2])
    assert np.isclose(brier_score(y, p), brier_score(1 - y, 1 - p))


def test_probabilities_outside_unit_interval_raise():
    assert _raises_value_error(brier_score, np.array([1, 0]), np.array([1.5, 0.2]))


def test_labels_must_be_binary():
    assert _raises_value_error(brier_score, np.array([3, 0]), np.array([0.5, 0.2]))


def test_length_mismatch_raises():
    assert _raises_value_error(brier_score, np.array([1, 0]), np.array([0.5]))


def test_empty_input_raises():
    assert _raises_value_error(brier_score, np.array([]), np.array([]))


def test_does_not_modify_inputs():
    y = np.array([1, 0])
    p = np.array([0.7, 0.1])
    before_y, before_p = y.copy(), p.copy()
    brier_score(y, p)
    assert np.array_equal(y, before_y)
    assert np.array_equal(p, before_p)
