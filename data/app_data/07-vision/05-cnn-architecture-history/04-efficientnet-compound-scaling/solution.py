def compound_scale(
    phi: int, alpha: float = 1.2, beta: float = 1.1, gamma: float = 1.15
) -> tuple[float, float, float]:
    depth_mult = alpha**phi
    width_mult = beta**phi
    resolution_mult = gamma**phi
    return depth_mult, width_mult, resolution_mult
