def momentum_update(key, query, m):
    """
    key: current key-encoder parameters
    query: query-encoder parameters
    m: momentum coefficient in [0, 1)

    Returns:
        The updated key-encoder parameters m * key + (1 - m) * query.
    """
    # TODO: Move the key encoder a small step toward the query encoder (see Theory).
    pass
