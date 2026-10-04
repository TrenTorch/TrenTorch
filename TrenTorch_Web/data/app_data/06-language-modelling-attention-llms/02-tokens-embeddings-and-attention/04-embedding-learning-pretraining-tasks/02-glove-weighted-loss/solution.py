import numpy as np


def cooccurrence_matrix(token_ids, V, window):
    X = np.zeros((V, V))
    n = len(token_ids)
    for i in range(n):
        for j in range(max(0, i - window), min(n, i + window + 1)):
            if j != i:
                X[token_ids[i], token_ids[j]] += 1.0 / abs(i - j)
    return X


def glove_weight(x, x_max, alpha):
    x = np.asarray(x, dtype=float)
    return np.where(x < x_max, (x / x_max) ** alpha, 1.0)


def glove_loss(W, W_tilde, b, b_tilde, X, x_max, alpha):
    X = np.asarray(X, dtype=float)
    mask = X > 0
    pred = W @ W_tilde.T + b[:, None] + b_tilde[None, :]
    err = np.zeros_like(X)
    err[mask] = pred[mask] - np.log(X[mask])
    return float((glove_weight(X, x_max, alpha) * err ** 2)[mask].sum())
