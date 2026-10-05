import numpy as np

def solve(X, y, knots):
    """The fixed ReLU basis has columns max(X_i-knot_j,0); least squares chooses weights minimizing the squared residual to y."""
    X,y,knots=np.asarray(X,dtype=float),np.asarray(y,dtype=float),np.asarray(knots,dtype=float); B=np.maximum(X[:,None]-knots[None,:],0); w=np.linalg.lstsq(B,y,rcond=None)[0]; return B@w,w
