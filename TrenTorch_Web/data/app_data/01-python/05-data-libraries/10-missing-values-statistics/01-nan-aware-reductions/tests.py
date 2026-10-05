"""
pytest tests.py
"""

import warnings

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
summary_ignoring_nan = _module.summary_ignoring_nan
count_missing = _module.count_missing
fill_with_column_means = _module.fill_with_column_means
rows_without_nan = _module.rows_without_nan
argmax_ignoring_nan = _module.argmax_ignoring_nan

M = np.array([[1.0, np.nan, 3.0], [4.0, 5.0, np.nan], [np.nan, np.nan, 9.0]])


def test_summary_ignores_the_holes():
    out = summary_ignoring_nan(np.array([1.0, np.nan, 3.0, 5.0]))
    assert out["count"] == 3
    assert out["mean"] == 3.0
    assert out["min"] == 1.0 and out["max"] == 5.0
    np.testing.assert_allclose(out["std"], np.std([1.0, 3.0, 5.0]))


def test_summary_of_a_complete_array_matches_the_plain_functions():
    a = np.random.default_rng(0).normal(size=20)
    out = summary_ignoring_nan(a)
    assert out["count"] == 20
    np.testing.assert_allclose([out["mean"], out["std"], out["min"], out["max"]], [a.mean(), a.std(), a.min(), a.max()])


def test_summary_with_no_known_values():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out = summary_ignoring_nan(np.array([np.nan, np.nan]))
    assert out["count"] == 0
    assert all(np.isnan(out[k]) for k in ("mean", "std", "min", "max"))


def test_summary_returns_python_numbers():
    out = summary_ignoring_nan(np.array([1.0, 2.0]))
    assert type(out["count"]) is int and type(out["mean"]) is float


def test_count_missing_per_column_and_per_row():
    np.testing.assert_array_equal(count_missing(M, 0), [1, 2, 1])
    np.testing.assert_array_equal(count_missing(M, 1), [1, 1, 2])


def test_count_missing_of_a_complete_array_is_zero():
    assert count_missing(np.ones((2, 3)), 0).sum() == 0


def test_fill_with_column_means_replaces_the_holes():
    out = fill_with_column_means(M)
    np.testing.assert_allclose(out, [[1.0, 5.0, 3.0], [4.0, 5.0, 6.0], [2.5, 5.0, 9.0]])


def test_fill_keeps_the_known_values_and_the_input():
    before = M.copy()
    out = fill_with_column_means(M)
    known = ~np.isnan(M)
    np.testing.assert_array_equal(out[known], M[known])
    np.testing.assert_array_equal(M, before)


def test_fill_leaves_no_nan_and_an_all_nan_column_becomes_zero():
    m = np.array([[np.nan, 1.0], [np.nan, 3.0]])
    out = fill_with_column_means(m)
    assert not np.isnan(out).any()
    np.testing.assert_allclose(out, [[0.0, 1.0], [0.0, 3.0]])


def test_fill_preserves_each_columns_mean():
    m = np.random.default_rng(1).normal(size=(30, 4))
    holey = m.copy()
    holey[np.random.default_rng(2).random(m.shape) < 0.25] = np.nan
    filled = fill_with_column_means(holey)
    np.testing.assert_allclose(filled.mean(axis=0), np.nanmean(holey, axis=0))


def test_rows_without_nan_keeps_complete_rows_in_order():
    m = np.array([[1.0, 2.0], [np.nan, 3.0], [4.0, 5.0], [6.0, np.nan]])
    np.testing.assert_array_equal(rows_without_nan(m), [[1.0, 2.0], [4.0, 5.0]])


def test_rows_without_nan_can_return_no_rows():
    assert rows_without_nan(np.array([[np.nan, 1.0]])).shape == (0, 2)


def test_argmax_ignoring_nan():
    assert argmax_ignoring_nan(np.array([1.0, np.nan, 7.0, 3.0])) == 2
    assert argmax_ignoring_nan(np.array([np.nan, 2.0])) == 1


def test_argmax_of_all_nan_is_minus_one():
    assert argmax_ignoring_nan(np.array([np.nan, np.nan])) == -1
