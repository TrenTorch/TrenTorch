"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
solve_and_verify = _module.solve_and_verify


def test_correctly_identifies_unsolvable_singular_system():
    singular = np.array([[1.0, 2.0], [2.0, 4.0]])
    b = np.array([1.0, 2.0])
    result = solve_and_verify(singular, b)
    assert result["is_solvable"] is False
    assert result["solution"] is None
    assert result["residual_norm"] is None


def test_correct_solution_for_solvable_system_2x2():
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])
    result = solve_and_verify(A, b)
    assert result["is_solvable"] is True
    np.testing.assert_allclose(result["solution"], [2.0, 1.0])


def test_correct_solution_for_solvable_system_3x3():
    A = np.array([[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]])
    b = np.array([8.0, -11.0, -3.0])
    result = solve_and_verify(A, b)
    assert result["is_solvable"] is True
    np.testing.assert_allclose(A @ result["solution"], b, atol=1e-8)


def test_residual_norm_very_close_to_zero_for_correct_solution():
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])
    result = solve_and_verify(A, b)
    assert result["residual_norm"] < 1e-8


def test_residual_norm_correctly_reflects_wrong_solution():
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    correct_solution = np.array([2.0, 1.0])
    wrong_solution = np.array([0.0, 0.0])
    residual = A @ wrong_solution - (A @ correct_solution)
    assert np.linalg.norm(residual) > 1e-3


def test_return_structure_consistency():
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])
    solvable_result = solve_and_verify(A, b)
    assert set(solvable_result.keys()) == {"is_solvable", "solution", "residual_norm"}

    singular = np.array([[1.0, 2.0], [2.0, 4.0]])
    unsolvable_result = solve_and_verify(singular, b)
    assert set(unsolvable_result.keys()) == {"is_solvable", "solution", "residual_norm"}
