import numpy as np


def box_iou(a, b):
    a = np.asarray(a, dtype=float)[:, None, :]
    b = np.asarray(b, dtype=float)[None, :, :]
    ix1, iy1 = np.maximum(a[..., 0], b[..., 0]), np.maximum(a[..., 1], b[..., 1])
    ix2, iy2 = np.minimum(a[..., 2], b[..., 2]), np.minimum(a[..., 3], b[..., 3])
    inter = np.clip(ix2 - ix1, 0, None) * np.clip(iy2 - iy1, 0, None)
    area_a = (a[..., 2] - a[..., 0]) * (a[..., 3] - a[..., 1])
    area_b = (b[..., 2] - b[..., 0]) * (b[..., 3] - b[..., 1])
    union = area_a + area_b - inter
    return np.where(union > 0, inter / np.where(union > 0, union, 1.0), 0.0)
