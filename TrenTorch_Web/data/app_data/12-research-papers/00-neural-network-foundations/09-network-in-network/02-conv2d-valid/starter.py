import numpy as np


def conv2d_valid(img, kernel):
    """
    img: 2D array, shape (H, W)
    kernel: 2D filter, shape (kh, kw)

    Returns:
        The 'valid' cross-correlation of img with kernel, shape
        (H - kh + 1, W - kw + 1). No padding.
    """
    # TODO: Slide the kernel over every valid position and sum the products.
    pass
