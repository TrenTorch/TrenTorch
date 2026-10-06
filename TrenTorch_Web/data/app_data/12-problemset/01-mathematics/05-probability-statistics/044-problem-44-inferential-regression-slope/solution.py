import numpy as np

def solve(x,y):
        x,y=np.asarray(x,float),np.asarray(y,float)
        if x.shape!=y.shape: raise ValueError('x and y must have the same length')
        xm,ym=x.mean(),y.mean(); slope=np.sum((x-xm)*(y-ym))/np.sum((x-xm)**2); return float(slope),float(ym-slope*xm)
