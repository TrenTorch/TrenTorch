"""
pytest data/app_data/04-seq-modeling/04-attention/02-causal-mask/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/04-attention/{Path(__file__).resolve().parent.name}")
build_causal_mask = _module.build_causal_mask


def test_shape_is_seq_len_by_seq_len():
    mask = build_causal_mask(5)
    assert mask.shape == (5, 5)


def test_diagonal_is_always_zero_allowed():
    mask = build_causal_mask(4)
    for i in range(4):
        assert mask[i, i] == 0.0


def test_lower_triangle_is_zero_allowed():
    mask = build_causal_mask(4)
    for i in range(4):
        for j in range(i + 1):
            assert mask[i, j] == 0.0


def test_strict_upper_triangle_is_negative_infinity():
    mask = build_causal_mask(4)
    for i in range(4):
        for j in range(i + 1, 4):
            assert mask[i, j] == -np.inf


def test_matches_hand_computed_small_example():
    mask = build_causal_mask(3)
    expected = np.array([[0.0, -np.inf, -np.inf], [0.0, 0.0, -np.inf], [0.0, 0.0, 0.0]])
    assert np.array_equal(mask, expected)


def test_composed_with_attention_a_position_never_attends_to_the_future():
    attn_module = load_solution("04-seq-modeling/04-attention/01-scaled-dot-product-attention")
    scaled_dot_product_attention = attn_module.scaled_dot_product_attention

    rng = np.random.RandomState(0)
    seq_len = 5
    Q = rng.randn(1, seq_len, 4)
    K = rng.randn(1, seq_len, 4)
    V = rng.randn(1, seq_len, 4)
    mask = build_causal_mask(seq_len)
    _, weights = scaled_dot_product_attention(Q, K, V, mask=mask)
    for i in range(seq_len):
        for j in range(i + 1, seq_len):
            assert np.isclose(weights[0, i, j], 0.0, atol=1e-9)


def test_diagonal_is_not_accidentally_masked():
    # Directly targets a mutant that uses k=0 instead of k=1 in the
    # upper-triangle construction, which would incorrectly forbid every
    # position from attending to ITSELF too.
    mask = build_causal_mask(3)
    assert mask[0, 0] == 0.0
    assert mask[1, 1] == 0.0
    assert mask[2, 2] == 0.0
