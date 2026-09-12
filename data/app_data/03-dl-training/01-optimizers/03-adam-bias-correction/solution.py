def update_moments(
    m: float, v: float, grad: float, beta1: float = 0.9, beta2: float = 0.999
) -> tuple[float, float]:
    m_new = beta1 * m + (1.0 - beta1) * grad
    v_new = beta2 * v + (1.0 - beta2) * grad**2
    return m_new, v_new


def bias_correct(moment: float, beta: float, t: int) -> float:
    return moment / (1.0 - beta**t)
