import numpy as np


def s3vm_objective(
    w: np.ndarray,
    b: float,
    X_l: np.ndarray,
    y_l: np.ndarray,
    X_u: np.ndarray,
    C: float,
    C_u: float,
) -> float:
    w = np.asarray(w, dtype=float)
    X_l = np.asarray(X_l, dtype=float)
    X_u = np.asarray(X_u, dtype=float)
    y_l = np.asarray(y_l, dtype=float)
    if w.ndim != 1:
        raise ValueError("w must be 1-D")
    d = w.shape[0]
    if X_l.ndim != 2 or X_l.shape[1] != d or y_l.shape != (X_l.shape[0],):
        raise ValueError("labeled inputs have inconsistent shapes")
    if X_u.size and (X_u.ndim != 2 or X_u.shape[1] != d):
        raise ValueError("unlabeled inputs have inconsistent shapes")
    if not np.all(np.isin(y_l, [-1.0, 1.0])):
        raise ValueError("labels must be -1 or +1")
    if C < 0 or C_u < 0:
        raise ValueError("C and C_u must be nonnegative")
    f_l = X_l @ w + b
    lab_term = np.maximum(0.0, 1.0 - y_l * f_l).sum()
    if X_u.size:
        f_u = X_u @ w + b
        unlab_term = np.maximum(0.0, 1.0 - np.abs(f_u)).sum()
    else:
        unlab_term = 0.0
    return float(0.5 * w @ w + C * lab_term + C_u * unlab_term)
