import numpy as np


def patchify(img, p):
    """
    img: a 2D square image, shape (H, W), H and W multiples of p
    p: patch side length

    Returns:
        The image cut into non-overlapping p-by-p patches, each flattened, in row-major order.
        Shape (N, p * p) with N = (H // p) * (W // p).
    """
    # TODO: Split the image into a grid of patches and flatten each one (see Theory).
    pass
