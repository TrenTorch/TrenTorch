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


def test_01_basic_example():
    _close(solve([0.5, 0.5]), 1.0)


def test_02_one_page_dominates():
    _close(solve([0.99, 0.01]), -(0.99 * math.log2(0.99) + 0.01 * math.log2(0.01)))


def test_03_three_buttons():
    _close(solve([0.5, 0.3, 0.2]), -(0.5 * math.log2(0.5) + 0.3 * math.log2(0.3) + 0.2 * math.log2(0.2)))


def test_04_uniform_three():
    _close(solve([1 / 3, 1 / 3, 1 / 3]), math.log2(3))


def test_05_no_clicks_on_some_slots():
    _close(solve([0.0, 0.0, 1.0]), 0.0)


def test_06_uniform_sixteen():
    _close(solve([1 / 16] * 16), 4.0)


def test_07_numpy_input():
    _close(solve(np.array([0.25, 0.75])), -(0.25 * math.log2(0.25) + 0.75 * math.log2(0.75)))


def test_08_order_does_not_matter():
    _close(solve([0.2, 0.5, 0.3]), -(0.5 * math.log2(0.5) + 0.3 * math.log2(0.3) + 0.2 * math.log2(0.2)))


def test_09_empty_raises():
    with pytest.raises(ValueError):
        solve([])


def test_10_does_not_sum_to_one_raises():
    with pytest.raises(ValueError):
        solve([0.4, 0.4])


def test_11_negative_probability_raises():
    with pytest.raises(ValueError):
        solve([1.2, -0.2])
