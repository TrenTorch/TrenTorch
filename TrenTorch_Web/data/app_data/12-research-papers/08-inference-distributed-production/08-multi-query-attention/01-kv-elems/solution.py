def kv_cache_elems(layers, kv_heads, seq, d_head):
    return 2 * layers * kv_heads * seq * d_head
