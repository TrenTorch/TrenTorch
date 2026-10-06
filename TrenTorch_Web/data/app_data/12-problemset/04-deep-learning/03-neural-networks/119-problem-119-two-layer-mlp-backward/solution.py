import numpy as np

def solve(X,dY,W1,W2,cache):
        z1,h=cache; dW2=h.T@dY; db2=dY.sum(0); dh=dY@W2.T; dz=dh*(z1>0); return dz@W1.T, X.T@dz, dz.sum(0), dW2, db2
