"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
determinant = _module.determinant
is_invertible = _module.is_invertible
safe_inverse = _module.safe_inverse
verify_inverse = _module.verify_inverse


def test_determinant_correctness_for_known_2x2_case():
    matrix = np.array([[1, 2], [3, 4]])
    assert np.isclose(determinant(matrix), -2.0)


def test_is_invertible_correctly_identifies_singular_matrix():
    singular = np.array([[1, 2], [2, 4]])
    assert is_invertible(singular) is False


def test_is_invertible_correctly_identifies_invertible_matrix():
    matrix = np.array([[1, 2], [3, 4]])
    assert is_invertible(matrix) is True


def test_safe_inverse_returns_none_for_singular_matrix_without_raising():
    singular = np.array([[1, 2], [2, 4]])
    assert safe_inverse(singular) is None


def test_verify_inverse_confirms_genuine_inverse():
    matrix = np.array([[1, 2], [3, 4]])
    inverse = safe_inverse(matrix)
    assert verify_inverse(matrix, inverse) is True


def test_verify_inverse_correctly_rejects_non_inverse():
    matrix = np.array([[1, 2], [3, 4]])
    assert verify_inverse(matrix, matrix) is False
