import numpy as np


def pointwise_conv(x: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    C_in, H, W = x.shape
    C_out = kernel.shape[0]
    weight = kernel.reshape(C_out, C_in)
    x_flat = x.reshape(C_in, H * W)
    out_flat = weight @ x_flat
    return out_flat.reshape(C_out, H, W)
