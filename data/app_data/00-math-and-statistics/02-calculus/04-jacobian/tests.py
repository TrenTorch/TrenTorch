"""
pytest data/app_data/00-math-and-statistics/02-calculus/04-jacobian/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/02-calculus/{Path(__file__).resolve().parent.name}")
jacobian = _module.jacobian


def _f(x):
    # f(x0, x1) = [x0^2, x0*x1, x1^3]
    return np.array([x[0] ** 2, x[0] * x[1], x[1] ** 3])


def test_jacobian_shape_matches_output_and_input_sizes():
    result = jacobian(_f, np.array([2.0, 3.0]))
    assert result.shape == (3, 2)


def test_jacobian_matches_hand_computation():
    # J = [[2x0, 0], [x1, x0], [0, 3x1^2]], at (2, 3):
    # [[4, 0], [3, 2], [0, 27]]
    result = jacobian(_f, np.array([2.0, 3.0]))
    expected = np.array([[4.0, 0.0], [3.0, 2.0], [0.0, 27.0]])
    assert np.allclose(result, expected, atol=1e-3)


def test_jacobian_of_scalar_valued_function_has_one_row():
    f = lambda x: x[0] ** 2 + x[1] ** 2
    result = jacobian(f, np.array([1.0, 2.0]))
    assert result.shape == (1, 2)
    assert np.allclose(result, [[2.0, 4.0]], atol=1e-3)


def test_jacobian_of_linear_map_equals_its_own_matrix():
    # For f(x) = W @ x, the Jacobian is exactly W, everywhere.
    w = np.array([[2.0, -1.0, 0.5], [0.0, 3.0, 1.0]])
    f = lambda x: w @ x
    result = jacobian(f, np.array([1.0, -2.0, 0.5]))
    assert np.allclose(result, w, atol=1e-3)


def test_jacobian_of_identity_function_is_the_identity_matrix():
    f = lambda x: x
    result = jacobian(f, np.array([1.0, 2.0, 3.0]))
    assert np.allclose(result, np.eye(3), atol=1e-3)


def test_jacobian_does_not_confuse_rows_and_columns():
    # Directly targets a mutant that transposes the result (writes to
    # result[j, :] instead of result[:, j]): using a rectangular (not
    # square) function makes a transpose bug produce the wrong shape
    # entirely, not just wrong values.
    f = lambda x: np.array([x[0] + x[1], x[0] - x[1], 2 * x[0]])  # R^2 -> R^3
    result = jacobian(f, np.array([1.0, 1.0]))
    assert result.shape == (3, 2)
    expected = np.array([[1.0, 1.0], [1.0, -1.0], [2.0, 0.0]])
    assert np.allclose(result, expected, atol=1e-3)
