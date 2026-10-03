import numpy as np


def average_precision(scores, is_tp, n_gt):
    scores = np.asarray(scores, dtype=float)
    if len(scores) == 0:
        return 0.0
    order = np.argsort(-scores, kind="stable")
    tp = np.asarray(is_tp, dtype=float)[order]
    ctp, cfp = np.cumsum(tp), np.cumsum(1.0 - tp)
    recall = np.concatenate([[0.0], ctp / n_gt, [1.0]])
    precision = np.concatenate([[1.0], ctp / (ctp + cfp), [0.0]])
    precision = np.maximum.accumulate(precision[::-1])[::-1]
    idx = np.where(recall[1:] != recall[:-1])[0]
    return float(np.sum((recall[idx + 1] - recall[idx]) * precision[idx + 1]))
