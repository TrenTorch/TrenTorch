import numpy as np


def lda_fit(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    X0, X1 = X[y == 0], X[y == 1]
    mu0, mu1 = X0.mean(axis=0), X1.mean(axis=0)
    n0, n1 = len(X0), len(X1)
    n = n0 + n1
    cov0 = (X0 - mu0).T @ (X0 - mu0)
    cov1 = (X1 - mu1).T @ (X1 - mu1)
    pooled_cov = (cov0 + cov1) / (n - 2)
    pooled_cov_inv = np.linalg.inv(pooled_cov)
    w = pooled_cov_inv @ (mu1 - mu0)
    prior0, prior1 = n0 / n, n1 / n
    b = (-0.5 * (mu1 @ pooled_cov_inv @ mu1)
         + 0.5 * (mu0 @ pooled_cov_inv @ mu0)
         + np.log(prior1 / prior0))
    return w, b
