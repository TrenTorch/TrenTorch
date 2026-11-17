import numpy as np


def quantization_error(x, bits):
    x = np.asarray(x, dtype=float)
    qmax = 2 ** (bits - 1) - 1
    m = np.max(np.abs(x))
    scale = m / qmax if m > 0 else 1.0
    q = np.clip(np.round(x / scale), -qmax, qmax)
    return float(np.mean(np.abs(x - q * scale)))
