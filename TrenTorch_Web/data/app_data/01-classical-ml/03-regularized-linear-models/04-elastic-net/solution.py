import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

soft_threshold = load_solution(
    "01-classical-ml/03-regularized-linear-models/03-lasso-regression"
).soft_threshold


def elastic_net_coordinate_descent(
    input: np.ndarray,
    target: np.ndarray,
    alpha: float = 1.0,
    l1_ratio: float = 0.5,
    epochs: int = 200,
) -> tuple[np.ndarray, np.ndarray]:
    n, d = input.shape
    x_mean = input.mean(axis=0)
    y_mean = target.mean()
    x_centered = input - x_mean
    y_centered = target - y_mean

    l1_penalty = alpha * l1_ratio
    l2_penalty = alpha * (1.0 - l1_ratio)

    weight = np.zeros(d)
    for _ in range(epochs):
        for j in range(d):
            residual = y_centered - x_centered @ weight + x_centered[:, j] * weight[j]
            rho_j = (x_centered[:, j] @ residual) / n
            z_j = (x_centered[:, j] @ x_centered[:, j]) / n
            weight[j] = soft_threshold(rho_j, l1_penalty) / (z_j + l2_penalty) if z_j > 0 else 0.0

    bias = y_mean - x_mean @ weight
    return weight.reshape(1, -1), np.array([bias])
