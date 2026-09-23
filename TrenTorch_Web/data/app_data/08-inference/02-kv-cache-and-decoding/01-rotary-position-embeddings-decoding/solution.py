import numpy as np


def apply_rope(x: np.ndarray, position, base: float = 10000.0) -> np.ndarray:
    x = np.array(x, dtype=float)
    single = x.ndim == 1
    if single:
        x = x[None, :]
        position = [position]
    positions = np.array(position, dtype=float)
    seq_len, d = x.shape
    half = d // 2
    i = np.arange(half)
    theta = base ** (-2.0 * i / d)
    angles = positions[:, None] * theta[None, :]
    cos, sin = np.cos(angles), np.sin(angles)

    x_even, x_odd = x[:, 0::2], x[:, 1::2]
    out = np.empty_like(x)
    out[:, 0::2] = x_even * cos - x_odd * sin
    out[:, 1::2] = x_even * sin + x_odd * cos
    return out[0] if single else out
