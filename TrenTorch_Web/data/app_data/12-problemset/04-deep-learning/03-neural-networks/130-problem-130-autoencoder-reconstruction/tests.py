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
    _close(solve([[1.0, 2.0], [3.0, 4.0]], [[1.0, 0.0], [0.0, 1.0]]), 5.5)


def test_02_singleton_boundary():
    _close(solve([[1.0, 2.0]], [[1.0, 0.0]]), 2.0)


def test_03_random_valid_case():
    _close(solve([1.26, 0.29, -4.2, 3.11, 3.2, 0.01, -0.17, -3.31], [0.91, 2.62, 2.31, -1.07, 1.63, -2.76, 4.2, 3.79]), 18.131075)


def test_04_random_valid_case():
    _close(solve([4.28, 0.1, 4.9, -0.59, -3.07, -2.99, 1.18, 4.36], [1.62, -2.59, 0.6, 3.35, -0.35, -1.72, 2.73, 4.95]), 7.5109)


def test_05_random_valid_case():
    _close(solve([2.63, -3.91, -0.49, 1.06, -3.58, 0.28, -1.24, 0.92], [0.02, 1.62, 4.78, 3.72, 1.88, 3.08, 0.75, 3.95]), 15.3792625)


def test_06_random_valid_case():
    _close(solve([-4.6, -3.4, 1.55, -2.51, 2.82, 1.93, 1.17, 2.44], [-2.72, -4.71, 3.78, 2.47, -2.45, 3.66, 0.17, -1.1]), 9.91515)


def test_07_random_valid_case():
    _close(solve([-3.3, -4.68, 0.16, -4.99, 1.77, -2.28, -2.05, 4.67], [0.81, 0.52, 1.87, 1.3, 1.47, 3.76, -2.47, 4.72]), 15.396349999999998)


def test_08_random_valid_case():
    _close(solve([-3.01, 2.92, 4.04, -0.4, 4.99, -0.04, -3.82, 2.63], [1.66, -0.58, -3.46, -3.49, 0.9, 0.6, -0.8, -2.93]), 19.628587500000002)


def test_09_random_valid_case():
    _close(solve([-2.67, -2.29, -2.2, -1.95, -2.29, 3.62, -0.87, 3.0], [3.74, 3.7, 4.29, 0.45, -2.32, 2.03, -4.29, 1.12]), 17.8260125)


def test_10_random_valid_case():
    _close(solve([0.32, 1.51, -3.1, -3.79, 0.03, 2.22, 4.14, -4.72], [-2.55, -1.93, 4.84, -0.2, 2.46, -0.43, 1.89, -1.24]), 15.762812499999999)


def test_11_random_valid_case():
    _close(solve([-1.09, 4.57, -3.03, 1.94, 2.31, 1.97, -2.63, 2.93], [-0.49, 0.99, 2.27, -1.36, 0.79, 4.94, -3.98, 0.48]), 8.8890875)


def test_12_random_valid_case():
    _close(solve([-2.61, 0.21, 0.45, 3.12, 0.26, -1.57, 2.75, -0.96], [0.46, -4.92, 0.44, -1.82, 3.14, 1.67, 2.69, -1.01]), 9.86795)
