import numpy as np


def conv2d_im2col(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    C_out, C_in, kH, kW = kernel.shape
    _, H, W = image.shape
    out_h, out_w = H - kH + 1, W - kW + 1

    windows = np.lib.stride_tricks.sliding_window_view(image, (kH, kW), axis=(1, 2))
    # windows: (C_in, out_h, out_w, kH, kW) -> (out_h*out_w, C_in*kH*kW)
    cols = windows.transpose(1, 2, 0, 3, 4).reshape(out_h * out_w, C_in * kH * kW)
    kernel_flat = kernel.reshape(C_out, C_in * kH * kW)

    out_flat = cols @ kernel_flat.T  # (out_h*out_w, C_out)
    return out_flat.T.reshape(C_out, out_h, out_w)
