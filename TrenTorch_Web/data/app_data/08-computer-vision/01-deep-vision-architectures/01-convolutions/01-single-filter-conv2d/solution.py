import numpy as np


def conv2d_single_filter(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    H, W = image.shape
    kH, kW = kernel.shape
    out_h, out_w = H - kH + 1, W - kW + 1
    output = np.empty((out_h, out_w), dtype=image.dtype)
    for i in range(out_h):
        for j in range(out_w):
            output[i, j] = np.sum(image[i : i + kH, j : j + kW] * kernel)
    return output
