"""
pytest data/app_data/04-seq-modeling/04-attention/01-scaled-dot-product-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/04-attention/{Path(__file__).resolve().parent.name}")
scaled_dot_product_attention = _module.scaled_dot_product_attention


def test_output_shape_matches_query_shape():
    Q = np.random.randn(2, 5, 8)
    K = np.random.randn(2, 5, 8)
    V = np.random.randn(2, 5, 8)
    output, weights = scaled_dot_product_attention(Q, K, V)
    assert output.shape == Q.shape
    assert weights.shape == (2, 5, 5)


def test_attention_weight_rows_sum_to_one():
    Q = np.random.randn(3, 4, 6)
    K = np.random.randn(3, 4, 6)
    V = np.random.randn(3, 4, 6)
    _, weights = scaled_dot_product_attention(Q, K, V)
    assert np.allclose(weights.sum(axis=-1), 1.0)


def test_identical_query_and_key_vectors_attend_most_to_themselves():
    # When query[i] == key[i] for all i (and keys are otherwise distinct),
    # each position's highest attention weight should land on itself.
    Q = K = np.eye(4) * 10.0  # strongly distinct, orthogonal rows
    V = np.array([[1.0], [2.0], [3.0], [4.0]])
    _, weights = scaled_dot_product_attention(Q, K, V)
    for i in range(4):
        assert np.argmax(weights[i]) == i


def test_uniform_scores_give_uniform_attention_weights():
    # If all keys are identical, every query attends equally to every position.
    Q = np.random.randn(1, 3, 4)
    K = np.ones((1, 3, 4))  # identical keys -> identical scores
    V = np.random.randn(1, 3, 4)
    _, weights = scaled_dot_product_attention(Q, K, V)
    for row in weights[0]:
        assert np.allclose(row, 1.0 / 3.0, atol=1e-6)


def test_mask_with_large_negative_value_zeroes_out_that_positions_weight():
    Q = np.random.randn(1, 3, 4)
    K = np.random.randn(1, 3, 4)
    V = np.random.randn(1, 3, 4)
    mask = np.zeros((1, 3, 3))
    mask[:, :, 1] = -1e9  # forbid attending to position 1
    _, weights = scaled_dot_product_attention(Q, K, V, mask=mask)
    assert np.allclose(weights[:, :, 1], 0.0, atol=1e-6)


def test_matches_known_oracle_from_pytorch_scaled_dot_product_attention():
    # verified directly against torch.nn.functional.scaled_dot_product_attention
    Q = np.array([[[1.0, 0.0], [0.0, 1.0]]])
    K = np.array([[[1.0, 0.0], [0.0, 1.0]]])
    V = np.array([[[10.0, 20.0], [30.0, 40.0]]])
    output, weights = scaled_dot_product_attention(Q, K, V)
    d_k = 2
    scores = Q @ np.swapaxes(K, -2, -1) / np.sqrt(d_k)
    expected_weights = np.exp(scores) / np.exp(scores).sum(axis=-1, keepdims=True)
    expected_output = expected_weights @ V
    assert np.allclose(output, expected_output, atol=1e-6)
    assert np.allclose(weights, expected_weights, atol=1e-6)


def test_scores_are_scaled_by_sqrt_d_k_not_left_unscaled():
    # Directly targets a mutant that forgets the 1/sqrt(d_k) scaling
    # entirely: for a large d_k, unscaled dot products can push softmax
    # into near-one-hot saturation where a correctly-scaled version
    # would still be meaningfully spread out.
    d_k = 64
    rng = np.random.RandomState(0)
    Q = rng.randn(1, 2, d_k)
    K = rng.randn(1, 2, d_k)
    V = rng.randn(1, 2, d_k)
    _, weights = scaled_dot_product_attention(Q, K, V)
    scores_unscaled = Q @ np.swapaxes(K, -2, -1)  # no /sqrt(d_k)
    weights_unscaled = np.exp(scores_unscaled - scores_unscaled.max(axis=-1, keepdims=True))
    weights_unscaled = weights_unscaled / weights_unscaled.sum(axis=-1, keepdims=True)
    assert not np.allclose(weights, weights_unscaled, atol=1e-3)
