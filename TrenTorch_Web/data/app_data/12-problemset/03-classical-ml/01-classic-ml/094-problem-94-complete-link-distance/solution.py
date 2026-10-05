import numpy as np

def solve(A,B):
        A=np.asarray(A,float); B=np.asarray(B,float); return float(np.max(np.sqrt(((A[:,None]-B[None,:])**2).sum(2))))
