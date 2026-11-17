import numpy as np

def solve(embeddings, length):
    """Return the first length rows of a learned positional-embedding table."""
    table = np.asarray(embeddings)
    if length < 0 or length > len(table):
        raise ValueError("length must be within the embedding table")
    return table[:length].copy()
