def joint_probability(x, parents, cpts) -> float:
    """
    Product over nodes of cpts[i][(parent values in order) + (x[i],)].
    Raise ValueError for length mismatch, wrong table rank, unnormalized rows,
    or an out-of-range value.
    """
    pass
