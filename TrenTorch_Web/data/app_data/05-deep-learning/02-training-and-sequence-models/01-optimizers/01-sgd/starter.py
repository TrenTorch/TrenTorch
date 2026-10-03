import numpy as np


def sgd_step(params: list[np.ndarray], grads: list[np.ndarray], lr: float) -> list[np.ndarray]:
    """
    Mirrors one step of torch.optim.SGD (no momentum): every parameter
    moves opposite its own gradient, scaled by the learning rate.

    `04-gd-step` (Classical ML) already did exactly this for one
    weight and one bias specifically; this generalizes to an arbitrary
    LIST of parameters (any number of them, any shapes), the shape
    every real optimizer in this track and in PyTorch itself actually
    takes: one update rule, applied uniformly to every parameter a
    model has.

    Returns a NEW list of updated parameters (does not mutate the
    input arrays in place).
    """
    pass
