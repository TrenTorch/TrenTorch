def kv_cache_bytes(layers, heads, d, seq, nbytes):
    return 2 * layers * heads * d * seq * nbytes
