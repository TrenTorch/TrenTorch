import numpy as np


def gaussian_kernel(size, sigma):
    r = size // 2
    k = np.arange(size) - r
    w = np.exp(-(k ** 2) / (2 * sigma ** 2))
    return w / w.sum()


def _filter_axis(padded, w, axis):
    size = len(w)
    n = padded.shape[axis] - size + 1
    out = np.zeros_like(padded[tuple(slice(0, n) if a == axis else slice(None) for a in range(padded.ndim))])
    for k in range(size):
        sl = tuple(slice(k, k + n) if a == axis else slice(None) for a in range(padded.ndim))
        out = out + w[k] * padded[sl]
    return out


def gaussian_blur(img, size, sigma):
    img = np.asarray(img, dtype=float)
    r = size // 2
    w = gaussian_kernel(size, sigma)
    padded = np.pad(img, r, mode="edge")
    rows = _filter_axis(padded, w, axis=1)
    return _filter_axis(rows, w, axis=0)
