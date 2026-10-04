import numpy as np

def solve(embeddings, length):
    """Implement learned positional embeddings according to the contract."""
    return embeddings[np.arange(length)]
