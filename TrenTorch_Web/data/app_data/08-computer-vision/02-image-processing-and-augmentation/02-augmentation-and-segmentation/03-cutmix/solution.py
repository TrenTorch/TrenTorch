import numpy as np


def cutmix_box(H, W, lam, cy, cx):
    cut_h = int(H * np.sqrt(1 - lam))
    cut_w = int(W * np.sqrt(1 - lam))
    y1, y2 = np.clip(cy - cut_h // 2, 0, H), np.clip(cy + cut_h // 2, 0, H)
    x1, x2 = np.clip(cx - cut_w // 2, 0, W), np.clip(cx + cut_w // 2, 0, W)
    return int(y1), int(y2), int(x1), int(x2)


def cutmix(img_a, img_b, box):
    y1, y2, x1, x2 = box
    out = np.array(img_a, copy=True)
    out[y1:y2, x1:x2] = np.asarray(img_b)[y1:y2, x1:x2]
    return out


def adjusted_lambda(box, H, W):
    y1, y2, x1, x2 = box
    return 1.0 - (y2 - y1) * (x2 - x1) / (H * W)
