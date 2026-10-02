def taylor_first_order(f, f_prime, a, x):
    """
    f, f_prime: functions taking a single float, returning a float
    a: the expansion point
    x: where to evaluate the approximation

    Returns:
        The first-order (tangent-line) Taylor approximation of f at x,
        centered at a: f(a) + f'(a) * (x - a).
    """
    # TODO: Implement from Theory's formula, N=1 case.
    pass


def taylor_second_order(f, f_prime, f_double_prime, a, x):
    """
    f, f_prime, f_double_prime: functions taking a single float,
        returning a float
    a: the expansion point
    x: where to evaluate the approximation

    Returns:
        The second-order Taylor approximation of f at x, centered at a.
    """
    # TODO: Implement using taylor_first_order plus the n=2 term from
    # Theory's formula.
    pass
