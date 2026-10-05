import numpy as np

def solve(x,y):
        score,t=best_binary_split(x,y); left=y[x<=t]; right=y[x>t];
        def mode(z):
            u,c=np.unique(z,return_counts=True); return u[np.argmax(c)]
        return t,mode(left),mode(right)
