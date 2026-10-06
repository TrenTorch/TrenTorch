import numpy as np

def solve(w,l1,l2):
        w=np.asarray(w,float); return float(l1*np.sum(np.abs(w))+0.5*l2*np.sum(w*w))
