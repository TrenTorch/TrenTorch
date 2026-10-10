"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    assert solve(4.0, 3.0, 1.0) == pytest.approx(-1.0)


def test_02_zero_gradient_gives_zero_weight():
    assert solve(0.0, 2.0, 1.0) == pytest.approx(0.0)


def test_03_negative_gradient_gives_positive_weight():
    assert solve(-6.0, 2.0, 0.0) == pytest.approx(3.0)


def test_04_regularization_shrinks_weight():
    assert abs(solve(4.0, 3.0, 5.0)) < abs(solve(4.0, 3.0, 0.0))


def test_05_returns_float():
    assert isinstance(solve(1.0, 1.0, 1.0), float)
