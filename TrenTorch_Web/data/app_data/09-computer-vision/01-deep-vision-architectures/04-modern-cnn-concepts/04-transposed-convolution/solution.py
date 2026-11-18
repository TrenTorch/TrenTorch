import numpy as np


def conv_transpose2d(x: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    _, H, W = x.shape
    _, _, kH, kW = kernel.shape
    out_h = (H - 1) * stride + kH
    out_w = (W - 1) * stride + kW
    output = np.zeros((1, out_h, out_w), dtype=x.dtype)
    k = kernel[0, 0]
    for i in range(H):
        for j in range(W):
            output[0, i * stride : i * stride + kH, j * stride : j * stride + kW] += x[0, i, j] * k
    return output
