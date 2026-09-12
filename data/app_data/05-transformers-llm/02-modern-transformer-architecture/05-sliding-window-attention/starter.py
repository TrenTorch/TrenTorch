import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

scaled_dot_product_attention = load_solution(
    "04-seq-modeling/04-attention/01-scaled-dot-product-attention"
).scaled_dot_product_attention


def build_sliding_window_mask(seq_len: int, window_size: int) -> np.ndarray:
    """
    Like `[04-seq-modeling/04-attention/02-causal-mask]`'s causal mask
    (no attending to the future), but ALSO forbidding attending too far
    into the PAST: position `i` may only attend to positions `j` with
    `i - window_size < j <= i` (itself and the `window_size - 1`
    positions immediately before it).
    """
    pass


def sliding_window_attention(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    window_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    `[01-scaled-dot-product-attention]`'s attention, restricted to a
    sliding window via `build_sliding_window_mask`.
    """
    pass
