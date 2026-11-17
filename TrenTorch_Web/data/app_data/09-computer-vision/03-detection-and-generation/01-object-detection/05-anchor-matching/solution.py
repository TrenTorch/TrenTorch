import numpy as np


def _iou_matrix(a, b):
    a, b = a[:, None, :], b[None, :, :]
    w = np.clip(np.minimum(a[..., 2], b[..., 2]) - np.maximum(a[..., 0], b[..., 0]), 0, None)
    h = np.clip(np.minimum(a[..., 3], b[..., 3]) - np.maximum(a[..., 1], b[..., 1]), 0, None)
    inter = w * h
    union = (a[..., 2] - a[..., 0]) * (a[..., 3] - a[..., 1]) + (b[..., 2] - b[..., 0]) * (b[..., 3] - b[..., 1]) - inter
    return np.where(union > 0, inter / np.where(union > 0, union, 1.0), 0.0)


def match_anchors(anchors, gt_boxes, pos_thresh, neg_thresh):
    anchors = np.asarray(anchors, dtype=float)
    gt = np.asarray(gt_boxes, dtype=float).reshape(-1, 4)
    A = len(anchors)
    if len(gt) == 0:
        return np.full(A, -1, dtype=int)
    iou = _iou_matrix(anchors, gt)
    best_gt = iou.argmax(axis=1)
    best_iou = iou.max(axis=1)
    matches = np.full(A, -2, dtype=int)
    matches[best_iou < neg_thresh] = -1
    pos = best_iou >= pos_thresh
    matches[pos] = best_gt[pos]
    for g in range(len(gt)):
        a = int(iou[:, g].argmax())
        if iou[a, g] > 0:
            matches[a] = g
    return matches
