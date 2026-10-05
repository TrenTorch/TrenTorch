import numpy as np


def logistic_grad_hess(y: np.ndarray, raw: np.ndarray):
    """
    Gradient and Hessian of logistic loss at raw scores. Returns (g, h).
    Raises ValueError when y has values other than 0 and 1.
    """
    pass


def leaf_weight(G: float, H: float, lam: float) -> float:
    """
    Optimal leaf value -G / (H + lam). Raises ValueError when lam <= 0.
    """
    pass


def split_gain(G_L: float, H_L: float, G_R: float, H_R: float, lam: float, gamma: float) -> float:
    """
    Second-order split gain minus gamma. Raises ValueError when lam <= 0.
    """
    pass
