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
    _close(solve([0.0, 2.0], [0, 1]), 0.4100375958014589)


def test_02_readme_example_2():
    _close(solve([1000.0, -1000.0], [1, 0]), 0.0)


def test_03_readme_example_3():
    _close(solve([1000.0], [0]), 1000.0)


def test_04_random_valid_case_1():
    _close(solve([6.03, -19.2, 4.19, 5.68, 5.3, -4.74, 4.94, 4.75], [0, 1, 1, 0, 0, 0, 0, 1]), 5.150033319055604)


def test_05_random_valid_case_2():
    _close(solve([-12.17, 3.47, 5.41, 6.19, 6.33, -6.24, 19.92, -0.77], [0, 1, 1, 1, 0, 0, 0, 0]), 3.3339229695644823)


def test_06_random_valid_case_3():
    _close(solve([19.36, -2.58, 4.41, 16.56, 11.55, 7.67, 18.1, -14.96], [1, 1, 1, 0, 0, 0, 0, 1]), 8.93819985612119)


def test_07_random_valid_case_4():
    _close(solve([0.75, -2.16, 16.59, 14.09, 12.02, 6.21, 14.97, -9.02], [0, 0, 0, 1, 0, 1, 1, 0]), 3.7322690371806275)


def test_08_random_valid_case_5():
    _close(solve([-16.74, 5.66, -4.27, -17.12, -19.81, -8.17, 0.5, 3.54], [0, 0, 1, 1, 1, 0, 0, 1]), 5.985040233745975)


def test_09_random_valid_case_6():
    _close(solve([-19.5, 8.46, 13.54, 10.66, -9.94, -0.66, -9.5, -18.53], [1, 0, 1, 0, 1, 1, 1, 1]), 9.708374536876692)


def test_10_random_valid_case_7():
    _close(solve([5.36, 3.66, -7.82, 16.98, 15.97, -3.51, -1.77, -15.31], [0, 0, 0, 1, 0, 1, 0, 0]), 3.589655730899658)


def test_11_random_valid_case_8():
    _close(solve([13.01, 0.58, 2.31, 9.08, -19.16, -2.75, -8.98, -16.89], [0, 0, 1, 1, 1, 0, 1, 1]), 7.402683590258218)


def test_12_random_valid_case_9():
    _close(solve([-3.91, 18.01, 13.15, -6.09, -2.13, 17.25, 0.28, -3.32], [1, 0, 1, 1, 0, 1, 1, 0]), 3.5928533970101184)
