"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    labels, C2 = solve(np.array([[0.0, 0.0], [1.0, 0.0], [10.0, 0.0]]), np.array([[0.0, 0.0], [10.0, 0.0]]))
    np.testing.assert_array_equal(labels, [0, 0, 1])
    np.testing.assert_allclose(C2, [[0.5, 0.0], [10.0, 0.0]])


def test_02_empty_cluster_keeps_previous_centroid():
    labels, C2 = solve(np.array([[0.0, 0.0], [1.0, 0.0]]), np.array([[0.0, 0.0], [100.0, 100.0]]))
    np.testing.assert_array_equal(labels, [0, 0])
    np.testing.assert_allclose(C2, [[0.5, 0.0], [100.0, 100.0]])


def test_03_point_on_centroid_keeps_label():
    labels, _ = solve(np.array([[5.0, 5.0]]), np.array([[5.0, 5.0], [0.0, 0.0]]))
    np.testing.assert_array_equal(labels, [0])
