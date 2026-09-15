import numpy as np


def smo_fit(
    X: np.ndarray,
    y: np.ndarray,
    C: float,
    tol: float,
    max_passes: int,
) -> tuple[np.ndarray, float]:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n = X.shape[0]
    K = X @ X.T
    alpha = np.zeros(n)
    b = 0.0
    passes = 0

    def f_now(i: int) -> float:
        return float(np.sum(alpha * y * K[:, i]) + b)

    while passes < max_passes:
        num_changed = 0
        for i in range(n):
            E_i = f_now(i) - y[i]
            if not ((y[i] * E_i < -tol and alpha[i] < C) or (y[i] * E_i > tol and alpha[i] > 0)):
                continue

            j = (i + 1) % n
            E_j = f_now(j) - y[j]
            alpha_i_old, alpha_j_old = alpha[i], alpha[j]

            if y[i] != y[j]:
                L = max(0.0, alpha[j] - alpha[i])
                H = min(C, C + alpha[j] - alpha[i])
            else:
                L = max(0.0, alpha[i] + alpha[j] - C)
                H = min(C, alpha[i] + alpha[j])
            if L == H:
                continue

            eta = 2 * K[i, j] - K[i, i] - K[j, j]
            if eta >= 0:
                continue

            alpha_j_new = alpha_j_old - y[j] * (E_i - E_j) / eta
            alpha_j_new = min(H, max(L, alpha_j_new))
            if abs(alpha_j_new - alpha_j_old) < 1e-5:
                continue

            alpha_i_new = alpha_i_old + y[i] * y[j] * (alpha_j_old - alpha_j_new)

            b1 = (
                b
                - E_i
                - y[i] * (alpha_i_new - alpha_i_old) * K[i, i]
                - y[j] * (alpha_j_new - alpha_j_old) * K[i, j]
            )
            b2 = (
                b
                - E_j
                - y[i] * (alpha_i_new - alpha_i_old) * K[i, j]
                - y[j] * (alpha_j_new - alpha_j_old) * K[j, j]
            )
            if 0 < alpha_i_new < C:
                b = b1
            elif 0 < alpha_j_new < C:
                b = b2
            else:
                b = (b1 + b2) / 2.0

            alpha[i] = alpha_i_new
            alpha[j] = alpha_j_new
            num_changed += 1

        if num_changed == 0:
            passes += 1
        else:
            passes = 0

    return alpha, b


def svm_decision_function(
    X: np.ndarray,
    y: np.ndarray,
    alpha: np.ndarray,
    b: float,
    queries: np.ndarray,
) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    alpha = np.asarray(alpha, dtype=float)
    queries = np.asarray(queries, dtype=float)
    K = queries @ X.T
    return K @ (alpha * y) + b
