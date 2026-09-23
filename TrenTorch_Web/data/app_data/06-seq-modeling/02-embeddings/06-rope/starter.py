import numpy as np


def compute_rope_angles(seq_len: int, dim: int) -> np.ndarray:
    """
    Computes the rotation angle for every (position, dimension-pair)
    combination, shape (seq_len, dim // 2). Uses the SAME frequency
    formula as `[03-sinusoidal-positional-encoding]`'s div_term:
    frequency[i] = 10000^(-2i/dim), so angle(pos, i) = pos * frequency[i].
    """
    position = np.arange(seq_len)[:, None]
    freq = 10000.0 ** (-np.arange(0, dim, 2) / dim)
    pass


def apply_rope(x: np.ndarray, angles: np.ndarray) -> np.ndarray:
    """
    Applies rotary position embedding to `x` (shape (..., dim), typically
    a query or key vector, or a batch/sequence of them), using the
    precomputed `angles` (shape (..., dim // 2), matching x's leading
    dimensions except the last). Unlike `[05-combine-token-positional-
    embeddings]`'s simple addition, RoPE ROTATES each consecutive PAIR of
    dimensions (x[..., 2i], x[..., 2i+1]) by that pair's own angle,
    treating each pair as a 2D point being rotated:

        x'_2i   = x_2i * cos(angle) - x_{2i+1} * sin(angle)
        x'_2i+1 = x_2i * sin(angle) + x_{2i+1} * cos(angle)
    """
    pass
