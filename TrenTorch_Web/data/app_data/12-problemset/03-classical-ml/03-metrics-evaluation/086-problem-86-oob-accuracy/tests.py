"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    assert solve([0, 1, 1], [0, 0, 1]) == pytest.approx(2 / 3)


def test_02_all_zero_labels_match():
    assert solve([0, 0, 0], [0, 0, 0]) == pytest.approx(1.0)


def test_03_negative_labels():
    assert solve([-1, -2, -2], [-1, -1, -2]) == pytest.approx(2 / 3)


def test_04_all_wrong():
    assert solve([0, 1], [1, 0]) == pytest.approx(0.0)


def test_05_singleton_boundary():
    assert solve([0], [0]) == pytest.approx(1.0)
