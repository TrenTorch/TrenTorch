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
    _close(solve([-2, 0, 3]), np.array([0.0, 0.0, 3.0]))


def test_02_readme_example_2():
    _close(solve([[1.5, -0.5], [-3.0, 4.0]]), np.array([[1.5, 0.0], [0.0, 4.0]]))


def test_03_random_valid_case_1():
    _close(solve([1.3, 3.56, 0.97, 2.2, -0.31, 3.39, -2.41, 4.15]), np.array([1.3, 3.56, 0.97, 2.2, 0.0, 3.39, 0.0, 4.15]))


def test_04_random_valid_case_2():
    _close(solve([-1.15, 0.2, 4.47, -2.44, 2.06, 1.48, 3.28, 1.8]), np.array([0.0, 0.2, 4.47, 0.0, 2.06, 1.48, 3.28, 1.8]))


def test_05_random_valid_case_3():
    _close(solve([-4.84, 2.82, 2.09, 0.53, 4.2, 3.22, 4.36, 2.68]), np.array([0.0, 2.82, 2.09, 0.53, 4.2, 3.22, 4.36, 2.68]))


def test_06_random_valid_case_4():
    _close(solve([-3.39, -0.85, 0.85, 2.2, 3.2, 3.14, -1.82, 3.14]), np.array([0.0, 0.0, 0.85, 2.2, 3.2, 3.14, 0.0, 3.14]))


def test_07_random_valid_case_5():
    _close(solve([1.84, 1.57, -3.09, 3.45, 4.23, 2.43, 2.68, 3.53]), np.array([1.84, 1.57, 0.0, 3.45, 4.23, 2.43, 2.68, 3.53]))


def test_08_random_valid_case_6():
    _close(solve([-4.02, -4.21, 0.42, 4.94, 1.19, 1.58, 0.04, 4.59]), np.array([0.0, 0.0, 0.42, 4.94, 1.19, 1.58, 0.04, 4.59]))


def test_09_random_valid_case_7():
    _close(solve([1.18, 0.13, 3.76, 1.2, -2.89, -2.01, -1.53, 0.96]), np.array([1.18, 0.13, 3.76, 1.2, 0.0, 0.0, 0.0, 0.96]))


def test_10_random_valid_case_8():
    _close(solve([-0.08, -1.67, -1.2, 1.77, -4.14, 1.3, 1.08, 0.95]), np.array([0.0, 0.0, 0.0, 1.77, 0.0, 1.3, 1.08, 0.95]))


def test_11_random_valid_case_9():
    _close(solve([2.79, -1.84, -4.61, 2.11, -4.76, -0.2, -4.18, 2.4]), np.array([2.79, 0.0, 0.0, 2.11, 0.0, 0.0, 0.0, 2.4]))


def test_12_random_valid_case_10():
    _close(solve([3.36, 0.64, -1.34, 4.44, -1.64, 1.05, -2.7, -0.83]), np.array([3.36, 0.64, 0.0, 4.44, 0.0, 1.05, 0.0, 0.0]))
