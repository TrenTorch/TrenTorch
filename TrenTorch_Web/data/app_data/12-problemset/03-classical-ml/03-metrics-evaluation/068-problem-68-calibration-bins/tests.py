"""Tests with varied inputs. Expected values were checked against independent references (SciPy, scikit-learn, PyTorch or a first-principles formula)."""
import math

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def _close(actual, expected, rtol=1e-6, atol=1e-8):
    if isinstance(expected, dict):
        assert set(actual) == set(expected)
        for k in expected:
            _close(actual[k], expected[k], rtol, atol)
        return
    if isinstance(expected, (tuple, list)) and not (len(expected) and isinstance(expected[0], (int, float, np.number)) and not isinstance(expected, tuple)):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            _close(a, e, rtol, atol)
        return
    a, e = np.asarray(actual), np.asarray(expected)
    assert a.shape == e.shape, (a.shape, e.shape)
    if a.dtype.kind in "biufc" and e.dtype.kind in "biufc":
        np.testing.assert_allclose(a, e, rtol=rtol, atol=atol, equal_nan=True)
    else:
        assert a.tolist() == e.tolist()


def test_01_basic_example():
    _close(solve([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9], 2), [(0.15, 0.0, 2), (0.85, 1.0, 2)])


def test_02_uninformative_model():
    _close(solve([0, 1, 0, 1], [0.1, 0.2, 0.8, 0.9], 2), [(0.15, 0.5, 2), (0.85, 0.5, 2)])


def test_03_bin_edges_p0_and_p1():
    _close(solve([1, 0], [1.0, 0.0], 2), [(0.0, 0.0, 1), (1.0, 1.0, 1)])


def test_04_half_goes_to_upper_bin():
    _close(solve([1, 0, 1], [0.5, 0.2, 0.5], 2), [(0.2, 0.0, 1), (0.5, 1.0, 2)])


def test_05_empty_bins_are_skipped():
    _close(solve([0, 1], [0.1, 0.9], 4), [(0.1, 0.0, 1), (0.9, 1.0, 1)])


def test_06_default_ten_bins():
    _close(solve([0, 0, 1, 1], [0.05, 0.15, 0.95, 0.99]), [(0.05, 0.0, 1), (0.15, 0.0, 1), (0.97, 1.0, 2)])


def test_07_single_bin():
    _close(solve([1, 0, 1, 1], [0.9, 0.4, 0.6, 0.7], 1), [(0.65, 0.75, 4)])


def test_08_three_bins():
    _close(solve([0, 0, 1, 0, 1, 1], [0.1, 0.3, 0.4, 0.5, 0.7, 0.95], 3), [(0.2, 0.0, 2), (0.45, 0.5, 2), (0.825, 1.0, 2)])


def test_09_numpy_input():
    _close(solve(np.array([1, 1, 0, 0]), np.array([0.9, 0.8, 0.3, 0.1]), 2), [(0.2, 0.0, 2), (0.85, 1.0, 2)])


def test_10_empty_input_gives_no_bins():
    _close(solve([], [], 5), [])


def test_11_probability_above_one_raises():
    with pytest.raises(ValueError):
        solve([1, 0], [1.5, 0.2], 2)


def test_12_negative_probability_raises():
    with pytest.raises(ValueError):
        solve([1, 0], [0.5, -0.1], 2)


def test_13_non_binary_label_raises():
    with pytest.raises(ValueError):
        solve([0.5, 1], [0.2, 0.9], 2)


def test_14_length_mismatch_raises():
    with pytest.raises(ValueError):
        solve([1, 0, 1], [0.2, 0.9], 2)
