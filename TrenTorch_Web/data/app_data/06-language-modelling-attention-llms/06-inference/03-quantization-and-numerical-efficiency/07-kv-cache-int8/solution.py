import numpy as np


def quantize_kv(kv):
    kv = np.asarray(kv, dtype=float)
    amax = np.abs(kv).max(axis=-1)
    scale = np.where(amax == 0, 1.0, amax / 127.0)
    q = np.clip(np.round(kv / scale[..., None]), -127, 127).astype(np.int8)
    return q, scale


def dequantize_kv(q, scale):
    return q.astype(float) * np.asarray(scale)[..., None]
