"""
pytest data/app_data/00-math-and-statistics/01-linear-algebra/08-positive-definite-matrices/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/01-linear-algebra/{Path(__file__).resolve().parent.name}"
)
is_symmetric = _module.is_symmetric
quadratic_form = _module.quadratic_form
is_positive_definite = _module.is_positive_definite


def test_is_symmetric_true_for_symmetric_matrix():
    a = np.array([[1.0, 2.0], [2.0, 3.0]])
    assert is_symmetric(a)


def test_is_symmetric_false_for_asymmetric_matrix():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert not is_symmetric(a)


def test_quadratic_form_matches_hand_computation():
    a = np.eye(2)
    x = np.array([3.0, 4.0])
    # x^T I x = x . x = 9 + 16 = 25
    assert np.isclose(quadratic_form(a, x), 25.0)


def test_identity_matrix_is_positive_definite():
    assert is_positive_definite(np.eye(3))


def test_negative_identity_is_not_positive_definite():
    assert not is_positive_definite(-np.eye(3))


def test_diagonal_matrix_with_mixed_signs_is_not_positive_definite():
    a = np.diag([2.0, -1.0, 3.0])
    assert not is_positive_definite(a)


def test_asymmetric_matrix_is_never_positive_definite():
    # Positive-definiteness is only defined for symmetric matrices --
    # even one whose "eigenvalues" (in the general, possibly-complex
    # sense) all have positive real part is excluded here.
    a = np.array([[2.0, 1.0], [0.0, 3.0]])
    assert not is_symmetric(a)
    assert not is_positive_definite(a)


def test_positive_definiteness_matches_quadratic_form_sign_on_many_directions():
    # The actual definition, sampled: for a genuinely positive-definite
    # matrix, the quadratic form must be positive along many random
    # directions, not just the coordinate axes.
    a = np.array([[2.0, 0.5], [0.5, 1.0]])
    assert is_positive_definite(a)
    rng = np.random.default_rng(0)
    for _ in range(20):
        x = rng.normal(size=2)
        if np.allclose(x, 0.0):
            continue
        assert quadratic_form(a, x) > 0.0


def test_is_positive_definite_rejects_positive_semi_definite_matrix():
    # Directly targets a mutant that checks eigenvalues >= 0 instead of
    # > 0: a rank-deficient matrix (one zero eigenvalue) is positive
    # SEMI-definite, not positive definite.
    a = np.array([[1.0, 1.0], [1.0, 1.0]])  # eigenvalues: 0 and 2
    eigenvalues = np.linalg.eigvalsh(a)
    assert np.any(np.isclose(eigenvalues, 0.0))
    assert not is_positive_definite(a)
