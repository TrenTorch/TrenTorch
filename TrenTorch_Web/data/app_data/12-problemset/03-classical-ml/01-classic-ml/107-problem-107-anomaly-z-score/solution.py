import numpy as np

def solve(x,threshold=3):
        X=np.asarray(X,float); mu=X.mean(0); sd=X.std(0); return np.divide(X-mu,sd,out=np.zeros_like(X),where=sd!=0)
