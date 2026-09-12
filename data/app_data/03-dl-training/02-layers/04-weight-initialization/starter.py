import numpy as np


def xavier_uniform_bound(fan_in: int, fan_out: int) -> float:
    """
    Returns `a` such that sampling weights uniformly from [-a, a] gives
    Xavier/Glorot initialization: designed to keep activation variance
    roughly constant across layers for a LINEAR or tanh-like activation.
    """
    pass


def xavier_normal_std(fan_in: int, fan_out: int) -> float:
    """
    Returns the standard deviation for sampling weights from a Gaussian
    N(0, std^2), the normal-distribution variant of Xavier/Glorot init.
    """
    pass


def kaiming_uniform_bound(fan_in: int, gain: float = np.sqrt(2.0)) -> float:
    """
    Returns `a` such that sampling weights uniformly from [-a, a] gives
    He/Kaiming initialization: designed for ReLU-family activations,
    which zero out roughly half their input, so Kaiming compensates by
    using MORE variance than Xavier does. `gain` defaults to sqrt(2), the
    standard gain for ReLU.
    """
    pass


def kaiming_normal_std(fan_in: int, gain: float = np.sqrt(2.0)) -> float:
    """
    The normal-distribution variant of kaiming_uniform_bound: returns the
    standard deviation for sampling weights from N(0, std^2).
    """
    pass
