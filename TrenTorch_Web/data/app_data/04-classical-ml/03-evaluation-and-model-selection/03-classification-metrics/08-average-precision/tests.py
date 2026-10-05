"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

average_precision = load_solution(__file__).average_precision


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_perfect_ranking_scores_one():
    y = np.array([1, 1, 0, 0])
    s = np.array([0.9, 0.8, 0.3, 0.1])
    assert np.isclose(average_precision(y, s), 1.0)


def test_worked_example_with_alternating_labels():
    y = np.array([1, 0, 1, 0])
    s = np.array([0.9, 0.8, 0.7, 0.1])
    # precision at recalls 0.5, 1.0 is 1.0 and 2/3, so AP = 0.5 + 0.5 * 2/3
    assert np.isclose(average_precision(y, s), 5.0 / 6.0)


def test_worst_ranking_scores_one_third_for_single_last_positive():
    y = np.array([0, 0, 1])
    s = np.array([0.9, 0.8, 0.1])
    assert np.isclose(average_precision(y, s), 1.0 / 3.0)


def test_tied_scores_are_evaluated_together():
    y = np.array([1, 0])
    s = np.array([0.5, 0.5])
    # one threshold: precision 0.5 at recall 1.0
    assert np.isclose(average_precision(y, s), 0.5)


def test_all_positive_labels_score_one():
    assert np.isclose(average_precision(np.array([1, 1]), np.array([0.2, 0.9])), 1.0)


def test_invariant_to_monotone_transform_of_scores():
    y = np.array([1, 0, 1, 0, 0])
    s = np.array([0.9, 0.7, 0.6, 0.4, 0.2])
    assert np.isclose(average_precision(y, s), average_precision(y, 10 * s + 3))


def test_score_is_between_zero_and_one():
    rng = np.random.default_rng(10)
    y = rng.integers(0, 2, size=50)
    y[0] = 1
    s = rng.random(50)
    assert 0.0 <= average_precision(y, s) <= 1.0


def test_better_ranking_scores_higher():
    y = np.array([1, 0, 0, 1])
    good = np.array([0.9, 0.2, 0.1, 0.8])
    bad = np.array([0.1, 0.9, 0.8, 0.2])
    assert average_precision(y, good) > average_precision(y, bad)


def test_no_positives_raises():
    assert _raises_value_error(average_precision, np.array([0, 0]), np.array([0.1, 0.9]))


def test_length_mismatch_raises():
    assert _raises_value_error(average_precision, np.array([1, 0]), np.array([0.5]))


def test_does_not_modify_inputs():
    y = np.array([1, 0, 1])
    s = np.array([0.3, 0.8, 0.5])
    before_y, before_s = y.copy(), s.copy()
    average_precision(y, s)
    assert np.array_equal(y, before_y)
    assert np.array_equal(s, before_s)


def test_returns_a_python_float():
    assert isinstance(average_precision(np.array([1, 0]), np.array([0.7, 0.2])), float)
