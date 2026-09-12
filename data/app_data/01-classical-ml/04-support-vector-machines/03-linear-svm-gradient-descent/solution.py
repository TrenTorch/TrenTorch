import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

hinge_loss = load_solution("01-classical-ml/04-support-vector-machines/01-hinge-loss").hinge_loss


def svm_objective(weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray, lambda_reg: float) -> float:
    scores = X @ weight + bias
    return hinge_loss(scores, y, reduction="mean") + lambda_reg * np.dot(weight, weight)


def svm_gradient(
    weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray, lambda_reg: float
) -> tuple[np.ndarray, float]:
    n = X.shape[0]
    scores = X @ weight + bias
    margin = y * scores
    violates_margin = (margin < 1.0).astype(float)

    grad_weight = -(violates_margin * y) @ X / n + 2.0 * lambda_reg * weight
    grad_bias = -np.sum(violates_margin * y) / n
    return grad_weight, grad_bias


def train_linear_svm(
    input: np.ndarray, target: np.ndarray, lr: float = 0.01, epochs: int = 1000, lambda_reg: float = 0.01
) -> tuple[np.ndarray, float]:
    n, d = input.shape
    weight = np.zeros(d)
    bias = 0.0
    for _ in range(epochs):
        grad_weight, grad_bias = svm_gradient(weight, bias, input, target, lambda_reg)
        weight = weight - lr * grad_weight
        bias = bias - lr * grad_bias
    return weight, bias
