import numpy as np


def triplet_loss(anchor: np.ndarray, positive: np.ndarray, negative: np.ndarray, margin: float = 1.0) -> float:
    """
    anchor: shape (N, D) -- N "reference" embeddings
    positive: shape (N, D) -- one embedding per anchor that SHOULD be
        close to it (e.g. another photo of the same person/object)
    negative: shape (N, D) -- one embedding per anchor that SHOULD be
        far from it (e.g. a photo of someone/something different)
    margin: how much closer the positive must be than the negative
        before the loss for that triplet becomes exactly zero

    Metric/representation learning without any fixed set of classes:
    instead of predicting "which of these K classes," directly train an
    embedding space where similar things end up close together and
    dissimilar things end up far apart, using relative comparisons.
    """
    # TODO: for each row, compute the Euclidean distance from anchor to
    # positive (np.linalg.norm(anchor - positive, axis=1)) and from
    # anchor to negative (same, with negative). The per-triplet loss is
    # max(0, dist_to_positive - dist_to_negative + margin) -- clip
    # negative values to 0 with np.maximum. Return the mean over all N
    # triplets, as a float.
    pass
