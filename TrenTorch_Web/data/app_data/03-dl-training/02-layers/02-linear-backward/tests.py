"""
pytest data/app_data/03-dl-training/02-layers/02-linear-backward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/02-layers/{Path(__file__).resolve().parent.name}")
linear_backward = _module.linear_backward


def test_shapes_match_the_original_forward_inputs():
    x = np.random.randn(5, 4)
    weight = np.random.randn(3, 4)
    grad_output = np.random.randn(5, 3)
    grad_x, grad_weight, grad_bias = linear_backward(grad_output, x, weight)
    assert grad_x.shape == x.shape
    assert grad_weight.shape == weight.shape
    assert grad_bias.shape == (3,)


def test_grad_bias_sums_grad_output_across_the_batch():
    grad_output = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    x = np.zeros((3, 2))
    weight = np.zeros((2, 2))
    _, _, grad_bias = linear_backward(grad_output, x, weight)
    assert np.allclose(grad_bias, [9.0, 12.0])


def test_hand_computed_gradients_for_a_single_sample():
    x = np.array([[1.0, 2.0]])
    weight = np.array([[1.0, 0.0], [0.0, 1.0]])  # identity, out_features=2
    grad_output = np.array([[1.0, 1.0]])
    grad_x, grad_weight, grad_bias = linear_backward(grad_output, x, weight)
    # grad_x = grad_output @ weight = [1,1] @ I = [1,1]
    assert np.allclose(grad_x, [[1.0, 1.0]])
    # grad_weight = grad_output.T @ x = [[1],[1]] @ [[1,2]] = [[1,2],[1,2]]
    assert np.allclose(grad_weight, [[1.0, 2.0], [1.0, 2.0]])
    assert np.allclose(grad_bias, [1.0, 1.0])


def test_matches_pytorch_autograd_oracle():
    # verified directly against torch.nn.Linear + loss.backward()
    x = np.array([[0.5, -1.0, 2.0]])
    weight = np.array([[1.0, 0.0, -1.0], [0.5, 0.5, 0.5]])
    grad_output = np.array([[1.0, 1.0]])
    grad_x, grad_weight, grad_bias = linear_backward(grad_output, x, weight)
    assert np.allclose(grad_x, [[1.5, 0.5, -0.5]])
    assert np.allclose(grad_weight, [[0.5, -1.0, 2.0], [0.5, -1.0, 2.0]])
    assert np.allclose(grad_bias, [1.0, 1.0])


def test_zero_grad_output_gives_zero_gradients_everywhere():
    x = np.random.randn(4, 3)
    weight = np.random.randn(2, 3)
    grad_output = np.zeros((4, 2))
    grad_x, grad_weight, grad_bias = linear_backward(grad_output, x, weight)
    assert np.allclose(grad_x, 0.0)
    assert np.allclose(grad_weight, 0.0)
    assert np.allclose(grad_bias, 0.0)


def test_grad_weight_uses_grad_output_transpose_not_grad_output_directly():
    # Directly targets a mutant that swaps the transpose, e.g. computing
    # x.T @ grad_output instead of grad_output.T @ x: for non-square,
    # differently-shaped batch/feature dimensions this produces a shape
    # error or, for a case where shapes happen to still multiply, the
    # WRONG matrix (a transpose of the correct answer).
    x = np.array([[1.0, 2.0], [3.0, 4.0]])
    weight = np.array([[1.0, 1.0], [1.0, 1.0]])
    grad_output = np.array([[1.0, 0.0], [0.0, 1.0]])
    _, grad_weight, _ = linear_backward(grad_output, x, weight)
    # correct: grad_output.T @ x = [[1,0],[0,1]] @ [[1,2],[3,4]] = [[1,2],[3,4]]
    assert np.allclose(grad_weight, [[1.0, 2.0], [3.0, 4.0]])
