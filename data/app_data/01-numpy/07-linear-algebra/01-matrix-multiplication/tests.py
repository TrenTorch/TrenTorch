"""
pytest data/app_data/01-numpy/07-linear-algebra/01-matrix-multiplication/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/07-linear-algebra/{Path(__file__).resolve().parent.name}")
matmul_from_scratch = _module.matmul_from_scratch
matmul_builtin = _module.matmul_builtin
compare_matmul_and_elementwise = _module.compare_matmul_and_elementwise


def test_matmul_from_scratch_matches_mathematical_definition():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    np.testing.assert_array_equal(matmul_from_scratch(a, b), [[19, 22], [43, 50]])


def test_matmul_from_scratch_and_builtin_agree():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    np.testing.assert_allclose(matmul_from_scratch(a, b), matmul_builtin(a, b))


def test_non_square_shape_compatible_matrices():
    a = np.arange(6).reshape(2, 3)
    b = np.arange(12).reshape(3, 4)
    result = matmul_from_scratch(a, b)
    assert result.shape == (2, 4)
    np.testing.assert_allclose(result, a @ b)


def test_compare_matmul_and_elementwise_correctly_detects_divergence():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    result = compare_matmul_and_elementwise(a, b)
    assert result["results_are_different"] is True


def test_matrix_multiplication_is_non_commutative_in_general():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[0, 1], [1, 0]])
    assert not np.array_equal(a @ b, b @ a)
