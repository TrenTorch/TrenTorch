import numpy as np


def flatten(image: np.ndarray) -> np.ndarray:
    """
    image: shape (C, H, W)

    Returns a 1D array of length C*H*W: every value from image, in the
    same channel-major, row-major order the array is already stored in.
    """
    # TODO: A single reshape. No loop, no transpose -- the array's own
    # memory layout is already in the order the flattened vector needs.
    pass
