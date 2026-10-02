def telescoping_partial_sum(f, n):
    """
    f: function taking an int, returning a float
    n: how many terms to add (int, n >= 0)

    Returns:
        The sum of the first n terms of (f(1) - f(2)) + (f(2) - f(3)) + ...,
        as a float. Calls f exactly twice when n >= 1 and not at all when
        n == 0, and never loops over the terms.
    """
    # TODO: Use the cancellation from Theory.
    pass


def telescoping_infinite_sum(f_first, f_limit):
    """
    f_first: the value f(1)
    f_limit: the limit of f(k) as k grows

    Returns:
        The sum of the infinite series (f(1) - f(2)) + (f(2) - f(3)) + ...
    """
    # TODO: Take the limit of the closed form from Theory.
    pass


def sum_reciprocal_products(n):
    """
    n: int, n >= 0

    Returns:
        The sum of 1 / (k * (k + 1)) for k = 1 .. n, as a float, without
        looping over the terms. Exactly 0.0 when n == 0.
    """
    # TODO: Rewrite each term as a difference, as in Theory, then collapse.
    pass
