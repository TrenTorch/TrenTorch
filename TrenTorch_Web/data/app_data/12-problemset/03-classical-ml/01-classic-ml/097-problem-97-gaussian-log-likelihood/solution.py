import numpy as np

def solve(x,mu,cov):
        x=np.asarray(x,float); mu=np.asarray(mu,float); S=np.asarray(cov,float); d=len(x); sign,ld=np.linalg.slogdet(S); return float(-0.5*(d*np.log(2*np.pi)+ld+(x-mu)@np.linalg.solve(S,x-mu)))
