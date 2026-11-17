import numpy as np


def batchnorm_train(x, gamma, beta, eps=1e-5):
    mean = x.mean(axis=0)
    var = x.var(axis=0)
    x_hat = (x - mean) / np.sqrt(var + eps)
    return gamma * x_hat + beta, mean, var
