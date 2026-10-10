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
    _close(solve([0.1, 0.7, 0.2]), 1)


def test_02_readme_example_2():
    _close(solve([1.0, 3.0, 3.0]), 1)


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([])


def test_04_random_valid_case_1():
    _close(solve([1.75, 1.76, 1.8, 4.42, 0.16, 1.99, 1.34, 4.79]), 7)


def test_05_random_valid_case_2():
    _close(solve([0.81, -4.9, -2.62, 1.71, -1.79, 4.9, 2.06, -3.7]), 5)


def test_06_random_valid_case_3():
    _close(solve([-3.95, 2.63, -1.7, 4.1, -0.74, 3.04, 0.26, 3.72]), 3)


def test_07_random_valid_case_4():
    _close(solve([-4.08, 2.59, 3.3, 2.29, 1.8, -1.22, -1.53, -2.83]), 2)


def test_08_random_valid_case_5():
    _close(solve([-0.51, 0.06, 1.64, -4.78, 3.93, 1.77, 0.46, -4.1]), 4)


def test_09_random_valid_case_6():
    _close(solve([-3.1, 4.98, 3.16, -1.95, -0.81, 4.93, 0.82, 0.32]), 1)


def test_10_random_valid_case_7():
    _close(solve([4.42, 3.95, 1.43, 4.54, 2.99, -1.97, 4.45, -2.36]), 3)


def test_11_random_valid_case_8():
    _close(solve([-0.98, 1.27, -0.14, 0.19, 0.81, 3.61, 0.59, 4.03]), 7)


def test_12_random_valid_case_9():
    _close(solve([4.5, 4.82, -2.33, 4.54, -3.28, 3.24, -2.19, 3.94]), 1)
