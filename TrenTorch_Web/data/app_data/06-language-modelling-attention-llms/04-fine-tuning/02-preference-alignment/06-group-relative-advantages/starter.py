import numpy as np


def group_advantages(rewards: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """(P, G) per-row (r - mean) / (std + eps), population std."""
    # TODO
    pass


def clipped_surrogate_loss(ratio: np.ndarray, advantage: np.ndarray, clip_eps: float) -> float:
    """Mean of -min(ratio * A, clip(ratio, 1 - clip_eps, 1 + clip_eps) * A)."""
    # TODO
    pass
