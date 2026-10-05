import numpy as np


def direct_logit_attribution(components: np.ndarray, W_U: np.ndarray, correct: int, wrong: int, scale: float) -> np.ndarray:
    """Per-component contribution to logit(correct) - logit(wrong), shape (C,)."""
    # TODO
    pass


def attribution_total(contributions: np.ndarray) -> float:
    """Sum of the per-component contributions."""
    # TODO
    pass
