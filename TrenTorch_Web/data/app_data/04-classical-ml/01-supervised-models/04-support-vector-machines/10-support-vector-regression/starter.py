import numpy as np

from _load import load_solution

epsilon_insensitive_loss = load_solution("support-vector-machines-epsilon-insensitive-loss").epsilon_insensitive_loss


def svr_objective(
    weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray, epsilon: float, lambda_reg: float
) -> float:
    """
    Mean epsilon-insensitive loss of X @ weight + bias against y, plus
    lambda_reg * ||weight||^2.
    """
    pass


def svr_gradient(
    weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray, epsilon: float, lambda_reg: float
) -> tuple[np.ndarray, float]:
    """
    Gradient of svr_objective. Points inside the tube contribute zero;
    points outside contribute sign(residual).
    """
    pass


def train_linear_svr(
    X: np.ndarray, y: np.ndarray, lr: float = 0.01, epochs: int = 1000, epsilon: float = 0.1, lambda_reg: float = 0.0
) -> tuple[np.ndarray, float]:
    """
    Plain gradient descent on svr_objective from zero weights and zero bias.
    Returns (weight, bias).
    """
    pass
