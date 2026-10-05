import numpy as np

def solve(labels):
        u,c=np.unique(labels,return_counts=True); return u[np.argmax(c)]
