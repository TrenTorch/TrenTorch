import numpy as np

def solve(predictions):
    """Implement random forest vote according to the contract."""
    P = np.asarray(predictions)
    out = []
    for row in P.T:
        u, c = np.unique(row, return_counts=True)
        out.append(u[np.argmax(c)])
    return np.asarray(out)
