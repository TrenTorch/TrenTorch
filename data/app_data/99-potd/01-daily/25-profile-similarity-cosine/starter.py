import numpy as np


def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    """
    Cosine similarity between two vectors.

    u, v: shape (d,).

    Return (u . v) / (||u|| * ||v||). If either vector is all zeros (norm
    0), return 0.0 instead of dividing by zero.
    """
    # TODO: check both norms before dividing, not just their product.
    pass
