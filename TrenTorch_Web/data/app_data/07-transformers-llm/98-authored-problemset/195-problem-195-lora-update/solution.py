import numpy as np

def solve(x, A, B):
    """Implement lora update according to the contract."""
    x, A, B = map(np.asarray, (x, A, B))
    return B @ (A @ x)
