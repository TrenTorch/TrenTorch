import numpy as np


def learned_positional_embedding(seq_len: int, position_table: np.ndarray) -> np.ndarray:
    """
    The learned alternative to `[03-sinusoidal-positional-encoding]`'s
    fixed formula: `position_table` (shape (max_seq_len, embed_dim)) is
    itself an ordinary, TRAINABLE parameter, exactly like
    `[01-token-embedding-lookup]`'s embedding_table, just indexed by
    POSITION (0, 1, 2, ..., always in order) rather than by an arbitrary
    token id. Returns the first `seq_len` rows, one per position.
    """
    pass
