import numpy as np

def solve(y):
        u,c=np.unique(y,return_counts=True); return u[np.argmax(c)]
