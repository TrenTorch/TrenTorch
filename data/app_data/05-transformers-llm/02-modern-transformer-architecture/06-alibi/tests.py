"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/06-alibi/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
compute_alibi_slopes = _module.compute_alibi_slopes
compute_alibi_bias = _module.compute_alibi_bias
alibi_causal_mask = _module.alibi_causal_mask

scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention
build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def test_slopes_shape_and_all_positive():
    slopes = compute_alibi_slopes(num_heads=8)
    assert slopes.shape == (8,)
    assert np.all(slopes > 0)


def test_slopes_are_strictly_decreasing():
    slopes = compute_alibi_slopes(num_heads=8)
    assert np.all(np.diff(slopes) < 0)


def test_slopes_form_a_geometric_sequence_with_ratio_2_pow_neg_8_over_n():
    num_heads = 8
    slopes = compute_alibi_slopes(num_heads)
    ratio = 2.0 ** (-8.0 / num_heads)
    assert np.isclose(slopes[0], ratio)
    for i in range(1, num_heads):
        assert np.isclose(slopes[i] / slopes[i - 1], ratio, atol=1e-8)


def test_bias_shape():
    bias = compute_alibi_bias(seq_len=5, num_heads=4)
    assert bias.shape == (4, 5, 5)


def test_bias_is_zero_on_the_diagonal():
    bias = compute_alibi_bias(seq_len=5, num_heads=4)
    for h in range(4):
        assert np.allclose(np.diag(bias[h]), 0.0)


def test_bias_gets_more_negative_the_further_in_the_past_the_key_is():
    bias = compute_alibi_bias(seq_len=6, num_heads=2)
    head0 = bias[0]
    last_row = head0[-1]  # query at the last position, varying key position
    # last_row[j] should be monotonically increasing as j increases
    # (closer keys are less negative / more recent).
    assert np.all(np.diff(last_row) > 0)


def test_bias_scales_with_the_heads_own_slope():
    slopes = compute_alibi_slopes(num_heads=4)
    bias = compute_alibi_bias(seq_len=5, num_heads=4)
    # bias[h, i, j] = -slopes[h] * (i - j); check the ratio between two
    # heads' bias at the same (i, j) matches the ratio between their slopes.
    i, j = 4, 1
    ratio_bias = bias[1, i, j] / bias[0, i, j]
    ratio_slopes = slopes[1] / slopes[0]
    assert np.isclose(ratio_bias, ratio_slopes, atol=1e-8)


def test_alibi_causal_mask_still_blocks_the_future():
    seq_len, num_heads = 6, 4
    mask = alibi_causal_mask(seq_len, num_heads)
    for h in range(num_heads):
        for i in range(seq_len):
            for j in range(i + 1, seq_len):
                assert mask[h, i, j] == -np.inf


def test_alibi_causal_mask_equals_bias_plus_causal_mask():
    seq_len, num_heads = 5, 3
    mask = alibi_causal_mask(seq_len, num_heads)
    expected = compute_alibi_bias(seq_len, num_heads) + build_causal_mask(seq_len)[None, :, :]
    assert np.allclose(mask, expected, atol=1e-8)


def test_alibi_integrated_with_attention_gives_more_weight_to_recent_keys_when_content_scores_are_tied():
    # With all content-based scores equal (e.g. identical keys), ALiBi's
    # bias is the ONLY thing distinguishing positions, so attention
    # weight should be strictly higher for more RECENT keys.
    seq_len, d_k, num_heads = 5, 4, 2
    q = np.ones((num_heads, seq_len, d_k))
    k = np.ones((num_heads, seq_len, d_k))  # identical keys -> identical raw scores
    v = np.random.RandomState(0).randn(num_heads, seq_len, d_k)
    mask = alibi_causal_mask(seq_len, num_heads)

    _, weights = scaled_dot_product_attention(q, k, v, mask=mask)
    last_row = weights[0, -1]  # query at the last position, across all causally-visible keys
    # weights should increase monotonically as the key position gets more recent
    assert np.all(np.diff(last_row) >= -1e-12)
