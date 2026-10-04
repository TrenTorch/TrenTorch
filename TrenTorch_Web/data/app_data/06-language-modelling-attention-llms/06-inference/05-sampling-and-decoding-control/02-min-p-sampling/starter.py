import numpy as np


def min_p_filter(probs: np.ndarray, min_p: float) -> np.ndarray:
    """Keep tokens with prob >= min_p * max(prob); zero the rest; renormalise."""
    # TODO
    pass
