import numpy as np

def solve(X, y, w):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.asarray(w, dtype=float)
    logits = X @ w
    probabilities = np.empty_like(logits)
    positive = logits >= 0
    probabilities[positive] = 1 / (1 + np.exp(-logits[positive]))
    exp_logits = np.exp(logits[~positive])
    probabilities[~positive] = exp_logits / (1 + exp_logits)
    residual = probabilities - y
    return X.T @ residual / len(y), float(residual.mean())
