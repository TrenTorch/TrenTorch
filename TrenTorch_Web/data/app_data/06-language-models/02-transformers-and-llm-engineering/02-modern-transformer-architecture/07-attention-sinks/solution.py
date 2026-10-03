
import numpy as np

from _load import load_solution

build_sliding_window_mask = load_solution("txf-modern-sliding-window-attention").build_sliding_window_mask


def attention_sink_mask(seq_len: int, window_size: int, num_sink_tokens: int) -> np.ndarray:
    window_mask = build_sliding_window_mask(seq_len, window_size)

    positions = np.arange(seq_len)
    is_causally_visible = positions[None, :] <= positions[:, None]
    is_sink_token = positions[None, :] < num_sink_tokens
    always_visible = is_sink_token & is_causally_visible

    return np.where(always_visible, 0.0, window_mask)
