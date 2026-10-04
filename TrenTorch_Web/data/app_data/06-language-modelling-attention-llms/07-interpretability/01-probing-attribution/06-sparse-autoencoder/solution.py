import numpy as np


def sae_forward(x, W_enc, b_enc, W_dec, b_dec):
    x = np.asarray(x, dtype=float)
    f = np.maximum((x - b_dec) @ W_enc + b_enc, 0.0)
    x_hat = f @ W_dec + b_dec
    return x_hat, f


def sae_loss(x, x_hat, f, l1_coeff):
    mse = ((np.asarray(x) - x_hat) ** 2).sum(axis=1).mean()
    l1 = np.abs(f).sum(axis=1).mean()
    return float(mse + l1_coeff * l1)
