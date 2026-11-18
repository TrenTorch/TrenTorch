import numpy as np

def solve(w, v, grad, lr, mu):
    """Momentum updates velocity as v_new=mu*v+grad and parameters as w_new=w-lr*v_new."""
    w,v,grad=np.asarray(w),np.asarray(v),np.asarray(grad); v=mu*v+grad; return v,w-lr*v
