"""
pytest data/app_data/02-math-and-statistics/01-linear-algebra/10-gaussian-elimination/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/01-linear-algebra/10-gaussian-elimination")
gaussian_eliminate = _module.gaussian_eliminate
back_substitute = _module.back_substitute


# ---- 1-2: basic correctness ----


def test_1_solves_a_2x2_system():
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])
    U, c = gaussian_eliminate(A, b)
    x = back_substitute(U, c)
    np.testing.assert_allclose(x, [2.0, 1.0], atol=1e-10)


def test_2_u_is_upper_triangular():
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])
    U, _ = gaussian_eliminate(A, b)
    assert np.isclose(U[1, 0], 0.0)


# ---- shape / general-case coverage ----


def test_3_solves_the_worked_3x3_example():
    A = np.array([[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]])
    b = np.array([8.0, -11.0, -3.0])
    U, c = gaussian_eliminate(A, b)
    x = back_substitute(U, c)
    np.testing.assert_allclose(x, [2.0, 3.0, -1.0], atol=1e-8)


def test_4_solution_satisfies_original_system():
    A = np.array([[3.0, 2.0], [1.0, 4.0]])
    b = np.array([7.0, 9.0])
    U, c = gaussian_eliminate(A, b)
    x = back_substitute(U, c)
    np.testing.assert_allclose(A @ x, b, atol=1e-10)


# ---- edge cases ----


def test_5_already_upper_triangular_system():
    A = np.array([[2.0, 3.0], [0.0, 5.0]])
    b = np.array([8.0, 10.0])
    U, c = gaussian_eliminate(A, b)
    np.testing.assert_allclose(U, A, atol=1e-10)
    np.testing.assert_allclose(c, b, atol=1e-10)
    x = back_substitute(U, c)
    np.testing.assert_allclose(A @ x, b, atol=1e-10)


def test_6_identity_system_returns_b_directly():
    A = np.eye(3)
    b = np.array([1.0, 2.0, 3.0])
    U, c = gaussian_eliminate(A, b)
    x = back_substitute(U, c)
    np.testing.assert_allclose(x, b, atol=1e-10)


def test_7_input_arrays_are_not_mutated():
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])
    A_original, b_original = A.copy(), b.copy()
    gaussian_eliminate(A, b)
    np.testing.assert_array_equal(A, A_original)
    np.testing.assert_array_equal(b, b_original)


# ---- mutation-catching ----


def test_8_b_is_transformed_in_lockstep_with_a():
    # A wrong implementation eliminating A but forgetting to update b
    # correspondingly would produce a c that doesn't solve to the right x.
    A = np.array([[1.0, 1.0], [2.0, 5.0]])
    b = np.array([6.0, 4.0])  # solution: x + y = 6, 2x + 5y = 4 -> x=34/3... use exact:
    U, c = gaussian_eliminate(A, b)
    x = back_substitute(U, c)
    np.testing.assert_allclose(A @ x, b, atol=1e-8)


def test_9_back_substitution_uses_already_solved_variables():
    # A wrong implementation solving each x_i independently (ignoring
    # later variables' contributions) would fail on a genuinely coupled
    # triangular system like this one.
    U = np.array([[2.0, 3.0, 1.0], [0.0, 4.0, 2.0], [0.0, 0.0, 5.0]])
    c = np.array([10.0, 16.0, 10.0])
    x = back_substitute(U, c)
    np.testing.assert_allclose(U @ x, c, atol=1e-10)


# ---- independent oracle ----


def test_10_matches_numpy_linalg_solve():
    A = np.array([[4.0, 3.0, 2.0], [1.0, 5.0, 1.0], [2.0, 1.0, 6.0]])
    b = np.array([11.0, 12.0, 15.0])
    U, c = gaussian_eliminate(A, b)
    x = back_substitute(U, c)
    expected = np.linalg.solve(A, b)
    np.testing.assert_allclose(x, expected, atol=1e-8)
