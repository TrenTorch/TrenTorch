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
    _close(solve([0.9, 0.8, 0.81, 0.82], 2), 3)


def test_02_readme_example_2():
    _close(solve([0.9, 0.8, 0.7], 2), -1)


def test_03_random_valid_case_1():
    _close(solve([0.5, 1.0, 0.6], 1), 1)


def test_04_random_valid_case_2():
    _close(solve([0.2, 0.8, 0.7], 1), 1)


def test_05_random_valid_case_3():
    _close(solve([0.7, 0.1, 0.8, 0.3], 4), -1)


def test_06_random_valid_case_4():
    _close(solve([0.4, 0.8, 0.2, 0.2, 0.7], 4), -1)


def test_07_random_valid_case_5():
    _close(solve([0.9, 0.5, 0.5, 0.2, 0.1], 3), -1)


def test_08_random_valid_case_6():
    _close(solve([0.5, 0.9, 0.8, 0.1, 0.2], 2), 2)


def test_09_random_valid_case_7():
    _close(solve([0.3, 0.3, 0.9, 0.9, 0.6, 1.0, 0.1], 1), 1)


def test_10_random_valid_case_8():
    _close(solve([0.5, 1.0, 0.2, 0.3, 0.8, 0.0, 0.6, 0.3], 3), -1)


def test_11_random_valid_case_9():
    _close(solve([0.8, 1.0, 0.5, 0.0, 0.1, 0.7, 0.8, 0.4, 0.2], 1), 1)


def test_12_random_valid_case_10():
    _close(solve([0.5, 0.6, 0.8, 1.0, 0.3, 0.2, 0.2, 0.3, 0.1], 3), 3)
