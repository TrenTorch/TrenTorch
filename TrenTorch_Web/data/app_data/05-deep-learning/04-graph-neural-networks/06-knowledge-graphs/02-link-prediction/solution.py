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
    if method == 'dot':
        return np.dot(u_emb, v_emb)
    elif method == 'euclidean':
        return -np.linalg.norm(u_emb - v_emb, ord=2)
    elif method == 'cosine':
        u_norm = np.linalg.norm(u_emb)
        v_norm = np.linalg.norm(v_emb)
        if u_norm < 1e-8 or v_norm < 1e-8:
            return 0.0
        return np.dot(u_emb, v_emb) / (u_norm * v_norm)
    else:
        raise ValueError(f"Unknown method: {method}")
