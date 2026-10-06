import numpy as np

def solve(keys, values):
        acc={}
        for k,v in zip(keys,values):
            s,n=acc.get(k,(0.0,0)); acc[k]=(s+v,n+1)
        return {k:s/n for k,(s,n) in acc.items()}
