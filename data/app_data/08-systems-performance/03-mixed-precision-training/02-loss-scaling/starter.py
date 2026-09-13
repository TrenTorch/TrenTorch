import numpy as np


def scale_loss(loss: float, scale: float) -> float:
    """
    loss: the ordinary, unscaled loss value
    scale: a large multiplier (e.g. 1024, 65536), chosen so that
        gradients computed from this scaled loss land well above
        01-fp16-bf16-representable-range's underflow floor

    Returns loss * scale. Since gradients scale linearly with the loss
    they're computed from (the chain rule multiplies through), scaling
    the loss before backpropagation scales every resulting gradient by
    the same factor -- pushing them up out of fp16's underflow range.
    """
    # TODO: one multiplication.
    pass


def unscale_gradients(gradients: list[np.ndarray], scale: float) -> list[np.ndarray]:
    """
    gradients: a list of gradient arrays computed from a SCALED loss
        (every one of them is `scale` times too large)
    scale: the same scale factor scale_loss used

    Returns the gradients divided back down by scale, before they're
    used in an actual optimizer step -- an update computed from
    still-scaled gradients would be `scale` times too big.
    """
    # TODO: divide every gradient array in the list by scale.
    pass


def has_inf_or_nan(gradients: list[np.ndarray]) -> bool:
    """
    gradients: a list of (post-backward, still-scaled) gradient arrays

    Returns True if ANY gradient contains an inf or nan value -- a sign
    that `scale` was set too high this step (it pushed some gradient
    past fp16's overflow ceiling) and this step's update should be
    skipped entirely, with `scale` reduced before the next attempt.
    """
    # TODO: for each array, check whether every element is finite
    # (np.isfinite); return True if ANY array has a non-finite element.
    pass
