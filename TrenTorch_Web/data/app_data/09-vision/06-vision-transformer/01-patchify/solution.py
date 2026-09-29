import numpy as np


def patchify(image: np.ndarray, patch_size: int) -> np.ndarray:
    C, H, W = image.shape
    p = patch_size
    n_h, n_w = H // p, W // p
    patches = image.reshape(C, n_h, p, n_w, p)
    patches = patches.transpose(1, 3, 0, 2, 4)
    return patches.reshape(n_h * n_w, C * p * p)
