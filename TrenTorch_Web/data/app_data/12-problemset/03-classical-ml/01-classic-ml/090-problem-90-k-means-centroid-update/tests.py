"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    np.testing.assert_allclose(solve([[0, 0], [2, 0], [10, 10]], [0, 0, 1], 2), [[1, 0], [10, 10]])


def test_02_empty_cluster_is_zero():
    np.testing.assert_allclose(solve([[0, 0], [2, 0], [4, 0]], [0, 0, 0], 2), [[2, 0], [0, 0]])


def test_03_negative_coordinates():
    np.testing.assert_allclose(solve([[-1, -1], [-3, -3]], [0, 0], 1), [[-2, -2]])


def test_04_singleton_point_is_its_own_centroid():
    np.testing.assert_allclose(solve([[7.0, 8.0]], [0], 1), [[7.0, 8.0]])
