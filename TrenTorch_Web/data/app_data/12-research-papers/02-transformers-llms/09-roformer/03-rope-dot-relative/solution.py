import numpy as np


def rope_dot(q, k, m, n, base=10000.0):
    def rotate(x, pos):
        d = x.shape[-1]
        theta = base ** (-2.0 * np.arange(d // 2) / d)
        ang = pos * theta
        out = np.empty_like(x, dtype=float)
        x1, x2 = x[0::2], x[1::2]
        out[0::2] = x1 * np.cos(ang) - x2 * np.sin(ang)
        out[1::2] = x1 * np.sin(ang) + x2 * np.cos(ang)
        return out

    return float(rotate(q, m) @ rotate(k, n))
