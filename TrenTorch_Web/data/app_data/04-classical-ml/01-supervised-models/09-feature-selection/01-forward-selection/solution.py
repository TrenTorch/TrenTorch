import numpy as np


def _r2(Xs: np.ndarray, y: np.ndarray) -> float:
    A = np.column_stack([np.ones(len(y)), Xs])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    ss_res = float(np.sum((y - A @ coef) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot == 0.0:
        return 0.0
    return 1.0 - ss_res / ss_tot


def forward_selection(X: np.ndarray, y: np.ndarray, k: int) -> list:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    d = X.shape[1]
    if k < 1 or k > d:
        raise ValueError("k must be between 1 and the number of features")
    selected = []
    for _ in range(k):
        best, best_score = None, -np.inf
        for j in range(d):
            if j in selected:
                continue
            score = _r2(X[:, selected + [j]], y)
            if score > best_score:
                best, best_score = j, score
        selected.append(best)
    return selected
