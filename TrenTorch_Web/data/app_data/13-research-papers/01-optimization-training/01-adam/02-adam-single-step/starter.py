import numpy as np


def adam_step(theta, grad, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
    """
    theta: current parameter value (float or NumPy array)
    grad: gradient of the loss with respect to theta at this step
    m, v: running first and second moment estimates from previous steps
    t: 1-based step count, used for bias correction
    lr, beta1, beta2, eps: Adam hyperparameters from the paper

    Returns:
        (theta, m, v): the updated parameter and the updated moments.
    """
    # TODO: Update m and v, bias-correct them, then apply the Adam update from Theory.
    pass
