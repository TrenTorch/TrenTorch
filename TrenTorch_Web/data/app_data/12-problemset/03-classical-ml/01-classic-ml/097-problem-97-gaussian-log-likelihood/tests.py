"""Tests with varied inputs. Expected values were checked against independent references (SciPy, scikit-learn, PyTorch or a first-principles formula)."""
import math

import numpy as np
from numpy.linalg import LinAlgError
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
    _close(solve([1.0, 2.0], [0.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]), -4.337877066409345)


def test_02_readme_example_2():
    _close(solve([0.0], [0.0], [[4.0]]), -1.612085713764618)


def test_03_invalid_input_raises():
    with pytest.raises(LinAlgError):
        solve([1.0], [0.0], [[1.0, 0.0]])


def test_04_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([], [0.0, 0.0], [[1.0, 0.0], [0.0, 1.0]])


def test_05_random_valid_case_1():
    _close(solve([2.57], [4.59], [[2.44]]), -2.2010850938408346)


def test_06_random_valid_case_2():
    _close(solve([3.95], [3.6], [[5.8841]]), -1.8154748405284293)


def test_07_random_valid_case_3():
    _close(solve([3.32], [0.67], [[1.0049]]), -4.415511319272805)


def test_08_random_valid_case_4():
    _close(solve([1.35], [0.54], [[2.0404]]), -1.4362887653068979)


def test_09_random_valid_case_5():
    _close(solve([-0.39], [-4.81], [[1.0841]]), -9.969737000723178)


def test_10_random_valid_case_6():
    _close(solve([-4.34], [2.66], [[1.3599999999999999]]), -19.087386765431596)


def test_11_random_valid_case_7():
    _close(solve([-4.47], [-1.85], [[2.2544000000000004]]), -2.8478254607371953)


def test_12_random_valid_case_8():
    _close(solve([1.49, 3.89], [0.3, 2.55], [[6.5704, 1.5042], [1.5042, 2.5141]]), -3.5368658015081382)
