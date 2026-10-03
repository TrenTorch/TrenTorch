import numpy as np


def lvq1_step(prototypes: np.ndarray, proto_labels: np.ndarray, x: np.ndarray, y: int, lr: float):
    P = np.array(prototypes, dtype=float)
    labels = np.asarray(proto_labels)
    x = np.asarray(x, dtype=float)
    if P.ndim != 2 or len(P) == 0:
        raise ValueError("prototypes must be a non-empty 2-D array")
    if labels.shape != (len(P),) or x.shape != (P.shape[1],):
        raise ValueError("proto_labels and x must match the prototypes")
    if lr < 0:
        raise ValueError("lr must be nonnegative")
    dist = ((P - x) ** 2).sum(axis=1)
    winner = int(np.argmin(dist))
    sign = 1.0 if labels[winner] == y else -1.0
    P[winner] += sign * lr * (x - P[winner])
    return P, winner
