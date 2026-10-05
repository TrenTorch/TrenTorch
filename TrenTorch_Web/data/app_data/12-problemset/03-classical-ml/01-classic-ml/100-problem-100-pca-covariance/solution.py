import numpy as np

def solve(X):
        X=np.asarray(X,float); Z=X-X.mean(0); return Z.T@Z/(len(X)-1)
