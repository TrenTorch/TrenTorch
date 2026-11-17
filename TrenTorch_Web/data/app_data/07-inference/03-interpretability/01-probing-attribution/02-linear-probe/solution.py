import numpy as np


def _sigmoid(z):
    return 0.5 * (1.0 + np.tanh(z / 2.0))


def train_linear_probe(X, y, steps, lr, l2):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, d = X.shape
    w, b = np.zeros(d), 0.0
    for _ in range(steps):
        p = _sigmoid(X @ w + b)
        r = p - y
        w = w - lr * (X.T @ r / n + l2 * w)
        b = b - lr * r.mean()
    return w, float(b)


def probe_accuracy(X, y, w, b):
    pred = (np.asarray(X) @ w + b > 0).astype(int)
    return float((pred == np.asarray(y)).mean())
