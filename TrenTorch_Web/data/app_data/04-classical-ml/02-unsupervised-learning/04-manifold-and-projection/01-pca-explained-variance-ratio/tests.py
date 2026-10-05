"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

explained_variance_ratio = load_solution(__file__).explained_variance_ratio


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_ratios_sum_to_one():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(50, 4))
    assert np.isclose(explained_variance_ratio(X).sum(), 1.0)


def test_ratios_are_sorted_descending():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(40, 5)) * np.array([5.0, 3.0, 2.0, 1.0, 0.5])
    r = explained_variance_ratio(X)
    assert np.all(np.diff(r) <= 1e-12)


def test_all_variance_on_one_axis_gives_ratio_one_then_zero():
    t = np.linspace(-1, 1, 20)
    X = np.column_stack([t, np.zeros(20)])
    r = explained_variance_ratio(X)
    assert np.isclose(r[0], 1.0)
    assert np.isclose(r[1], 0.0)


def test_equal_variance_axes_split_evenly():
    X = np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]])
    r = explained_variance_ratio(X)
    assert np.allclose(r, [0.5, 0.5])


def test_adding_a_constant_column_shift_does_not_change_ratios():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(30, 3))
    assert np.allclose(explained_variance_ratio(X), explained_variance_ratio(X + 100.0))


def test_scaling_all_data_does_not_change_ratios():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(30, 3))
    assert np.allclose(explained_variance_ratio(X), explained_variance_ratio(7.0 * X))


def test_number_of_ratios_is_min_of_rows_and_columns():
    X = np.random.default_rng(4).normal(size=(3, 6))
    assert explained_variance_ratio(X).shape == (3,)


def test_constant_data_gives_all_zeros():
    X = np.ones((5, 3))
    assert np.allclose(explained_variance_ratio(X), 0.0)


def test_single_row_raises():
    assert _raises_value_error(explained_variance_ratio, np.array([[1.0, 2.0]]))


def test_ratios_are_nonnegative():
    X = np.random.default_rng(5).normal(size=(25, 4))
    assert np.all(explained_variance_ratio(X) >= 0)


def test_does_not_modify_the_data():
    X = np.random.default_rng(6).normal(size=(10, 3))
    before = X.copy()
    explained_variance_ratio(X)
    assert np.array_equal(X, before)
