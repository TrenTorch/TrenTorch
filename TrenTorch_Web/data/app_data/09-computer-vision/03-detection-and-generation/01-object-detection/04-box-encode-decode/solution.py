import numpy as np


def _to_cxcywh(b):
    w, h = b[:, 2] - b[:, 0], b[:, 3] - b[:, 1]
    return b[:, 0] + w / 2, b[:, 1] + h / 2, w, h


def encode_boxes(gt, anchors):
    gx, gy, gw, gh = _to_cxcywh(np.asarray(gt, dtype=float))
    ax, ay, aw, ah = _to_cxcywh(np.asarray(anchors, dtype=float))
    return np.stack([(gx - ax) / aw, (gy - ay) / ah, np.log(gw / aw), np.log(gh / ah)], axis=1)


def decode_boxes(deltas, anchors):
    d = np.asarray(deltas, dtype=float)
    ax, ay, aw, ah = _to_cxcywh(np.asarray(anchors, dtype=float))
    cx, cy = ax + aw * d[:, 0], ay + ah * d[:, 1]
    w, h = aw * np.exp(d[:, 2]), ah * np.exp(d[:, 3])
    return np.stack([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], axis=1)
