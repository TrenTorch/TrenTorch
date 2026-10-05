"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
corrected_resampled_t = _module.corrected_resampled_t


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_hand_example_gives_exactly_three():
    # mean 2, var 1, correction 1/3 + 1/9 = 4/9, so t = 2 / sqrt(4/9) = 3.
    assert np.isclose(corrected_resampled_t(np.array([1.0, 2.0, 3.0]), 9, 1), 3.0)


def test_correction_makes_statistic_smaller_than_uncorrected():
    d = np.array([1.0, 2.0, 3.0])
    uncorrected = d.mean() / (d.std(ddof=1) / np.sqrt(3))
    assert corrected_resampled_t(d, 9, 1) < uncorrected


def test_larger_test_fraction_shrinks_statistic():
    d = np.array([1.0, 2.0, 3.0])
    small_test = corrected_resampled_t(d, 90, 10)
    large_test = corrected_resampled_t(d, 50, 50)
    assert abs(large_test) < abs(small_test)


def test_sign_follows_mean_difference():
    d = np.array([-1.0, -2.0, -3.0])
    assert corrected_resampled_t(d, 9, 1) < 0


def test_scaling_differences_leaves_statistic_unchanged():
    # Mean and standard deviation both scale by 4, so the ratio is unchanged.
    d = np.array([0.5, 1.5, 2.5, 1.0])
    assert np.isclose(corrected_resampled_t(4 * d, 9, 1), corrected_resampled_t(d, 9, 1))


def test_shift_changes_statistic():
    d = np.array([1.0, 2.0, 3.0])
    assert corrected_resampled_t(d + 1, 9, 1) > corrected_resampled_t(d, 9, 1)


def test_more_repeats_with_same_pattern_increase_statistic():
    d = np.array([1.0, 2.0, 3.0])
    assert corrected_resampled_t(np.tile(d, 3), 9, 1) > corrected_resampled_t(d, 9, 1)


def test_zero_mean_gives_zero_statistic():
    d = np.array([-1.0, 0.0, 1.0])
    assert np.isclose(corrected_resampled_t(d, 9, 1), 0.0)


def test_single_repeat_raises():
    assert _raises_value_error(corrected_resampled_t, np.array([1.0]), 9, 1)


def test_zero_variance_raises():
    assert _raises_value_error(corrected_resampled_t, np.array([2.0, 2.0, 2.0]), 9, 1)


def test_nonpositive_train_size_raises():
    assert _raises_value_error(corrected_resampled_t, np.array([1.0, 2.0]), 0, 1)


def test_nonpositive_test_size_raises():
    assert _raises_value_error(corrected_resampled_t, np.array([1.0, 2.0]), 9, -1)


def test_inputs_are_not_modified():
    d = np.array([1.0, 2.0, 3.0])
    d0 = d.copy()
    corrected_resampled_t(d, 9, 1)
    assert np.array_equal(d, d0)
