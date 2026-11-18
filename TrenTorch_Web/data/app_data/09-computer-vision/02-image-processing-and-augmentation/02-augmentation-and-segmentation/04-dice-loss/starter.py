import numpy as np


def dice_coefficient(pred: np.ndarray, target: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """Per-sample soft Dice, shape (N,)."""
    # TODO
    pass


def dice_loss(pred: np.ndarray, target: np.ndarray, eps: float = 1e-6) -> float:
    """1 - mean Dice."""
    # TODO
    pass
