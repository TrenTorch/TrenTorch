import numpy as np

def solve(X):
        X=np.asarray(X,float); return X-X.mean(0)
