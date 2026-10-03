import numpy as np


def oof_predictions(model_fn, X: np.ndarray, y: np.ndarray, n_splits: int = 3) -> np.ndarray:
    X = np.asarray(X)
    y = np.asarray(y)
    n = len(X)
    if not 2 <= n_splits <= n:
        raise ValueError("n_splits must satisfy 2 <= n_splits <= number of rows")
    out = np.zeros(n)
    for block in np.array_split(np.arange(n), n_splits):
        train = np.setdiff1d(np.arange(n), block)
        out[block] = model_fn(X[train], y[train], X[block])
    return out


def stacking_weights(P: np.ndarray, y: np.ndarray) -> np.ndarray:
    P = np.asarray(P, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(P) != len(y):
        raise ValueError("P and y must have the same number of rows")
    w, *_ = np.linalg.lstsq(P, y, rcond=None)
    return w
