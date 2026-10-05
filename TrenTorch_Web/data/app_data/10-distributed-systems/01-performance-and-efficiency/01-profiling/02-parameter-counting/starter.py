import numpy as np


def count_parameters(params: list[np.ndarray]) -> int:
    """
    params: a list of arrays, one per parameter tensor of some model
        (e.g. a Linear layer's weight and bias, each its own array)

    Returns the total number of scalar values across every array --
    exactly what `sum(p.numel() for p in model.parameters())` computes
    for a real PyTorch model.
    """
    # TODO: sum each array's .size (total element count) across the list.
    pass


def count_trainable_parameters(params: list[np.ndarray], requires_grad: list[bool]) -> int:
    """
    params: same as above
    requires_grad: one bool per entry in params -- True if that
        parameter is trainable (would receive gradient updates), False
        if it's frozen

    Returns the total element count of only the TRAINABLE parameters --
    exactly what `sum(p.numel() for p in model.parameters() if
    p.requires_grad)` computes.
    """
    # TODO: sum p.size only where the matching requires_grad entry is True.
    pass
