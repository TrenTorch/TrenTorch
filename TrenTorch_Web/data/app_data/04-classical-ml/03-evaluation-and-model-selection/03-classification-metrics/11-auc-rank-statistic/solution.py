import numpy as np


def auc_rank(scores: np.ndarray, labels: np.ndarray) -> float:
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels)
    if s.ndim != 1 or y.shape != s.shape:
        raise ValueError("scores and labels must be 1-D with the same length")
    if not np.all(np.isin(y, [0, 1])):
        raise ValueError("labels must be 0 or 1")
    n_pos = int(y.sum())
    n_neg = y.size - n_pos
    if n_pos == 0 or n_neg == 0:
        raise ValueError("both classes must be present")
    order = np.argsort(s, kind="stable")
    ranks = np.empty(s.size, dtype=float)
    i = 0
    while i < s.size:
        j = i
        while j + 1 < s.size and s[order[j + 1]] == s[order[i]]:
            j += 1
        ranks[order[i : j + 1]] = (i + j) / 2 + 1
        i = j + 1
    r_pos = ranks[y == 1].sum()
    return float((r_pos - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))
