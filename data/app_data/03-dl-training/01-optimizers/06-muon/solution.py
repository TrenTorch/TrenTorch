import numpy as np


def newton_schulz_orthogonalize(G: np.ndarray, steps: int = 5, eps: float = 1e-7) -> np.ndarray:
    a, b, c = 3.4445, -4.7750, 2.0315
    X = G / (np.linalg.norm(G) + eps)

    transposed = X.shape[0] > X.shape[1]
    if transposed:
        X = X.T

    for _ in range(steps):
        A = X @ X.T
        B = b * A + c * (A @ A)
        X = a * X + B @ X

    if transposed:
        X = X.T
    return X


def muon_step(
    param: np.ndarray, grad: np.ndarray, momentum_buf: np.ndarray, lr: float, momentum: float = 0.95
) -> tuple[np.ndarray, np.ndarray]:
    new_buf = momentum * momentum_buf + grad
    update = newton_schulz_orthogonalize(new_buf)
    new_param = param - lr * update
    return new_param, new_buf
