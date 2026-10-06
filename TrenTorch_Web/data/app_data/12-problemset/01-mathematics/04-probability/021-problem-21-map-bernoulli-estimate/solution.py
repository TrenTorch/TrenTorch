import numpy as np

def solve(x, a, b):
        x=np.asarray(x,float); a_post=a+np.sum(x); b_post=b+len(x)-np.sum(x)
        return float((a_post-1)/(a_post+b_post-2))
