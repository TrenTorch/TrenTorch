"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
fractional_split_gain = _module.fractional_split_gain


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_perfect_split_without_missing_values_gains_one_bit():
    gain, p_left = fractional_split_gain([1.0, 2.0, 8.0, 9.0], [0, 0, 1, 1], 5.0)
    assert np.isclose(gain, 1.0)
    assert np.isclose(p_left, 0.5)


def test_missing_row_scales_gain_by_known_fraction():
    gain, _ = fractional_split_gain([1.0, 2.0, 8.0, 9.0, np.nan], [0, 0, 1, 1, 0], 5.0)
    assert np.isclose(gain, 0.8)


def test_missing_rows_do_not_count_toward_routing_weight():
    _, p_left = fractional_split_gain([1.0, 2.0, 8.0, 9.0, np.nan], [0, 0, 1, 1, 0], 5.0)
    assert np.isclose(p_left, 0.5)


def test_uninformative_split_has_zero_gain():
    gain, _ = fractional_split_gain([1.0, 2.0, 3.0, 4.0], [0, 1, 0, 1], 2.5)
    assert np.isclose(gain, 0.0)


def test_threshold_below_all_values_sends_everything_right_with_zero_gain():
    gain, p_left = fractional_split_gain([1.0, 2.0, 8.0, 9.0], [0, 0, 1, 1], 0.0)
    assert np.isclose(gain, 0.0)
    assert p_left == 0.0


def test_pure_parent_has_zero_gain():
    gain, _ = fractional_split_gain([1.0, 2.0, 8.0, 9.0], [1, 1, 1, 1], 5.0)
    assert np.isclose(gain, 0.0)


def test_threshold_is_inclusive_on_the_left():
    # x = 5 equals the threshold, so both rows go left and the right branch is empty.
    gain, p_left = fractional_split_gain([1.0, 5.0], [0, 1], 5.0)
    assert np.isclose(gain, 0.0)
    assert p_left == 1.0


def test_gain_does_not_depend_on_label_names():
    base, _ = fractional_split_gain([1.0, 2.0, 8.0, 9.0], [0, 0, 1, 1], 5.0)
    renamed, _ = fractional_split_gain([1.0, 2.0, 8.0, 9.0], [5, 5, 7, 7], 5.0)
    assert np.isclose(base, renamed)


def test_gain_is_never_negative_on_random_data():
    rng = np.random.default_rng(0)
    for _ in range(20):
        x = rng.normal(size=30)
        x[rng.random(30) < 0.2] = np.nan
        y = rng.integers(0, 3, size=30)
        gain, _ = fractional_split_gain(x, y, 0.0)
        assert gain >= -1e-12


def test_gain_is_at_most_the_known_fraction():
    x = np.array([1.0, 2.0, 8.0, 9.0, np.nan, np.nan])
    y = np.array([0, 0, 1, 1, 0, 1])
    gain, _ = fractional_split_gain(x, y, 5.0)
    assert gain <= 4 / 6 + 1e-12


def test_all_missing_values_raise():
    assert _raises_value_error(fractional_split_gain, [np.nan, np.nan], [0, 1], 0.0)


def test_length_mismatch_raises():
    assert _raises_value_error(fractional_split_gain, [1.0, 2.0], [0, 1, 1], 0.0)


def test_inputs_are_not_modified():
    x = np.array([1.0, 2.0, np.nan, 9.0])
    y = np.array([0, 0, 1, 1])
    x0, y0 = x.copy(), y.copy()
    fractional_split_gain(x, y, 5.0)
    assert np.array_equal(x, x0, equal_nan=True) and np.array_equal(y, y0)
