"""
pytest data/app_data/00-math-and-statistics/01-linear-algebra/06-eigenvalues-eigenvectors/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/01-linear-algebra/{Path(__file__).resolve().parent.name}"
)
eigen_decomposition = _module.eigen_decomposition
verify_eigenpair = _module.verify_eigenpair


def test_eigenvalues_of_identity_are_all_one():
    eigenvalues, _ = eigen_decomposition(np.eye(3))
    assert np.allclose(eigenvalues, [1.0, 1.0, 1.0])


def test_eigenvalues_of_diagonal_matrix_are_its_diagonal_entries():
    a = np.diag([2.0, 5.0, 1.0])
    eigenvalues, _ = eigen_decomposition(a)
    assert np.allclose(sorted(eigenvalues), [1.0, 2.0, 5.0])


def test_eigenvectors_are_unit_length():
    a = np.array([[2.0, 1.0], [1.0, 2.0]])
    _, eigenvectors = eigen_decomposition(a)
    for i in range(eigenvectors.shape[1]):
        assert np.isclose(np.linalg.norm(eigenvectors[:, i]), 1.0)


def test_every_returned_pair_satisfies_the_eigenvalue_equation():
    a = np.array([[2.0, 1.0], [1.0, 2.0]])
    eigenvalues, eigenvectors = eigen_decomposition(a)
    for i in range(len(eigenvalues)):
        assert verify_eigenpair(a, eigenvalues[i], eigenvectors[:, i])


def test_eigenvalues_sum_to_the_trace():
    # A well-known invariant: sum of eigenvalues == trace (sum of
    # diagonal entries), for any square matrix.
    a = np.array([[4.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]])
    eigenvalues, _ = eigen_decomposition(a)
    assert np.isclose(np.sum(eigenvalues), np.trace(a))


def test_verify_eigenpair_rejects_a_non_eigenvector():
    a = np.array([[2.0, 0.0], [0.0, 3.0]])
    # [1, 1] is not an eigenvector of this matrix (it would need to be
    # scaled by different amounts in each coordinate).
    not_an_eigenvector = np.array([1.0, 1.0])
    assert not verify_eigenpair(a, 2.0, not_an_eigenvector)
    assert not verify_eigenpair(a, 3.0, not_an_eigenvector)


def test_verify_eigenpair_accepts_known_eigenpair_of_diagonal_matrix():
    a = np.diag([2.0, 3.0])
    assert verify_eigenpair(a, 2.0, np.array([1.0, 0.0]))
    assert verify_eigenpair(a, 3.0, np.array([0.0, 1.0]))


def test_verify_eigenpair_rejects_wrong_eigenvalue_for_a_correct_eigenvector():
    # Directly targets a mutant that only checks direction (that A @ v
    # is parallel to v) without checking the scale factor matches the
    # claimed eigenvalue.
    a = np.diag([2.0, 3.0])
    correct_eigenvector = np.array([1.0, 0.0])
    wrong_eigenvalue = 5.0
    assert not verify_eigenpair(a, wrong_eigenvalue, correct_eigenvector)
