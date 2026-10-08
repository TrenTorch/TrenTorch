import numpy as np


def batchnorm_inference(x, gamma, beta, running_mean, running_var, eps=1e-5):
    return gamma * (x - running_mean) / np.sqrt(running_var + eps) + beta
