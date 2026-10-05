import numpy as np


def optics(X: np.ndarray, min_samples: int, max_eps: float = np.inf):
    X = np.asarray(X, dtype=float)
    n = len(X)
    if not 1 <= min_samples <= n:
        raise ValueError("min_samples must satisfy 1 <= min_samples <= number of rows")
    D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)
    core = np.sort(D, axis=1)[:, min_samples - 1]
    core = np.where(core <= max_eps, core, np.inf)

    reach = np.full(n, np.inf)
    processed = np.zeros(n, dtype=bool)
    order = []

    def update(p):
        nb = np.flatnonzero((D[p] <= max_eps) & ~processed)
        newr = np.maximum(core[p], D[p, nb])
        reach[nb] = np.minimum(reach[nb], newr)

    for start in range(n):
        if processed[start]:
            continue
        processed[start] = True
        order.append(start)
        if not np.isfinite(core[start]):
            continue
        update(start)
        while True:
            cand = np.flatnonzero(~processed & np.isfinite(reach))
            if len(cand) == 0:
                break
            q = cand[np.argmin(reach[cand])]
            processed[q] = True
            order.append(q)
            if np.isfinite(core[q]):
                update(q)
    return np.array(order, dtype=int), reach
