def solve(beams, alpha):
    """Select the beam maximizing score divided by length raised to alpha."""
    if not beams:
        raise ValueError("beams must not be empty")
    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    return max(beams, key=lambda item: (item[1] / max(1, len(item[0])) ** alpha, tuple(-x for x in item[0])))
