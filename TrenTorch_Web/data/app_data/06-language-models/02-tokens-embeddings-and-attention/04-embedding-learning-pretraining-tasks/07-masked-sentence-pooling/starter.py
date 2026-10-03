import numpy as np


def pool_sentence(hidden: np.ndarray, mask: np.ndarray, mode: str) -> np.ndarray:
    """Pool (B, T, d) token states to (B, d) using only real tokens; modes 'cls', 'mean', 'max'."""
    # TODO
    pass
