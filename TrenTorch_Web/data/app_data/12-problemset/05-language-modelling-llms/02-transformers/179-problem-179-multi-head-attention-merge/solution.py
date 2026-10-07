import numpy as np

def solve(heads):
    values = np.asarray(heads, dtype=float)
    batch, n_heads, time, width = values.shape
    return values.transpose(0, 2, 1, 3).reshape(batch, time, n_heads * width)
