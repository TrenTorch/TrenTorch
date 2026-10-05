"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
paired_t_statistic = _module.paired_t_statistic


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_hand_example_matches_closed_form():
    # d = [1, 2, 3]: mean 2, sd 1, t = 2 / (1 / sqrt(3)) = 2 sqrt(3).
    a = np.array([2.0, 3.0, 4.0])
    b = np.array([1.0, 1.0, 1.0])
    assert np.isclose(paired_t_statistic(a, b), 2 * np.sqrt(3))


def test_swapping_models_flips_the_sign():
    a = np.array([0.8, 0.82, 0.79, 0.85])
    b = np.array([0.78, 0.8, 0.8, 0.8])
    assert np.isclose(paired_t_statistic(a, b), -paired_t_statistic(b, a))


def test_equal_means_give_zero_statistic():
    a = np.array([1.0, 2.0, 3.0, 4.0])
    b = np.array([2.0, 1.0, 4.0, 3.0])
    assert np.isclose(paired_t_statistic(a, b), 0.0)


def test_shifting_both_samples_leaves_statistic_unchanged():
    a = np.array([0.8, 0.82, 0.79, 0.85])
    b = np.array([0.78, 0.8, 0.8, 0.8])
    assert np.isclose(paired_t_statistic(a + 5, b + 5), paired_t_statistic(a, b))


def test_scaling_both_samples_leaves_statistic_unchanged():
    a = np.array([0.8, 0.82, 0.79, 0.85])
    b = np.array([0.78, 0.8, 0.8, 0.8])
    assert np.isclose(paired_t_statistic(3 * a, 3 * b), paired_t_statistic(a, b))


def test_larger_mean_difference_gives_larger_statistic():
    a = np.array([1.0, 1.2, 1.1, 1.3])
    b = np.array([0.9, 1.0, 1.0, 1.1])
    b_far = b - 0.5
    assert abs(paired_t_statistic(a, b_far)) > abs(paired_t_statistic(a, b))


def test_more_folds_with_same_pattern_increase_statistic():
    d = np.array([1.0, 2.0, 3.0])
    small = paired_t_statistic(d, np.zeros(3))
    big = paired_t_statistic(np.tile(d, 4), np.zeros(12))
    assert big > small


def test_statistic_is_a_float():
    assert isinstance(paired_t_statistic(np.array([1.0, 2.0, 4.0]), np.zeros(3)), float)


def test_zero_spread_raises():
    assert _raises_value_error(paired_t_statistic, np.array([2.0, 2.0, 2.0]), np.array([1.0, 1.0, 1.0]))


def test_single_fold_raises():
    assert _raises_value_error(paired_t_statistic, np.array([2.0]), np.array([1.0]))


def test_length_mismatch_raises():
    assert _raises_value_error(paired_t_statistic, np.array([1.0, 2.0]), np.array([1.0]))


def test_two_dimensional_input_raises():
    assert _raises_value_error(paired_t_statistic, np.ones((2, 2)), np.zeros((2, 2)))


def test_inputs_are_not_modified():
    a = np.array([0.8, 0.82, 0.79, 0.85])
    b = np.array([0.78, 0.8, 0.8, 0.8])
    a0, b0 = a.copy(), b.copy()
    paired_t_statistic(a, b)
    assert np.array_equal(a, a0) and np.array_equal(b, b0)
