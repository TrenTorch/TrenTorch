"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
running_total = _module.running_total
cumulative_max = _module.cumulative_max
consecutive_differences = _module.consecutive_differences
percent_change = _module.percent_change
moving_average = _module.moving_average

A = np.array([3, 1, 4, 1, 5])


def test_running_total():
    np.testing.assert_array_equal(running_total(A), [3, 4, 8, 9, 14])


def test_running_total_last_element_is_the_sum():
    a = np.random.default_rng(0).integers(0, 9, size=30)
    assert running_total(a)[-1] == a.sum()


def test_cumulative_max():
    np.testing.assert_array_equal(cumulative_max(A), [3, 3, 4, 4, 5])


def test_cumulative_max_never_decreases():
    a = np.random.default_rng(1).normal(size=50)
    assert np.all(np.diff(cumulative_max(a)) >= 0)


def test_consecutive_differences():
    np.testing.assert_array_equal(consecutive_differences(A), [-2, 3, -3, 4])


def test_differences_are_one_shorter_and_the_running_total_rebuilds_the_series():
    d = consecutive_differences(A)
    assert len(d) == len(A) - 1
    np.testing.assert_array_equal(A[0] + np.cumsum(d), A[1:])


def test_percent_change():
    out = percent_change(np.array([100.0, 110.0, 99.0]))
    np.testing.assert_allclose(out, [0.1, -0.1])


def test_percent_change_is_nan_after_a_zero():
    out = percent_change(np.array([0.0, 5.0, 10.0]))
    assert np.isnan(out[0])
    np.testing.assert_allclose(out[1], 1.0)


def test_percent_change_is_a_float_array_for_integer_input():
    out = percent_change(np.array([2, 3, 6]))
    assert out.dtype.kind == "f"
    np.testing.assert_allclose(out, [0.5, 1.0])


def test_moving_average_known_values():
    np.testing.assert_allclose(moving_average(np.array([1, 2, 3, 4, 5]), 3), [2.0, 3.0, 4.0])


def test_moving_average_length_and_window_one():
    a = np.arange(10.0)
    assert len(moving_average(a, 4)) == 7
    np.testing.assert_allclose(moving_average(a, 1), a)


def test_moving_average_window_equal_to_the_length_is_the_mean():
    a = np.array([2.0, 4.0, 9.0])
    np.testing.assert_allclose(moving_average(a, 3), [a.mean()])


def test_moving_average_matches_a_brute_force_loop():
    a = np.random.default_rng(2).normal(size=60)
    w = 7
    expected = [a[i : i + w].mean() for i in range(len(a) - w + 1)]
    np.testing.assert_allclose(moving_average(a, w), expected)
