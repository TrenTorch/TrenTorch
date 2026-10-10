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
    _close(solve([-2, 0, 3]), np.array([0, 0, 3]))


def test_02_readme_example_2():
    _close(solve([[-1.5, 2.5], [0.0, -0.1]]), np.array([[0.0, 2.5], [0.0, 0.0]]))


def test_03_random_valid_case_1():
    _close(solve([2.68, 3.11, 0.04, 0.64, 4.73, 0.98, -1.33, 4.7]), np.array([2.68, 3.11, 0.04, 0.64, 4.73, 0.98, 0.0, 4.7]))


def test_04_random_valid_case_2():
    _close(solve([2.48, 2.81, 3.2, -1.25, 3.01, 3.05, 1.82, -4.75]), np.array([2.48, 2.81, 3.2, 0.0, 3.01, 3.05, 1.82, 0.0]))


def test_05_random_valid_case_3():
    _close(solve([4.21, 3.4, 0.36, -3.54, 4.16, -2.32, 2.07, 2.69]), np.array([4.21, 3.4, 0.36, 0.0, 4.16, 0.0, 2.07, 2.69]))


def test_06_random_valid_case_4():
    _close(solve([3.26, -3.81, -0.2, -4.82, 4.24, 4.31, -2.32, 4.89]), np.array([3.26, 0.0, 0.0, 0.0, 4.24, 4.31, 0.0, 4.89]))


def test_07_random_valid_case_5():
    _close(solve([-2.11, 1.8, -2.17, -0.17, 3.3, 2.83, -1.83, -1.05]), np.array([0.0, 1.8, 0.0, 0.0, 3.3, 2.83, 0.0, 0.0]))


def test_08_random_valid_case_6():
    _close(solve([1.91, 0.67, -1.88, -1.23, 0.1, -0.61, -4.62, 4.99]), np.array([1.91, 0.67, 0.0, 0.0, 0.1, 0.0, 0.0, 4.99]))


def test_09_random_valid_case_7():
    _close(solve([-4.34, 4.98, 2.86, 2.88, 2.07, -2.08, -4.08, 0.81]), np.array([0.0, 4.98, 2.86, 2.88, 2.07, 0.0, 0.0, 0.81]))


def test_10_random_valid_case_8():
    _close(solve([3.45, -3.62, -2.67, 4.21, -0.99, -0.93, 3.9, 2.22]), np.array([3.45, 0.0, 0.0, 4.21, 0.0, 0.0, 3.9, 2.22]))


def test_11_random_valid_case_9():
    _close(solve([0.0, -1.54, 0.3, 1.61, 1.07, -3.52, -4.46, -4.36]), np.array([0.0, 0.0, 0.3, 1.61, 1.07, 0.0, 0.0, 0.0]))


def test_12_random_valid_case_10():
    _close(solve([1.17, 0.89, -3.63, 4.55, 1.26, -3.18, -0.51, -2.57]), np.array([1.17, 0.89, 0.0, 4.55, 1.26, 0.0, 0.0, 0.0]))
