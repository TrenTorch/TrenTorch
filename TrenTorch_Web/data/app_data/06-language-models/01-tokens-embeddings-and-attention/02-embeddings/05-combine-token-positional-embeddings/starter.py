import numpy as np


def combine_embeddings(token_embeddings: np.ndarray, positional_embeddings: np.ndarray) -> np.ndarray:
    """
    Combines `[01-token-embedding-lookup]`'s per-token embeddings (shape
    (batch_size, seq_len, embed_dim)) with `[03-sinusoidal-positional-
    encoding]`'s or `[04-learned-positional-embedding]`'s per-position
    embeddings (shape (seq_len, embed_dim)), so every token's final
    representation carries BOTH what the token is AND where it sits in
    the sequence.
    """
    pass
