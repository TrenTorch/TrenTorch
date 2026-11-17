def kv_cache_memory_footprint(
    n_layers: int,
    n_heads: int,
    d_head: int,
    seq_len: int,
    batch_size: int,
    bytes_per_element: int,
    variant: str,
    n_kv_heads: int | None = None,
) -> dict:
    """
    variant: one of "mha", "mqa", "gqa" (case-insensitive).
    n_kv_heads: required only when variant == "gqa".

    Returns a dict with keys "kv_heads_used", "bytes_per_token_per_layer",
    "bytes_per_token", "total_bytes", "total_mib".
    """
    # TODO: Map variant -> effective kv_heads (n_heads for mha, 1 for
    # mqa, n_kv_heads for gqa), then compute the byte totals from Theory.
    pass
