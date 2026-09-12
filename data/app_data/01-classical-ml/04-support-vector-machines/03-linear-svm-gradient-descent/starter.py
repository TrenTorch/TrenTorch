import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

hinge_loss = load_solution("01-classical-ml/04-support-vector-machines/01-hinge-loss").hinge_loss


def svm_objective(weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray, lambda_reg: float) -> float:
    """
    The soft-margin SVM's training objective: mean hinge loss plus an
    L2 penalty on the weights (encouraging a SMALL ||weight||, which,
    per Margin maximization intuition's own geometric_margin formula,
    is exactly what makes the margin LARGE for a given functional
    margin, connecting this objective directly back to that question's
    margin-maximization goal).

        objective = hinge_loss(X @ weight + bias, y) + lambda_reg * ||weight||^2
    """
    pass


def svm_gradient(
    weight: np.ndarray, bias: float, X: np.ndarray, y: np.ndarray, lambda_reg: float
) -> tuple[np.ndarray, float]:
    """
    The (sub)gradient of svm_objective. Hinge loss's kink at the
    margin boundary means its derivative is only PIECEWISE defined:
    zero contribution from any point with margin >= 1 (comfortably
    correct, hinge_loss's own "stop caring" property), and a
    contribution of `-y_i * x_i` from every point that violates the
    margin (margin < 1).

        grad_weight = -mean(y_i * x_i for violating points) + 2 * lambda_reg * weight
        grad_bias   = -mean(y_i for violating points)
    """
    pass


def train_linear_svm(
    input: np.ndarray, target: np.ndarray, lr: float = 0.01, epochs: int = 1000, lambda_reg: float = 0.01
) -> tuple[np.ndarray, float]:
    """
    Plain gradient descent on svm_objective, using svm_gradient at
    every step, the exact same training-loop shape Full Training Loop
    and Full Linear Regression Training Loop both already use.
    """
    pass
