import numpy as np


def center_crop(x, h, w):
    H, W = x.shape[:2]
    top = (H - h) // 2
    left = (W - w) // 2
    return x[top : top + h, left : left + w]
