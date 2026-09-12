"""
pytest data/app_data/06-inference/01-attention-mechanisms/02-multi-head-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

multi_head_attention = load_solution(
    f"06-inference/01-attention-mechanisms/{Path(__file__).resolve().parent.name}"
).multi_head_attention
scaled_dot_product_attention = load_solution(
    "06-inference/01-attention-mechanisms/01-scaled-dot-product-attention"
).scaled_dot_product_attention


def test_single_token_identity_weights_returns_input_unchanged():
    X = np.array([[1.0, 0.0, 1.0, 0.0]])
    I = np.eye(4)
    output = multi_head_attention(X, I, I, I, I, n_heads=2)
    # Single token -> softmax is trivially [1.0] per head -> each head
    # just returns its own V slice -> concat is X itself -> W_O=I keeps it.
    assert np.allclose(output, X)


def test_output_shape_matches_input():
    rng = np.random.default_rng(0)
    seq_len, d_model, n_heads = 5, 8, 4
    X = rng.normal(size=(seq_len, d_model))
    W_Q, W_K, W_V, W_O = (rng.normal(size=(d_model, d_model)) for _ in range(4))
    output = multi_head_attention(X, W_Q, W_K, W_V, W_O, n_heads)
    assert output.shape == (seq_len, d_model)


def test_single_head_matches_plain_scaled_dot_product_attention():
    rng = np.random.default_rng(1)
    seq_len, d_model = 4, 6
    X = rng.normal(size=(seq_len, d_model))
    W_Q, W_K, W_V = (rng.normal(size=(d_model, d_model)) for _ in range(3))
    W_O = np.eye(d_model)
    output = multi_head_attention(X, W_Q, W_K, W_V, W_O, n_heads=1)
    expected, _ = scaled_dot_product_attention(X @ W_Q, X @ W_K, X @ W_V)
    assert np.allclose(output, expected, atol=1e-8)


def test_causal_mask_blocks_future_tokens():
    X = np.array([[1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0]])
    I = np.eye(4)
    mask = np.array([[1, 0], [1, 1]])
    output = multi_head_attention(X, I, I, I, I, n_heads=2, mask=mask)
    # Position 0 can only see itself -> its output equals its own V (= X row 0).
    assert np.allclose(output[0], X[0])


def test_four_heads_dhead_one():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(3, 4))
    W_Q, W_K, W_V, W_O = (rng.normal(size=(4, 4)) for _ in range(4))
    output = multi_head_attention(X, W_Q, W_K, W_V, W_O, n_heads=4)
    assert output.shape == (3, 4)
    assert np.all(np.isfinite(output))
