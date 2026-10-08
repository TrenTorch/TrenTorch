def group_index(head, n_heads, n_kv):
    """
    head: query head index, 0 to n_heads - 1
    n_heads: number of query heads
    n_kv: number of key-value heads, dividing n_heads

    Returns:
        The key-value head that query head `head` uses.
    """
    # TODO: Divide the query heads evenly into n_kv groups and return the group index (see Theory).
    pass
