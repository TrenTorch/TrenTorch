import numpy as np


def ipo_loss(pi_chosen, pi_rejected, ref_chosen, ref_rejected, tau: float) -> float:
    """Mean (h - 1/(2 tau))**2 with h the log-ratio difference."""
    # TODO
    pass


def simpo_loss(pi_chosen, pi_rejected, len_chosen, len_rejected, beta: float, gamma: float) -> float:
    """Reference-free, length-normalised loss with a target margin gamma."""
    # TODO
    pass
