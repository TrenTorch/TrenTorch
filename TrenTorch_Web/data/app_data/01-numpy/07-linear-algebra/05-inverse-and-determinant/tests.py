"""
pytest data/app_data/01-numpy/07-linear-algebra/05-inverse-and-determinant/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/07-linear-algebra/{Path(__file__).resolve().parent.name}")
determinant = _module.determinant
is_invertible = _module.is_invertible
safe_inverse = _module.safe_inverse
verify_inverse = _module.verify_inverse


def test_determinant_correctness_for_known_2x2_case():
    matrix = np.array([[1, 2], [3, 4]])
    assert determinant(matrix) == pytest.approx(-2.0)


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
