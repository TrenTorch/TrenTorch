def momentum_update(key, query, m):
    return m * key + (1 - m) * query
