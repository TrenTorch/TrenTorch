import numpy as np

def solve(logits,temperature):
        z=np.asarray(logits,float)/temperature; z-=z.max(); p=np.exp(z); return p/p.sum()
