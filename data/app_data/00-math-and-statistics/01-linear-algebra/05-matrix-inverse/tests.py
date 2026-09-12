"""
pytest data/app_data/00-math-and-statistics/01-linear-algebra/05-matrix-inverse/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/01-linear-algebra/{Path(__file__).resolve().parent.name}")
determinant = _module.determinant
is_invertible = _module.is_invertible
matrix_inverse = _module.matrix_inverse


def test_determinant_of_identity_is_one():
    assert np.isclose(determinant(np.eye(3)), 1.0)


def test_determinant_matches_hand_computation():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    # 1*4 - 2*3 = -2
    assert np.isclose(determinant(a), -2.0)


def test_is_invertible_true_for_nonsingular_matrix():
    assert is_invertible(np.array([[1.0, 2.0], [3.0, 4.0]]))


def test_is_invertible_false_for_singular_matrix():
    # second row is a multiple of the first -- rank-deficient, det = 0
    a = np.array([[1.0, 2.0], [2.0, 4.0]])
    assert not is_invertible(a)


def test_matrix_inverse_matches_definition():
    a = np.array([[4.0, 7.0], [2.0, 6.0]])
    a_inv = matrix_inverse(a)
    assert np.allclose(a @ a_inv, np.eye(2), atol=1e-10)
    assert np.allclose(a_inv @ a, np.eye(2), atol=1e-10)


def test_matrix_inverse_of_identity_is_identity():
    assert np.allclose(matrix_inverse(np.eye(4)), np.eye(4))


def test_matrix_inverse_raises_on_singular_matrix():
    a = np.array([[1.0, 2.0], [2.0, 4.0]])
    with pytest.raises(np.linalg.LinAlgError):
        matrix_inverse(a)


def test_is_invertible_uses_a_tolerance_not_exact_equality():
    # Directly targets a mutant that checks `determinant(a) == 0.0`
    # exactly: a genuinely singular matrix's determinant, computed in
    # floating point, is very rarely a bit-exact zero.
    a = np.array([[1.0, 2.0], [2.0, 4.0000000001]])
    det = determinant(a)
    assert det != 0.0  # floating-point noise, not exactly zero
    assert not is_invertible(a)  # but still correctly flagged as singular
