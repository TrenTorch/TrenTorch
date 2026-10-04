import numpy as np

def solve(x,mean,var,gamma,beta,eps=1e-5):
    x=np.asarray(x,float); return gamma*(x-mean)/np.sqrt(var+eps)+beta
