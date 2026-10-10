"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


class _Seq:
    def __init__(self, values):
        self.values = list(values)

    def uniform(self, a, b):
        return self.values.pop(0)


def test_01_basic_example():
    assert solve(0.4, 0.0, 1.0, 2, _Seq([0.5, 0.25])) == 2


def test_02_depth_cap_zero():
    assert solve(0.4, 0.0, 1.0, 0, _Seq([])) == 0


def test_03_degenerate_interval_stops_immediately():
    assert solve(0.4, 0.5, 0.5, 5, _Seq([])) == 0


def test_04_single_split_when_x_is_above():
    assert solve(0.9, 0.0, 1.0, 1, _Seq([0.5])) == 1


def test_05_returns_int():
    assert isinstance(solve(0.4, 0.0, 1.0, 1, _Seq([0.5])), int)
