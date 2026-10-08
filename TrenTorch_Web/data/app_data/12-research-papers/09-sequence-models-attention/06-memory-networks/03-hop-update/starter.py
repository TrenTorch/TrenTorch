import numpy as np


def hop_update(u, o):
    """
    u: current controller state (question embedding), shape (d,)
    o: output read from memory in this hop, shape (d,)

    Returns:
        The updated state u + o, passed to the next hop.
    """
    # TODO: Add the memory read to the controller state (see Theory).
    pass
