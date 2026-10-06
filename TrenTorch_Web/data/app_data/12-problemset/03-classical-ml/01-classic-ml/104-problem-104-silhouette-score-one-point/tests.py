"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    assert solve([1.0, 3.0], [5.0, 7.0]) == pytest.approx(0.6)


def test_02_zero_distances_give_zero():
    assert solve([0.0], [0.0]) == pytest.approx(0.0)


def test_03_equal_distances_give_zero():
    assert solve([2.0], [2.0]) == pytest.approx(0.0)


def test_04_singleton_boundary():
    assert solve([1.0], [5.0]) == pytest.approx(0.8)


def test_05_point_closer_to_other_cluster_is_negative():
    assert solve([5.0], [1.0]) == pytest.approx(-0.8)
