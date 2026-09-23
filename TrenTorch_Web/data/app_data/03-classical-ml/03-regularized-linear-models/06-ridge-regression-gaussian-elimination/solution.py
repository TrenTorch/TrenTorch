import numpy as np


def gaussian_elimination_solve(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = a.shape[0]
    aug = np.hstack([a.astype(float), b.reshape(-1, 1).astype(float)])

    for k in range(n):
        pivot_row = k + int(np.argmax(np.abs(aug[k:, k])))
        if pivot_row != k:
            aug[[k, pivot_row]] = aug[[pivot_row, k]]
        pivot = aug[k, k]
        for i in range(k + 1, n):
            factor = aug[i, k] / pivot
            aug[i, k:] -= factor * aug[k, k:]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (aug[i, -1] - aug[i, i + 1 : n] @ x[i + 1 :]) / aug[i, i]
    return x


def ridge_regression_predict(
    input: np.ndarray, target: np.ndarray, lam: float, queries: np.ndarray
) -> np.ndarray:
    n = input.shape[0]
    x_augmented = np.hstack([input, np.ones((n, 1))])
    d_plus_one = x_augmented.shape[1]

    a = x_augmented.T @ x_augmented + lam * np.eye(d_plus_one)
    b = x_augmented.T @ target
    theta = gaussian_elimination_solve(a, b)

    m = queries.shape[0]
    queries_augmented = np.hstack([queries, np.ones((m, 1))])
    return queries_augmented @ theta
