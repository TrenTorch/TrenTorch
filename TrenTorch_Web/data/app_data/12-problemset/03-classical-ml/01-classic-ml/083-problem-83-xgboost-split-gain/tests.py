"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    assert solve(3.0, 2.0, -1.0, 1.0, 2.0, 3.0, 1.0) == pytest.approx(1.25)


def test_02_no_gain_when_children_equal_parent():
    assert solve(2.0, 1.0, 2.0, 1.0, 4.0, 2.0, 0.0) == pytest.approx(0.0)


def test_03_zero_inputs_give_zero_gain():
    assert solve(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0) == pytest.approx(0.0)


def test_04_negative_gradients_are_squared():
    assert solve(-3.0, 2.0, 3.0, 2.0, 0.0, 4.0, 0.0) == pytest.approx(0.5 * (4.5 + 4.5 - 0.0))


def test_05_singleton_boundary():
    assert solve(1.0, 1.0, 0.0, 1.0, 1.0, 2.0, 0.0) == pytest.approx(0.25)
