import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

mse_gradient = load_solution("01-classical-ml/01-linear-regression/03-mse-gradient").mse_gradient


def ridge_grad(
    input: np.ndarray,
    weight: np.ndarray,
    bias: np.ndarray | None,
    target: np.ndarray,
    lam: float,
) -> tuple[np.ndarray, np.ndarray | None]:
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    return grad_weight + 2 * lam * weight, grad_bias
