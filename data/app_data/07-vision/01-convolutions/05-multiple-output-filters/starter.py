import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

conv2d_multi_channel = load_solution("07-vision/01-convolutions/04-multi-channel-input").conv2d_multi_channel


def conv2d_multi_filter(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    image:  shape (C_in, H, W)
    kernel: shape (C_out, C_in, kH, kW) -- C_out independent filters,
            each one shaped like 04-multi-channel-input's kernel

    Returns shape (C_out, H - kH + 1, W - kW + 1): each output channel
    is that filter's own multi-channel convolution over the same image.
    """
    # TODO: For each of the C_out filters, run
    # 04-multi-channel-input's conv2d_multi_channel with that filter's
    # own (C_in, kH, kW) slice of kernel, and stack the C_out results.
    pass
