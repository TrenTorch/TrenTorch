"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[3.0, 0.0], [0.0, 1.0]]), [1.0, 1.9403252174826334e-48], atol=1e-6)


def test_all_positive_values():
    np.testing.assert_allclose(solve([[5.0, 0.0], [0.0, 1.0]]), [1.0, 1.2676506002282294e-70], atol=1e-6)


def test_all_negative_values():
    np.testing.assert_allclose(solve([[-5.0, 0.0], [0.0, -1.0]]), [1.0, 1.2676506002282294e-70], atol=1e-6)


def test_repeated_values():
    np.testing.assert_allclose(solve([[2.0, 0.0], [0.0, 2.0]]), [0.7071067811865476, 0.7071067811865476], atol=1e-6)


def test_mixed_signs():
    np.testing.assert_allclose(solve([[3.0, 0.0], [0.0, -2.0]]), [1.0, 2.45965442657983e-18], atol=1e-6)


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[1e-08, 0.0], [0.0, 1e-09]]), [1.0, 1.0000000000000047e-100], atol=1e-6)


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[100000000.0, 0.0], [0.0, 100.0]]), [1.0, 0.0], atol=1e-6)


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[0.0, 0.0], [0.0, 0.0]]), [0.0, 0.0])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[7.0]]), [1.0])


def test_parameter_nudge():
    A = [[2.0, 1.0], [1.0, 2.0]]
    np.testing.assert_allclose(solve(A, steps=1), solve(A, steps=50), atol=1e-6)


def test_reversed_order():
    A = [[5.0, 0.0], [0.0, 1.0]]
    B = [[1.0, 0.0], [0.0, 5.0]]
    np.testing.assert_allclose(solve(A), solve(B)[::-1], atol=1e-6)


@pytest.mark.skip(reason="Not applicable: a 1e5 x 1e5 dense matrix cannot be materialised")
def test_large_n_1e5():
    pass


def test_empty_or_degenerate_input():
    assert solve(np.zeros((0, 0))).shape == (0,)
