import numpy as np


def quantize_int8_symmetric(x: np.ndarray) -> dict:
    x = np.array(x, dtype=float)
    max_abs = np.max(np.abs(x)) if x.size > 0 else 0.0
    scale = max_abs / 127.0 if max_abs > 0 else 0.0

    if scale == 0.0:
        q = np.zeros_like(x, dtype=int)
    else:
        q = np.clip(np.round(x / scale), -127, 127).astype(int)

    x_hat = q * scale
    return {"quantized": q, "scale": float(scale), "dequantized": x_hat}
