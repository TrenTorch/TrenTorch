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
    _close(solve([3.0, 4.0], [1.0, 0.0]), 3.0)


def test_02_readme_example_2():
    _close(solve([3.0, 4.0], [3.0, 4.0]), 5.0)


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([], [1.0, -1.0])


def test_04_random_valid_case_1():
    _close(solve([4.85, 1.93, 0.04, 2.4], [2.74, 4.38, 0.47, 0.42]), 4.374706087379364)


def test_05_random_valid_case_2():
    _close(solve([-2.0, 0.44, -0.14, -1.03], [0.4, 1.0, 1.53, 2.68]), -1.0202134242401364)


def test_06_random_valid_case_3():
    _close(solve([4.72, -2.42, 3.24, 2.79], [1.17, 4.81, 4.93, -0.16]), 1.3464047937680539)


def test_07_random_valid_case_4():
    _close(solve([3.5, -2.74, -1.69, -1.97], [2.85, 0.53, 0.46, 4.95]), -0.3485971285427243)


def test_08_random_valid_case_5():
    _close(solve([3.16, 2.24, 2.89, 0.89], [-4.05, -2.64, 1.74, 2.69]), -1.9464835833269638)


def test_09_random_valid_case_6():
    _close(solve([4.31, 1.23, 3.48, 2.91], [-1.41, -1.55, -4.12, 1.11]), -4.016100745633034)


def test_10_random_valid_case_7():
    _close(solve([-2.07, -0.15, -1.44, 1.15], [1.09, 4.05, 3.86, 0.77]), -1.3103222920831499)


def test_11_random_valid_case_8():
    _close(solve([1.17, -4.89, -0.63, 1.1], [-2.76, -2.11, 1.27, 2.49]), 2.024578534781527)


def test_12_random_valid_case_9():
    _close(solve([-3.96, -0.91, 1.83, -1.94], [3.19, 2.85, 3.65, -1.6]), -0.9308880185024504)
