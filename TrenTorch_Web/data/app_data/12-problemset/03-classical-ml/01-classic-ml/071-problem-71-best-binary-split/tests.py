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
    _close(solve([1.0, 2.0, 3.0, 4.0], [0, 0, 1, 1]), (0.0, 2.0))


def test_02_readme_example_2():
    _close(solve([1.0, 2.0, 3.0, 4.0, 5.0], [0, 1, 0, 1, 1]), (0.26666666666666666, 3.0))


def test_03_readme_example_3():
    _close(solve([2.0, 2.0], [0, 1]), None)


def test_04_random_valid_case_1():
    _close(solve([3.3, 4.93, -0.91, 2.55, -4.58, 3.05, -3.7, 2.75, 3.04, 4.23, 3.47, -0.4], [1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0]), (0.2708333333333333, -0.4))


def test_05_random_valid_case_2():
    _close(solve([-3.5, 3.08, 1.51, 3.49, -3.52, 1.26, -0.16, 2.76, -3.21, 0.2, 4.25, 0.06], [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0]), (0.26666666666666655, -3.5))


def test_06_random_valid_case_3():
    _close(solve([2.87, -3.67, 3.99, 3.27, -0.4, -0.22, -2.9, 4.17, 0.38, -4.32, 0.05, 3.37], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]), (0.3125, 2.87))


def test_07_random_valid_case_4():
    _close(solve([3.17, -2.26, 4.25, -3.8, 2.38, -3.07, -4.6, 4.42, 2.71, -4.24, 4.67, -4.2], [1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1]), (0.26666666666666655, 4.25))


def test_08_random_valid_case_5():
    _close(solve([4.39, 4.09, 2.77, 0.62, 4.29, -1.7, -1.13, 0.82, 0.74, -1.35, -3.59, 4.06], [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0]), (0.3428571428571429, 0.82))


def test_09_random_valid_case_6():
    _close(solve([0.47, -4.46, 3.29, 3.03, 4.21, -0.73, 1.99, -4.58, 0.36, -3.1, -2.57, 2.62], [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0]), (0.4444444444444444, -3.1))


def test_10_random_valid_case_7():
    _close(solve([3.64, -3.13, 3.28, -1.16, 2.94, 4.25, 3.34, 0.56, 1.29, -4.98, 0.72, -2.11], [1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0]), (0.45454545454545464, -4.98))


def test_11_random_valid_case_8():
    _close(solve([-1.4, -1.35, 3.71, -1.19, 0.97, 3.31, 4.75, -4.3, -1.64, -0.23, 0.0, -1.32], [0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1]), (0.42424242424242425, 3.71))


def test_12_random_valid_case_9():
    _close(solve([0.92, 3.64, -3.52, -1.01, 3.75, -0.53, -2.19, 2.43, 1.9, -1.17, 0.9, -3.06], [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1]), (0.3125, -1.17))
