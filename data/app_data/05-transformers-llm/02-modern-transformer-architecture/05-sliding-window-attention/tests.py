"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/05-sliding-window-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
build_sliding_window_mask = _module.build_sliding_window_mask
sliding_window_attention = _module.sliding_window_attention

build_causal_mask = load_solution("04-seq-modeling/04-attention/02-causal-mask").build_causal_mask


def test_mask_shape_is_seq_len_by_seq_len():
    mask = build_sliding_window_mask(6, window_size=3)
    assert mask.shape == (6, 6)


def test_each_position_attends_to_at_most_window_size_positions():
    seq_len, window_size = 10, 4
    mask = build_sliding_window_mask(seq_len, window_size)
    allowed_counts = np.sum(mask == 0.0, axis=-1)
    assert np.all(allowed_counts <= window_size)


def test_last_position_attends_to_exactly_window_size_positions_when_window_fits():
    seq_len, window_size = 10, 4
    mask = build_sliding_window_mask(seq_len, window_size)
    last_row_allowed = np.sum(mask[-1] == 0.0)
    assert last_row_allowed == window_size


def test_is_still_causal_no_position_attends_to_the_future():
    seq_len, window_size = 8, 3
    mask = build_sliding_window_mask(seq_len, window_size)
    for i in range(seq_len):
        for j in range(i + 1, seq_len):
            assert mask[i, j] == -np.inf


def test_window_size_equal_to_seq_len_reduces_to_ordinary_causal_mask():
    seq_len = 6
    sliding_mask = build_sliding_window_mask(seq_len, window_size=seq_len)
    causal_mask = build_causal_mask(seq_len)
    assert np.array_equal(sliding_mask, causal_mask)


def test_window_size_one_only_allows_attending_to_self():
    seq_len = 5
    mask = build_sliding_window_mask(seq_len, window_size=1)
    expected = np.where(np.eye(seq_len) == 1, 0.0, -np.inf)
    assert np.array_equal(mask, expected)


def test_sliding_window_attention_output_shape():
    rng = np.random.RandomState(0)
    seq_len, d_k = 8, 4
    q, k, v = rng.randn(seq_len, d_k), rng.randn(seq_len, d_k), rng.randn(seq_len, d_k)
    output, weights = sliding_window_attention(q, k, v, window_size=3)
    assert output.shape == (seq_len, d_k)
    assert weights.shape == (seq_len, seq_len)


def test_sliding_window_attention_weights_are_zero_outside_the_window():
    rng = np.random.RandomState(1)
    seq_len, d_k, window_size = 8, 4, 3
    q, k, v = rng.randn(seq_len, d_k), rng.randn(seq_len, d_k), rng.randn(seq_len, d_k)
    _, weights = sliding_window_attention(q, k, v, window_size=window_size)
    for i in range(seq_len):
        for j in range(seq_len):
            if j > i or j <= i - window_size:
                assert weights[i, j] < 1e-10


def test_sliding_window_attention_output_at_a_late_position_is_unaffected_by_an_out_of_window_early_token():
    rng = np.random.RandomState(2)
    seq_len, d_k, window_size = 8, 4, 2
    q = rng.randn(seq_len, d_k)
    k, v = rng.randn(seq_len, d_k), rng.randn(seq_len, d_k)

    out_original, _ = sliding_window_attention(q, k, v, window_size=window_size)

    k_perturbed = k.copy()
    v_perturbed = v.copy()
    k_perturbed[0] += rng.randn(d_k) * 10.0
    v_perturbed[0] += rng.randn(d_k) * 10.0
    out_perturbed, _ = sliding_window_attention(q, k_perturbed, v_perturbed, window_size=window_size)

    # Position (seq_len - 1)'s window is [seq_len - window_size, seq_len - 1],
    # which does not include position 0.
    assert np.allclose(out_original[-1], out_perturbed[-1], atol=1e-8)
