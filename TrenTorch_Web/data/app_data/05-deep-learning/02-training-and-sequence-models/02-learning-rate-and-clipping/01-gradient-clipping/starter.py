import numpy as np


def compute_global_norm(grads: list[np.ndarray]) -> float:
    """
    The GLOBAL norm across every gradient array, as if every one of
    them were flattened and concatenated into one giant vector:

        global_norm = sqrt(sum of every gradient's own squared values, across ALL arrays)

    NOT the norm of each array separately, one single number
    summarizing the whole gradient's overall magnitude.
    """
    pass


def clip_grad_norm(grads: list[np.ndarray], max_norm: float) -> list[np.ndarray]:
    """
    If the GLOBAL norm (compute_global_norm, already provided above)
    exceeds max_norm, rescale EVERY gradient array by the SAME factor
    so the global norm becomes exactly max_norm. If it's already
    within max_norm, leave every gradient unchanged (but still return
    fresh copies, not the original arrays).

        clip_coef = max_norm / (global_norm + eps)   # eps avoids divide-by-zero
        if clip_coef < 1: scale every gradient by clip_coef
        else: leave gradients as they are
    """
    pass
