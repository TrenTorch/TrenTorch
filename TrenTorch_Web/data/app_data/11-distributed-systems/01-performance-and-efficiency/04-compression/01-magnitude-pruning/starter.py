import numpy as np


def magnitude_prune(weight: np.ndarray, sparsity: float) -> np.ndarray:
    """
    weight: any-shape float array
    sparsity: fraction (0 to 1) of weight's elements to zero out

    Magnitude pruning's premise: a weight close to zero contributes
    almost nothing to the layer's output, so zeroing out the smallest-
    magnitude fraction of weights should hurt accuracy far less than
    zeroing out an equally-sized RANDOM fraction would.

    Returns a new array, same shape as weight, with the smallest-
    magnitude `sparsity` fraction of elements set to exactly 0.0 and
    every other element unchanged.
    """
    # TODO: flatten |weight|, find the value at the (sparsity * size)-th
    # position when sorted ascending (np.partition is a fast way to find
    # a single order statistic without a full sort), use it as a
    # threshold, and zero out every element whose magnitude is <=
    # that threshold. Handle sparsity <= 0 (nothing to prune) as a
    # special case.
    pass
