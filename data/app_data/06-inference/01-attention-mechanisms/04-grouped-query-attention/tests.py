"""
pytest data/app_data/06-inference/01-attention-mechanisms/04-grouped-query-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

grouped_query_attention = load_solution(
    f"06-inference/01-attention-mechanisms/{Path(__file__).resolve().parent.name}"
).grouped_query_attention
multi_head_attention = load_solution(
    "06-inference/01-attention-mechanisms/02-multi-head-attention"
).multi_head_attention
multi_query_attention = load_solution(
    "06-inference/01-attention-mechanisms/03-multi-query-attention"
).multi_query_attention


def test_output_shape():
    rng = np.random.default_rng(0)
    seq_len, d_model, n_heads, n_kv_heads = 5, 8, 4, 2
    d_head = d_model // n_heads
    X = rng.normal(size=(seq_len, d_model))
    W_Q = rng.normal(size=(d_model, d_model))
    W_K = rng.normal(size=(d_model, n_kv_heads * d_head))
    W_V = rng.normal(size=(d_model, n_kv_heads * d_head))
    W_O = rng.normal(size=(d_model, d_model))
    output = grouped_query_attention(X, W_Q, W_K, W_V, W_O, n_heads, n_kv_heads)
    assert output.shape == (seq_len, d_model)


def test_n_kv_heads_equals_n_heads_reduces_to_mha():
    rng = np.random.default_rng(1)
    seq_len, d_model, n_heads = 3, 4, 2
    X = rng.normal(size=(seq_len, d_model))
    W_Q = rng.normal(size=(d_model, d_model))
    W_K = rng.normal(size=(d_model, d_model))
    W_V = rng.normal(size=(d_model, d_model))
    W_O = rng.normal(size=(d_model, d_model))

    gqa_out = grouped_query_attention(X, W_Q, W_K, W_V, W_O, n_heads, n_kv_heads=n_heads)
    mha_out = multi_head_attention(X, W_Q, W_K, W_V, W_O, n_heads)
    assert np.allclose(gqa_out, mha_out, atol=1e-8)


def test_n_kv_heads_one_reduces_to_mqa():
    rng = np.random.default_rng(2)
    seq_len, d_model, n_heads = 4, 4, 4
    d_head = 1
    X = rng.normal(size=(seq_len, d_model))
    W_Q = rng.normal(size=(d_model, d_model))
    W_K = rng.normal(size=(d_model, d_head))
    W_V = rng.normal(size=(d_model, d_head))
    W_O = rng.normal(size=(d_model, d_model))

    gqa_out = grouped_query_attention(X, W_Q, W_K, W_V, W_O, n_heads, n_kv_heads=1)
    mqa_out = multi_query_attention(X, W_Q, W_K, W_V, W_O, n_heads)
    assert np.allclose(gqa_out, mqa_out, atol=1e-8)


def test_four_heads_two_groups_single_token():
    X = np.array([[1.0, 0.0, 1.0, 0.0]])
    W_Q = np.eye(4)
    W_K = np.array([[1, 0], [0, 1], [1, 0], [0, 1]], dtype=float)
    W_V = np.array([[1, 0], [0, 1], [1, 0], [0, 1]], dtype=float)
    W_O = np.eye(4)
    output = grouped_query_attention(X, W_Q, W_K, W_V, W_O, n_heads=4, n_kv_heads=2)
    assert output.shape == (1, 4)
    assert np.all(np.isfinite(output))
