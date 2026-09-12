import numpy as np


def sgd_momentum_step(
    params: list[np.ndarray],
    grads: list[np.ndarray],
    velocities: list[np.ndarray],
    lr: float,
    momentum: float = 0.9,
) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """
    Mirrors torch.optim.SGD(momentum=momentum): instead of stepping
    directly opposite the CURRENT gradient (plain SGD), accumulate a
    running "velocity" that blends the current gradient with the
    PREVIOUS velocity, and step opposite that instead.

        new_velocity = momentum * velocity + grad
        new_param    = param - lr * new_velocity

    `velocities` starts as a list of zero arrays (one per parameter)
    before the very first step, and must be threaded through to the
    NEXT call, this function returns the updated velocities alongside
    the updated params specifically so a training loop can carry them
    forward, step after step.

    Returns (new_params, new_velocities).
    """
    pass
