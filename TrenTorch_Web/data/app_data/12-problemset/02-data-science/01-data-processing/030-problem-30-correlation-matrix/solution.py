import numpy as np

def solve(x):
        X=np.asarray(X,float); Z=(X-X.mean(0))/X.std(0); return (Z.T@Z)/(len(X)-1)
