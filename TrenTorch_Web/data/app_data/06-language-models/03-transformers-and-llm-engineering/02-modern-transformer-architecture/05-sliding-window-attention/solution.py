
import numpy as np

from _load import load_solution

scaled_dot_product_attention = load_solution("seq-attention-scaled-dot-product").scaled_dot_product_attention


def build_sliding_window_mask(seq_len: int, window_size: int) -> np.ndarray:
    positions = np.arange(seq_len)
    distance = positions[:, None] - positions[None, :]
    allowed = (distance >= 0) & (distance < window_size)
    mask = np.where(allowed, 0.0, -np.inf)
    return mask


def sliding_window_attention(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    window_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    seq_len = query.shape[-2]
    mask = build_sliding_window_mask(seq_len, window_size)
    return scaled_dot_product_attention(query, key, value, mask=mask)
