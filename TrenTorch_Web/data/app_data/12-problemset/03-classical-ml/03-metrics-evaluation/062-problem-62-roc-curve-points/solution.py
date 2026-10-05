import numpy as np

def solve(y, scores):
    y = np.asarray(y)
    scores = np.asarray(scores, dtype=float)
    positive_count = np.sum(y == 1)
    negative_count = np.sum(y == 0)
    points = []
    for threshold in np.unique(scores)[::-1]:
        selected = scores >= threshold
        true_positive = np.sum((y == 1) & selected)
        false_positive = np.sum((y == 0) & selected)
        tpr = true_positive / positive_count if positive_count else 0.0
        fpr = false_positive / negative_count if negative_count else 0.0
        points.append((float(fpr), float(tpr)))
    return points
