import numpy as np


def conv2d_with_stride(image: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    H, W = image.shape
    kH, kW = kernel.shape
    out_h = (H - kH) // stride + 1
    out_w = (W - kW) // stride + 1
    output = np.empty((out_h, out_w), dtype=image.dtype)
    for i in range(out_h):
        for j in range(out_w):
            row, col = i * stride, j * stride
            output[i, j] = np.sum(image[row : row + kH, col : col + kW] * kernel)
    return output
