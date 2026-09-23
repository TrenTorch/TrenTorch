import numpy as np


def collaborative_scores(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    """
    Collaborative-filtering score matrix.

    U: shape (n_users, d), user embeddings.
    V: shape (n_items, d), item embeddings.

    Return R_hat = U @ V.T, shape (n_users, n_items): entry (u, i) is the
    dot product of user u's and item i's embedding.
    """
    # TODO: V.T swaps V's axes to (d, n_items) so the shared dimension d lines up.
    pass
