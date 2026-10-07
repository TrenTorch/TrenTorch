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


def test_01_fair_coin():
    _close(solve([0.5, 0.5]), 1.0)


def test_02_certain_outcome():
    _close(solve([1.0, 0.0]), 0.0)


def test_03_uniform_four():
    _close(solve([0.25, 0.25, 0.25, 0.25]), 2.0)


def test_04_dyadic_distribution():
    _close(solve([0.5, 0.25, 0.25]), 1.5)


def test_05_biased_coin():
    _close(solve([0.7, 0.3]), -(0.7 * math.log2(0.7) + 0.3 * math.log2(0.3)))


def test_06_single_outcome():
    _close(solve([1.0]), 0.0)


def test_07_uniform_ten():
    _close(solve([0.1] * 10), math.log2(10))


def test_08_zeros_are_ignored():
    _close(solve([0.0, 0.5, 0.0, 0.5]), 1.0)


def test_09_skewed_three():
    _close(solve([0.9, 0.05, 0.05]), -(0.9 * math.log2(0.9) + 2 * 0.05 * math.log2(0.05)))


def test_10_uniform_eight():
    _close(solve([1 / 8] * 8), 3.0)


def test_11_empty_raises():
    with pytest.raises(ValueError):
        solve([])


def test_12_does_not_sum_to_one_raises():
    with pytest.raises(ValueError):
        solve([0.5, 0.6])


def test_13_negative_probability_raises():
    with pytest.raises(ValueError):
        solve([-0.5, 1.5])


def test_14_two_dimensional_raises():
    with pytest.raises(ValueError):
        solve([[0.5, 0.5]])
