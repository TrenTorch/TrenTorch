import numpy as np

NF4_LEVELS = np.array([-1.0, -0.6961928009986877, -0.5250730514526367, -0.39491748809814453, -0.28444138169288635, -0.18477343022823334, -0.09105003625225449, 0.0, 0.07958029955625534, 0.16093020141391754, 0.24611230194568542, 0.33791524171829224, 0.44070982933883667, 0.5626170039176941, 0.7229568362236755, 1.0])


def nf4_quantize(w, block_size):
    blocks = np.asarray(w, dtype=float).reshape(-1, block_size)
    scales = np.abs(blocks).max(axis=1)
    safe = np.where(scales == 0, 1.0, scales)
    normed = blocks / safe[:, None]
    codes = np.abs(normed[..., None] - NF4_LEVELS[None, None, :]).argmin(axis=2)
    return codes.reshape(-1), scales


def nf4_dequantize(codes, scales, block_size):
    levels = NF4_LEVELS[np.asarray(codes)].reshape(-1, block_size)
    return (levels * np.asarray(scales)[:, None]).reshape(-1)
