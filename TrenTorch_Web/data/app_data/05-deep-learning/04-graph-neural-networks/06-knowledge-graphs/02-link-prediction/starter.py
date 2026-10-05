import numpy as np


def link_prediction_score(u_emb, v_emb, method='dot'):
    """Score edge likelihood between two nodes.

    Args:
        u_emb: Node u embedding, shape (embedding_dim,).
        v_emb: Node v embedding, shape (embedding_dim,).
        method: Scoring method ('dot', 'euclidean', 'cosine').

    Returns:
        Scalar score.
    """
    pass
