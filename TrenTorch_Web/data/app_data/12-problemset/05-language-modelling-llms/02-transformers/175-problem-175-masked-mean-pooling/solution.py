import numpy as np

def solve(embeddings, mask):
    values = np.asarray(embeddings, dtype=float)
    valid = np.asarray(mask, dtype=bool)[..., None]
    totals = np.sum(np.where(valid, values, 0), axis=1)
    counts = valid.sum(axis=1)
    return np.divide(totals, counts, out=np.zeros_like(totals), where=counts != 0)
