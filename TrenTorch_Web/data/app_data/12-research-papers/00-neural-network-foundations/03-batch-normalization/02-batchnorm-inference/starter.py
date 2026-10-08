import numpy as np


def batchnorm_inference(x, gamma, beta, running_mean, running_var, eps=1e-5):
    """
    x: activations to normalize, shape (N, D) (N may be 1)
    gamma, beta: learned scale and shift, shape (D,)
    running_mean, running_var: statistics tracked during training, shape (D,)
    eps: small constant for numerical stability

    Returns:
        The output using the running statistics instead of batch statistics.
    """
    # TODO: Normalize with the running statistics, then scale and shift.
    pass
