import numpy as np


def quantize_int4_groupwise(W: np.ndarray, group_size: int) -> dict:
    W = np.array(W, dtype=float)
    out_features, in_features = W.shape
    assert in_features % group_size == 0, "in_features must be divisible by group_size"
    n_groups = in_features // group_size

    W_grouped = W.reshape(out_features, n_groups, group_size)
    max_abs = np.max(np.abs(W_grouped), axis=-1)
    scale = np.where(max_abs > 0, max_abs / 7.0, 0.0)

    safe_scale = np.where(scale == 0, 1.0, scale)
    Q_grouped = np.round(W_grouped / safe_scale[:, :, None])
    Q_grouped = np.clip(Q_grouped, -7, 7)
    Q_grouped = np.where(scale[:, :, None] == 0, 0, Q_grouped).astype(int)

    W_hat_grouped = Q_grouped * scale[:, :, None]

    Q = Q_grouped.reshape(out_features, in_features)
    W_hat = W_hat_grouped.reshape(out_features, in_features)
    return {"quantized": Q, "scale": scale, "dequantized": W_hat}
