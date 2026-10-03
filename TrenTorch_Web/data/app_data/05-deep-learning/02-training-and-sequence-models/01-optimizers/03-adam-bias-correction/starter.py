def update_moments(
    m: float, v: float, grad: float, beta1: float = 0.9, beta2: float = 0.999
) -> tuple[float, float]:
    """
    SGD + Momentum tracked one running average (velocity). Adam tracks
    TWO: `m`, a running average of the gradient itself (like momentum's
    velocity), and `v`, a running average of the SQUARED gradient
    (tracking gradient MAGNITUDE, regardless of sign).

        m_new = beta1 * m + (1 - beta1) * grad
        v_new = beta2 * v + (1 - beta2) * grad^2

    Both start at 0 before the first step, this is exactly the source
    of the "bias toward zero" bias_correct exists to fix.
    """
    pass


def bias_correct(moment: float, beta: float, t: int) -> float:
    """
    Because m and v both START at exactly 0, their EARLY values are
    systematically biased toward 0 (a weighted average that's mostly
    "0, blended with a little bit of real signal" underestimates the
    true running average). This divides that bias back out, using the
    step count `t` (1-indexed: t=1 on the very first update).

        bias_correct(moment, beta, t) = moment / (1 - beta^t)

    As t grows large, beta^t -> 0, so this correction fades away on
    its own, exactly when it's no longer needed (the running average
    has had enough real updates to no longer be dominated by its
    zero starting point).
    """
    pass
