import numpy as np


def forward_noise(x0, ab, eps):
    """
    x0: clean data sample
    ab: cumulative product of (1 - beta) up to this step, in (0, 1]
    eps: standard normal noise with the same shape as x0

    Returns:
        The noised sample x_t = sqrt(ab) * x0 + sqrt(1 - ab) * eps.
    """
    # TODO: Mix the clean sample and the noise with the cumulative weights (see Theory).
    pass
