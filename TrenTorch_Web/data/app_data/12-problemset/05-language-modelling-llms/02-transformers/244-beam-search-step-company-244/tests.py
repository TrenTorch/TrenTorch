"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    out = solve([([1], -1.0)], [-0.5, -2.0], 2)
    assert out == [([1, 0], -1.5), ([1, 1], -3.0)]


def test_02_width_one_keeps_best():
    assert solve([([1], -1.0)], [-0.5, -2.0], 1) == [([1, 0], -1.5)]


def test_03_ties_break_by_sequence():
    out = solve([([0], 0.0), ([1], 0.0)], [0.0, -1.0], 3)
    assert out == [([0, 0], 0.0), ([1, 0], 0.0), ([0, 1], -1.0)]


def test_04_empty_beams_gives_empty():
    assert solve([], [0.0, -1.0], 2) == []
