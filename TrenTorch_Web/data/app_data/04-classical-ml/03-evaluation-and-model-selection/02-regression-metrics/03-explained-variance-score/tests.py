"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
explained_variance_score = _module.explained_variance_score


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_perfect_prediction_scores_one():
    y = np.array([1.0, 4.0, 2.0, 7.0])
    assert np.isclose(explained_variance_score(y, y), 1.0)


def test_constant_offset_does_not_reduce_the_score():
    y = np.array([1.0, 4.0, 2.0, 7.0])
    assert np.isclose(explained_variance_score(y, y + 3.0), 1.0)


def test_r2_would_penalize_the_same_offset_but_this_score_does_not():
    y = np.array([1.0, 4.0, 2.0, 7.0])
    y_pred = y + 3.0
    residual_mean_squared = np.mean((y - y_pred) ** 2)
    assert residual_mean_squared > 0.0
    assert np.isclose(explained_variance_score(y, y_pred), 1.0)


def test_known_value_with_noise_only_in_the_residuals():
    # residuals are [1, -1, 1, -1] with var 1; y = [0, 2, 0, 2] with var 1
    y = np.array([0.0, 2.0, 0.0, 2.0])
    y_pred = np.array([-1.0, 3.0, -1.0, 3.0])
    assert np.isclose(explained_variance_score(y, y_pred), 0.0)


def test_predicting_a_constant_gives_zero_when_the_target_varies():
    y = np.array([1.0, 2.0, 3.0, 4.0])
    assert np.isclose(explained_variance_score(y, np.full(4, y.mean())), 0.0)


def test_scale_of_the_target_does_not_change_the_score():
    rng = np.random.default_rng(0)
    y = rng.normal(size=20)
    y_pred = y + rng.normal(scale=0.3, size=20)
    assert np.isclose(explained_variance_score(y, y_pred), explained_variance_score(50.0 * y, 50.0 * y_pred))


def test_matches_one_minus_the_ratio_of_population_variances():
    rng = np.random.default_rng(1)
    y = rng.normal(size=25)
    y_pred = rng.normal(size=25)
    expected = 1.0 - np.var(y - y_pred) / np.var(y)
    assert np.isclose(explained_variance_score(y, y_pred), expected)


def test_score_is_at_most_one():
    rng = np.random.default_rng(2)
    y = rng.normal(size=30)
    assert explained_variance_score(y, y + rng.normal(size=30)) <= 1.0


def test_constant_target_raises():
    assert _raises_value_error(explained_variance_score, np.array([5.0, 5.0]), np.array([4.0, 6.0]))


def test_shape_mismatch_raises():
    assert _raises_value_error(explained_variance_score, np.array([1.0, 2.0]), np.array([1.0]))


def test_accepts_python_lists():
    assert np.isclose(explained_variance_score([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0)


def test_more_noise_gives_a_lower_score():
    rng = np.random.default_rng(3)
    y = rng.normal(size=100)
    noise = rng.normal(size=100)
    small = explained_variance_score(y, y + 0.1 * noise)
    large = explained_variance_score(y, y + 1.0 * noise)
    assert small > large


def test_does_not_modify_its_inputs():
    y = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.5, 2.0, 2.0])
    y_before, pred_before = y.copy(), y_pred.copy()
    explained_variance_score(y, y_pred)
    assert np.array_equal(y, y_before)
    assert np.array_equal(y_pred, pred_before)
