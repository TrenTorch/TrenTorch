import numpy as np


def quantize_int8_per_channel(W: np.ndarray) -> dict:
    W = np.array(W, dtype=float)
    max_abs = np.max(np.abs(W), axis=1)
    scale = np.where(max_abs > 0, max_abs / 127.0, 0.0)

    safe_scale = np.where(scale == 0, 1.0, scale)
    Q = np.round(W / safe_scale[:, None])
    Q = np.clip(Q, -127, 127)
    Q = np.where(scale[:, None] == 0, 0, Q).astype(int)

    W_hat = Q * scale[:, None]
    return {"quantized": Q, "scale": scale, "dequantized": W_hat}
