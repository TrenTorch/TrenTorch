import numpy as np

def solve(logits,target):
        p=np.asarray(p,float); p=p[p>0]
        return float(-np.sum(p*np.log2(p)))
