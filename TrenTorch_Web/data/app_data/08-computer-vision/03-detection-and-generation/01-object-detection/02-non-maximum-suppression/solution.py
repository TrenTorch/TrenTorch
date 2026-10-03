import numpy as np


def _iou_one_to_many(box, boxes):
    x1 = np.maximum(box[0], boxes[:, 0])
    y1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[2], boxes[:, 2])
    y2 = np.minimum(box[3], boxes[:, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    union = (box[2] - box[0]) * (box[3] - box[1]) + (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1]) - inter
    return np.where(union > 0, inter / np.where(union > 0, union, 1.0), 0.0)


def nms(boxes, scores, iou_thresh):
    boxes = np.asarray(boxes, dtype=float)
    order = np.argsort(-np.asarray(scores, dtype=float), kind="stable")
    suppressed = np.zeros(len(boxes), dtype=bool)
    keep = []
    for i in order:
        if suppressed[i]:
            continue
        keep.append(int(i))
        suppressed |= _iou_one_to_many(boxes[i], boxes) > iou_thresh
    return keep
