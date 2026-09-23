def forward_difference(f, x: float, eps: float = 1e-5) -> float:
    """
    The derivative's limit definition, approximated with a small but
    finite step instead of an actual limit:

        f'(x) ~= (f(x + eps) - f(x)) / eps
    """
    pass


def central_difference(f, x: float, eps: float = 1e-5) -> float:
    """
    Same idea as forward_difference, but stepping symmetrically in both
    directions instead of only forward:

        f'(x) ~= (f(x + eps) - f(x - eps)) / (2 * eps)

    See Theory for why this is meaningfully more accurate than the
    forward version, for the same eps.
    """
    pass
