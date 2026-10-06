import numpy as np

def solve(grads,clip):
        gs=[np.asarray(g,float) for g in grads]; n=np.sqrt(sum(np.sum(g*g) for g in gs)); scale=min(1.0,clip/n) if n else 1.0; return [g*scale for g in gs]
