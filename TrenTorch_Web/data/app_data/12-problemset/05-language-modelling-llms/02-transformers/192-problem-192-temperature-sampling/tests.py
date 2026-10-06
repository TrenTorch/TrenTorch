"""Tests with hand-computed expected values (not taken from the solution)."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_01_basic_example():
    np.testing.assert_allclose(solve([1.0, 2.0], 1.0), [0.2689414213699951, 0.7310585786300049], atol=1e-9)


def test_02_higher_temperature_flattens():
    np.testing.assert_allclose(solve([1.0, 2.0], 2.0), [0.3775406687981454, 0.6224593312018546], atol=1e-9)


def test_03_equal_logits_are_uniform():
    np.testing.assert_allclose(solve([0.0, 0.0], 1.0), [0.5, 0.5])


def test_04_singleton_boundary():
    np.testing.assert_allclose(solve([5.0], 1.0), [1.0])


def test_05_large_logits_are_stable():
    np.testing.assert_allclose(solve([1000.0, 1000.0], 1.0), [0.5, 0.5])
