def kv_cache_bytes(layers, heads, d, seq, nbytes):
    """
    layers: transformer layers
    heads: attention heads (key and value heads)
    d: head dimension
    seq: sequence length in tokens
    nbytes: bytes per element (2 for fp16)

    Returns:
        The bytes of the key and value cache for one sequence.
    """
    # TODO: Count the keys and values stored for every layer, head and token (see Theory).
    pass
