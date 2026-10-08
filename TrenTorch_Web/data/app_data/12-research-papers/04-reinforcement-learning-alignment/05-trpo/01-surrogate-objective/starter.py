import numpy as np


def surrogate_objective(ratio, advantage):
    """
    ratio: pi_new(a | s) / pi_old(a | s), per sample
    advantage: advantage estimate per sample

    Returns:
        The mean of ratio * advantage, the TRPO surrogate objective.
    """
    # TODO: Average the importance-weighted advantages (see Theory).
    pass
