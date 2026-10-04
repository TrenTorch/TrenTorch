import numpy as np

def solve(ids):
    """Return input token IDs and next-token targets shifted by one position."""
        ids=np.asarray(ids); return ids[:-1],ids[1:]
