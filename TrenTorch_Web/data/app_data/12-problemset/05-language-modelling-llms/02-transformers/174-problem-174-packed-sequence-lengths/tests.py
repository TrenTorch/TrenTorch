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
    _close(solve([3, 1, 2]), np.array([0, 3, 4]))


def test_02_readme_example_2():
    _close(solve([0, 4, 0, 2]), np.array([0, 0, 4, 4]))


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([-4, -2, -3])


def test_04_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([-2.0, 0.0, 2.0])


def test_05_random_valid_case_1():
    _close(solve([7, 1, 7, 4, 0, 3]), np.array([0, 7, 8, 15, 19, 19]))


def test_06_random_valid_case_2():
    _close(solve([3, 1, 1, 1, 0, 7]), np.array([0, 3, 4, 5, 6, 6]))


def test_07_random_valid_case_3():
    _close(solve([6, 6, 5, 0, 6, 7]), np.array([0, 6, 12, 17, 17, 23]))


def test_08_random_valid_case_4():
    _close(solve([4, 7, 0, 1, 7, 0]), np.array([0, 4, 11, 11, 12, 19]))


def test_09_random_valid_case_5():
    _close(solve([6, 7, 4, 3, 4, 4]), np.array([0, 6, 13, 17, 20, 24]))


def test_10_random_valid_case_6():
    _close(solve([4, 7, 7, 1, 4, 4]), np.array([0, 4, 11, 18, 19, 23]))


def test_11_random_valid_case_7():
    _close(solve([6, 4, 3, 4, 7, 5]), np.array([0, 6, 10, 13, 17, 24]))


def test_12_random_valid_case_8():
    _close(solve([2, 7, 2, 4, 5, 5]), np.array([0, 2, 9, 11, 15, 20]))
