import numpy as np


def kernel_pegasos(K: np.ndarray, y: np.ndarray, lam: float = 0.1, iterations: int = 1000) -> np.ndarray:
    n = len(y)
    alpha = np.zeros(n)
    for t in range(1, iterations + 1):
        i = (t - 1) % n
        decision = (alpha * y) @ K[:, i] / (lam * t)
        if y[i] * decision < 1.0:
            alpha[i] += 1.0
    return alpha
