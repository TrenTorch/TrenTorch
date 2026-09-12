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
    variant = variant.lower()
    if variant == "mha":
        kv_heads = n_heads
    elif variant == "mqa":
        kv_heads = 1
    elif variant == "gqa":
        if n_kv_heads is None:
            raise ValueError("n_kv_heads required for gqa")
        kv_heads = n_kv_heads
    else:
        raise ValueError(f"unknown variant {variant!r}")

    bytes_per_token_per_layer = 2 * kv_heads * d_head * bytes_per_element
    bytes_per_token = n_layers * bytes_per_token_per_layer
    total_bytes = batch_size * seq_len * bytes_per_token

    return {
        "kv_heads_used": kv_heads,
        "bytes_per_token_per_layer": bytes_per_token_per_layer,
        "bytes_per_token": bytes_per_token,
        "total_bytes": total_bytes,
        "total_mib": total_bytes / (1024**2),
    }
