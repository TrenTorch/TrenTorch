import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

mse_gradient = load_solution("01-classical-ml/01-linear-regression/03-mse-gradient").mse_gradient
gd_step = load_solution("01-classical-ml/01-linear-regression/04-gd-step").gd_step


def train_linear_regression_production(
    input: np.ndarray,
    target: np.ndarray,
    lr: float,
    epochs: int,
    batch_size: int,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    n_samples, in_features = input.shape
    weight = np.zeros((1, in_features))
    bias = np.zeros(1)
    target_2d = target.reshape(-1, 1)
    rng = np.random.default_rng(seed)

    for _ in range(epochs):
        order = rng.permutation(n_samples)
        for start in range(0, n_samples, batch_size):
            batch_idx = order[start : start + batch_size]
            input_batch, target_batch = input[batch_idx], target_2d[batch_idx]
            grad_weight, grad_bias = mse_gradient(input_batch, weight, bias, target_batch)
            weight, bias = gd_step(weight, bias, grad_weight, grad_bias, lr)

    return weight, bias
