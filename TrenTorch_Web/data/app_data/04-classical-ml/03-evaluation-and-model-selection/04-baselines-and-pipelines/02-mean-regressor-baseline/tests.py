"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
mean_regressor_baseline = _module.mean_regressor_baseline


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_predicts_the_training_mean():
    y = np.array([1.0, 2.0, 6.0])
    assert np.allclose(mean_regressor_baseline(y, 3), np.full(3, 3.0))


def test_output_length_is_n_samples():
    assert mean_regressor_baseline(np.array([1.0, 2.0]), 9).shape == (9,)


def test_zero_samples_returns_an_empty_array():
    assert mean_regressor_baseline(np.array([1.0]), 0).shape == (0,)


def test_integer_targets_give_a_float_output():
    result = mean_regressor_baseline(np.array([1, 2]), 2)
    assert result.dtype == np.float64
    assert np.allclose(result, 1.5)


def test_mean_is_not_the_median():
    y = np.array([0.0, 0.0, 10.0])
    assert np.allclose(mean_regressor_baseline(y, 1), np.array([10.0 / 3.0]))


def test_all_predictions_are_identical():
    result = mean_regressor_baseline(np.array([3.0, -1.0, 4.0]), 5)
    assert np.all(result == result[0])


def test_the_baseline_has_zero_r_squared_on_its_own_training_data():
    y = np.array([2.0, 4.0, 9.0, 1.0])
    predictions = mean_regressor_baseline(y, len(y))
    ss_res = np.sum((y - predictions) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    assert np.isclose(1.0 - ss_res / ss_tot, 0.0)


def test_negative_targets_are_averaged_correctly():
    assert np.allclose(mean_regressor_baseline(np.array([-2.0, -4.0]), 1), np.array([-3.0]))


def test_empty_training_targets_raise():
    assert _raises_value_error(mean_regressor_baseline, np.array([]), 2)


def test_result_does_not_depend_on_the_order_of_targets():
    a = mean_regressor_baseline(np.array([1.0, 5.0, 2.0]), 2)
    b = mean_regressor_baseline(np.array([5.0, 2.0, 1.0]), 2)
    assert np.allclose(a, b)


def test_does_not_modify_its_input():
    y = np.array([1.0, 2.0])
    y_before = y.copy()
    mean_regressor_baseline(y, 3)
    assert np.array_equal(y, y_before)


def test_returns_a_numpy_array():
    assert isinstance(mean_regressor_baseline([1.0, 3.0], 2), np.ndarray)
