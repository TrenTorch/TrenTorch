import numpy as np

def solve(x,mu,sigma,pi):
    x=float(x); mu=np.asarray(mu,float); sigma=np.asarray(sigma,float); pi=np.asarray(pi,float)
    q=pi*np.exp(-0.5*((x-mu)/sigma)**2)/sigma
    return q/q.sum()
