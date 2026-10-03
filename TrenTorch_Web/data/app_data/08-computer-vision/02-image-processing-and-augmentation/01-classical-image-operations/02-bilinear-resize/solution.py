import numpy as np


def bilinear_resize(img, out_h, out_w):
    img = np.asarray(img, dtype=float)
    H, W = img.shape
    y = np.clip((np.arange(out_h) + 0.5) * H / out_h - 0.5, 0, H - 1)
    x = np.clip((np.arange(out_w) + 0.5) * W / out_w - 0.5, 0, W - 1)
    y0, x0 = np.floor(y).astype(int), np.floor(x).astype(int)
    y1, x1 = np.minimum(y0 + 1, H - 1), np.minimum(x0 + 1, W - 1)
    wy, wx = (y - y0)[:, None], (x - x0)[None, :]
    top = img[y0[:, None], x0[None, :]] * (1 - wx) + img[y0[:, None], x1[None, :]] * wx
    bot = img[y1[:, None], x0[None, :]] * (1 - wx) + img[y1[:, None], x1[None, :]] * wx
    return top * (1 - wy) + bot * wy
