"""
pytest data/app_data/02-math-and-statistics/01-linear-algebra/11-lu-decomposition/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

lu_decompose = load_solution("02-math-and-statistics/01-linear-algebra/11-lu-decomposition").lu_decompose


# ---- 1-2: basic correctness ----


def test_1_lu_reconstructs_a_2x2_matrix():
    A = np.array([[4.0, 3.0], [6.0, 3.0]])
    L, U = lu_decompose(A)
    np.testing.assert_allclose(L @ U, A, atol=1e-10)


def test_2_u_is_upper_triangular():
    A = np.array([[4.0, 3.0], [6.0, 3.0]])
    _, U = lu_decompose(A)
    assert np.isclose(U[1, 0], 0.0)


# ---- shape / general-case coverage ----


def test_3_l_has_ones_on_the_diagonal():
    A = np.array([[2.0, 1.0, 1.0], [4.0, 3.0, 3.0], [8.0, 7.0, 9.0]])
    L, _ = lu_decompose(A)
    np.testing.assert_allclose(np.diag(L), [1.0, 1.0, 1.0])


def test_4_l_is_lower_triangular():
    A = np.array([[2.0, 1.0, 1.0], [4.0, 3.0, 3.0], [8.0, 7.0, 9.0]])
    L, _ = lu_decompose(A)
    for i in range(3):
        for j in range(i + 1, 3):
            assert np.isclose(L[i, j], 0.0)


def test_5_3x3_reconstruction():
    A = np.array([[2.0, 1.0, 1.0], [4.0, 3.0, 3.0], [8.0, 7.0, 9.0]])
    L, U = lu_decompose(A)
    np.testing.assert_allclose(L @ U, A, atol=1e-10)


# ---- edge cases ----


def test_6_identity_matrix_decomposes_to_itself():
    A = np.eye(3)
    L, U = lu_decompose(A)
    np.testing.assert_allclose(L, np.eye(3), atol=1e-10)
    np.testing.assert_allclose(U, np.eye(3), atol=1e-10)


def test_7_already_upper_triangular_matrix():
    A = np.array([[2.0, 3.0], [0.0, 5.0]])
    L, U = lu_decompose(A)
    np.testing.assert_allclose(L, np.eye(2), atol=1e-10)
    np.testing.assert_allclose(U, A, atol=1e-10)


def test_8_input_array_is_not_mutated():
    A = np.array([[4.0, 3.0], [6.0, 3.0]])
    original = A.copy()
    lu_decompose(A)
    np.testing.assert_array_equal(A, original)


# ---- mutation-catching ----


def test_9_u_actually_reflects_elimination_not_a_copy_of_a():
    # A wrong implementation that never actually eliminates (returns U=A,
    # L=identity) would pass reconstruction trivially but fail this check.
    A = np.array([[4.0, 3.0], [6.0, 3.0]])
    _, U = lu_decompose(A)
    assert not np.allclose(U, A)


def test_10_multiplier_sign_is_correct():
    # A wrong sign on the multiplier (adding instead of subtracting)
    # would still zero SOME entry but produce the wrong U and L.
    A = np.array([[2.0, 4.0], [1.0, 5.0]])
    L, U = lu_decompose(A)
    assert np.isclose(L[1, 0], 0.5)  # multiplier = 1/2
    np.testing.assert_allclose(U[1], [0.0, 3.0], atol=1e-10)


# ---- independent oracle ----


def test_11_matches_a_hand_computed_reference_case():
    # A = [[4, 3], [6, 3]]: multiplier = 6/4 = 1.5
    # U = [[4, 3], [0, 3 - 1.5*3]] = [[4, 3], [0, -1.5]]
    A = np.array([[4.0, 3.0], [6.0, 3.0]])
    L, U = lu_decompose(A)
    np.testing.assert_allclose(L, [[1.0, 0.0], [1.5, 1.0]], atol=1e-10)
    np.testing.assert_allclose(U, [[4.0, 3.0], [0.0, -1.5]], atol=1e-10)
