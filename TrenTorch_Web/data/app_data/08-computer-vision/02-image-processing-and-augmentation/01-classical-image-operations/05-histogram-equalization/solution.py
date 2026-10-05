import numpy as np


def equalize_histogram(img):
    img = np.asarray(img)
    hist = np.bincount(img.ravel(), minlength=256)
    cdf = np.cumsum(hist)
    cdf_min = cdf[hist > 0][0]
    N = img.size
    if N == cdf_min:
        return img.copy()
    lut = np.clip(np.round((cdf - cdf_min) / (N - cdf_min) * 255), 0, 255).astype(np.uint8)
    return lut[img]
