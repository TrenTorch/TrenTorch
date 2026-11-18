def group_index(head, n_heads, n_kv):
    return head // (n_heads // n_kv)
