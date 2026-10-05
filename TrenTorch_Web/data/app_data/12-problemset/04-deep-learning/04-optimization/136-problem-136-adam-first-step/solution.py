import numpy as np

def solve(w, g, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-08):
    """Adam updates first and second moments, corrects their initialization bias, and divides the corrected first moment by sqrt(corrected second moment)+eps."""
    w,g,m,v=map(np.asarray,(w,g,m,v)); m=beta1*m+(1-beta1)*g; v=beta2*v+(1-beta2)*g*g; mh=m/(1-beta1**t); vh=v/(1-beta2**t); return w-lr*mh/(np.sqrt(vh)+eps),m,v
