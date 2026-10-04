import numpy as np


def steering_vector(pos_acts: np.ndarray, neg_acts: np.ndarray, normalize: bool = True) -> np.ndarray:
    """Difference of mean activations, optionally scaled to unit length."""
    # TODO
    pass


def apply_steering(resid: np.ndarray, v: np.ndarray, alpha: float, positions=None) -> np.ndarray:
    """Copy of resid with alpha * v added at `positions` (all rows if None)."""
    # TODO
    pass
