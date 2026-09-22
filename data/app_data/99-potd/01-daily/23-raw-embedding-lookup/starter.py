import numpy as np


def embedding_lookup(E: np.ndarray, ids: np.ndarray) -> np.ndarray:
    """
    Table lookup: turn token ids into their embedding vectors.

    E: shape (V, d), row i is token i's embedding.
    ids: shape (n,), integer token ids in [0, V - 1], can repeat.

    Return shape (n, d): row k is E[ids[k]].
    """
    # TODO: E[ids] is NumPy fancy indexing, one expression, no loop.
    pass
