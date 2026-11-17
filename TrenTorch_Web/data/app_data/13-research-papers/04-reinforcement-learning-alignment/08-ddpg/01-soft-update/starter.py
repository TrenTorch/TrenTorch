import numpy as np


def soft_update(target, online, tau):
    """
    target: target network parameters (array)
    online: online network parameters, same shape
    tau: update rate in [0, 1]

    Returns:
        The new target parameters (1 - tau) * target + tau * online.
    """
    # TODO: Move the target a fraction tau toward the online parameters (see Theory).
    pass
