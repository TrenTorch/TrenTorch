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
    _close(solve([3.0, 4.0]), 5.0)


def test_02_readme_example_2():
    _close(solve([3e200, 4e200]), 4.9999999999999995e+200)


def test_03_invalid_input_raises():
    with pytest.raises(ValueError):
        solve([])


def test_04_random_valid_case_1():
    _close(solve([4.06, 4.1, 2.47]), 6.2765038038704315)


def test_05_random_valid_case_2():
    _close(solve([1.04, -0.29, -2.97]), 3.1601582238868993)


def test_06_random_valid_case_3():
    _close(solve([3.13, -2.83, 4.84, 4.83]), 8.034942439121764)


def test_07_random_valid_case_4():
    _close(solve([-2.65, 4.96, 2.13, 1.01]), 6.09763068740638)


def test_08_random_valid_case_5():
    _close(solve([3.01, -0.03, -4.59, -2.3]), 5.951394794499857)


def test_09_random_valid_case_6():
    _close(solve([0.63, -2.87, -4.18, -3.97]), 6.470479116726983)


def test_10_random_valid_case_7():
    _close(solve([-0.19, 0.54, 2.62, 1.99, 3.86]), 5.104096394074078)


def test_11_random_valid_case_8():
    _close(solve([1.07, 1.41, -4.07, -4.7, -3.53]), 7.365378469569639)


def test_12_random_valid_case_9():
    _close(solve([3.23, -4.51, -3.16, -1.31, -0.1]), 6.518028843139619)
