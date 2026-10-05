import numpy as np


def rotate_nearest(img, angle_deg):
    img = np.asarray(img)
    H, W = img.shape
    cy, cx = (H - 1) / 2, (W - 1) / 2
    a = np.deg2rad(angle_deg)
    c, s = np.cos(a), np.sin(a)
    r, col = np.meshgrid(np.arange(H), np.arange(W), indexing="ij")
    dy, dx = r - cy, col - cx
    sy = np.rint(c * dy + s * dx + cy).astype(int)
    sx = np.rint(-s * dy + c * dx + cx).astype(int)
    ok = (sy >= 0) & (sy < H) & (sx >= 0) & (sx < W)
    out = np.zeros_like(img)
    out[ok] = img[sy[ok], sx[ok]]
    return out
