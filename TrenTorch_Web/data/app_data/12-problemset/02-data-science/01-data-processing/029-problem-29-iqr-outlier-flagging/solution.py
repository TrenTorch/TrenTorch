import numpy as np

def solve(x):
        x=np.asarray(x,float); q1,q3=np.quantile(x,[.25,.75]); iqr=q3-q1
        return (x < q1-1.5*iqr) | (x > q3+1.5*iqr)
