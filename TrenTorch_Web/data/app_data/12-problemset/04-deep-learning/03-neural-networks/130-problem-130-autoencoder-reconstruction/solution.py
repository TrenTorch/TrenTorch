import numpy as np

def solve(x, recon):
    """Autoencoder reconstruction loss is the mean squared difference between the original input and its reconstruction."""
    return float(np.mean((np.asarray(x)-np.asarray(recon))**2))
