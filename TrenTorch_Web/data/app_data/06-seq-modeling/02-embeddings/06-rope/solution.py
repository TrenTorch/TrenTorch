import numpy as np


def compute_rope_angles(seq_len: int, dim: int) -> np.ndarray:
    position = np.arange(seq_len)[:, None]
    freq = 10000.0 ** (-np.arange(0, dim, 2) / dim)
    return position * freq


def apply_rope(x: np.ndarray, angles: np.ndarray) -> np.ndarray:
    cos = np.cos(angles)
    sin = np.sin(angles)

    x1 = x[..., 0::2]
    x2 = x[..., 1::2]

    rotated = np.empty_like(x)
    rotated[..., 0::2] = x1 * cos - x2 * sin
    rotated[..., 1::2] = x1 * sin + x2 * cos
    return rotated
