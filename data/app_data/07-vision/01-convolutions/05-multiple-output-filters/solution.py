import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_channel = load_solution("07-vision/01-convolutions/04-multi-channel-input").conv2d_multi_channel


def conv2d_multi_filter(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    C_out, C_in, kH, kW = kernel.shape
    _, H, W = image.shape
    output = np.empty((C_out, H - kH + 1, W - kW + 1), dtype=image.dtype)
    for f in range(C_out):
        output[f] = conv2d_multi_channel(image, kernel[f])
    return output
