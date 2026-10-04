import numpy as np

def solve(rewards):
        r=np.asarray(rewards,float); return (r-r.mean())/r.std()
