import numpy as np

def solve(predictions):
    p=np.asarray(predictions,int)
    counts=np.bincount(p)
    return int(np.flatnonzero(counts==counts.max())[0])
