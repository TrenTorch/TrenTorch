"""
pytest data/app_data/06-inference/01-attention-mechanisms/05-multi-head-latent-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

multi_head_latent_attention = load_solution(
    f"06-inference/01-attention-mechanisms/{Path(__file__).resolve().parent.name}"
).multi_head_latent_attention
multi_head_attention = load_solution(
    "06-inference/01-attention-mechanisms/02-multi-head-attention"
).multi_head_attention


def test_output_and_cache_shapes():
    rng = np.random.default_rng(0)
    seq_len, d_model, n_heads, d_latent = 5, 8, 4, 3
    X = rng.normal(size=(seq_len, d_model))
    W_Q = rng.normal(size=(d_model, d_model))
    W_DKV = rng.normal(size=(d_model, d_latent))
    W_UK = rng.normal(size=(d_latent, d_model))
    W_UV = rng.normal(size=(d_latent, d_model))
    W_O = rng.normal(size=(d_model, d_model))
    output, cache = multi_head_latent_attention(X, W_Q, W_DKV, W_UK, W_UV, W_O, n_heads)
    assert output.shape == (seq_len, d_model)
    assert cache.shape == (seq_len, d_latent)


def test_latent_compression_matches_equivalent_low_rank_mha():
    # K_full = (X @ W_DKV) @ W_UK == X @ (W_DKV @ W_UK), so MLA must
    # match plain MHA given that composed low-rank K/V projection.
    rng = np.random.default_rng(1)
    seq_len, d_model, n_heads, d_latent = 4, 4, 2, 2
    X = rng.normal(size=(seq_len, d_model))
    W_Q = rng.normal(size=(d_model, d_model))
    W_DKV = rng.normal(size=(d_model, d_latent))
    W_UK = rng.normal(size=(d_latent, d_model))
    W_UV = rng.normal(size=(d_latent, d_model))
    W_O = rng.normal(size=(d_model, d_model))

    mla_out, _ = multi_head_latent_attention(X, W_Q, W_DKV, W_UK, W_UV, W_O, n_heads)

    W_K_composed = W_DKV @ W_UK
    W_V_composed = W_DKV @ W_UV
    mha_out = multi_head_attention(X, W_Q, W_K_composed, W_V_composed, W_O, n_heads)

    assert np.allclose(mla_out, mha_out, atol=1e-8)


def test_cache_is_narrower_than_full_kv_width():
    rng = np.random.default_rng(2)
    seq_len, d_model, n_heads, d_latent = 3, 8, 4, 2
    X = rng.normal(size=(seq_len, d_model))
    W_Q = rng.normal(size=(d_model, d_model))
    W_DKV = rng.normal(size=(d_model, d_latent))
    W_UK = rng.normal(size=(d_latent, d_model))
    W_UV = rng.normal(size=(d_latent, d_model))
    W_O = rng.normal(size=(d_model, d_model))
    _, cache = multi_head_latent_attention(X, W_Q, W_DKV, W_UK, W_UV, W_O, n_heads)
    assert cache.shape[-1] < d_model  # d_latent < n_heads * d_head is a real compression


def test_no_nan_or_inf():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(6, 6))
    W_Q = rng.normal(size=(6, 6))
    W_DKV = rng.normal(size=(6, 2))
    W_UK = rng.normal(size=(2, 6))
    W_UV = rng.normal(size=(2, 6))
    W_O = rng.normal(size=(6, 6))
    output, cache = multi_head_latent_attention(X, W_Q, W_DKV, W_UK, W_UV, W_O, n_heads=3)
    assert np.all(np.isfinite(output))
    assert np.all(np.isfinite(cache))
