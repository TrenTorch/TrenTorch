import numpy as np


def conv2d_valid(img, kernel):
    H, W = img.shape
    kh, kw = kernel.shape
    out = np.zeros((H - kh + 1, W - kw + 1))
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i, j] = np.sum(img[i : i + kh, j : j + kw] * kernel)
    return out
