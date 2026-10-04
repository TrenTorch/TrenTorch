import numpy as np

def solve(x, recon):
    """Implement autoencoder reconstruction according to the contract."""
    return float(np.mean((np.asarray(x) - np.asarray(recon)) ** 2))
