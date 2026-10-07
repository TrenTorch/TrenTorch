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
    _close(solve([1.0, np.nan, 3.0, 100.0]), np.array([1.0, 3.0, 3.0, 100.0]))


def test_02_readme_example_2():
    _close(solve([2.0, 4.0, np.nan, 10.0]), np.array([2.0, 4.0, 4.0, 10.0]))


def test_03_random_valid_case_1():
    _close(solve([4.8, 1.58, 1.43, 4.99, float('nan'), 1.3, 0.51, float('nan')]), np.array([4.8, 1.58, 1.43, 4.99, 1.505, 1.3, 0.51, 1.505]))


def test_04_random_valid_case_2():
    _close(solve([float('nan'), 2.34, -2.07, float('nan'), 4.1, 1.52, 2.42, 3.6]), np.array([2.38, 2.34, -2.07, 2.38, 4.1, 1.52, 2.42, 3.6]))


def test_05_random_valid_case_3():
    _close(solve([float('nan'), -3.9, float('nan'), 1.79, 3.5, 4.14, 4.12, -3.44]), np.array([2.645, -3.9, 2.645, 1.79, 3.5, 4.14, 4.12, -3.44]))


def test_06_random_valid_case_4():
    _close(solve([-1.7, 4.69, 0.0, float('nan'), 3.72, 0.98, -4.57, float('nan')]), np.array([-1.7, 4.69, 0.0, 0.49, 3.72, 0.98, -4.57, 0.49]))


def test_07_random_valid_case_5():
    _close(solve([4.31, 0.42, float('nan'), -1.6, 1.13, -2.32, 0.85, float('nan')]), np.array([4.31, 0.42, 0.635, -1.6, 1.13, -2.32, 0.85, 0.635]))


def test_08_random_valid_case_6():
    _close(solve([-2.48, 1.61, 3.38, float('nan'), 3.89, float('nan'), -4.05, 2.62]), np.array([-2.48, 1.61, 3.38, 2.115, 3.89, 2.115, -4.05, 2.62]))


def test_09_random_valid_case_7():
    _close(solve([float('nan'), 1.43, 0.34, -1.78, float('nan'), 2.26, -0.78, 2.79]), np.array([0.885, 1.43, 0.34, -1.78, 0.885, 2.26, -0.78, 2.79]))


def test_10_random_valid_case_8():
    _close(solve([0.26, 0.49, float('nan'), float('nan'), 2.43, -4.96, -4.29, 3.85]), np.array([0.26, 0.49, 0.375, 0.375, 2.43, -4.96, -4.29, 3.85]))


def test_11_random_valid_case_9():
    _close(solve([float('nan'), float('nan'), -1.71, 4.73, 4.11, -2.22, 3.46, 0.16]), np.array([1.81, 1.81, -1.71, 4.73, 4.11, -2.22, 3.46, 0.16]))


def test_12_random_valid_case_10():
    _close(solve([-2.02, 3.57, 0.9, -2.99, -1.25, float('nan'), float('nan'), 3.77]), np.array([-2.02, 3.57, 0.9, -2.99, -1.25, -0.175, -0.175, 3.77]))
