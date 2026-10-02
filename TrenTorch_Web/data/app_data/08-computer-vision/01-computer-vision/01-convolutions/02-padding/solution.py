
import numpy as np

from _load import load_solution

conv2d_single_filter = load_solution("vision-conv-single-filter").conv2d_single_filter


def conv2d_with_padding(image: np.ndarray, kernel: np.ndarray, padding: str = "valid") -> np.ndarray:
    if padding == "valid":
        return conv2d_single_filter(image, kernel)
    if padding == "same":
        kH, kW = kernel.shape
        pad_h, pad_w = (kH - 1) // 2, (kW - 1) // 2
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)))
        return conv2d_single_filter(padded, kernel)
    raise ValueError(f"unknown padding mode {padding!r}")
