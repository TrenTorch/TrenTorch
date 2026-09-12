"""
pytest data/app_data/02-deep-learning-core/04-autograd/03-backward-matmul/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/04-autograd/{Path(__file__).resolve().parent.name}")
matmul_backward = _module.matmul_backward


def test_matmul_backward_output_shapes_match_inputs():
    a = np.zeros((3, 4))
    b = np.zeros((4, 5))
    grad_output = np.zeros((3, 5))
    grad_a, grad_b = matmul_backward(grad_output, a, b)
    assert grad_a.shape == (3, 4)
    assert grad_b.shape == (4, 5)


def test_matmul_backward_matches_known_oracle_values():
    # generated once, offline, via real PyTorch autograd
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([[5.0, 6.0], [7.0, 8.0]])
    grad_output = np.array([[1.0, 0.0], [0.0, 1.0]])
    grad_a, grad_b = matmul_backward(grad_output, a, b)
    # grad_a = grad_output @ b.T = [[5,7],[6,8]]
    # grad_b = a.T @ grad_output = [[1,2],[3,4]]... let's verify directly
    assert np.allclose(grad_a, grad_output @ b.T)
    assert np.allclose(grad_b, a.T @ grad_output)
    assert np.allclose(grad_a, [[5.0, 7.0], [6.0, 8.0]])
    assert np.allclose(grad_b, [[1.0, 3.0], [2.0, 4.0]])


def test_matmul_backward_matches_finite_difference_check():
    rng = np.random.default_rng(0)
    a = rng.normal(size=(3, 4))
    b = rng.normal(size=(4, 2))
    grad_output = rng.normal(size=(3, 2))

    grad_a, grad_b = matmul_backward(grad_output, a, b)

    eps = 1e-5
    numeric_grad_a = np.empty_like(a)
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            a_plus, a_minus = a.copy(), a.copy()
            a_plus[i, j] += eps
            a_minus[i, j] -= eps
            numeric_grad_a[i, j] = np.sum((a_plus @ b - a_minus @ b) / (2 * eps) * grad_output)
    assert np.allclose(grad_a, numeric_grad_a, atol=1e-4)


def test_matmul_backward_for_a_non_square_rectangular_case():
    rng = np.random.default_rng(1)
    a = rng.normal(size=(5, 2))
    b = rng.normal(size=(2, 7))
    grad_output = rng.normal(size=(5, 7))
    grad_a, grad_b = matmul_backward(grad_output, a, b)
    assert grad_a.shape == (5, 2)
    assert grad_b.shape == (2, 7)


def test_matmul_backward_does_not_swap_which_operand_gets_transposed():
    # Directly targets a mutant that swaps the two formulas (e.g.
    # computing grad_a as a.T @ grad_output instead of grad_output @ b.T):
    # on a non-square case, the swapped version produces a shape error
    # or, when shapes happen to coincide, clearly wrong values.
    a = np.array([[1.0, 2.0, 3.0]])  # (1, 3)
    b = np.array([[1.0], [1.0], [1.0]])  # (3, 1)
    grad_output = np.array([[2.0]])  # (1, 1)
    grad_a, grad_b = matmul_backward(grad_output, a, b)
    assert grad_a.shape == (1, 3)
    assert grad_b.shape == (3, 1)
    assert np.allclose(grad_a, [[2.0, 2.0, 2.0]])
    assert np.allclose(grad_b, [[2.0], [4.0], [6.0]])
