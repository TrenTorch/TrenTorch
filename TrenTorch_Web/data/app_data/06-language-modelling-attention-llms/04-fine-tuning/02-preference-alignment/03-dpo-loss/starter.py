import numpy as np


def dpo_implicit_reward(pi_logp: np.ndarray, ref_logp: np.ndarray, beta: float) -> np.ndarray:
    """beta * (pi_logp - ref_logp)."""
    # TODO: One line.
    pass


def dpo_loss(pi_chosen, pi_rejected, ref_chosen, ref_rejected, beta: float) -> float:
    """Mean DPO loss over the pairs."""
    # TODO: Implicit rewards, their difference, stable -log sigmoid, mean.
    pass
