"""
pytest data/app_data/00-math-and-statistics/01-linear-algebra/03-matrix-multiplication/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/01-linear-algebra/{Path(__file__).resolve().parent.name}"
)
matmul_from_scratch = _module.matmul_from_scratch


def test_matches_hand_computation():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([[5.0, 6.0], [7.0, 8.0]])
    # [[1*5+2*7, 1*6+2*8], [3*5+4*7, 3*6+4*8]] = [[19, 22], [43, 50]]
    assert np.allclose(matmul_from_scratch(a, b), [[19.0, 22.0], [43.0, 50.0]])


def test_matches_numpy_matmul_on_random_matrices():
    rng = np.random.default_rng(0)
    a = rng.normal(size=(4, 3))
    b = rng.normal(size=(3, 5))
    assert np.allclose(matmul_from_scratch(a, b), a @ b, atol=1e-10)


def test_output_shape_is_m_by_n_not_k_by_k():
    a = np.zeros((4, 3))
    b = np.zeros((3, 5))
    assert matmul_from_scratch(a, b).shape == (4, 5)


def test_identity_matrix_leaves_input_unchanged():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    identity = np.eye(2)
    assert np.allclose(matmul_from_scratch(a, identity), a)


def test_vector_shaped_matrices_reduce_to_dot_product():
    a = np.array([[1.0, 2.0, 3.0]])  # (1, 3)
    b = np.array([[4.0], [5.0], [6.0]])  # (3, 1)
    result = matmul_from_scratch(a, b)
    assert result.shape == (1, 1)
    assert np.isclose(result[0, 0], 32.0)


def test_raises_on_mismatched_inner_dimensions():
    a = np.zeros((2, 3))
    b = np.zeros((4, 2))
    with pytest.raises(ValueError):
        matmul_from_scratch(a, b)


def test_matmul_is_not_confused_with_elementwise_multiplication():
    # Directly targets a mutant that reduces to a*b broadcast rather than
    # the row-dot-column reduction, e.g. only works when a and b happen
    # to be square and same-shaped. Uses genuinely rectangular,
    # non-square shapes where elementwise multiply isn't even valid.
    a = np.array([[1.0, 0.0, 2.0], [0.0, 1.0, 3.0]])  # (2, 3)
    b = np.array([[1.0], [2.0], [1.0]])  # (3, 1)
    result = matmul_from_scratch(a, b)
    assert result.shape == (2, 1)
    assert np.allclose(result, [[3.0], [5.0]])
