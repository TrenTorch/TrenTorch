import numpy as np

def solve(y,p):
    y=np.asarray(y); p=np.asarray(p)
    return (int(((y==1)&(p==1)).sum()),int(((y==0)&(p==0)).sum()),int(((y==0)&(p==1)).sum()),int(((y==1)&(p==0)).sum()))
