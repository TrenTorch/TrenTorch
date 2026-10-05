import numpy as np


def transe_score(h, r, t):
    """Compute TransE score for a triplet.

    Args:
        h: Head embedding, shape (embedding_dim,).
        r: Relation embedding, shape (embedding_dim,).
        t: Tail embedding, shape (embedding_dim,).

    Returns:
        Scalar score (lower is better).
    """
    return np.linalg.norm(h + r - t, ord=2)
