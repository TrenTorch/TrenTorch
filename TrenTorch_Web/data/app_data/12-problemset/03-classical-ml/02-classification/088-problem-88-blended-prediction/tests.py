"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_unweighted_mean_over_models():
    np.testing.assert_allclose(solve([[1.0, 2.0], [3.0, 4.0]], [1.0, 1.0]), [2.0, 3.0])


def test_02_weighted_average_over_models():
    np.testing.assert_allclose(solve([[1.0, 2.0], [3.0, 4.0]], [1.0, 3.0]), [2.5, 3.5])


def test_03_zero_predictions():
    np.testing.assert_allclose(solve([[0.0, 0.0], [0.0, 0.0]], [1.0, 1.0]), [0.0, 0.0])


def test_04_single_model_is_identity():
    np.testing.assert_allclose(solve([[5.0, -1.0]], [2.0]), [5.0, -1.0])
