import numpy as np

def solve(x):
        A=np.asarray(A,bool); B=np.asarray(B,bool)
        den=np.sum(B)
        return 0.0 if den==0 else float(np.sum(A & B)/den)
