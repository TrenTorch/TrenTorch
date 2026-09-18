"""
pytest data/app_data/04-seq-modeling/04-attention/04-mha-split-heads/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/04-attention/{Path(__file__).resolve().parent.name}")
split_heads = _module.split_heads
multi_head_attention_per_head = _module.multi_head_attention_per_head


def test_split_heads_output_shape():
    x = np.random.randn(2, 5, 12)
    result = split_heads(x, num_heads=3)
    assert result.shape == (2, 3, 5, 4)


def test_split_heads_preserves_consecutive_chunks():
    x = np.arange(24).reshape(1, 2, 12).astype(float)  # batch=1, seq_len=2, d_model=12
    result = split_heads(x, num_heads=3)  # d_k = 4
    # head 0 should be x's first 4 columns, head 1 the next 4, head 2 the last 4
    assert np.allclose(result[0, 0], x[0, :, 0:4])
    assert np.allclose(result[0, 1], x[0, :, 4:8])
    assert np.allclose(result[0, 2], x[0, :, 8:12])


def test_split_heads_with_a_single_head_is_equivalent_to_adding_a_head_axis():
    x = np.random.randn(2, 4, 6)
    result = split_heads(x, num_heads=1)
    assert result.shape == (2, 1, 4, 6)
    assert np.allclose(result[:, 0, :, :], x)


def test_multi_head_attention_output_shape():
    Q = np.random.randn(2, 5, 12)
    K = np.random.randn(2, 5, 12)
    V = np.random.randn(2, 5, 12)
    output, weights = multi_head_attention_per_head(Q, K, V, num_heads=3)
    assert output.shape == (2, 3, 5, 4)
    assert weights.shape == (2, 3, 5, 5)


def test_multi_head_attention_matches_a_manual_per_head_loop():
    rng = np.random.RandomState(0)
    batch, seq_len, d_model, num_heads = 2, 4, 8, 2
    d_k = d_model // num_heads
    Q = rng.randn(batch, seq_len, d_model)
    K = rng.randn(batch, seq_len, d_model)
    V = rng.randn(batch, seq_len, d_model)

    scaled_dot_product_attention = load_solution(
        "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
    ).scaled_dot_product_attention

    manual_outputs = []
    for h in range(num_heads):
        Qh = Q[:, :, h * d_k : (h + 1) * d_k]
        Kh = K[:, :, h * d_k : (h + 1) * d_k]
        Vh = V[:, :, h * d_k : (h + 1) * d_k]
        out_h, _ = scaled_dot_product_attention(Qh, Kh, Vh)
        manual_outputs.append(out_h)
    expected = np.stack(manual_outputs, axis=1)

    result, _ = multi_head_attention_per_head(Q, K, V, num_heads=num_heads)
    assert np.allclose(result, expected, atol=1e-6)


def test_multi_head_attention_respects_a_mask():
    Q = np.random.randn(1, 3, 4)
    K = np.random.randn(1, 3, 4)
    V = np.random.randn(1, 3, 4)
    mask = np.zeros((1, 3, 3))
    mask[:, :, 2] = -1e9
    _, weights = multi_head_attention_per_head(Q, K, V, num_heads=2, mask=mask)
    assert np.allclose(weights[:, :, :, 2], 0.0, atol=1e-6)


def test_split_heads_does_not_interleave_dimensions_across_heads():
    # Directly targets a mutant that splits d_model with a different
    # (incorrect) ordering, e.g. by transposing BEFORE the reshape
    # instead of after (x.transpose then reshape), which would scramble
    # WHICH original dimensions end up in which head, instead of clean
    # consecutive chunks.
    x = np.arange(8).reshape(1, 1, 8).astype(float)  # d_model=8, single batch/seq position
    result = split_heads(x, num_heads=2)  # d_k = 4
    assert np.allclose(result[0, 0, 0], [0.0, 1.0, 2.0, 3.0])
    assert np.allclose(result[0, 1, 0], [4.0, 5.0, 6.0, 7.0])
