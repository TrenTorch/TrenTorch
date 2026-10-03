
import numpy as np

from _load import load_solution

scaled_dot_product_attention = load_solution("seq-attention-scaled-dot-product").scaled_dot_product_attention


def build_sliding_window_mask(seq_len: int, window_size: int) -> np.ndarray:
    """
    Like `[06-language-models/01-tokens-embeddings-and-attention/03-attention/02-causal-mask]`'s causal mask
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
