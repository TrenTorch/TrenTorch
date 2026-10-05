import numpy as np

def solve(g,max_norm):
    g=np.asarray(g,float); n=np.linalg.norm(g)
    return g if n<=max_norm or n==0 else g*(max_norm/n)
