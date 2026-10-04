import numpy as np

def solve(X, y, batch_size, seed=0):
    """Mini-batches use one seeded permutation, contiguous chunks of at most batch_size indices, and keep the final short batch."""
    indices = np.arange(len(X))
    np.random.default_rng(seed).shuffle(indices)
    features = np.asarray(X)
    labels = np.asarray(y)
    return [
        (features[batch].tolist(), labels[batch].tolist())
        for batch in (indices[start:start + batch_size] for start in range(0, len(indices), batch_size))
    ]
