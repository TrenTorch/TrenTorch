import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

build_sliding_window_mask = load_solution(
    "05-transformers-llm/02-modern-transformer-architecture/05-sliding-window-attention"
).build_sliding_window_mask


def attention_sink_mask(seq_len: int, window_size: int, num_sink_tokens: int) -> np.ndarray:
    """
    `[05-sliding-window-attention]`'s bounded window, but with the first
    `num_sink_tokens` positions kept ALWAYS visible (subject only to
    ordinary causality, `j <= i`), regardless of how far outside the
    sliding window they'd otherwise fall.
    """
    pass
