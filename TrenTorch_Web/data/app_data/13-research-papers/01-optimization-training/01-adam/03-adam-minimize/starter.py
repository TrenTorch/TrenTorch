import numpy as np


def adam_minimize(grad_fn, theta0, steps, lr=0.1, beta1=0.9, beta2=0.999, eps=1e-8):
    """
    grad_fn: function taking theta (NumPy array) and returning the gradient
        at theta (same shape)
    theta0: starting parameter value (float or NumPy array)
    steps: number of Adam updates to run
    lr, beta1, beta2, eps: Adam hyperparameters

    Returns:
        A list of length steps + 1: theta0, then theta after each update.
    """
    # TODO: Run the Adam loop from Theory, recording theta after every step.
    pass
