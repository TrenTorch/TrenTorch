import numpy as np


def dilated_conv2d(image: np.ndarray, kernel: np.ndarray, dilation: int = 1) -> np.ndarray:
    H, W = image.shape
    kH, kW = kernel.shape
    eff_kH = (kH - 1) * dilation + 1
    eff_kW = (kW - 1) * dilation + 1
    out_h, out_w = H - eff_kH + 1, W - eff_kW + 1
    output = np.empty((out_h, out_w), dtype=image.dtype)
    for i in range(out_h):
        for j in range(out_w):
            patch = image[i : i + eff_kH : dilation, j : j + eff_kW : dilation]
            output[i, j] = np.sum(patch * kernel)
    return output
