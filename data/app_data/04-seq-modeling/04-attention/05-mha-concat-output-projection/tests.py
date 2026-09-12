"""
pytest data/app_data/04-seq-modeling/04-attention/05-mha-concat-output-projection/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/04-attention/{Path(__file__).resolve().parent.name}")
concat_heads = _module.concat_heads
multi_head_attention = _module.multi_head_attention

split_heads = load_solution("04-seq-modeling/04-attention/04-mha-split-heads").split_heads


def test_concat_heads_output_shape():
    x = np.random.randn(2, 3, 5, 4)  # (batch, num_heads, seq_len, d_k)
    result = concat_heads(x)
    assert result.shape == (2, 5, 12)


def test_concat_heads_is_the_inverse_of_split_heads():
    x = np.random.randn(2, 5, 12)
    reconstructed = concat_heads(split_heads(x, num_heads=3))
    assert np.allclose(reconstructed, x)


def test_concat_heads_preserves_consecutive_chunks():
    x = np.zeros((1, 2, 1, 4))
    x[0, 0, 0] = [1.0, 2.0, 3.0, 4.0]
    x[0, 1, 0] = [5.0, 6.0, 7.0, 8.0]
    result = concat_heads(x)
    assert np.allclose(result[0, 0], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])


def test_multi_head_attention_output_shape_matches_d_model():
    Q = np.random.randn(2, 5, 12)
    K = np.random.randn(2, 5, 12)
    V = np.random.randn(2, 5, 12)
    weight_o = np.random.randn(12, 12)
    bias_o = np.random.randn(12)
    output, weights = multi_head_attention(Q, K, V, num_heads=3, weight_o=weight_o, bias_o=bias_o)
    assert output.shape == (2, 5, 12)
    assert weights.shape == (2, 3, 5, 5)


def test_identity_projection_leaves_concatenated_output_unchanged():
    rng = np.random.RandomState(0)
    Q = rng.randn(1, 4, 8)
    K = rng.randn(1, 4, 8)
    V = rng.randn(1, 4, 8)
    weight_o = np.eye(8)
    bias_o = np.zeros(8)

    per_head_output, _ = load_solution(
        "04-seq-modeling/04-attention/04-mha-split-heads"
    ).multi_head_attention_per_head(Q, K, V, num_heads=2)
    expected_concat = concat_heads(per_head_output)

    output, _ = multi_head_attention(Q, K, V, num_heads=2, weight_o=weight_o, bias_o=bias_o)
    assert np.allclose(output, expected_concat, atol=1e-6)


def test_output_projection_is_applied_after_concatenation_not_before():
    # Directly targets a mutant that applies the projection to EACH
    # head separately (before concatenation), using a weight_o shaped
    # for the full d_model: a per-head-then-concat application would
    # produce mismatched shapes or, if forced to "work" incorrectly,
    # numerically different results from a correct post-concat
    # projection.
    rng = np.random.RandomState(1)
    Q = rng.randn(1, 3, 6)
    K = rng.randn(1, 3, 6)
    V = rng.randn(1, 3, 6)
    weight_o = rng.randn(6, 6)
    bias_o = np.zeros(6)

    per_head_output, _ = load_solution(
        "04-seq-modeling/04-attention/04-mha-split-heads"
    ).multi_head_attention_per_head(Q, K, V, num_heads=2)
    concatenated = concat_heads(per_head_output)
    expected = concatenated @ weight_o.T + bias_o

    result, _ = multi_head_attention(Q, K, V, num_heads=2, weight_o=weight_o, bias_o=bias_o)
    assert np.allclose(result, expected, atol=1e-6)
