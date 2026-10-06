import numpy as np

def solve(x):
        X=np.asarray(X,float); med=np.median(X,0); q1=np.quantile(X,.25,0); q3=np.quantile(X,.75,0); iqr=q3-q1
        return np.divide(X-med,iqr,out=np.zeros_like(X),where=iqr!=0)
