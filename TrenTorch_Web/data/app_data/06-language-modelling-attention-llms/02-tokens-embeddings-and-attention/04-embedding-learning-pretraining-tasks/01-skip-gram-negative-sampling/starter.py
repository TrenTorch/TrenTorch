import numpy as np


def skipgram_pairs(token_ids: list[int], window: int) -> list[tuple[int, int]]:
    """(center, context) pairs within `window` positions, in position order."""
    # TODO
    pass


def sgns_loss(W_in: np.ndarray, W_out: np.ndarray, center, context, negatives) -> float:
    """Mean skip-gram negative-sampling loss over a batch."""
    # TODO
    pass
