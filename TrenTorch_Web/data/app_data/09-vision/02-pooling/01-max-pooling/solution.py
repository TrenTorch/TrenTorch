import numpy as np


def max_pool2d(image: np.ndarray, kernel_size: int, stride: int | None = None) -> np.ndarray:
    if stride is None:
        stride = kernel_size
    C, H, W = image.shape
    out_h = (H - kernel_size) // stride + 1
    out_w = (W - kernel_size) // stride + 1
    output = np.empty((C, out_h, out_w), dtype=image.dtype)
    for i in range(out_h):
        for j in range(out_w):
            row, col = i * stride, j * stride
            window = image[:, row : row + kernel_size, col : col + kernel_size]
            output[:, i, j] = window.max(axis=(1, 2))
    return output
