import numpy as np


def reward_model_loss(r_chosen: np.ndarray, r_rejected: np.ndarray) -> float:
    """Mean Bradley-Terry loss: -log sigmoid(r_chosen - r_rejected)."""
    # TODO: Use np.logaddexp(0, -d) for stability.
    pass


def preference_accuracy(r_chosen: np.ndarray, r_rejected: np.ndarray) -> float:
    """Fraction of pairs where the chosen reward is strictly higher."""
    # TODO: Compare the two arrays and average.
    pass
