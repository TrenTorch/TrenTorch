"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    assert solve([[1, 2], [1, 3], [2, 3]]) == [(1, 2, 3)]


def test_02_no_matching_prefix_gives_empty():
    assert solve([[1, 2], [3, 4]]) == []


def test_03_singleton_gives_empty():
    assert solve([[1]]) == []


def test_04_order_does_not_matter():
    assert solve([[2, 3], [1, 3], [1, 2]]) == [(1, 2, 3)]


def test_05_three_way_join():
    assert solve([[1, 2], [1, 3], [1, 4]]) == [(1, 2, 3), (1, 2, 4), (1, 3, 4)]
