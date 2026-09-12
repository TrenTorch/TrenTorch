"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/04-flash-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
flash_attention = _module.flash_attention

scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention
build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def test_matches_full_attention_with_a_single_block():
    rng = np.random.RandomState(0)
    seq_len, d_k = 6, 4
    q, k, v = rng.randn(seq_len, d_k), rng.randn(seq_len, d_k), rng.randn(seq_len, d_k)
    expected, _ = scaled_dot_product_attention(q, k, v)
    result = flash_attention(q, k, v, block_size=seq_len)
    assert np.allclose(result, expected, atol=1e-8)


def test_matches_full_attention_with_many_small_blocks():
    rng = np.random.RandomState(1)
    seq_len, d_k = 10, 4
    q, k, v = rng.randn(seq_len, d_k), rng.randn(seq_len, d_k), rng.randn(seq_len, d_k)
    expected, _ = scaled_dot_product_attention(q, k, v)

    for block_size in [1, 2, 3, 4, 7, 10, 100]:
        result = flash_attention(q, k, v, block_size=block_size)
        assert np.allclose(result, expected, atol=1e-6), f"mismatch at block_size={block_size}"


def test_matches_full_attention_with_a_causal_mask():
    rng = np.random.RandomState(2)
    seq_len, d_k = 8, 4
    q, k, v = rng.randn(seq_len, d_k), rng.randn(seq_len, d_k), rng.randn(seq_len, d_k)
    mask = build_causal_mask(seq_len)
    expected, _ = scaled_dot_product_attention(q, k, v, mask=mask)

    for block_size in [1, 3, 8]:
        result = flash_attention(q, k, v, block_size=block_size, mask=mask)
        assert np.allclose(result, expected, atol=1e-6), f"mismatch at block_size={block_size}"


def test_matches_full_attention_with_leading_batch_and_head_dimensions():
    rng = np.random.RandomState(3)
    batch, num_heads, seq_len, d_k = 2, 3, 5, 4
    q = rng.randn(batch, num_heads, seq_len, d_k)
    k = rng.randn(batch, num_heads, seq_len, d_k)
    v = rng.randn(batch, num_heads, seq_len, d_k)
    expected, _ = scaled_dot_product_attention(q, k, v)
    result = flash_attention(q, k, v, block_size=2)
    assert np.allclose(result, expected, atol=1e-6)


def test_output_is_a_valid_convex_combination_of_value_rows():
    # A structural sanity check: attention output must always lie within
    # the convex hull of the value vectors (a weighted average with
    # nonnegative weights summing to 1), regardless of chunking.
    rng = np.random.RandomState(4)
    seq_len, d_k = 5, 3
    q, k, v = rng.randn(seq_len, d_k), rng.randn(seq_len, d_k), rng.randn(seq_len, d_k)
    result = flash_attention(q, k, v, block_size=2)
    assert np.all(result >= v.min(axis=0) - 1e-6)
    assert np.all(result <= v.max(axis=0) + 1e-6)


def test_uses_the_running_max_for_numerical_stability_not_a_fixed_reference():
    # Directly targets a mutant that skips the running-max correction
    # (e.g. uses exp(scores) directly without subtracting a running max),
    # which would silently diverge (inf/nan) for large-magnitude scores.
    rng = np.random.RandomState(5)
    seq_len, d_k = 6, 4
    q = rng.randn(seq_len, d_k) * 50.0  # large magnitude -> large raw scores
    k = rng.randn(seq_len, d_k) * 50.0
    v = rng.randn(seq_len, d_k)
    result = flash_attention(q, k, v, block_size=2)
    assert np.all(np.isfinite(result))
