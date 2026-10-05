import numpy as np


def average_precision(y_true: np.ndarray, scores: np.ndarray) -> float:
    y_true = np.asarray(y_true)
    scores = np.asarray(scores, dtype=float)
    if y_true.shape != scores.shape:
        raise ValueError("y_true and scores must have the same length")
    positives = np.sum(y_true == 1)
    if positives == 0:
        raise ValueError("average precision needs at least one positive label")
    order = np.argsort(-scores, kind="stable")
    labels = (y_true[order] == 1).astype(float)
    sorted_scores = scores[order]
    tp = np.cumsum(labels)
    fp = np.cumsum(1.0 - labels)
    cut = np.append(np.flatnonzero(np.diff(sorted_scores) != 0), len(scores) - 1)
    precision = tp[cut] / (tp[cut] + fp[cut])
    recall = tp[cut] / positives
    recall_prev = np.concatenate([[0.0], recall[:-1]])
    return float(np.sum((recall - recall_prev) * precision))
