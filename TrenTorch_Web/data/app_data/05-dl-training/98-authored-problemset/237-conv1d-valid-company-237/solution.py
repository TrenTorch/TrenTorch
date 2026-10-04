import numpy as np

def solve(x,k):
    x=np.asarray(x,float); k=np.asarray(k,float); return np.array([np.dot(x[i:i+len(k)],k) for i in range(len(x)-len(k)+1)])
