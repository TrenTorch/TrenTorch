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
    _close(solve([1, 1, 0, 0], [0.9, 0.7, 0.6, 0.2]), 0.7)


def test_02_readme_example_2():
    _close(solve([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]), 0.35)


def test_03_random_valid_case_1():
    _close(solve([1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0.75, 0.3, 0.94, 0.65, 0.88, 0.24, 0.15, 0.57, 0.85, 0.2, 0.8, 0.6, 0.68, 0.93, 0.72, 0.58]), 0.65)


def test_04_random_valid_case_2():
    _close(solve([1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0], [0.4, 0.9, 0.52, 0.11, 0.61, 0.1, 0.65, 0.58, 0.93, 0.41, 0.66, 0.01, 0.33, 0.21, 0.99, 0.72]), 0.21)


def test_05_random_valid_case_3():
    _close(solve([0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0], [0.03, 0.15, 0.08, 0.52, 0.89, 0.79, 0.1, 0.11, 0.5, 0.49, 0.83, 0.23, 0.35, 0.4, 0.27, 0.73]), 0.08)


def test_06_random_valid_case_4():
    _close(solve([1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0], [0.06, 0.26, 0.2, 0.12, 0.53, 0.29, 0.9, 0.3, 0.62, 0.94, 0.89, 0.49, 0.43, 0.57, 0.67, 0.16]), 0.62)


def test_07_random_valid_case_5():
    _close(solve([0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], [0.41, 0.43, 0.58, 0.05, 0.41, 0.8, 0.1, 0.05, 0.82, 0.34, 0.8, 0.09, 0.38, 0.69, 0.81, 0.12]), 0.69)


def test_08_random_valid_case_6():
    _close(solve([1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1], [0.47, 0.28, 0.54, 0.04, 0.71, 0.89, 0.6, 0.38, 0.77, 0.13, 0.9, 0.42, 0.81, 0.02, 0.05, 0.31]), 0.04)


def test_09_random_valid_case_7():
    _close(solve([1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0], [0.7, 0.39, 0.97, 0.18, 0.38, 0.38, 0.2, 0.71, 0.21, 0.28, 0.48, 0.48, 0.95, 0.78, 0.17, 0.36]), 0.7)


def test_10_random_valid_case_8():
    _close(solve([1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0.21, 0.81, 0.3, 0.69, 0.05, 0.98, 0.27, 0.82, 0.33, 0.75, 0.45, 0.7, 0.25, 0.47, 0.48, 0.76]), 0.7)


def test_11_random_valid_case_9():
    _close(solve([0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1], [0.99, 0.08, 0.53, 0.6, 0.33, 0.27, 0.24, 0.35, 0.31, 0.2, 0.68, 0.46, 0.21, 0.74, 0.08, 0.21]), 0.21)


def test_12_random_valid_case_10():
    _close(solve([0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0], [0.07, 0.59, 0.75, 0.32, 0.32, 0.08, 0.7, 0.93, 0.13, 0.98, 0.74, 0.6, 0.63, 0.44, 0.86, 0.68]), 0.32)
