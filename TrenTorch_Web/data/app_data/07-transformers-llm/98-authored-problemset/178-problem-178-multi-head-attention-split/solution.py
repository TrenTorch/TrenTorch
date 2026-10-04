import numpy as np

def solve(X, n_heads):
    """Split (batch, time, features) into (batch, heads, time, head_features)."""
    values = np.asarray(X)
    batch, time, features = values.shape
    if n_heads <= 0 or features % n_heads:
        raise ValueError("feature size must be divisible by positive n_heads")
    return values.reshape(batch, time, n_heads, features // n_heads).transpose(0, 2, 1, 3)
