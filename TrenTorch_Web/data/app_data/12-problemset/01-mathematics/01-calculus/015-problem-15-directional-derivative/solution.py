import numpy as np

def solve(grad, direction):
        d=np.asarray(direction,float); d=d/np.linalg.norm(d)
        return float(grad @ d)
