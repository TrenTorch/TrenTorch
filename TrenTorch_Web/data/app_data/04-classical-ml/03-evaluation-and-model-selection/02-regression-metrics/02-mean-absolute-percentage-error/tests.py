"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
mean_absolute_percentage_error = _module.mean_absolute_percentage_error


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_perfect_prediction_scores_zero():
    y = np.array([1.0, 2.0, 5.0])
    assert np.isclose(mean_absolute_percentage_error(y, y), 0.0)


def test_known_value_over_forecast_by_one_hundred_percent():
    # |1 - 2| / 1 = 1.0, so MAPE = 100
    assert np.isclose(mean_absolute_percentage_error(np.array([1.0]), np.array([2.0])), 100.0)


def test_known_value_under_forecast_by_half():
    # |10 - 5| / 10 = 0.5, so MAPE = 50
    assert np.isclose(mean_absolute_percentage_error(np.array([10.0]), np.array([5.0])), 50.0)


def test_average_of_two_percentages():
    # (|100 - 90| / 100 + |50 - 55| / 50) / 2 = (0.1 + 0.1) / 2 = 0.1, so MAPE = 10
    result = mean_absolute_percentage_error(np.array([100.0, 50.0]), np.array([90.0, 55.0]))
    assert np.isclose(result, 10.0)


def test_over_and_under_forecasts_of_the_same_size_score_the_same_for_one_true_value():
    over = mean_absolute_percentage_error(np.array([10.0]), np.array([12.0]))
    under = mean_absolute_percentage_error(np.array([10.0]), np.array([8.0]))
    assert np.isclose(over, 20.0)
    assert np.isclose(under, 20.0)


def test_the_same_absolute_error_costs_more_on_a_smaller_true_value():
    small_target = mean_absolute_percentage_error(np.array([2.0]), np.array([3.0]))
    large_target = mean_absolute_percentage_error(np.array([200.0]), np.array([201.0]))
    assert small_target > large_target


def test_scaling_both_inputs_leaves_the_score_unchanged():
    y = np.array([2.0, 4.0, 8.0])
    y_pred = np.array([2.5, 3.0, 9.0])
    assert np.isclose(
        mean_absolute_percentage_error(y, y_pred),
        mean_absolute_percentage_error(10.0 * y, 10.0 * y_pred),
    )


def test_negative_true_values_use_their_absolute_value():
    # |-10 - -8| / |-10| = 0.2, so MAPE = 20
    assert np.isclose(mean_absolute_percentage_error(np.array([-10.0]), np.array([-8.0])), 20.0)


def test_zero_in_the_true_values_raises():
    assert _raises_value_error(mean_absolute_percentage_error, np.array([0.0, 1.0]), np.array([1.0, 1.0]))


def test_shape_mismatch_raises():
    assert _raises_value_error(mean_absolute_percentage_error, np.array([1.0, 2.0]), np.array([1.0]))


def test_result_is_never_negative():
    rng = np.random.default_rng(0)
    y = rng.uniform(1.0, 5.0, size=20)
    assert mean_absolute_percentage_error(y, rng.uniform(1.0, 5.0, size=20)) >= 0.0


def test_matches_an_explicit_loop():
    y = np.array([3.0, 7.0, 2.0])
    p = np.array([2.0, 8.0, 2.5])
    expected = 100.0 * np.mean([abs(a - b) / abs(a) for a, b in zip(y, p)])
    assert np.isclose(mean_absolute_percentage_error(y, p), expected)


def test_accepts_python_lists():
    assert np.isclose(mean_absolute_percentage_error([10.0, 20.0], [10.0, 20.0]), 0.0)


def test_does_not_modify_its_inputs():
    y = np.array([4.0, 5.0])
    p = np.array([3.0, 6.0])
    y_before, p_before = y.copy(), p.copy()
    mean_absolute_percentage_error(y, p)
    assert np.array_equal(y, y_before)
    assert np.array_equal(p, p_before)
