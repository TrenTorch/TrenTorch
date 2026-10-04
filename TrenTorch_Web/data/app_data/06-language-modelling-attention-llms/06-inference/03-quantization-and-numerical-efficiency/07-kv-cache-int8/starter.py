import numpy as np


def quantize_kv(kv: np.ndarray):
    """kv: (T, H, d) -> (q int8 (T, H, d), scale (T, H))."""
    # TODO
    pass


def dequantize_kv(q: np.ndarray, scale: np.ndarray) -> np.ndarray:
    """Reconstruct floats: q * scale[..., None]."""
    # TODO
    pass
