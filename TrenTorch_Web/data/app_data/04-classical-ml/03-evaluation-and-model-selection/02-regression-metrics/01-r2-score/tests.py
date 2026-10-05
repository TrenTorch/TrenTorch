"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
r2_score = _module.r2_score


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_perfect_prediction_scores_one():
    y = np.array([1.0, 2.0, 3.0, 4.0])
    assert np.isclose(r2_score(y, y), 1.0)


def test_predicting_the_mean_scores_zero():
    y = np.array([1.0, 2.0, 3.0, 4.0])
    assert np.isclose(r2_score(y, np.full(4, y.mean())), 0.0)


def test_worse_than_the_mean_scores_below_zero():
    y = np.array([1.0, 2.0, 3.0])
    assert r2_score(y, np.array([3.0, 2.0, 1.0])) < 0.0


def test_known_value_on_a_small_example():
    # y mean = 2.5, SS_tot = 5.0; residuals 0.5, -0.5, 0.5, -0.5 give SS_res = 1.0
    y = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 2.5, 2.5, 3.5])
    assert np.isclose(r2_score(y, y_pred), 0.8)


def test_scale_of_the_target_does_not_change_the_score():
    y = np.array([1.0, 3.0, 2.0, 5.0])
    y_pred = np.array([1.2, 2.7, 2.4, 4.6])
    assert np.isclose(r2_score(y, y_pred), r2_score(1000.0 * y, 1000.0 * y_pred))


def test_shift_of_both_inputs_does_not_change_the_score():
    y = np.array([1.0, 3.0, 2.0, 5.0])
    y_pred = np.array([1.2, 2.7, 2.4, 4.6])
    assert np.isclose(r2_score(y, y_pred), r2_score(y + 7.0, y_pred + 7.0))


def test_score_is_at_most_one():
    rng = np.random.default_rng(0)
    y = rng.normal(size=30)
    assert r2_score(y, y + rng.normal(size=30)) <= 1.0


def test_constant_target_raises():
    assert _raises_value_error(r2_score, np.array([2.0, 2.0, 2.0]), np.array([1.0, 2.0, 3.0]))


def test_shape_mismatch_raises():
    assert _raises_value_error(r2_score, np.array([1.0, 2.0]), np.array([1.0, 2.0, 3.0]))


def test_accepts_python_lists():
    assert np.isclose(r2_score([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0)


def test_matches_one_minus_the_ratio_of_sums_of_squares():
    rng = np.random.default_rng(1)
    y = rng.normal(size=25)
    y_pred = rng.normal(size=25)
    expected = 1.0 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2)
    assert np.isclose(r2_score(y, y_pred), expected)


def test_does_not_modify_its_inputs():
    y = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.1, 1.9, 3.2])
    y_before, pred_before = y.copy(), y_pred.copy()
    r2_score(y, y_pred)
    assert np.array_equal(y, y_before)
    assert np.array_equal(y_pred, pred_before)
