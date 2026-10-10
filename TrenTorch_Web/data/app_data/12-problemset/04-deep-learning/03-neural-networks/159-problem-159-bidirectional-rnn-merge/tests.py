"""Tests with expected values computed from an independently written reference, not from the solution."""
import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_basic_example():
    np.testing.assert_allclose(solve([[1.0, 2.0]], [[3.0, 4.0]]), [[1.0, 2.0, 3.0, 4.0]])


def test_exact_zero_inputs():
    np.testing.assert_allclose(solve([[0.0, 0.0]], [[0.0, 0.0]]), [[0.0, 0.0, 0.0, 0.0]])


def test_all_negative_values():
    np.testing.assert_allclose(solve([[-1.0, -2.0]], [[-3.0, -4.0]]), [[-1.0, -2.0, -3.0, -4.0]])


def test_all_positive_values():
    np.testing.assert_allclose(solve([[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]), [[1.0, 2.0, 5.0, 6.0], [3.0, 4.0, 7.0, 8.0]])


def test_singleton_boundary():
    np.testing.assert_allclose(solve([[1.0]], [[2.0]]), [[1.0, 2.0]])


def test_repeated_values():
    np.testing.assert_allclose(solve([[2.0, 2.0]], [[2.0, 2.0]]), [[2.0, 2.0, 2.0, 2.0]])


def test_mixed_signs():
    np.testing.assert_allclose(solve([[-1.0, 1.0]], [[1.0, -1.0]]), [[-1.0, 1.0, 1.0, -1.0]])


def test_tiny_magnitudes():
    np.testing.assert_allclose(solve([[1e-08]], [[2e-08]]), [[1e-08, 2e-08]])


def test_large_magnitudes():
    np.testing.assert_allclose(solve([[100000000.0]], [[200000000.0]]), [[100000000.0, 200000000.0]])


def test_parameter_nudge():
    forward = [[1.0, 2.0]]
    np.testing.assert_allclose(solve(forward, [[3.0, 4.0]])[0, :2], np.array(forward[0]))


def test_reversed_order():
    forward = [[1.0], [2.0]]
    backward = [[3.0], [4.0]]
    np.testing.assert_allclose(solve(forward, backward)[::-1], solve(forward[::-1], backward[::-1]))


def test_mismatched_leading_dimensions_raise():
    with pytest.raises(ValueError):
        solve([[1.0, 2.0]], [[1.0], [2.0]])


def test_large_n_1e5():
    forward = np.ones((100000, 1))
    backward = np.ones((100000, 1)) * 2
    out = solve(forward, backward)
    assert out.shape == (100000, 2)
    np.testing.assert_allclose(out[0], [1.0, 2.0])


def test_empty_or_degenerate_input():
    out = solve(np.zeros((0, 1)), np.zeros((0, 1)))
    assert out.shape == (0, 2)
