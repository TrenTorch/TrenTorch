import numpy as np

def solve(x,y):
        x,y=np.asarray(x,float),np.asarray(y,float); xm,ym=x.mean(),y.mean(); slope=np.sum((x-xm)*(y-ym))/np.sum((x-xm)**2); return float(slope),float(ym-slope*xm)
