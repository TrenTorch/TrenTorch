"""
pytest data/app_data/09-systems-distributed/02-parallelism/07-ring-attention-online-softmax/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/02-parallelism/{Path(__file__).resolve().parent.name}")
attention_chunk_stats = _module.attention_chunk_stats
merge_chunk_stats = _module.merge_chunk_stats
ring_attention = _module.ring_attention
scaled_dot_product_attention = _module.scaled_dot_product_attention


def _random_qkv(seed, n_queries=3, seq_len=12, d=4):
    rng = np.random.default_rng(seed)
    q = rng.normal(size=(n_queries, d))
    k = rng.normal(size=(seq_len, d))
    v = rng.normal(size=(seq_len, d))
    return q, k, v


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_ring_attention_matches_full_attention():
    q, k, v = _random_qkv(0)
    full_out, _ = scaled_dot_product_attention(q, k, v)

    k_chunks = np.array_split(k, 4)
    v_chunks = np.array_split(v, 4)
    ring_out = ring_attention(q, k_chunks, v_chunks)
    assert np.allclose(ring_out, full_out, atol=1e-8)


def test_02_single_chunk_equals_full_attention():
    q, k, v = _random_qkv(1)
    full_out, _ = scaled_dot_product_attention(q, k, v)
    ring_out = ring_attention(q, [k], [v])
    assert np.allclose(ring_out, full_out, atol=1e-8)


# --- General-case coverage --------------------------------------------


def test_03_matches_full_attention_for_various_chunk_counts():
    q, k, v = _random_qkv(2, seq_len=24)
    full_out, _ = scaled_dot_product_attention(q, k, v)
    for num_chunks in (1, 2, 3, 6, 24):
        k_chunks = np.array_split(k, num_chunks)
        v_chunks = np.array_split(v, num_chunks)
        ring_out = ring_attention(q, k_chunks, v_chunks)
        assert np.allclose(ring_out, full_out, atol=1e-7)


def test_04_result_is_order_independent_across_chunk_boundaries():
    q, k, v = _random_qkv(3, seq_len=16)
    k_chunks_a = np.array_split(k, 2)
    v_chunks_a = np.array_split(v, 2)
    k_chunks_b = np.array_split(k, 8)
    v_chunks_b = np.array_split(v, 8)
    out_a = ring_attention(q, k_chunks_a, v_chunks_a)
    out_b = ring_attention(q, k_chunks_b, v_chunks_b)
    assert np.allclose(out_a, out_b, atol=1e-7)


def test_05_output_rows_sum_to_a_convex_combination_of_values():
    # Attention output must lie within the convex hull of V's rows --
    # a real property of any valid softmax-weighted average.
    q, k, v = _random_qkv(4, seq_len=10)
    k_chunks, v_chunks = np.array_split(k, 3), np.array_split(v, 3)
    out = ring_attention(q, k_chunks, v_chunks)
    assert np.all(out >= v.min(axis=0) - 1e-6)
    assert np.all(out <= v.max(axis=0) + 1e-6)


# --- Parameter handling -------------------------------------------------


def test_06_chunk_stats_shapes():
    q, k, v = _random_qkv(5, n_queries=2, seq_len=5, d=3)
    chunk_output, chunk_sum, chunk_max = attention_chunk_stats(q, k, v)
    assert chunk_output.shape == (2, 3)
    assert chunk_sum.shape == (2, 1)
    assert chunk_max.shape == (2, 1)


def test_07_merge_is_associative_over_more_chunks():
    q, k, v = _random_qkv(6, seq_len=20)
    full_out, _ = scaled_dot_product_attention(q, k, v)
    k_chunks, v_chunks = np.array_split(k, 5), np.array_split(v, 5)
    ring_out = ring_attention(q, k_chunks, v_chunks)
    assert np.allclose(ring_out, full_out, atol=1e-7)


# --- Edge cases ---------------------------------------------------------


def test_08_uneven_chunk_sizes_still_match():
    q, k, v = _random_qkv(7, seq_len=13)
    full_out, _ = scaled_dot_product_attention(q, k, v)
    k_chunks, v_chunks = np.array_split(k, 4), np.array_split(v, 4)
    assert any(kc.shape[0] != k_chunks[0].shape[0] for kc in k_chunks)
    ring_out = ring_attention(q, k_chunks, v_chunks)
    assert np.allclose(ring_out, full_out, atol=1e-7)


def test_09_single_key_value_pair_per_chunk():
    q, k, v = _random_qkv(8, seq_len=6)
    full_out, _ = scaled_dot_product_attention(q, k, v)
    k_chunks = [k[i : i + 1] for i in range(k.shape[0])]
    v_chunks = [v[i : i + 1] for i in range(v.shape[0])]
    ring_out = ring_attention(q, k_chunks, v_chunks)
    assert np.allclose(ring_out, full_out, atol=1e-7)


# --- Independent correctness oracle -----------------------------------


def test_10_merge_actually_rescales_rather_than_naively_summing():
    # Directly targets a mutant that just adds chunk stats to the
    # accumulator without rescaling by the max correction (which would
    # only coincidentally work when every chunk happens to share the
    # same max): use chunks with deliberately very different score
    # scales so a naive-sum mutant produces a visibly wrong answer.
    rng = np.random.default_rng(9)
    q = rng.normal(size=(2, 4)) * 5  # large-magnitude queries -> spread-out scores
    k = rng.normal(size=(10, 4))
    v = rng.normal(size=(10, 4))
    full_out, _ = scaled_dot_product_attention(q, k, v)
    k_chunks, v_chunks = np.array_split(k, 3), np.array_split(v, 3)
    ring_out = ring_attention(q, k_chunks, v_chunks)
    assert np.allclose(ring_out, full_out, atol=1e-6)
