import numpy as np


def compute_scale_zero_point(x: np.ndarray, num_bits: int = 8) -> tuple[float, int]:
    qmin, qmax = -(2 ** (num_bits - 1)), 2 ** (num_bits - 1) - 1
    x_min, x_max = float(x.min()), float(x.max())
    scale = (x_max - x_min) / (qmax - qmin) if x_max > x_min else 1.0
    zero_point = round(qmin - x_min / scale)
    zero_point = int(np.clip(zero_point, qmin, qmax))
    return scale, zero_point


def quantize(x: np.ndarray, num_bits: int = 8) -> tuple[np.ndarray, float, int]:
    qmin, qmax = -(2 ** (num_bits - 1)), 2 ** (num_bits - 1) - 1
    scale, zero_point = compute_scale_zero_point(x, num_bits)
    q = np.round(x / scale + zero_point)
    q = np.clip(q, qmin, qmax).astype(np.int8)
    return q, scale, zero_point
