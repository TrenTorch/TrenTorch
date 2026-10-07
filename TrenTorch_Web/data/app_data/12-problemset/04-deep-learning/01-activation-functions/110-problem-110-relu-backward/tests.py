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


def test_01_readme_example_1():
    _close(solve([-2, 0, 3]), np.array([0.0, 0.0, 1.0]))


def test_02_readme_example_2():
    _close(solve([[1.0, -1.0], [0.5, 0.0]]), np.array([[1.0, 0.0], [1.0, 0.0]]))


def test_03_random_valid_case_1():
    _close(solve([-0.59, 1.68, 4.06, 4.16, 3.9, 1.6, -4.98, 3.88]), np.array([0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]))


def test_04_random_valid_case_2():
    _close(solve([2.14, 4.3, -4.07, -3.56, 1.61, 1.94, 4.94, 3.56]), np.array([1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]))


def test_05_random_valid_case_3():
    _close(solve([3.44, -4.85, 4.64, 1.37, 2.25, 3.51, 4.33, -0.12]), np.array([1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0]))


def test_06_random_valid_case_4():
    _close(solve([-2.2, -0.03, 3.72, -4.24, 2.45, -2.16, 0.83, 2.9]), np.array([0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0]))


def test_07_random_valid_case_5():
    _close(solve([-3.04, 1.62, 2.13, 2.2, 1.2, -4.03, -1.95, -1.72]), np.array([0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0]))


def test_08_random_valid_case_6():
    _close(solve([-4.02, 0.44, 2.03, -2.07, 2.4, -4.63, 3.02, 4.89]), np.array([0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0]))


def test_09_random_valid_case_7():
    _close(solve([2.48, 3.74, -4.57, 3.61, -4.76, -1.2, 0.64, -1.24]), np.array([1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0]))


def test_10_random_valid_case_8():
    _close(solve([3.64, 4.44, -2.42, -3.64, 0.89, 4.75, -4.87, 2.93]), np.array([1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0]))


def test_11_random_valid_case_9():
    _close(solve([4.18, 0.11, -1.62, 1.89, -3.66, -3.91, 1.3, -0.02]), np.array([1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0]))


def test_12_random_valid_case_10():
    _close(solve([-3.07, 0.37, 3.14, -1.45, -1.49, 1.6, 1.76, -3.94]), np.array([0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0]))
