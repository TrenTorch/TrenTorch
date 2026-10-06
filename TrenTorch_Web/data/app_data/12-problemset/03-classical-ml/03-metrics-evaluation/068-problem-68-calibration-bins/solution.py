import numpy as np

def solve(y,p,bins=10):
        y=np.asarray(y); p=np.asarray(p); out=[]
        edges=np.linspace(0,1,bins+1)
        for i in range(bins):
            m=(p>=edges[i])&(p<edges[i+1] if i<bins-1 else p<=edges[i+1]);
            if np.any(m): out.append((float(p[m].mean()),float(y[m].mean()),int(m.sum())))
        return out
