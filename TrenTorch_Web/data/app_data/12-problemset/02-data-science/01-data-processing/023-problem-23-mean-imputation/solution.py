import numpy as np

def solve(x):
        x=np.asarray(x,float).copy(); m=np.nanmean(x); x[np.isnan(x)]=m; return x
