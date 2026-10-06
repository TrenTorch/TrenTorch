import numpy as np

def solve(x,degree):
        x=np.asarray(x,float); return np.column_stack([x**d for d in range(1,degree+1)])
