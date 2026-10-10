import numpy as np

def solve(ids,pad_id):
        return (np.asarray(ids)!=pad_id).astype(int)
