"""
pytest data/app_data/02-math-and-statistics/01-linear-algebra/13-qr-decomposition/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

qr_decompose = load_solution(
    "02-math-and-statistics/01-linear-algebra/13-qr-decomposition"
).qr_decompose


# ---- 1-2: basic correctness ----


def test_1_qr_reconstructs_a_2x2_matrix():
    A = np.array([[1.0, 1.0], [0.0, 1.0]])
    Q, R = qr_decompose(A)
    np.testing.assert_allclose(Q @ R, A, atol=1e-10)


def test_2_q_columns_are_orthonormal():
    A = np.array([[1.0, 1.0], [0.0, 1.0]])
    Q, _ = qr_decompose(A)
    np.testing.assert_allclose(Q.T @ Q, np.eye(2), atol=1e-10)


# ---- shape / general-case coverage ----


def test_3_r_is_upper_triangular():
    A = np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0]])
    _, R = qr_decompose(A)
    for i in range(3):
        for j in range(i):
            assert np.isclose(R[i, j], 0.0)


def test_4_3x3_reconstruction():
    A = np.array([[1.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0]])
    Q, R = qr_decompose(A)
    np.testing.assert_allclose(Q @ R, A, atol=1e-10)


def test_5_tall_rectangular_matrix():
    A = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    Q, R = qr_decompose(A)
    assert Q.shape == (3, 2)
    assert R.shape == (2, 2)
    np.testing.assert_allclose(Q @ R, A, atol=1e-10)


# ---- edge cases ----


def test_6_identity_matrix_decomposes_to_itself():
    A = np.eye(3)
    Q, R = qr_decompose(A)
    np.testing.assert_allclose(Q, np.eye(3), atol=1e-10)
    np.testing.assert_allclose(R, np.eye(3), atol=1e-10)


def test_7_already_orthonormal_columns():
    A = np.array([[1.0, 0.0], [0.0, 1.0]])
    Q, R = qr_decompose(A)
    np.testing.assert_allclose(Q, A, atol=1e-10)
    np.testing.assert_allclose(R, np.eye(2), atol=1e-10)


def test_8_input_array_is_not_mutated():
    A = np.array([[1.0, 1.0], [0.0, 1.0]])
    original = A.copy()
    qr_decompose(A)
    np.testing.assert_array_equal(A, original)


# ---- mutation-catching ----


def test_9_r_diagonal_is_positive_norm_not_zero():
    # A wrong implementation that never actually normalizes (or divides
    # by the wrong quantity) would produce a non-unit-length Q column,
    # detectable via Q's columns failing to have norm 1.
    A = np.array([[3.0, 1.0], [4.0, 0.0]])
    Q, R = qr_decompose(A)
    np.testing.assert_allclose(np.linalg.norm(Q[:, 0]), 1.0, atol=1e-10)
    np.testing.assert_allclose(np.linalg.norm(Q[:, 1]), 1.0, atol=1e-10)


def test_10_r_correctly_captures_projection_not_just_reconstruction():
    # Checks R's specific entries against a hand-traced computation,
    # catching an implementation that reconstructs A correctly by some
    # other means without R actually holding the projection coefficients.
    A = np.array([[3.0, 1.0], [4.0, 0.0]])
    Q, R = qr_decompose(A)
    # First column: norm 5, so Q[:,0] = [0.6, 0.8], R[0,0] = 5.
    np.testing.assert_allclose(Q[:, 0], [0.6, 0.8], atol=1e-10)
    assert np.isclose(R[0, 0], 5.0)
    # R[0,1] = Q[:,0] . A[:,1] = 0.6*1 + 0.8*0 = 0.6
    assert np.isclose(R[0, 1], 0.6, atol=1e-10)


# ---- independent oracle ----


def test_11_matches_numpy_qr_up_to_sign():
    # np.linalg.qr can flip signs on Q's columns (and correspondingly on
    # R's rows) relative to plain Gram-Schmidt, so compare reconstruction
    # and orthonormality rather than exact entries against the library.
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    Q, R = qr_decompose(A)
    np.testing.assert_allclose(Q @ R, A, atol=1e-10)
    np.testing.assert_allclose(Q.T @ Q, np.eye(2), atol=1e-10)
