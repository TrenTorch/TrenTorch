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
    _close(solve([1.0, 2.0, 3.0, 4.0, 100.0]), np.array([False, False, False, False, True]))


def test_02_readme_example_2():
    _close(solve([1.0, 2.0, 3.0]), np.array([False, False, False]))


def test_03_invalid_input_raises():
    with pytest.raises(IndexError):
        solve([])


def test_04_random_valid_case_1():
    _close(solve([50.0, 4.86, 3.25, 3.0, 1.0, 4.6, -4.31, 0.38, 4.74, 2.1, 4.43, -2.4, 4.43, 2.37]), np.array([True, False, False, False, False, False, True, False, False, False, False, False, False, False]))


def test_05_random_valid_case_2():
    _close(solve([50.0, 1.04, -1.07, 3.63, 3.1, -3.33, 3.68, 4.97, -1.7, 0.14, 4.06, 0.64, 4.62, 3.58]), np.array([True, False, False, False, False, False, False, False, False, False, False, False, False, False]))


def test_06_random_valid_case_3():
    _close(solve([50.0, 4.5, 1.47, -4.51, -4.4, 1.49, -3.58, -4.38, -0.14, 2.57, 4.49, 2.39, 1.32, 4.8]), np.array([True, False, False, False, False, False, False, False, False, False, False, False, False, False]))


def test_07_random_valid_case_4():
    _close(solve([50.0, 3.84, -3.2, 0.35, 4.45, -4.17, -4.75, 0.59, 2.1, 1.72, 2.47, -2.32, 4.79, -3.04]), np.array([True, False, False, False, False, False, False, False, False, False, False, False, False, False]))


def test_08_random_valid_case_5():
    _close(solve([50.0, 1.46, 0.63, -3.76, 1.62, -3.39, 0.76, 1.19, 2.76, 4.61, -4.32, 2.38, 4.1, -3.11]), np.array([True, False, False, False, False, False, False, False, False, False, False, False, False, False]))


def test_09_random_valid_case_6():
    _close(solve([50.0, 2.57, 1.85, 4.55, 2.19, -2.07, 0.36, -4.89, 3.91, -3.44, -3.21, 0.73, 3.63, 4.53]), np.array([True, False, False, False, False, False, False, False, False, False, False, False, False, False]))


def test_10_random_valid_case_7():
    _close(solve([50.0, -3.0, -3.73, -3.45, 3.27, 2.45, 1.8, 0.19, -4.11, -4.28, 4.65, -0.67, 2.47, -2.4]), np.array([True, False, False, False, False, False, False, False, False, False, False, False, False, False]))


def test_11_random_valid_case_8():
    _close(solve([50.0, 2.87, 2.42, -0.73, -3.12, -4.09, -1.06, -1.03, -1.8, 0.7, 2.26, 2.64, 2.26, 0.97]), np.array([True, False, False, False, False, False, False, False, False, False, False, False, False, False]))


def test_12_random_valid_case_9():
    _close(solve([50.0, 1.07, -2.17, 4.45, 2.61, -2.41, 1.19, -2.44, 1.77, 1.5, -1.01, 2.59, 2.77, -1.16]), np.array([True, False, False, False, False, False, False, False, False, False, False, False, False, False]))
