from itertools import product


def is_bipartite(n, edges):
    return any(all(c[a] != c[b] for a, b in edges) for c in product((0, 1), repeat=n))
