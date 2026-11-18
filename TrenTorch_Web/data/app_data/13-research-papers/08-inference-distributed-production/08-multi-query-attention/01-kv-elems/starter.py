def kv_cache_elems(layers, kv_heads, seq, d_head):
    """
    layers: transformer layers
    kv_heads: number of key-value heads (1 for multi-query attention)
    seq: sequence length in tokens
    d_head: dimension of each head

    Returns:
        The number of cached elements, keys and values together.
    """
    # TODO: Count the keys and values stored for every layer, kv head and token (see Theory).
    pass
