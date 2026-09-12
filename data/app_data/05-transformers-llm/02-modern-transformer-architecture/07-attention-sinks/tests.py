"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/07-attention-sinks/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
attention_sink_mask = _module.attention_sink_mask

build_sliding_window_mask = load_solution(
    "05-transformers-llm/02-modern-transformer-architecture/05-sliding-window-attention"
).build_sliding_window_mask


def test_mask_shape():
    mask = attention_sink_mask(seq_len=10, window_size=3, num_sink_tokens=2)
    assert mask.shape == (10, 10)


def test_zero_sink_tokens_reduces_to_ordinary_sliding_window_mask():
    seq_len, window_size = 10, 3
    sink_mask = attention_sink_mask(seq_len, window_size, num_sink_tokens=0)
    window_mask = build_sliding_window_mask(seq_len, window_size)
    assert np.array_equal(sink_mask, window_mask)


def test_sink_tokens_are_visible_from_a_far_away_late_query_position():
    seq_len, window_size, num_sink_tokens = 20, 3, 2
    mask = attention_sink_mask(seq_len, window_size, num_sink_tokens)
    late_query = seq_len - 1
    for sink in range(num_sink_tokens):
        assert mask[late_query, sink] == 0.0


def test_still_causal_no_position_attends_to_the_future_even_for_sink_tokens():
    seq_len, window_size, num_sink_tokens = 8, 2, 3
    mask = attention_sink_mask(seq_len, window_size, num_sink_tokens)
    for i in range(seq_len):
        for j in range(i + 1, seq_len):
            assert mask[i, j] == -np.inf


def test_non_sink_positions_outside_the_window_are_still_masked():
    seq_len, window_size, num_sink_tokens = 10, 2, 1
    mask = attention_sink_mask(seq_len, window_size, num_sink_tokens)
    late_query = 9
    # position 5 is a non-sink token (index >= num_sink_tokens) outside
    # the window [late_query - window_size + 1, late_query] = [8, 9].
    assert mask[late_query, 5] == -np.inf


def test_a_sink_token_that_has_not_occurred_yet_is_still_masked():
    # Position 0 has not been "generated" yet from the perspective of an
    # even earlier query; causality must still apply to sink tokens.
    seq_len, window_size, num_sink_tokens = 5, 2, 3
    mask = attention_sink_mask(seq_len, window_size, num_sink_tokens)
    # Query at position 1 cannot see sink token at position 2 (future).
    assert mask[1, 2] == -np.inf
    # But it can see sink tokens at positions 0 and 1 (past/self).
    assert mask[1, 0] == 0.0
    assert mask[1, 1] == 0.0


def test_increasing_num_sink_tokens_only_ever_reveals_more_never_hides():
    # Directly targets a mutant that accidentally REMOVES visibility
    # somewhere when combining the sink and window logic.
    seq_len, window_size = 12, 3
    mask_fewer_sinks = attention_sink_mask(seq_len, window_size, num_sink_tokens=1)
    mask_more_sinks = attention_sink_mask(seq_len, window_size, num_sink_tokens=4)
    visible_fewer = mask_fewer_sinks == 0.0
    visible_more = mask_more_sinks == 0.0
    # Every position visible with fewer sinks must still be visible with more.
    assert np.all(visible_more[visible_fewer])
