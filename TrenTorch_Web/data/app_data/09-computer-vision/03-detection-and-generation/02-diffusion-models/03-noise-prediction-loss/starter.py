import numpy as np


def noise_prediction_loss(eps_pred: np.ndarray, eps: np.ndarray) -> float:
    """Mean squared error between predicted and true noise."""
    # TODO
    pass


def predict_x0(x_t: np.ndarray, eps_pred: np.ndarray, t: int, alpha_bars: np.ndarray) -> np.ndarray:
    """Clean-image estimate implied by a noise prediction."""
    # TODO
    pass
