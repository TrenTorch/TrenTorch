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
    _close(solve(['a', 'a', 'b'], [1.0, 2.0, 4.0]), {'a': 1.5, 'b': 4.0})


def test_02_readme_example_2():
    _close(solve(['x', 'y', 'x', 'y', 'x'], [10.0, 1.0, 20.0, 3.0, 30.0]), {'x': 20.0, 'y': 2.0})


def test_03_random_valid_case_1():
    _close(solve(['b', 'c', 'a', 'b', 'c', 'c', 'b', 'b', 'c', 'b', 'b', 'b', 'a', 'b', 'c'], [1.58, 1.22, 4.13, 2.57, 0.68, 2.51, 4.53, 1.91, 1.92, 0.31, 1.32, 1.03, -1.18, 0.01, -1.21]), {'b': 1.6575, 'c': 1.024, 'a': 1.475})


def test_04_random_valid_case_2():
    _close(solve(['a', 'a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'a', 'a', 'a', 'a', 'c'], [-0.08, 3.87, 4.47, 0.31, 0.96, 3.32, 1.83, -0.76, -4.54, 3.4, 2.22, -0.99, -0.8, 4.48, 0.83]), {'a': 1.7760000000000002, 'b': -0.01749999999999996, 'c': 0.83})


def test_05_random_valid_case_3():
    _close(solve(['b', 'c', 'b', 'a', 'a', 'c', 'c', 'b', 'a', 'c', 'a', 'c', 'c', 'b', 'c'], [-1.65, -1.06, -4.54, 0.11, 4.8, -1.48, -1.76, -1.9, 2.69, 0.5, 0.31, 4.36, -4.1, 4.87, 4.68]), {'b': -0.8049999999999999, 'c': 0.16285714285714295, 'a': 1.9774999999999998})


def test_06_random_valid_case_4():
    _close(solve(['b', 'c', 'a', 'c', 'c', 'c', 'b', 'a', 'c', 'b', 'b', 'b', 'c', 'c', 'b'], [-0.99, -2.96, 3.93, 0.92, 3.4, -3.45, 0.11, 0.91, 0.26, 1.12, -0.86, 3.84, -3.71, 0.44, 2.92]), {'b': 1.0233333333333332, 'c': -0.7285714285714285, 'a': 2.42})


def test_07_random_valid_case_5():
    _close(solve(['a', 'b', 'a', 'c', 'c', 'b', 'c', 'b', 'c', 'c', 'b', 'b', 'c', 'c', 'c'], [-3.56, 2.69, -3.43, 3.9, 2.88, -2.02, 2.13, -3.77, 3.34, -1.0, -1.69, 3.39, 0.59, -0.94, 4.72]), {'a': -3.495, 'b': -0.27999999999999997, 'c': 1.9525000000000001})


def test_08_random_valid_case_6():
    _close(solve(['c', 'b', 'c', 'b', 'b', 'a', 'c', 'b', 'c', 'b', 'b', 'c', 'c', 'b', 'c'], [-2.83, 0.62, -2.03, 4.28, -3.41, 1.23, 3.82, -0.08, -4.55, 2.42, -0.59, 2.5, 4.09, 4.98, 4.88]), {'c': 0.84, 'b': 1.1742857142857144, 'a': 1.23})


def test_09_random_valid_case_7():
    _close(solve(['c', 'c', 'b', 'b', 'a', 'a', 'b', 'c', 'c', 'c', 'b', 'a', 'a', 'c', 'a'], [-2.39, 3.34, 3.89, 4.39, -2.44, -2.52, -0.97, 4.68, 0.77, 3.15, 4.89, -0.16, 4.72, 3.23, -1.77]), {'c': 2.13, 'b': 3.05, 'a': -0.43400000000000005})


def test_10_random_valid_case_8():
    _close(solve(['c', 'c', 'b', 'a', 'b', 'a', 'b', 'c', 'b', 'a', 'a', 'c', 'a', 'a', 'a'], [-0.88, 4.3, -0.32, 2.78, 1.69, 4.95, 3.25, -3.04, 4.52, -4.91, -3.31, 1.09, -2.74, 0.16, -1.16]), {'c': 0.3675, 'b': 2.285, 'a': -0.6042857142857142})


def test_11_random_valid_case_9():
    _close(solve(['c', 'c', 'b', 'c', 'c', 'b', 'b', 'c', 'b', 'c', 'c', 'b', 'b', 'b', 'c'], [1.54, -1.92, -3.67, 2.52, -4.25, 0.76, -3.1, 1.75, -2.95, 1.59, -4.65, 1.93, 2.98, -4.21, 3.46]), {'c': 0.0050000000000000044, 'b': -1.1800000000000002})


def test_12_random_valid_case_10():
    _close(solve(['b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'c', 'c', 'c', 'a', 'c', 'a', 'c'], [-2.99, 1.23, -4.96, -3.72, 4.26, 3.0, -4.96, -0.36, 3.26, -0.03, -2.15, 0.49, 0.75, 4.22, -4.8]), {'b': -3.8900000000000006, 'c': 0.27000000000000013, 'a': 0.6875})
