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
    _close(solve([1.0, 2.0, 3.0], 0.1), 1.4000000000000001)


def test_02_readme_example_2():
    _close(solve([0.0, 0.0], 5.0), 0.0)


def test_03_random_valid_case_1():
    _close(solve([0.88, 0.47, 2.43, -2.95, 4.62, 4.69], 0.2), 11.788640000000001)


def test_04_random_valid_case_2():
    _close(solve([1.08, -2.07, 0.58, 1.79, 4.2, 0.59], 0.56), 15.108744)


def test_05_random_valid_case_3():
    _close(solve([-1.15, -0.82, 4.58, 1.07, 4.18, 3.9], 0.21), 11.927705999999999)


def test_06_random_valid_case_4():
    _close(solve([1.84, 0.59, -2.0, -3.17, 3.41, 0.58], 0.34), 10.114014000000003)


def test_07_random_valid_case_5():
    _close(solve([0.12, -1.37, 3.1, -3.03, 4.62, 3.51], 0.53), 28.803751000000002)


def test_08_random_valid_case_6():
    _close(solve([0.97, -3.91, 1.0, -2.29, 0.99, 0.27], 0.79), 18.585619000000005)


def test_09_random_valid_case_7():
    _close(solve([4.95, -3.51, 4.05, -2.74, 2.77, 3.15], 0.12), 9.399372)


def test_10_random_valid_case_8():
    _close(solve([-3.0, -3.94, -1.26, -3.04, 1.31, 2.7], 0.11), 4.879479)


def test_11_random_valid_case_9():
    _close(solve([-2.31, 0.31, -3.31, 0.79, 0.21, 4.24], 0.22), 7.707502000000001)


def test_12_random_valid_case_10():
    _close(solve([0.54, 4.61, 4.36, -0.56, -3.98, 0.69], 0.06), 3.4310040000000006)
