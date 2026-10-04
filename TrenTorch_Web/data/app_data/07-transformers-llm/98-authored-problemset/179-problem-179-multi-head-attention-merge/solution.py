import numpy as np

def solve(heads):
    """Merge (batch, heads, time, head_features) into feature-concatenated states."""
    values = np.asarray(heads)
    batch, n_heads, time, width = values.shape
    return values.transpose(0, 2, 1, 3).reshape(batch, time, n_heads * width)
