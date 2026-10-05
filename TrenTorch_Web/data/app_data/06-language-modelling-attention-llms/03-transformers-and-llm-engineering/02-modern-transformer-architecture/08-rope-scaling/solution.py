
import numpy as np

from _load import load_solution

apply_rope = load_solution("seq-embeddings-rope").apply_rope


def compute_rope_angles_scaled(seq_len: int, dim: int, scale_factor: float) -> np.ndarray:
    position = np.arange(seq_len)[:, None] / scale_factor
    freq = 10000.0 ** (-np.arange(0, dim, 2) / dim)
    return position * freq
