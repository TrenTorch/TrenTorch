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
    _close(solve([1, 2, 4, 7], [0, 0, 1, 1]), 3.0)


def test_02_readme_example_2():
    _close(solve([3.0, 3.0], [0, 1]), None)


def test_03_random_valid_case_1():
    _close(solve([1.97, 4.4, 4.98, 0.8, 4.6, -1.17, -1.66, 3.58, 3.48, 2.82, 2.94, 1.7, -4.31, -4.74], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0]), 3.99)


def test_04_random_valid_case_2():
    _close(solve([-2.2, 3.32, 2.51, -0.6, 3.27, 4.53, 4.56, -3.66, 1.2, -2.1, 0.4, 1.73, -1.39, -1.02], [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]), -1.205)


def test_05_random_valid_case_3():
    _close(solve([-0.6, -1.96, -3.76, 4.73, 2.75, -2.32, 1.96, 1.85, -3.97, 3.87, 2.86, 1.51, 2.77, 0.8], [0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0]), -3.865)


def test_06_random_valid_case_4():
    _close(solve([0.58, -4.1, 1.14, -3.6, -2.42, 1.95, 1.07, 3.41, 3.51, -3.48, 3.55, -2.79, 0.62, 2.24], [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1]), 3.46)


def test_07_random_valid_case_5():
    _close(solve([1.99, 2.38, 0.44, 2.06, -3.96, -1.93, 1.45, 1.68, -3.36, 4.6, -3.25, 3.2, 2.92, -0.87], [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1]), 1.565)


def test_08_random_valid_case_6():
    _close(solve([-1.6, -0.92, -2.59, 1.57, 4.85, -4.2, 4.2, -4.33, 1.78, -1.33, -1.96, 2.94, 4.18, 3.53], [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1]), -3.395)


def test_09_random_valid_case_7():
    _close(solve([2.81, -2.94, 2.73, -2.73, 4.45, 2.71, 1.35, -4.54, -2.03, 2.52, -0.8, -2.56, 3.3, 1.89], [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]), 0.275)


def test_10_random_valid_case_8():
    _close(solve([1.44, -0.38, 0.29, 3.84, 1.44, -4.6, -4.22, 2.66, 1.68, -0.5, 4.06, 2.42, -2.75, -1.34], [1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1]), -3.485)


def test_11_random_valid_case_9():
    _close(solve([2.01, -1.1, 2.53, -1.76, -2.04, 0.67, 4.52, -1.8, -0.88, 2.84, 3.75, -4.45, 4.56, 4.58], [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]), -0.10499999999999998)


def test_12_random_valid_case_10():
    _close(solve([-4.07, -0.41, 0.36, -3.42, 1.68, 2.03, -0.02, -2.55, -2.76, 0.63, -2.5, 2.33, 0.89, 4.1], [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1]), -0.215)
