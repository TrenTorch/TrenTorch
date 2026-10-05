import numpy as np

def solve(X,C,labels):
        X=np.asarray(X,float); C=np.asarray(C,float); labels=np.asarray(labels); return float(sum(np.sum((X[labels==k]-C[k])**2) for k in range(len(C))))
