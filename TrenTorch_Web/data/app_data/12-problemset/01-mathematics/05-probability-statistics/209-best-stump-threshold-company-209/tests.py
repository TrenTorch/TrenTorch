"""Tests for the stump threshold: midpoint of consecutive distinct sorted values minimizing weighted Gini impurity."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example_perfect_split():
    assert solve([1, 2, 3, 4], [0, 0, 1, 1]) == pytest.approx(2.5)


def test_02_reversed_input_order():
    assert solve([4, 3, 2, 1], [1, 1, 0, 0]) == pytest.approx(2.5)


def test_03_all_same_label_prefers_smallest_threshold():
    assert solve([1, 2, 3], [0, 0, 0]) == pytest.approx(1.5)


def test_04_singleton_raises():
    with pytest.raises(ValueError):
        solve([5.0], [1])


def test_05_repeated_values_use_midpoint_between_groups():
    assert solve([1, 1, 2, 2], [0, 0, 1, 1]) == pytest.approx(1.5)


def test_06_negative_values():
    assert solve([-3, -2, -1, 0], [1, 1, 0, 0]) == pytest.approx(-1.5)


def test_07_mixed_signs():
    assert solve([-2, 0, 2], [0, 1, 1]) == pytest.approx(-1.0)


def test_08_tiny_magnitudes():
    assert solve([1e-9, 2e-9, 3e-9], [0, 1, 1]) == pytest.approx(1.5e-9)


def test_09_large_magnitudes():
    assert solve([1e6, 2e6], [0, 1]) == pytest.approx(1.5e6)


def test_10_zero_inputs():
    assert solve([0.0, 0.0, 1.0, 1.0], [0, 0, 1, 1]) == pytest.approx(0.5)


def test_11_empty_input_raises():
    with pytest.raises(ValueError):
        solve([], [])
