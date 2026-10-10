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
    _close(solve([1, 2], [0.5, -1], 0.1), np.array([0.95, 2.1]))


def test_02_readme_example_2():
    _close(solve([0.0], [10.0], 0.01), np.array([-0.1]))


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve(np.array([]), np.array([1.0, -1.0, 2.0]), 1)


def test_04_random_valid_case_1():
    _close(solve([-2.9, -4.76, 0.67, 2.93, 3.43], [3.7, 1.74, -3.54, 1.6, 1.9], 0.53), np.array([-4.861000000000001, -5.6822, 2.5462000000000002, 2.082, 2.423]))


def test_05_random_valid_case_2():
    _close(solve([0.11, 1.76, 3.12, 2.9, 1.88], [-3.58, -4.68, 2.27, 4.53, -2.2], 0.86), np.array([3.1888, 5.7848, 1.1678000000000002, -0.9958000000000005, 3.7720000000000002]))


def test_06_random_valid_case_3():
    _close(solve([3.67, 0.43, 2.4, -0.29, -4.72], [2.15, 2.89, 3.43, -3.44, 3.98], 0.43), np.array([2.7455, -0.8127000000000002, 0.9250999999999998, 1.1891999999999998, -6.4314]))


def test_07_random_valid_case_4():
    _close(solve([0.88, -0.85, 2.4, 0.39, 3.36], [3.98, -0.47, 2.28, 3.34, -3.32], 0.92), np.array([-2.7816, -0.41759999999999997, 0.3024, -2.6828, 6.4144]))


def test_08_random_valid_case_5():
    _close(solve([-1.49, 4.22, -2.18, 3.7, -2.53], [0.38, -3.98, -2.07, 1.1, -3.8], 0.49), np.array([-1.6762, 6.1701999999999995, -1.1657000000000002, 3.161, -0.6679999999999999]))


def test_09_random_valid_case_6():
    _close(solve([2.88, -2.24, -1.78, 0.76, 3.63], [-0.73, 2.34, -4.69, 2.66, 2.16], 0.2), np.array([3.026, -2.708, -0.8419999999999999, 0.22799999999999998, 3.198]))


def test_10_random_valid_case_7():
    _close(solve([-2.63, -4.3, 0.13, -1.69, 4.34], [2.8, -4.42, 3.75, 1.21, -4.04], 0.13), np.array([-2.9939999999999998, -3.7253999999999996, -0.35750000000000004, -1.8473, 4.8652]))


def test_11_random_valid_case_8():
    _close(solve([2.63, -1.59, -0.62, -2.64, 4.24], [4.2, 4.51, -0.78, 3.71, -2.32], 0.45), np.array([0.7399999999999998, -3.6195000000000004, -0.26899999999999996, -4.3095, 5.284000000000001]))


def test_12_random_valid_case_9():
    _close(solve([-3.35, 3.79, -1.03, 0.44, -2.17], [4.27, 3.99, -1.91, 3.67, -2.58], 0.3), np.array([-4.631, 2.593, -0.4570000000000001, -0.661, -1.396]))
