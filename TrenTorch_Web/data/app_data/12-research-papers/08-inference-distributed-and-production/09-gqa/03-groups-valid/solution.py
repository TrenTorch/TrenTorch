def groups_valid(n_heads, n_kv):
    return n_kv >= 1 and n_kv <= n_heads and n_heads % n_kv == 0
