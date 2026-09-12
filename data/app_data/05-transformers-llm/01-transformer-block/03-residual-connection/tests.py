"""
pytest data/app_data/05-transformers-llm/01-transformer-block/03-residual-connection/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/01-transformer-block/{Path(__file__).resolve().parent.name}")
residual_connection = _module.residual_connection
residual_connection_backward = _module.residual_connection_backward


def test_forward_is_elementwise_addition():
    x = np.array([1.0, 2.0, 3.0])
    sublayer_output = np.array([0.1, -0.2, 0.3])
    result = residual_connection(x, sublayer_output)
    assert np.allclose(result, [1.1, 1.8, 3.3])


def test_output_shape_matches_input_shape():
    x = np.random.randn(2, 5, 8)
    sublayer_output = np.random.randn(2, 5, 8)
    result = residual_connection(x, sublayer_output)
    assert result.shape == x.shape


def test_zero_sublayer_output_leaves_x_unchanged():
    x = np.random.randn(3, 4)
    sublayer_output = np.zeros((3, 4))
    result = residual_connection(x, sublayer_output)
    assert np.allclose(result, x)


def test_backward_passes_gradient_through_unchanged_to_both_inputs():
    grad_output = np.array([1.0, -2.0, 0.5])
    grad_x, grad_sublayer_output = residual_connection_backward(grad_output)
    assert np.allclose(grad_x, grad_output)
    assert np.allclose(grad_sublayer_output, grad_output)


def test_gradient_norm_does_not_shrink_across_many_stacked_residual_additions():
    # Contrast with 04-seq-modeling/03-recurrent-neural-networks/03-bptt-vanishing-exploding:
    # repeated MULTIPLICATION by a recurrent weight matrix shrinks or
    # explodes a gradient exponentially over many steps. Repeated
    # ADDITION (what a residual connection contributes to the gradient
    # path) does not: the gradient reaching x through the "skip" path is
    # identical at every depth, regardless of how many blocks are stacked.
    grad_output = np.array([1.0, 1.0, 1.0, 1.0])
    grad = grad_output.copy()
    for _ in range(50):
        grad_x, _ = residual_connection_backward(grad)
        grad = grad_x
    assert np.allclose(np.linalg.norm(grad), np.linalg.norm(grad_output), atol=1e-8)


def test_forward_is_not_accidentally_asymmetric_between_its_two_arguments():
    # Directly targets a mutant that only returns one of the two inputs,
    # or scales one of them, instead of a true elementwise sum.
    x = np.array([2.0, 0.0, -3.0])
    sublayer_output = np.array([5.0, 5.0, 5.0])
    result = residual_connection(x, sublayer_output)
    assert np.allclose(result, x + sublayer_output)
    assert not np.allclose(result, x)
    assert not np.allclose(result, sublayer_output)
