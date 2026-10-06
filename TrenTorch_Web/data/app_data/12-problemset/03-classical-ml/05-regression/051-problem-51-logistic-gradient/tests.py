"""Executable tests: 2 visible examples + 11 targeted edge/performance cases.

The case names document the hidden-test categories. Expected values are materialized
from the reference implementation at authoring time; the agent should not have to
invent edge cases or expected outputs.
"""
import numpy as np
from numpy import array
import pytest
from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve

def _assert_close(actual, expected):
    if isinstance(actual, tuple) and isinstance(expected, tuple):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            _assert_close(a, e)
        return
    a, e = np.asarray(actual), np.asarray(expected)
    if a.dtype.kind in "biufc" and e.dtype.kind in "biufc":
        np.testing.assert_allclose(a, e, atol=1e-6, rtol=1e-6, equal_nan=True)
    else:
        assert a.tolist() == e.tolist()


def test_01_basic_example():
    args = [[[1.0, 2.0], [2.0, 1.0]], [0, 1], [0.2, 0.7]]
    actual = solve(*args)
    expected = (array([0.1662693 , 0.70714844]), 0.29113924536452107)
    _assert_close(actual, expected)

def test_02_exact_zero_inputs():
    args = [[[1.0, 2.0], [2.0, 1.0]], [0, 0], [0, 0]]
    actual = solve(*args)
    expected = (array([0.75, 0.75]), 0.5)
    _assert_close(actual, expected)

def test_03_all_negative_values():
    args = [[[1.0, 2.0], [2.0, 1.0]], [-1, -2], [-1.2, -1.7]]
    actual = solve(*args)
    expected = (array([2.5212784 , 2.01810305]), 1.5131271506191726)
    _assert_close(actual, expected)

def test_04_all_positive_values():
    args = [[[1.0, 2.0], [2.0, 1.0]], [1, 2], [1.2, 1.7]]
    actual = solve(*args)
    expected = (array([-1.0212784 , -0.51810305]), -0.5131271506191726)
    _assert_close(actual, expected)

def test_05_singleton_boundary():
    args = [[[1.0, 2.0]], [0], [0.2]]
    with pytest.raises(ValueError):
        solve(*args)

def test_06_repeated_values():
    args = [[[1.0, 2.0], [2.0, 1.0]], [2, 2], [2, 2]]
    actual = solve(*args)
    expected = (array([-1.50370893, -1.50370893]), -1.0024726231566348)
    _assert_close(actual, expected)

def test_07_mixed_signs():
    args = [[[1.0, 2.0], [2.0, 1.0]], [-2.0, 2.0], [-2.0, 2.0]]
    actual = solve(*args)
    expected = (array([-0.44039854,  1.94039854]), 0.4999999999999999)
    _assert_close(actual, expected)

def test_08_tiny_magnitudes():
    args = [[[1.0, 2.0], [2.0, 1.0]], [1e-08, 1e-08], [1e-08, 1e-08]]
    actual = solve(*args)
    expected = (array([0.75, 0.75]), 0.49999999750000007)
    _assert_close(actual, expected)

def test_09_large_magnitudes():
    args = [[[1.0, 2.0], [2.0, 1.0]], [1000.0, 1000.0], [1000.0, 1000.0]]
    actual = solve(*args)
    expected = (array([-1498.5, -1498.5]), -999.0)
    _assert_close(actual, expected)

def test_10_parameter_nudge():
    args = [[[1.0, 2.0], [2.0, 1.0]], [0, 1], [0.2, 0.7]]
    actual = solve(*args)
    expected = (array([0.1662693 , 0.70714844]), 0.29113924536452107)
    _assert_close(actual, expected)

def test_11_reversed_order():
    args = [[[1.0, 2.0], [2.0, 1.0]], [1, 0], [0.7, 0.2]]
    actual = solve(*args)
    expected = (array([0.70714844, 0.1662693 ]), 0.29113924536452107)
    _assert_close(actual, expected)


def test_13_empty_or_degenerate_input():
    args = [[[1.0, 2.0], [2.0, 1.0]], [], [0.2, 0.7]]
    with pytest.raises(ValueError):
        solve(*args)
