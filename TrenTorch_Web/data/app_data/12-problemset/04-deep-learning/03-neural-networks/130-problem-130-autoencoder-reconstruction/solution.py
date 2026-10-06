import numpy as np

def solve(x,recon):
        return float(np.mean((np.asarray(x)-np.asarray(recon))**2))
