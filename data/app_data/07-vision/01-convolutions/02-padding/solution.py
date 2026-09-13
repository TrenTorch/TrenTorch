import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_single_filter = load_solution("07-vision/01-convolutions/01-single-filter-conv2d").conv2d_single_filter


def conv2d_with_padding(image: np.ndarray, kernel: np.ndarray, padding: str = "valid") -> np.ndarray:
    if padding == "valid":
        return conv2d_single_filter(image, kernel)
    if padding == "same":
        kH, kW = kernel.shape
        pad_h, pad_w = (kH - 1) // 2, (kW - 1) // 2
        padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)))
        return conv2d_single_filter(padded, kernel)
    raise ValueError(f"unknown padding mode {padding!r}")
