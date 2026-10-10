import numpy as np

def solve(values, categories):
        cats=list(categories); pos={c:i for i,c in enumerate(cats)}
        out=np.zeros((len(values),len(cats)),dtype=int)
        for r,v in enumerate(values): out[r,pos[v]]=1
        return out
