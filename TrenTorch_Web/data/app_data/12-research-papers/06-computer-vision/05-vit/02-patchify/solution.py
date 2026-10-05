import numpy as np


def patchify(img, p):
    img = np.asarray(img, dtype=float)
    H, W = img.shape
    return img.reshape(H // p, p, W // p, p).transpose(0, 2, 1, 3).reshape(-1, p * p)
