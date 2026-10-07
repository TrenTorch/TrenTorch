import numpy as np

def solve(y, scores):
    y = np.asarray(y)
    scores = np.asarray(scores, dtype=float)
    best_j, best_t = -np.inf, None
    for t in np.unique(scores):
        p = scores >= t
        tp = ((y == 1) & p).sum()
        fn = ((y == 1) & ~p).sum()
        fp = ((y == 0) & p).sum()
        tn = ((y == 0) & ~p).sum()
        tpr = tp / (tp + fn) if tp + fn else 0
        fpr = fp / (fp + tn) if fp + tn else 0
        j = tpr - fpr
        if j > best_j + 1e-12:
            best_j, best_t = j, t
    return best_t
