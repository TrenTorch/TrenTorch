import numpy as np

def solve(x):
        x=np.asarray(x,float); p=float(np.mean(x)); return p, p*(1-p)
