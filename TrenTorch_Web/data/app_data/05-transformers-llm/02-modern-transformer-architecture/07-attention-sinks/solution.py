import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

build_sliding_window_mask = load_solution(
    "05-transformers-llm/02-modern-transformer-architecture/05-sliding-window-attention"
).build_sliding_window_mask


def attention_sink_mask(seq_len: int, window_size: int, num_sink_tokens: int) -> np.ndarray:
    window_mask = build_sliding_window_mask(seq_len, window_size)

    positions = np.arange(seq_len)
    is_causally_visible = positions[None, :] <= positions[:, None]
    is_sink_token = positions[None, :] < num_sink_tokens
    always_visible = is_sink_token & is_causally_visible

    return np.where(always_visible, 0.0, window_mask)
