
import numpy as np

from _load import load_solution

conv2d_multi_channel = load_solution("vision-conv-multi-channel").conv2d_multi_channel


def conv2d_multi_filter(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    C_out, C_in, kH, kW = kernel.shape
    _, H, W = image.shape
    output = np.empty((C_out, H - kH + 1, W - kW + 1), dtype=image.dtype)
    for f in range(C_out):
        output[f] = conv2d_multi_channel(image, kernel[f])
    return output
