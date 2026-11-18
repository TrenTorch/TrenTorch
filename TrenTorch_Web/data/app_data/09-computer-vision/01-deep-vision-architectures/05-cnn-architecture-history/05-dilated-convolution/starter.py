import numpy as np


def dilated_conv2d(image: np.ndarray, kernel: np.ndarray, dilation: int = 1) -> np.ndarray:
    """
    image: shape (H, W)
    kernel: shape (kH, kW)
    dilation: spacing (in pixels) between consecutive kernel taps;
        dilation=1 is a plain, ordinary convolution

    A dilated ("atrous") convolution keeps the same number of kernel
    weights, but spreads them out in the input, skipping (dilation - 1)
    pixels between each tap. This grows the receptive field without
    adding any parameters or any extra compute.
    """
    # TODO: compute the kernel's EFFECTIVE size once dilation is applied:
    # eff_kH = (kH - 1) * dilation + 1 (same for eff_kW). Then, for every
    # output position (i, j), take the strided patch
    # image[i : i+eff_kH : dilation, j : j+eff_kW : dilation] (this
    # slice, with a `dilation` step, picks out exactly the pixels the
    # spread-out kernel taps land on) and sum its elementwise product
    # with kernel.
    pass
