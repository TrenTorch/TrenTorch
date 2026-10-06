"""Contract tests for this authored problem."""
import numpy as np
import pytest

from _load import load_solution

solve = load_solution(__file__).solve

def _assert_equal(actual, expected):
    if isinstance(actual, np.ndarray):
        np.testing.assert_allclose(actual, np.asarray(expected), atol=1e-6, rtol=1e-6)
    elif isinstance(actual, tuple):
        assert isinstance(expected, tuple) and len(actual) == len(expected)
        for left, right in zip(actual, expected):
            _assert_equal(left, right)
    elif isinstance(actual, list):
        assert isinstance(expected, (list, tuple)) and len(actual) == len(expected)
        for left, right in zip(actual, expected):
            _assert_equal(left, right)
    elif isinstance(actual, dict):
        assert isinstance(expected, dict) and actual.keys() == expected.keys()
        for key in actual:
            _assert_equal(actual[key], expected[key])
    elif isinstance(actual, (float, np.floating)) or isinstance(expected, float):
        assert actual == pytest.approx(expected, rel=1e-6, abs=1e-6)
    else:
        assert actual == expected

def test_visible_example_1():
    _assert_equal(solve(2, seed=0), [{"lr": 0.0035305856304085927, "depth": 6}, {"lr": 1.4584585665958855e-05, "depth": 4}])

def test_visible_example_2():
    _assert_equal(solve(1, seed=7), [{"lr": 0.0031650594102156206, "depth": 7}])


def test_properties_ranges_and_count():
    configs = solve(50, seed=3)
    assert len(configs) == 50
    assert all(1e-5 <= c["lr"] <= 1e-1 for c in configs)
    assert all(2 <= c["depth"] <= 9 for c in configs)


def test_same_seed_is_repeatable():
    assert solve(5, seed=11) == solve(5, seed=11)
