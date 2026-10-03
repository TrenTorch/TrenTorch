import numpy as np


def _average_rank_desc(row: np.ndarray) -> np.ndarray:
    # Rank 1 goes to the largest score. Tied scores share the mean of their positions.
    order = np.argsort(-row, kind="stable")
    ranks = np.empty(row.size, dtype=float)
    i = 0
    while i < row.size:
        j = i
        while j + 1 < row.size and row[order[j + 1]] == row[order[i]]:
            j += 1
        ranks[order[i : j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def friedman_statistic(scores: np.ndarray) -> float:
    S = np.asarray(scores, dtype=float)
    if S.ndim != 2 or S.shape[0] < 1 or S.shape[1] < 2:
        raise ValueError("scores must be (N, k) with N >= 1 and k >= 2")
    if not np.all(np.isfinite(S)):
        raise ValueError("scores must be finite")
    N, k = S.shape
    ranks = np.vstack([_average_rank_desc(row) for row in S])
    R = ranks.sum(axis=0)
    return float(12.0 / (N * k * (k + 1)) * np.sum(R ** 2) - 3 * N * (k + 1))
