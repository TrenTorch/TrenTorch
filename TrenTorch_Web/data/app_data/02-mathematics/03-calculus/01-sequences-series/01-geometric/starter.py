def geometric_partial_sum(a, r, n):
    """
    a: first term (float)
    r: common ratio (float)
    n: how many terms to add (int, n >= 0)

    Returns:
        The sum of the first n terms of a + a*r + a*r**2 + ..., as a
        float, in constant time (no loop over the terms). Handles r == 1.
    """
    # TODO: Implement the closed form from Theory.
    pass


def geometric_series_sum(a, r):
    """
    a: first term, r: common ratio

    Returns:
        The sum of the infinite series, as a float.

    Raises:
        ValueError: if abs(r) >= 1, because the series has no finite sum.
    """
    # TODO: Implement the infinite-sum formula from Theory.
    pass


def terms_needed(a, r, tolerance):
    """
    a: first term, r: common ratio with abs(r) < 1, tolerance: float > 0

    Returns:
        The smallest integer n >= 0 such that the infinite sum minus the
        sum of the first n terms is smaller than tolerance in absolute
        value. Returns 0 when a == 0.

    Raises:
        ValueError: if abs(r) >= 1 or tolerance <= 0.
    """
    # TODO: Solve the tail inequality from Theory for n.
    pass
