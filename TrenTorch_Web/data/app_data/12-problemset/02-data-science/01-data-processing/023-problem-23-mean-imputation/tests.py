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
    _close(solve([1.0, np.nan, 3.0]), np.array([1.0, 2.0, 3.0]))


def test_02_readme_example_2():
    _close(solve([np.nan, 4.0, 6.0, np.nan]), np.array([5.0, 4.0, 6.0, 5.0]))


def test_03_random_valid_case_1():
    _close(solve([-1.1, 1.4, float('nan'), -1.2, 2.84, -4.72, 3.2, float('nan')]), np.array([-1.1, 1.4, 0.07000000000000002, -1.2, 2.84, -4.72, 3.2, 0.07000000000000002]))


def test_04_random_valid_case_2():
    _close(solve([1.54, -3.2, 4.69, 2.06, float('nan'), 3.24, 1.94, float('nan')]), np.array([1.54, -3.2, 4.69, 2.06, 1.7116666666666667, 3.24, 1.94, 1.7116666666666667]))


def test_05_random_valid_case_3():
    _close(solve([float('nan'), -4.56, float('nan'), 2.97, -2.9, 4.4, 3.56, 2.95]), np.array([1.07, -4.56, 1.07, 2.97, -2.9, 4.4, 3.56, 2.95]))


def test_06_random_valid_case_4():
    _close(solve([3.9, float('nan'), 3.42, -2.61, 4.92, 0.41, 0.29, float('nan')]), np.array([3.9, 1.7216666666666667, 3.42, -2.61, 4.92, 0.41, 0.29, 1.7216666666666667]))


def test_07_random_valid_case_5():
    _close(solve([4.02, -0.5, -0.96, 2.88, 2.74, 3.84, float('nan'), float('nan')]), np.array([4.02, -0.5, -0.96, 2.88, 2.74, 3.84, 2.0033333333333334, 2.0033333333333334]))


def test_08_random_valid_case_6():
    _close(solve([float('nan'), 4.64, 3.02, 2.84, -4.78, float('nan'), 1.66, 1.24]), np.array([1.4366666666666665, 4.64, 3.02, 2.84, -4.78, 1.4366666666666665, 1.66, 1.24]))


def test_09_random_valid_case_7():
    _close(solve([float('nan'), -2.22, -3.84, 2.9, 0.88, 0.61, 2.93, float('nan')]), np.array([0.20999999999999996, -2.22, -3.84, 2.9, 0.88, 0.61, 2.93, 0.20999999999999996]))


def test_10_random_valid_case_8():
    _close(solve([-3.56, float('nan'), 3.99, -3.23, 4.1, 3.14, float('nan'), -3.9]), np.array([-3.56, 0.09000000000000008, 3.99, -3.23, 4.1, 3.14, 0.09000000000000008, -3.9]))


def test_11_random_valid_case_9():
    _close(solve([-0.26, -2.36, 0.08, 3.13, 0.37, float('nan'), -1.0, float('nan')]), np.array([-0.26, -2.36, 0.08, 3.13, 0.37, -0.006666666666666691, -1.0, -0.006666666666666691]))


def test_12_random_valid_case_10():
    _close(solve([float('nan'), -3.84, float('nan'), -3.56, 0.11, 4.54, 3.26, 3.64]), np.array([0.6916666666666668, -3.84, 0.6916666666666668, -3.56, 0.11, 4.54, 3.26, 3.64]))
