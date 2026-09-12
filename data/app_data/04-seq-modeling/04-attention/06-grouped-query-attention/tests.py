"""
pytest data/app_data/04-seq-modeling/04-attention/06-grouped-query-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/04-attention/{Path(__file__).resolve().parent.name}")
repeat_kv_heads = _module.repeat_kv_heads
grouped_query_attention = _module.grouped_query_attention

split_heads = load_solution("04-seq-modeling/04-attention/04-mha-split-heads").split_heads
multi_head_attention_per_head = load_solution(
    "04-seq-modeling/04-attention/04-mha-split-heads"
).multi_head_attention_per_head


def test_repeat_kv_heads_output_shape():
    x = np.random.randn(2, 2, 5, 4)  # (batch, num_kv_heads, seq_len, d_k)
    result = repeat_kv_heads(x, num_repeats=3)
    assert result.shape == (2, 6, 5, 4)


def test_repeat_kv_heads_repeats_consecutively_not_interleaved():
    x = np.array([[[[1.0]], [[2.0]]]])  # (batch=1, num_kv_heads=2, seq_len=1, d_k=1)
    result = repeat_kv_heads(x, num_repeats=2)
    flattened = result[0, :, 0, 0]
    assert np.allclose(flattened, [1.0, 1.0, 2.0, 2.0])


def test_repeat_kv_heads_with_num_repeats_one_is_identity():
    x = np.random.randn(2, 3, 5, 4)
    result = repeat_kv_heads(x, num_repeats=1)
    assert np.allclose(result, x)


def test_grouped_query_attention_output_shape():
    d_model_q, num_query_heads = 12, 4
    d_k = d_model_q // num_query_heads
    num_kv_heads = 2
    d_model_kv = num_kv_heads * d_k

    Q = np.random.randn(2, 5, d_model_q)
    K = np.random.randn(2, 5, d_model_kv)
    V = np.random.randn(2, 5, d_model_kv)
    output, weights = grouped_query_attention(Q, K, V, num_query_heads=num_query_heads, num_kv_heads=num_kv_heads)
    assert output.shape == (2, num_query_heads, 5, d_k)
    assert weights.shape == (2, num_query_heads, 5, 5)


def test_equal_query_and_kv_heads_reduces_to_ordinary_multi_head_attention():
    rng = np.random.RandomState(0)
    Q = rng.randn(2, 5, 12)
    K = rng.randn(2, 5, 12)
    V = rng.randn(2, 5, 12)

    gqa_output, gqa_weights = grouped_query_attention(Q, K, V, num_query_heads=3, num_kv_heads=3)
    mha_output, mha_weights = multi_head_attention_per_head(Q, K, V, num_heads=3)

    assert np.allclose(gqa_output, mha_output)
    assert np.allclose(gqa_weights, mha_weights)


def test_query_heads_in_the_same_group_attend_using_the_same_kv_head():
    rng = np.random.RandomState(1)
    d_model_q, num_query_heads = 8, 4
    d_k = d_model_q // num_query_heads
    num_kv_heads = 2
    d_model_kv = num_kv_heads * d_k

    Q = rng.randn(1, 4, d_model_q)
    K = rng.randn(1, 4, d_model_kv)
    V = rng.randn(1, 4, d_model_kv)

    key_heads = split_heads(K, num_kv_heads)
    repeated = repeat_kv_heads(key_heads, num_query_heads // num_kv_heads)
    # query heads 0 and 1 should both pair with kv head 0
    assert np.allclose(repeated[:, 0], key_heads[:, 0])
    assert np.allclose(repeated[:, 1], key_heads[:, 0])
    # query heads 2 and 3 should both pair with kv head 1
    assert np.allclose(repeated[:, 2], key_heads[:, 1])
    assert np.allclose(repeated[:, 3], key_heads[:, 1])


def test_fewer_kv_heads_still_produces_a_valid_probability_distribution():
    d_model_q, num_query_heads = 12, 4
    d_k = d_model_q // num_query_heads
    num_kv_heads = 2
    d_model_kv = num_kv_heads * d_k

    Q = np.random.randn(1, 5, d_model_q)
    K = np.random.randn(1, 5, d_model_kv)
    V = np.random.randn(1, 5, d_model_kv)
    _, weights = grouped_query_attention(Q, K, V, num_query_heads=num_query_heads, num_kv_heads=num_kv_heads)
    assert np.allclose(weights.sum(axis=-1), 1.0)


def test_repeat_kv_heads_uses_repeat_not_tile_ordering():
    # Directly targets a mutant that uses np.tile instead of np.repeat
    # (or an incorrect axis), which produces an INTERLEAVED [A, B, A, B]
    # pattern instead of the correct grouped [A, A, B, B] pattern,
    # silently assigning the wrong kv head to each query-head group.
    x = np.array([[[[1.0]], [[2.0]], [[3.0]]]])  # 3 kv heads
    result = repeat_kv_heads(x, num_repeats=2)
    flattened = result[0, :, 0, 0]
    assert np.allclose(flattened, [1.0, 1.0, 2.0, 2.0, 3.0, 3.0])
    assert not np.allclose(flattened, [1.0, 2.0, 3.0, 1.0, 2.0, 3.0])
