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
    _close(solve([0, 0, 0, 1, 1, 1], 1/3), (np.array([0, 1, 3, 4]), np.array([2, 5])))


def test_02_readme_example_2():
    _close(solve([0, 0, 0, 0, 1, 1], 0.5, seed=3), (np.array([0, 1, 4]), np.array([2, 3, 5])))


def test_03_random_valid_case_1():
    _close(solve([0, 0, 1, 0, 0, 0, 1, 0, 1, 2, 1, 0, 0, 1, 2, 0, 2, 1, 2, 2, 0, 0, 0, 1, 1], 0.3, 2), (np.array([1, 2, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, 22, 24]), np.array([0, 3, 6, 9, 18, 20, 21, 23])))


def test_04_random_valid_case_2():
    _close(solve([1, 1, 1, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 2, 0, 1, 1, 0, 1, 0, 0, 1, 2, 2], 0.3, 2), (np.array([0, 2, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 24]), np.array([1, 3, 4, 6, 18, 19, 20, 23])))


def test_05_random_valid_case_3():
    _close(solve([0, 2, 1, 2, 0, 2, 0, 0, 0, 2, 1, 1, 1, 0, 0, 1, 0, 2, 0, 1, 1, 0, 1, 0, 0], 0.3, 2), (np.array([2, 3, 4, 5, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 24]), np.array([0, 1, 6, 9, 10, 20, 21, 23])))


def test_06_random_valid_case_4():
    _close(solve([0, 2, 0, 1, 0, 2, 0, 1, 0, 1, 1, 2, 1, 1, 2, 1, 0, 2, 0, 0, 0, 0, 0, 1, 0], 0.3, 2), (np.array([2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 23, 24]), np.array([0, 1, 4, 7, 14, 15, 21, 22])))


def test_07_random_valid_case_5():
    _close(solve([2, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 2, 2, 1, 1, 0, 1, 0, 1, 2], 0.3, 2), (np.array([1, 3, 5, 6, 7, 8, 9, 10, 11, 13, 15, 16, 18, 19, 22, 23, 24]), np.array([0, 2, 4, 12, 14, 17, 20, 21])))


def test_08_random_valid_case_6():
    _close(solve([0, 2, 0, 0, 2, 0, 2, 2, 0, 1, 0, 2, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1], 0.3, 2), (np.array([2, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 20, 21, 23, 24]), np.array([0, 1, 3, 7, 12, 18, 19, 22])))


def test_09_random_valid_case_7():
    _close(solve([1, 2, 0, 2, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 2, 1, 2, 0, 2, 1, 0, 0, 0], 0.3, 2), (np.array([0, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 24]), np.array([1, 2, 4, 6, 17, 18, 22, 23])))


def test_10_random_valid_case_8():
    _close(solve([0, 0, 2, 0, 0, 0, 1, 1, 0, 1, 2, 1, 0, 0, 1, 0, 2, 1, 2, 1, 2, 0, 1, 0, 0], 0.3, 2), (np.array([1, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 22, 24]), np.array([0, 2, 3, 7, 18, 19, 21, 23])))


def test_11_random_valid_case_9():
    _close(solve([1, 0, 2, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 2, 2, 0, 1, 0, 2, 0, 1, 1, 0, 0, 2], 0.3, 2), (np.array([0, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 23, 24]), np.array([1, 2, 4, 6, 18, 19, 20, 22])))


def test_12_random_valid_case_10():
    _close(solve([1, 0, 0, 0, 0, 2, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 2, 1, 2, 0, 1, 1, 2, 0, 2], 0.3, 2), (np.array([0, 2, 4, 6, 7, 9, 10, 11, 12, 13, 14, 16, 17, 18, 21, 23, 24]), np.array([1, 3, 5, 8, 15, 19, 20, 22])))
