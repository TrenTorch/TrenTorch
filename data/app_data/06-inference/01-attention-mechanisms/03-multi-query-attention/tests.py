"""
pytest data/app_data/06-inference/01-attention-mechanisms/03-multi-query-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

multi_query_attention = load_solution(
    f"06-inference/01-attention-mechanisms/{Path(__file__).resolve().parent.name}"
).multi_query_attention
multi_head_attention = load_solution(
    "06-inference/01-attention-mechanisms/02-multi-head-attention"
).multi_head_attention


def test_output_shape():
    rng = np.random.default_rng(0)
    seq_len, d_model, n_heads, d_head = 5, 8, 4, 2
    X = rng.normal(size=(seq_len, d_model))
    W_Q = rng.normal(size=(d_model, d_model))
    W_K = rng.normal(size=(d_model, d_head))
    W_V = rng.normal(size=(d_model, d_head))
    W_O = rng.normal(size=(n_heads * d_head, d_model))
    output = multi_query_attention(X, W_Q, W_K, W_V, W_O, n_heads)
    assert output.shape == (seq_len, d_model)


def test_single_token_every_head_uses_same_shared_kv():
    X = np.array([[1.0, 0.0, 1.0, 0.0]])
    W_Q = np.eye(4)
    W_K = np.eye(4)[:, :2]
    W_V = np.eye(4)[:, 2:]
    W_O = np.eye(4)
    output = multi_query_attention(X, W_Q, W_K, W_V, W_O, n_heads=2)
    # Single token -> softmax is trivially [1.0] regardless of Q -> each
    # head's output is exactly the shared V (broadcast to both heads).
    V = X @ W_V
    assert np.allclose(output, np.concatenate([V, V], axis=-1))


def test_matches_mha_when_kv_heads_manually_duplicated():
    # MQA with a shared (seq_len, d_head) K/V must match MHA where every
    # head is GIVEN the identical duplicated K/V weight slice.
    rng = np.random.default_rng(1)
    seq_len, d_model, n_heads = 3, 4, 2
    d_head = d_model // n_heads
    X = rng.normal(size=(seq_len, d_model))
    W_Q = rng.normal(size=(d_model, d_model))
    W_K_shared = rng.normal(size=(d_model, d_head))
    W_V_shared = rng.normal(size=(d_model, d_head))
    W_O = rng.normal(size=(n_heads * d_head, d_model))

    mqa_out = multi_query_attention(X, W_Q, W_K_shared, W_V_shared, W_O, n_heads)

    # Build MHA weights where every head's K/V slice is the same shared projection.
    W_K_mha = np.tile(W_K_shared, (1, n_heads))
    W_V_mha = np.tile(W_V_shared, (1, n_heads))
    mha_out = multi_head_attention(X, W_Q, W_K_mha, W_V_mha, W_O, n_heads)

    assert np.allclose(mqa_out, mha_out, atol=1e-8)


def test_causal_mask_applied():
    X = np.array([[1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0]])
    W_Q, W_O = np.eye(4), np.eye(4)
    W_K = np.eye(4)[:, :2]
    W_V = np.eye(4)[:, 2:]
    mask = np.array([[1, 0], [1, 1]])
    output = multi_query_attention(X, W_Q, W_K, W_V, W_O, n_heads=2, mask=mask)
    V = X @ W_V
    assert np.allclose(output[0], np.concatenate([V[0], V[0]]))
